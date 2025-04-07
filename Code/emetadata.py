import subprocess

def get_exif_data(file_path):
    """Runs ExifTool to extract metadata from an image."""
    result = subprocess.run(['exiftool', file_path], capture_output=True, text=True)
    return result.stdout

# Example usage
image_path = r'E:\Uni\grad project\verifai\image_files\POC\Desk_Original.png'
metadata = get_exif_data(image_path)
print(metadata)
