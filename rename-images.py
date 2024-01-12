import os
import re
from transformers import pipeline
from PIL import Image

def sanitize_filename(name):
    return re.sub(r'[^\w\s-]', '', name.replace(' ', '_').lower())

def rename_images(folder_path):
    print(f"Processing folder: {folder_path}")
    pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large", max_new_tokens=60)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                try:
                    file_path = os.path.join(root, file)
                    with Image.open(file_path) as img:
                        response = pipe(img)
                        if 'generated_text' in response[0]:
                            caption = response[0]['generated_text']
                            print(f'Caption: {caption}')

                            new_name = sanitize_filename(caption) + os.path.splitext(file)[1]
                            new_file_path = os.path.join(root, new_name)

                            os.rename(file_path, new_file_path)
                            print(f'Renamed "{file}" to "{new_name}"')
                        else:
                            print(f'No caption found for {file}')
                except Exception as e:
                    print(f'Error processing {file}: {e}')

rename_images('./')
