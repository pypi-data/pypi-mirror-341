# Easy Image Converter

## 📷 Overview

**Easy Image Converter** is a powerful command-line interface (CLI) tool that allows you to quickly and easily bulk convert and resize image files. Whether you're a developer, designer, or simply someone who works with images often, this tool helps automate image processing tasks, making it faster, simpler, and more efficient.

With Easy Image Converter, you can convert images to different formats (e.g., JPEG, PNG, WEBP), resize them to custom dimensions, and apply compression, all with a few simple commands.

---

## 🛠 Features

- **Bulk Image Conversion**: Convert multiple images at once from one format to another (e.g., from PNG to JPEG, WEBP, etc.).
- **Resize Images**: Automatically resize your images to custom dimensions, keeping your workflow smooth and efficient.
- **Compression**: Control the output quality of images to reduce file sizes, especially for web usage or storage optimization.
- **Progress Bar**: Visual progress indication while converting and resizing images using the `tqdm` library.
- **Easy to Use**: Accessible through the command line, no need for complicated software or manual image editing.

---

## 🚀 Installation

### 1. Install via `pip`
To install the **Easy Image Converter** package, simply run the following command in your terminal:

```bash
pip install easy-img-converter
```

## 2. Install from Source

If you'd like to install from source, clone the repository and run the following:

```bash
git clone https://github.com/NavvneetK/easy-img-converter.git
cd easy-img-converter
pip install .
```

---
## 🧑‍💻 Usage

After installing Easy Image Converter, you can use it directly from your terminal.

## Converting Images
To convert a batch of images to a specific format (e.g., from PNG to JPEG), run the following command:

```bash
bulkimgconvert --input /path/to/input/folder --output /path/to/output/folder --format JPEG
```

--`input`: Path to the folder containing the images you want to convert.

--`output`: Path to the folder where converted images will be saved.

--`format`: The format you want to convert the images to (JPEG, PNG, WEBP).

  Example:
  Convert all images in images/ to JPEG and save them in converted/:
```bash
bulkimgconvert --input images/ --output converted/ --format JPEG
```


## Resize Images
-You can also resize the images during conversion. For example, to resize the images to 800x600 pixels, use the --resize option:

```bash

bulkimgconvert --input /path/to/input/folder --output /path/to/output/folder --format JPEG --resize 800 600
```
--`resize:` The dimensions to resize the images to (width height).

-Example:
Convert and resize images to 800x600 pixels:

```bash
bulkimgconvert --input images/ --output resized/ --format JPEG --resize 800 600
```

## Adjust Compression Quality
  For formats like JPEG and WEBP, you can control the compression level using the --quality option. The default is 85, but you can increase or decrease it based on your preference:

```bash
bulkimgconvert --input /path/to/input/folder --output /path/to/output/folder --format JPEG --quality 75
--quality: The compression quality (from 0 to 100, where 100 is the best quality but largest file size).
```

Example:
Convert and compress images at 75% quality:

```bash
bulkimgconvert --input images/ --output compressed/ --format JPEG --quality 75
```

---

## 📚 Requirements

Python 3.6+: The tool requires Python 3.6 or higher.

`Pillow`: The Python Imaging Library (PIL) fork, used for image processing.

`tqdm`: A Python library for adding progress bars to loops.

You can install the required dependencies using:

```bash
pip install -r requirements.txt
```

---
## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🛠 Contributing

Feel free to fork this project, make your changes, and submit a pull request! Contributions are welcome and encouraged.

If you have any ideas for new features, bug fixes, or improvements, feel free to open an issue or create a pull request.
