@echo off

echo IMPORTANT: The automation scripts run on Python, so Python must be installed to your computer. Read the "gallery_automation_README.md" file for more information. If Python is not installed to your computer, then press Ctrl+C to abort the program.

pause

echo IMPORTANT: ImageMagick must be downloaded and added to the "Path" variable of your computer. Read the "gallery_automation_README.md" file for more information. If ImageMagick is not added to the "Path" variable, then press Ctrl+C to abort the program.

pause

pip3 install wget

mkdir ..\images\gallery

mkdir ..\ChunkyGallery\gallery\img\gallery

python get_images.py

del submissionsheet.csv

pause
