def main():
    sheetUrl = "https://docs.google.com/spreadsheets/d/1B3PD0AAc_gwNES8b1uaETQwswkjEcHbwJy8EH9M1k88/export?format=csv" # URL for gallery submission spreadsheet in CSV format
    print("Attempting to download \"" + sheetUrl + "\" to \"submissionsheet.csv\"") # Notify the user about the current action
    try:
        wget.download(sheetUrl, 'submissionsheet.csv') # Download the gallery submission sheet in CSV format
    except Exception as e:
        print("Failed to download \"" + sheetUrl + "\"")
        print("Error code: " + str(e))
        exit()
    print("Attempting to open \"submissionsheet.csv\"") # Notify the user about the current action
    try:
        submissionsheet = open("submissionsheet.csv") # Open the submission spreadsheet
    except Exception as e:
        print("Failed to open \"submissionsheet.csv\"")
        print("Error code: " + str(e))
        exit()
    submissionsheet.readline() # Skip the first line
    numLines = len(submissionsheet.readlines()) # Record the number of remaining lines
    submissionsheet.seek(0) # Return to the beginning of the file
    submissionsheet.readline() # Skip the first line
    print(str(numLines) + " images will be downloaded.") # Print number of lines
    
    i = 1
    while i <= numLines: # Repeat for every entry on the spreadsheet
        url, fullFilename, filename, renderNameNoEdit = getData(submissionsheet) # Get data from the spreadsheet
        print("Attempting to download \"" + url + "\" to \"" + fullFilename + "\"") # Notify the user about the current action
        try:
            wget.download(url, fullFilename) # Download the image file
            createThm(fullFilename, filename) # Create a thumbnail of the image file
            createHtml(filename, renderNameNoEdit) # Create an HTML image page
        except Exception as e:
            print("Failed to download \"" + url + "\"")
            print("Error code: " + str(e))
        i = i + 1 # Increment the counter

def getData(submissionsheet):
    line = str(submissionsheet.readline()) # Read the next line of the spreadsheet
    firstComma = line.index(",", 0) # Record the loactions of the first five commas
    secondComma = line.index(",", firstComma + 1)
    thirdComma = line.index(",", secondComma + 1)
    fourthComma = line.index(",", thirdComma + 1)
    fifthComma = line.index(",", fourthComma + 1)
    idBegin = firstComma + 34 # Specify the location of the Google Drive file ID in the URL
    idEnd = secondComma
    _id = line[idBegin:idEnd]
    url = str("https://drive.google.com/uc?id=" + _id) # Create a new URL from the Google Drive ID
    renderNameBegin = thirdComma + 1 # Specify the location of the title of the render in the entry
    renderNameEnd = fourthComma
    renderAuthorBegin = fourthComma + 1 # Specify the location of the author of the render in the entry
    renderAuthorEnd = fifthComma
    renderName = line[renderNameBegin:renderNameEnd].replace(" ", "_") # Replace all spaces in the render title with underscores
    renderAuthor = line[renderAuthorBegin:renderAuthorEnd].replace(" ", "_") # Replace all spaces in the author name with underscores
    renderNameNoEdit = line[renderNameBegin:renderNameEnd] # Record the name of the author without editing it
    filePath = str("../images/gallery/") # Folder into which the images are downloaded
    filename = str(renderAuthor + "-" + renderName) # Generate the filename from the name of the author and the name of the render joined by a hyphen
    fullFilename = str(filePath + filename) # Record the full file path of the image
    return url, fullFilename, filename, renderNameNoEdit # Return recorded values

def createThm(fullFilename, filename):
    outputFile = str("../ChunkyGallery/gallery/img/gallery/" + filename + "-thm.jpg") # Set the thumbnail output file
    print("\nAttempting to generate thumbnail image from \"" + filename + "\"") # Notify the user about the current action
    try:
        subprocess.run(["magick", fullFilename, "-resize", "720", "-quality", "90%", outputFile]) # Run ImageMagick to create the thumbnails
    except Exception as e:
        print("Failed to generate thumbnail image from \"" + filename + "\". Is ImageMagick properly added to Path?")
        print("Error code: " + str(e))
        exit()

def createHtml(filename, renderNameNoEdit):
    outputFile = str("../ChunkyGallery/gallery/img/gallery/" + filename + ".html") # Set the HTML output file
    url = str("https://raw.githubusercontent.com/chunky-dev/gallery/main/images/gallery/" + filename) # Generate a URL from the filename
    html = str("""<!DOCTYPE html>
<html>
    <head>
        <meta charset=\"utf-8\">
        <link rel=\"stylesheet\" href=\"../styles.css\">
        <title>\n            """ + 
            renderNameNoEdit + """
        </title>
    </head>
    <body>
        <img src=\"""" + url + """\">
    </body>
</html>
""") # Generate HTML file contents from the unedited render name and the URL
    print("Attempting to write HTML file for \"" + filename + "\"") # Notify the user about the current action
    imageHtml = open(outputFile, "w") # Create a new HTML file
    imageHtml.write(html) # Write the contents to the file
    imageHtml.close() # Close the file
    
import wget
import subprocess

main() # Program starts here
