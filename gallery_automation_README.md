# Gallery Automation

## Setup

### ImageMagick

**IMPORTANT**: Ensure that ImageMagick is downloaded and added to the `Path` variable of your computer. Otherwise, this program will not function properly. Instructions to do this properly are located below.

1. Download the `ImageMagick-7.1.0-portable-Q16-x64.zip` build from the <a href="https://imagemagick.org/script/download.php#windows" target="_blank">ImageMagick downloads page</a>.

2. Extract the contents of the ZIP file to a location on your computer.

3. Locate the `magick.exe` file in file explorer, and copy the folder path in the address bar.

4. Open the User Environment Variables window. This can often be found by searching in the Search Bar.

5. Click on the `Path` variable to select it, and then click `Edit...`.

6. At the end of the string of text in the `Variable value` input field, add a semicolon `;`, and then paste in the folder path that you copied in Step 3.

7. Click `OK`.

8. Click `OK`.

9. Open a `cmd` window.

10. Run the command, `magick` to ensure that ImageMagick has successfully been added to the `Path` variable.

If you get the error, `Invalid argument or not enough arguments`, then ImageMagick has been successfully added to the `Path` variable.

### Python

**IMPORTANT**: The automation scripts run on Python, so ensure that the Python has been properly installed. Python can be downloaded from <a href="https://www.python.org/downloads/windows/" target="_blank">here</a>. Download the latest build of Python 3 that is compatible with your version of Windows. When running the installer, ensure that pip is set to be installed. Otherwise, the script will not function properly.

---

## Automation

To begin the automation process, simply run `GalleryAutomate.bat`. You will be notified about installing Python and adding ImageMagick to the `Path` variable. If you have already done both, then simply press any key to continue the process.

The images will automatically be downloaded to "images/gallery", and the thumbnails and the HTML image pages will be automatically generated and saved to "ChunkyGallery/gallery/img/gallery".

The only manual part of the process is adding the image links to the `index.md` file in "ChunkyGallery/gallery".
