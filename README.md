# Pyoneer
Developed by Peter Nelson<br>
Stern Security<br>
www.sternsecurity.com

Pyoneer is a Data Discovery tool written in python for the purpose finding keywords in files or files with specified extensions and producing output of the filename and search term found, NOT the actual data found.

## Current Active Development
* Multi-Threading
* Moving search code into functions
* Code logic to treat all other files as flat files

## Currently Working Searches
* DOCX
* DOC
* XLSX
* PDF
* PDF-OCR
* Text files (CSV,TXT,etc)

## TODO
* Add regex search items. ex 555-55-5555 for SSN
* Prompt for user input, Search root dir, output path, custom file extension and file type.
* Create better output reporting, maybe an html with links to files.
* Expand database functionality, currently just finds files.
* Perform filename search for search terms, currently only looking at file extensions.
* Convert remaining 'document=' opens to with statements.
* Review XLS functionality, may need fixes.
* Rework output to path,filename.ext,ext/type,term|term|term

## Search Code that Requires Review
* XLS

## Required Python Modules
* textract- https://textract.readthedocs.io/en/stable/
* PyPDF2- https://pypi.org/project/PyPDF2/
* olefile- https://pypi.org/project/olefile/
