# Pyoneer
Developed by Peter Nelson<br>
Stern Security<br>
www.sternsecurity.com

Pyoneer is a Data Discovery tool written in python3 and using concurrent.futures and asyncio for multi-processing. It has been written for the purpose finding keywords in files or files with specified extensions and producing output of the filename and search term found, NOT the actual data found.<br>
<br>

## Current Active Development
* Add file size limits (read first 25MB of file over 25MB)
* Perform filename search for search terms
* PDF-OCR- Requires extracting the images and processing them separately.

## Recent Changes
* Integrated concurrent.futures in to asyncio context manager
* Added resume functionality
* Added folder/file match limit/continue
* Improved output
* Improved regex performance
* Improved on screen status
* Added more search file types and ability to skip
* Fixed excluding directories

## Currently Working Searches
* DOCX
* DOC
* XLSX
* XLS
* PDF
* Image OCR (jpg,png,tiff)
* Any file not matching the above or excluded is read and searched as a flat file.

## TODO
* Add regex search items. ex 555-55-5555 for SSN
* Prompt for user input, Search root dir, output path, custom file extension and file type.
* Create better output and reporting, maybe an html with links to files.
  * (Partially worked on, CSV output is improved)
* Expand database functionality, currently just finds files.
* Perform filename search for search terms, currently only looking at file extensions.
  * (Partially worked on, added functionality to ignore specified files and folders)

## Search Code that Requires Review
* No issues known at this time

## Required Python Modules
* textract- https://textract.readthedocs.io/en/stable/</br>
`apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev`</br>
`pip install textract`

* PyPDF2- https://pypi.org/project/PyPDF2/</br>
`pip3 install PyPDF2`

* olefile- https://pypi.org/project/olefile/</br>
`pip3 install olefile`
