import wget

url = "https://docs.google.com/spreadsheets/d/1B3PD0AAc_gwNES8b1uaETQwswkjEcHbwJy8EH9M1k88/export?format=csv" # URL for gallery submission spreadsheet in CSV format

wget.download(url, 'submissionsheet.csv') # Download the gallery submission sheet in CSV format
