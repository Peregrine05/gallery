<p align="center">
  <img width="100" src="https://raw.githubusercontent.com/llbit/chunky-docs/master/images/logo.png" alt="Chunky logo">
</p>
<h1 align="center"> Chunky Gallery </h1>

<div align="center">Chunky is a Minecraft rendering tool that uses Path Tracing to create realistic images of your Minecraft worlds. View the website <a href="https://chunky-dev.github.io/docs/" target="_blank">here</a>. This is the repository for the <a href="https://chunky-dev.github.io/gallery/" target="_blank">Chunky Gallery</a>.</div>

## Build Instructions

This site uses <a href="https://www.mkdocs.org/" target="_blank">mkdocs</a>. Python version 3.5 or greater is required. Installation instructions are located [below](#dependencies), in the `Python` section.

1. Clone this repository.

2. (optional) Set up a Python <a href="https://docs.python.org/3/library/venv.html" target="_blank">virtual environment</a>.

3. Install the required packages with pip by using the command, `pip3 install -r requirements.txt`.

4. If running Windows, simply run `serve.bat`. Otherwise, change the working directory to `./ChunkyGallery`.

5. Serve the site for development by using the command, `python -m mkdocs serve --dev-addr 127.0.0.1:8001`.

6. Build a preview of the final site by using the command, `python -m mkdocs build`.

---

## Usage of `auto_gallery.py`

### Dependencies

- Python: This script runs on Python; therefore, Python must be installed on your computer. Download Python from <a href="https://www.python.org/downloads/" target="_blank">here</a>. Download the latest release of Python 3 that is compatible with your operating system. When running the installer, ensure that pip is set to be installed. Pip will be used to install the next dependency.

- wget: This script uses the Python wget module to download the gallery images. If pip is installed, then the wget module can be installed with the command, `pip3 install wget`.

- ImageMagick: This script uses ImageMagick to generate the thumbnails for the images. On Windows, ImageMagick should be added to the `Path` environment variable for the script to function properly.

1. Download the `ImageMagick-7.1.0-portable-Q16-x64.zip` build from the <a href="https://imagemagick.org/script/download.php#windows" target="_blank">ImageMagick downloads page</a>.

2. Extract the contents of the ZIP file to a location on your computer.

3. Locate the `magick.exe` file in file explorer, and copy the folder path that is in the address bar.

4. Open the `Environment Variables` window. This can often be found by searching in the Search Bar.

5. Click on the `Path` variable to select it, and then click `Edit...`.

6. At the end of the string of text in the `Variable value` input field, add a semicolon `;`, and then paste the folder path that you copied in Step 3.

7. Click `OK`.

8. Click `OK`.

9. Open a `cmd` window, and run the command, `magick` to ensure that ImageMagick has successfully been added to the `Path` variable.

If you get the error, `Invalid argument or not enough arguments`, then ImageMagick has been successfully added to the `Path` variable.

### Key Files and Folders

- `gallery.csv` -  Contains a list of all Gallery entries we have. Due to mistakes that have been made, we currently have "full" information for only new submissions.

- `templates\` - Contains some .html templates which are used to create original image pages and gallery containers.

- `ChunkyGallery\gallery\index.md` - is the target file for the script and must have `<!--GALLERY_START-->` and `<!--GALLERY_END-->` tags in order for the script to function.

### New Entries

1. Import new entries from https://docs.google.com/spreadsheets/d/1B3PD0AAc_gwNES8b1uaETQwswkjEcHbwJy8EH9M1k88/edit?usp=sharing into `gallery.csv`.

2. Clean-up new entries in `gallery.csv`; add missing credits, clean up features, etc.

3. Run `auto_gallery.py`.

4. Fix any errors you come across... This is usually stray spaces.

5. PR `images\gallery\` changes first.

6. PR all other changes.

### For updating templates/force re-gen

By default we do not re-generate files.

1. Delete/clear `ChunkyGallery\gallery\img\thumbnail` and `ChunkyGallery\gallery\image_html` | It is not recommended to clear `images\gallery`. As some entries do not have a Google Drive URL, we cannot recover these easily.

2. Run `auto_gallery.py`.

3. Fix any errors you come across...

4. PR as normal.
