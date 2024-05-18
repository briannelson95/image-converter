# ImageConverter V2

Version 2 is here and now supports batch conversions! At the top of the window you now have the option to do a [single conversion](#single-conversion) or [batch conversion](#batch-conversion)

This is a quick and simple image converter that allows you to convert the most common image formats to other. 

Supported formats include:
- WebP
- JPG (JPeg)
- PNG
- HEIC*

**The application only allows to convert image from HEIC to other formats, I didn't see a need to convert them to HEIC*

## Installation

To install head over to [releases](https://github.com/briannelson95/image-converter/releases) and download the most recent Installer.exe or macOS.dmg. Upon opening it will take you through a quick install wizard and then open the program.

## Usage

![](/images//Capture.PNG)

### Single Conversion
To use [ImageConverter](https://github.com/briannelson95/image-converter/) you select an image from your computer using the Browse button. 
You will see a preview of the image if the format is supported under the preview is your output folder, if you don't specify a folder it will save to the file your original image is in. On the right hand side you select what format you would like to convert to and if you want to rename the file. If you don't set a name the name will be the original name of the file with the new extention. You can allow the application to open the destination folder for you by ticking the checkbox and then click Convert.

### Batch Conversion
Batch conversion works very similarly to the single conversion, except there is no image preview and instead shows you a list of files. The conversion works for multiple types so you can have png, jpg, webp, and heic selected and convert them all to one type. When choosing an output directory, if you don't choose one or choose the same one the images are already in, the program will default to creating a folder within that directory titled `conversion-[date-time]` so that you don't have to go looking for those files.

You also have the option to delete an image that has been selected. You can click on the file name of the image you want to delete and press `backspace` or right click on the file and choose "Remove"

![](/images/batch-delete.png)

- Select your image files
- Select your conversion type
- Choose output folder (directory)/leave it blank to get a subfolder
- Convert