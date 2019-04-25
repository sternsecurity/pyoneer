# pyoneer
Developed by Peter Nelson<br>
Stern Security<br>
www.sternsecurity.com

Pyoneer is a work in progress Data Discovery tool written in python for the purpose finding keywords in files or files with specified extensions and producing output of the filename and search term found, NOT the actual data found.

## Currently Working Searches
* DOCX
* DOC
* XLSX
* PDF
* Text files (CSV,TXT,etc)

## Search Code that Requires Review
* XLS
* PDF-OCR

## Required Python Modules
* textract- https://textract.readthedocs.io/en/stable/
* PyPDF2- https://pypi.org/project/PyPDF2/
* olefile- https://pypi.org/project/olefile/
