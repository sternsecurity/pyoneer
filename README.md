# Pyoneer
Developed by Peter Nelson<br>
Stern Security<br>
www.sternsecurity.com

Pyoneer is a Data Discovery tool written in python3 and using concurrent.futures for multi-poccessing. It has been written  for the purpose finding keywords in files or files with specified extensions and producing output of the filename and search term found, NOT the actual data found.<br>
<br>
Last testing of the script, it proccessed over 200,000 local files in less than 30 minutes, scanning a remote share will add time.

## Current Active Development
* Add file size limits (read first 25MB of file over 25MB)

## Currently Working Searches
* DOCX
* DOC
* XLSX
* XLS
* PDF
* PDF-OCR
* Image OCR (jpg,png,tiff)
* Text files (CSV,TXT,etc)

## TODO
* Add regex search items. ex 555-55-5555 for SSN
* Prompt for user input, Search root dir, output path, custom file extension and file type.
* Create better output reporting, maybe an html with links to files.
** (Partially worked on, CSV output is improved)
* Expand database functionality, currently just finds files.
* Perform filename search for search terms, currently only looking at file extensions.
** (Partially worked on, added functionality to ignore specified files and folders)

## Search Code that Requires Review
* No issues known at this time

## Required Python Modules
* textract- https://textract.readthedocs.io/en/stable/
* PyPDF2- https://pypi.org/project/PyPDF2/
* olefile- https://pypi.org/project/olefile/
