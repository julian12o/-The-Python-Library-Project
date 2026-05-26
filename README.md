# Image Batch Processor

Takes a folder of images, applies a filter, resizes them, and saves the results as JPEGs. Runs on multiple threads so it processes everything at once.

## Install

You need Python 3.7+ and Pillow. Install Pillow with:

pip install Pillow

## How to use

Run the script and answer the prompts. You can type a folder name, a full path, or just press Enter to use the defaults.

Filters you can pick from: blur, sharpen, grayscale, contour, none

Supported image types: jpg, jpeg, png, bmp, webp

Processed files are saved as originalname_processed.jpg in your output folder.
