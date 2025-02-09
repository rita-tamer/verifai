# import os
# import json
# import subprocess
# from PIL import Image, ExifTags
# from lxml import etree

# # List of AI-related metadata keys
# ai_metadata_keys = [
#     "Credit", "JUMD Type", "JUMD Label", "Actions Action", "Actions Software Agent", 
#     "Claim Generator", "Signature", "Assertions Url"
#     # , "C2PA Thumbnails/Manifests"
# ]

# # Function to extract EXIF metadata
# def extract_exif_metadata(image_path):
#     exif_list = []
#     img = Image.open(image_path)
#     exif_data = img.getexif()

#     if len(exif_data) == 0:
#         print("No EXIF data found.")
#         return exif_list

#     for key, value in exif_data.items():
#         if key in ExifTags.TAGS:
#             key_name = ExifTags.TAGS[key]
#             if key_name in ai_metadata_keys:
#                 exif_list.append((key_name, value))

#     return exif_list

# # Function to extract XMP metadata
# def extract_xmp_metadata(image_path):
#     xmp_data = {}
#     img = Image.open(image_path)

#     if img.info.get("xml"):
#         xml_tree = etree.fromstring(img.info["xml"])
#         for elem in xml_tree.iter():
#             if any(ai_key.lower() in elem.tag.lower() for ai_key in ai_metadata_keys):
#                 xmp_data[elem.tag] = elem.text

#     return xmp_data

# # Function to extract metadata using ExifTool (best for C2PA)
# def extract_exiftool_metadata(image_path):
#     exiftool_path = r"C:\ExifTool\exiftool.exe"  # Ensure this is the correct path
#     result = subprocess.run([exiftool_path, "-json", image_path], capture_output=True, text=True)
 
#     try:
#         metadata = json.loads(result.stdout)[0]
#     except (json.JSONDecodeError, IndexError):
#         print("Failed to extract metadata using ExifTool.")
#         return {}

#     # Filter for AI-related metadata
#     ai_data = {k: v for k, v in metadata.items() if any(ai_key.lower() in k.lower() for ai_key in ai_metadata_keys)}
#     return ai_data

# # Main function
# def analyze_image(image_path):
#     print(f"Analyzing {image_path}...\n")

#     exif_data = extract_exif_metadata(image_path)
#     xmp_data = extract_xmp_metadata(image_path)
#     exiftool_data = extract_exiftool_metadata(image_path)

#     print("== Extracted EXIF Metadata ==")
#     for key, value in exif_data:
#         print(f"{key}: {value}")

#     print("\n== Extracted XMP Metadata ==")
#     for key, value in xmp_data.items():
#         print(f"{key}: {value}")

#     print("\n== Extracted C2PA Metadata via ExifTool ==")
#     for key, value in exiftool_data.items():
#         print(f"{key}: {value}")

# # Run analysis on an image
# image_path = "image.png"  # Change to your image filename
# analyze_image(image_path)

# import pyexiv2

# def extract_xmp_metadata(image_path):
#     metadata = pyexiv2.ImageMetadata(image_path)
#     metadata.read()
#     return metadata.xmp_keys

# xmp_data = extract_xmp_metadata("Geminii.jpg")
# print(xmp_data)
import exiftool

# Define the metadata keys you are interested in.
target_keys = [
    "Credit", "JUMD Type", "JUMD Label", 
    "Actions Action", "Actions Software Agent", 
    "Claim Generator", "Signature", 
    "Assertions Url"
    # , "C2PA Thumbnails/Manifests"
]

def extract_target_metadata(image_path):
    with exiftool.ExifTool() as et:
        # Get metadata as a dictionary (pyexiftool returns a list of dicts)
        metadata_list = et.get_metadata(image_path)
        
    # There should be only one dictionary in the list for a single image.
    if not metadata_list:
        print("No metadata found for the image.")
        return

    metadata = metadata_list[0]
    
    # Loop through all metadata entries and check for your target keys
    for key, value in metadata.items():
        # We use lower() to do a case-insensitive match
        for target in target_keys:
            if target.lower() in key.lower():
                print(f"Key: {key}, Value: {value}")

# Replace "Geminii.jpg" with your image filename.
extract_target_metadata("Geminii.jpg")
