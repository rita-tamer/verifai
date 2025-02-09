import os 
from PIL import Image, ExifTags
# from PIL.ExifTags import TAGS

# img_file = 'Apple.webp'
# image = Image.open(img_file)

# exif = {}

# for tag, value in image._getexif().items():
#     if tag in TAGS:
#         exif[TAGS[tag]] = value

# print(exif)

ex_list = []

img = Image.open("Geminii.jpg")

exif_data = img.getexif()

if len(exif_data) == 0:
    print("Sorry, there was no exif data found for this image.")
else:
    for key, data in exif_data.items():

        if key in ExifTags.TAGS:

            key_name = ExifTags.TAGS[key]

            if key_name not in ex_list:
                print (f"Key: {key_name}, Value: {data}")