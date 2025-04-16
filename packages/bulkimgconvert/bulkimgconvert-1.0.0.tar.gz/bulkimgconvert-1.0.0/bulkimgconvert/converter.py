import os
from PIL import Image
import argparse
from pathlib import Path
from tqdm import tqdm

def convert_images(input_folder, output_folder, format="JPEG", resize=None, quality=85):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    image_files = [file for file in input_folder.iterdir() if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']]

    for file in tqdm(image_files, desc="Converting images", unit="image"):
        img = Image.open(file)

        if resize:
            img = img.resize(resize)

        new_file = output_folder / f"{file.stem}.{format.lower()}"

        # Save with compression/quality setting
        save_kwargs = {}
        if format.upper() in ["JPEG", "WEBP"]:
            save_kwargs['quality'] = quality

        img.convert("RGB").save(new_file, format=format, **save_kwargs)

    print("✅ Conversion done!")

