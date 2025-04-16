# pictora

A powerful image management tool designed to work with AI systems for intelligent image organization. This tool enables AI to read, understand, and organize local image files into appropriate folders based on their content and characteristics.

## Project Purpose

This tool is specifically designed to:
- Allow AI systems to access and analyze local image files
- Enable AI-driven image categorization and organization
- Provide a robust interface for AI to manage and process images
- Support automated image sorting and folder management
- Facilitate AI-powered image content understanding and classification

## Installation

### Installation via MCP (Claude Desktop)

Add the following configuration to your MCP settings file:

```json
"mcpServers": {
  "pictora": {
    "command": "uvx",
    "args": ["pictora"]
  }
}
```

## MCP API Features

### Directory Management
- **create_directory**: Creates a new directory at the specified path. Can optionally create parent directories and handle existing directories. Essential for AI-driven folder organization.

### Image File Operations
- **list_image_files**: Scans a directory and returns a formatted list of all valid image files found, including file count and alphabetical listing. Enables AI to discover and analyze available images.
- **read_image**: Reads an image file and returns it as an Image object for further processing. Allows AI to access and analyze image content.
- **copy_image**: Copies an image file to a new location while preserving all metadata. Used by AI to organize images into appropriate categories.
- **move_image**: Moves an image file to a new location, with options to handle existing files and preserve metadata. Enables AI to reorganize images based on content analysis.
- **delete_image**: Safely deletes an image file with optional confirmation. Provides AI with the ability to manage unwanted or duplicate images.
- **create_image**: Generates a new blank image with specified dimensions, color, and format. Useful for AI-generated image processing tasks.

### Supported Image Formats
The tool supports the following image formats for AI analysis:
- JPG/JPEG
- PNG
- GIF
- BMP
- WebP
- TIFF
- ICO
- JFIF
- SVG

### File Management Features
- Automatic directory creation for AI-driven organization
- Overwrite protection with optional override
- Comprehensive error handling and status reporting
- File metadata preservation during operations
- Validation of image files before processing
- Support for batch operations and automated organization

## AI Integration

This tool is designed to work seamlessly with AI systems, providing:
- Direct access to local image files for AI analysis
- Tools for AI-driven image organization
- Support for automated folder creation and management
- Metadata preservation during AI-driven reorganization
- Robust error handling for automated operations

## Error Handling
All operations include comprehensive error handling and return detailed status information including:
- Success/failure status
- Error messages (if any)
- File metadata
- Operation details

## License

This project is distributed under the MIT License.
