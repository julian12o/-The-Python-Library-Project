# Image Batch Processor

Accepts an images folder, applies a filter, resizes images, and saves output images as .jpgs. Processes all data in parallel by using multithreading.

## Installation

Requirements are Python 3.7+ and Pillow library. To install Pillow library, run:

pip install Pillow

## Usage

Execute the code and follow instructions from the console. As an input folder you may specify its name, complete path, or leave it blank to accept default options.

Filtering options: blur, sharpen, grayscale, contour, none

Image types accepted: jpg, jpeg, png, bmp, webp

Output images' names are originalimagename_processed.jpg.
