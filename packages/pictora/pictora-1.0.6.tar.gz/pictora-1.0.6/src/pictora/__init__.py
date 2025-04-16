from mcp.server.fastmcp import FastMCP, Image
import os
import base64
import glob
import shutil
import re
from PIL import Image as PILImage
from io import BytesIO
from typing import Dict, List, Any, Optional, Union


# Create Image Manager MCP server
mcp = FastMCP("imagent-mcp")

# Supported image extensions
SUPPORTED_IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', 
    '.tiff', '.tif', '.ico', '.jfif', '.svg'
}

# Helper function: Check if file is a valid image
def is_valid_image(filepath: str) -> bool:
    """
    Check if the file is a valid image file.
    
    Args:
        filepath (str): File path to check
        
    Returns:
        bool: True if the file is an image, False otherwise
    """
    try:
        _, ext = os.path.splitext(filepath.lower())
        if ext in SUPPORTED_IMAGE_EXTENSIONS:
            with PILImage.open(filepath) as _:
                return True
    except Exception:
        pass
    return False

# Create directory function
@mcp.tool()
def create_directory(
    directory_path: str,
    exist_ok: bool = True,
    parents: bool = True
) -> Dict[str, Any]:
    """
    Create a directory at the specified path. Creates a new directory if it doesn't exist,
    and handles existing directories according to settings.
    
    Args:
        directory_path (str): Path of the directory to create
        exist_ok (bool): Whether to ignore errors if directory exists (default: True)
        parents (bool): Whether to create parent directories if needed (default: True)
    
    Returns:
        Dict[str, Any]: Directory creation result information
    """
    try:
        # Normalize path
        directory_path = os.path.abspath(directory_path)
        
        # Check if directory exists
        already_exists = os.path.exists(directory_path)
        
        if already_exists:
            # Handle existing directory
            if not os.path.isdir(directory_path):
                return {
                    "success": False,
                    "error": f"Specified path exists but is not a directory: {directory_path}"
                }
            elif not exist_ok:
                return {
                    "success": False,
                    "error": f"Directory already exists: {directory_path}"
                }
            else:
                return {
                    "success": True,
                    "message": f"Directory already exists: {directory_path}",
                    "path": directory_path,
                    "created": False
                }
        
        # Create directory
        if parents:
            os.makedirs(directory_path)
        else:
            # May raise error if parent directory doesn't exist
            try:
                os.mkdir(directory_path)
            except FileNotFoundError:
                return {
                    "success": False,
                    "error": f"Parent path does not exist. Set parents=True: {directory_path}"
                }
        
        return {
            "success": True,
            "message": f"Directory created successfully: {directory_path}",
            "path": directory_path,
            "created": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# MCP tool: List image files in directory
@mcp.tool()
def list_image_files(folder: str) -> str:
    """
    Return a text list of image files in the specified folder.
    
    Args:
        folder (str): Folder path to search for image files
    
    Returns:
        str: Text list of image files
    """
    try:
        # Normalize folder path
        folder = os.path.abspath(folder)
        
        # Check if folder exists
        if not os.path.exists(folder):
            return f"Error: Folder does not exist: {folder}"
        
        if not os.path.isdir(folder):
            return f"Error: Specified path is not a directory: {folder}"
        
        # Check all files in folder
        image_files = []
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath) and is_valid_image(filepath):
                image_files.append(filename)
        
        # Format result
        if not image_files:
            return f"No image files found in folder: {folder}"
        
        # Sort alphabetically
        image_files.sort()
        
        # Generate result text
        result_lines = [
            f"Folder: {folder}",
            f"Number of image files: {len(image_files)}",
            "---",
            *[f"{i+1}. {name}" for i, name in enumerate(image_files)]
        ]
        
        return "\n".join(result_lines)
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Read image function
@mcp.tool()
def read_image(image_path: str) -> Image:
    """
    Read an image file and return it as an Image object.
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        Image: Image object
    """
    img = PILImage.open(image_path)
    buffer = BytesIO()
    img_format = img.format.lower() if img.format else "png"
    img.save(buffer, format=img_format)
    return Image(data=buffer.getvalue(), format=img_format)

# Copy image function
@mcp.tool()
def copy_image(
    source_path: str,
    destination_path: str,
    overwrite: bool = False
) -> Dict[str, Any]:
    """
    Copy an image file. Can copy to the same or different path, with the same or different filename.
    
    Args:
        source_path (str): Source image file path
        destination_path (str): Destination image file path (including filename)
        overwrite (bool): Whether to overwrite if destination file exists
    
    Returns:
        Dict[str, Any]: Copy result information
    """
    try:
        # Normalize paths
        source_path = os.path.abspath(source_path)
        destination_path = os.path.abspath(destination_path)
        
        # Check if source file exists
        if not os.path.exists(source_path):
            return {
                "success": False,
                "error": f"Source file does not exist: {source_path}"
            }
        
        # Check if source file is an image
        if not is_valid_image(source_path):
            return {
                "success": False,
                "error": f"Source file is not a valid image: {source_path}"
            }
        
        # Check if destination file exists
        if os.path.exists(destination_path) and not overwrite:
            return {
                "success": False,
                "error": f"Destination file already exists and overwrite is not allowed: {destination_path}"
            }
        
        # Create destination directory
        destination_dir = os.path.dirname(destination_path)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # Copy file
        shutil.copy2(source_path, destination_path)
        
        # Collect file information
        file_size = os.path.getsize(destination_path)
        with PILImage.open(destination_path) as img:
            width, height = img.size
            format_name = img.format
        
        return {
            "success": True,
            "message": "Image file copied successfully.",
            "source_path": source_path,
            "destination_path": destination_path,
            "file_size": file_size,
            "width": width,
            "height": height,
            "format": format_name
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Move image function
@mcp.tool()
def move_image(
    source_path: str,
    destination_path: str,
    overwrite: bool = False
) -> Dict[str, Any]:
    """
    Move an image file. Can move to the same or different path, with the same or different filename.
    
    Args:
        source_path (str): Source image file path
        destination_path (str): Destination image file path (including filename)
        overwrite (bool): Whether to overwrite if destination file exists
    
    Returns:
        Dict[str, Any]: Move result information
    """
    try:
        # Normalize paths
        source_path = os.path.abspath(source_path)
        destination_path = os.path.abspath(destination_path)
        
        # Check if source file exists
        if not os.path.exists(source_path):
            return {
                "success": False,
                "error": f"Source file does not exist: {source_path}"
            }
        
        # Check if source file is an image
        if not is_valid_image(source_path):
            return {
                "success": False,
                "error": f"Source file is not a valid image: {source_path}"
            }
        
        # Check if destination file exists
        if os.path.exists(destination_path) and not overwrite:
            return {
                "success": False,
                "error": f"Destination file already exists and overwrite is not allowed: {destination_path}"
            }
        
        # Save file information before moving
        file_name = os.path.basename(source_path)
        file_size = os.path.getsize(source_path)
        with PILImage.open(source_path) as img:
            width, height = img.size
            format_name = img.format
        
        # Create destination directory
        destination_dir = os.path.dirname(destination_path)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # Move file
        shutil.move(source_path, destination_path)
        
        return {
            "success": True,
            "message": "Image file moved successfully.",
            "source_path": source_path,
            "destination_path": destination_path,
            "file_name": file_name,
            "file_size": file_size,
            "width": width,
            "height": height,
            "format": format_name
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Delete image function
@mcp.tool()
def delete_image(
    image_path: str,
    confirm: bool = True
) -> Dict[str, Any]:
    """
    Delete an image file.
    
    Args:
        image_path (str): Path of the image file to delete
        confirm (bool): Confirmation for deletion (default: True, prevents accidental deletion)
    
    Returns:
        Dict[str, Any]: Deletion result information
    """
    try:
        # Normalize path
        image_path = os.path.abspath(image_path)
        
        # Check if file exists
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"File does not exist: {image_path}"
            }
        
        # Check if file is an image
        if not is_valid_image(image_path):
            return {
                "success": False,
                "error": f"File is not a valid image: {image_path}"
            }
        
        # Confirm deletion
        if not confirm:
            return {
                "success": False,
                "error": "File deletion not confirmed. Set confirm=True to confirm deletion."
            }
        
        # Save file information before deletion
        file_size = os.path.getsize(image_path)
        file_name = os.path.basename(image_path)
        
        # Delete file
        os.remove(image_path)
        
        return {
            "success": True,
            "message": "Image file deleted successfully.",
            "deleted_path": image_path,
            "file_name": file_name,
            "file_size": file_size
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Create new image function
@mcp.tool()
def create_image(
    output_path: str,
    width: int = 512,
    height: int = 512,
    color: str = "#FFFFFF",
    format: str = "png",
    overwrite: bool = False
) -> Dict[str, Any]:
    """
    Create a new image.
    
    Args:
        output_path (str): Path for the new image file
        width (int): Image width in pixels (default: 512)
        height (int): Image height in pixels (default: 512)
        color (str): Background color (HTML color code) (default: "#FFFFFF" white)
        format (str): Image format (default: "png")
        overwrite (bool): Whether to overwrite if file exists (default: False)
    
    Returns:
        Dict[str, Any]: Creation result information
    """
    try:
        # Normalize path
        output_path = os.path.abspath(output_path)
        
        # Check if file exists
        if os.path.exists(output_path) and not overwrite:
            return {
                "success": False,
                "error": f"File already exists and overwrite is not allowed: {output_path}"
            }
        
        # Create output directory
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Process color code
        try:
            if color.startswith('#'):
                color_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            else:
                # Handle basic color names
                colors = {
                    "white": (255, 255, 255),
                    "black": (0, 0, 0),
                    "red": (255, 0, 0),
                    "green": (0, 255, 0),
                    "blue": (0, 0, 255),
                    "yellow": (255, 255, 0),
                    "purple": (128, 0, 128),
                    "gray": (128, 128, 128)
                }
                color_rgb = colors.get(color.lower(), (255, 255, 255))
        except Exception:
            color_rgb = (255, 255, 255)  # Use white on error
        
        # Create image
        img = PILImage.new('RGB', (width, height), color_rgb)
        
        # Save image
        img.save(output_path, format=format)
        
        # Collect file information
        file_size = os.path.getsize(output_path)
        
        return {
            "success": True,
            "message": "New image created successfully.",
            "path": output_path,
            "width": width,
            "height": height,
            "format": format,
            "color": color,
            "file_size": file_size
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    mcp.run(transport='stdio')
