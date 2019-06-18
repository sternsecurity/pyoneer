
"""
Written by Peter Nelson
Stern Security
www.sternsecurity.com
"""

import time
import os
import zipfile
import olefile
import re
import PyPDF2
import textract
from concurrent.futures import ProcessPoolExecutor


# Search though file contents with the following extensions
xmlDocExt = [".docx", ".xlsx"]
oleDocExt = [".doc", ".xls"]
imgExt = [".jpg", ".tiff", ".png"]

# Exclude the following directories files and extensions
excludeExt = [".mp4", ".mpg", ".mov", ".bmp", ".iso", ".dmg", ".zip", ".exe", ".msi", ".mp3", ".pptx", ".ppt", ".jar", ".gz", ".lock"]
excludeFile = ["desktop.ini", "thumbs.db", ".DS_Store"]
excludedirs = ["Windows"]

# Search for the below extensions only, set to true of false
checkfordb = 'true'
dbExt = [".ldf", ".mdf", ".db", ".sql", ".sqlite"]
checkforransom = 'false'
ransomExt = [".nozelesn"]
checkforvm = 'false'
vmExt = [".vmdk", ".vram", ".ovf", ".ova", ".vbox", ".vdi"]

# Keyword search criteria
searchTerms = re.compile('(name|visa|ssn|dob|account|password|bin|phone|address|zip|member|birthdate|social|credit|card|ccv|report)', re.I)

# XML search tags for DOCX and XLSX
xlsxsearch = re.compile('<[v|t]>.*?</[v|t]>')
docxsearch = re.compile('<w:t>.*?</w:t>')

# Change this variable to the path to search
rootPath = "/PATH/TO/SEARCH/"
# Change this to the path for search results output.
outputPath = "/PATH/TO/WRITE/OUTPUT"

start_time = time.time()
filecount = 0


# Worker function called by the main thread
# Exception is commented out for flat files because when a byte that isn't uft-8 can't be read
# it's caught as an exception and is very noisy.
# EG:
# 'utf-8' codec can't decode byte 0x## in position #####: invalid start byte
# 'utf-8' codec can't decode byte 0x## in position #####: invalid continuation byte
def do_work(filePath):
	if filePath.lower().endswith(tuple(xmlDocExt)) or filePath.lower().endswith(tuple(oleDocExt)) or filePath.lower().endswith('.pdf') or filePath.lower().endswith(tuple(imgExt)):
		if filePath.lower().endswith(tuple(xmlDocExt)) and "~$" not in filePath:
			try:
				with zipfile.ZipFile(str(filePath), 'r') as parentDoc:
					outputTerm = ""
					xmlDocs = parentDoc.namelist()
					for doc in xmlDocs:
						searchTarget = re.findall('.*\.xml', doc)
						if searchTarget:
							xmlContent = parentDoc.read(doc)
							if xmlContent is not "":
								xmlContentStr = str(xmlContent)
								if filePath.lower().endswith(".xlsx"):
									regContent = xlsxsearch
									filetype = ("xlsx")
								if filePath.lower().endswith(".docx"):
									regContent = docxsearch
									filetype = ("docx")
								text_re = re.findall(regContent, xmlContentStr)
								for item in text_re:
									searchResult = searchTerms.findall(item)
									if searchResult:
										for term in searchResult:
											if term not in outputTerm:
												outputTerm += term + '|'
				zipfile.ZipFile.close(parentDoc)
				if outputTerm is not "":
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
						outfile.close()
			except Exception as e:
				print(e)
				pass
		if filePath.lower().endswith(tuple(oleDocExt)) and "~$" not in filePath:
			try:
				with olefile.OleFileIO(filePath) as oleDoc:
					outputTerm = ""
					if filePath.lower().endswith(".doc"):
						oleContent = oleDoc.openstream('WordDocument')
						filetype = "doc"
					else:
						oleContent = oleDoc.openstream('Workbook')
						filetype = "xls"
					oleData = oleContent.read()
					oleStr = str(oleData)
					olefile.OleFileIO.close(oleDoc)
					searchResult = searchTerms.findall(oleStr)
					if searchResult:
						for term in searchResult:
							if term not in outputTerm:
								outputTerm += term + '|'
				if outputTerm is not "":
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
						outfile.close()
			except Exception as e:
				print(e)
				pass
		if filePath.lower().endswith('.pdf'):
			try:
				with open(filePath, 'rb') as openPdffile:
					filetype = "pdf"
					pdfReader = PyPDF2.PdfFileReader(openPdffile)
					numPages = pdfReader.numPages
					count = 0
					pdfText = ''
					outputTerm = ''
					while count < numPages:
						pdfPage = pdfReader.getPage(count)
						count += 1
						pdfText += pdfPage.extractText()
						if not pdfText:
							pdfTextOCR = textract.process(filePath, method='tesseract', language='eng')
							pdfText = str(pdfTextOCR)
						searchResult = searchTerms.findall(pdfText)
						if searchResult:
							for term in searchResult:
								if term not in outputTerm:
									outputTerm += term + '|'
				if outputTerm is not "":
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
						outfile.close()
			except Exception as e:
				print(e)
				pass
		if filePath.lower().endswith(tuple(imgExt)):
			try:
				filetype = "image"
				outputTerm = ''
				imgTextocr = textract.process(filePath, method='tesseract', language='eng')
				imgText = str(imgTextocr)
				searchResult = searchTerms.findall(imgText)
				if searchResult:
					for term in searchResult:
						if term not in outputTerm:
							outputTerm += term + '|'
				if outputTerm is not "":
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
						outfile.close()
			except Exception as e:
				print(e)
				pass
	else:
		if filePath.lower().endswith(tuple(ransomExt)) or filePath.lower().endswith(tuple(dbExt)) or filePath.lower().endswith(tuple(vmExt)):
			if checkforransom == 'true':
				if filePath.lower().endswith(tuple(ransomExt)):
					filetype = "ransom"
					outputTerm = "Ransomware Extension Found\n"
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
						outfile.close()
			if checkfordb == 'true':
				if filePath.lower().endswith(tuple(dbExt)):
					filetype = "database"
					outputTerm = "Database File Found\n"
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
						outfile.close()
			if checkforvm == 'true':
				if filePath.lower().endswith(tuple(vmExt)):
					filetype = "vm"
					outputTerm = "Virtual Machine File Found\n"
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
						outfile.close()
		else:
			try:
				with open(filePath) as flatFile:
					filetype = "flatfile"
					outputTerm = ""
					flatData = flatFile.read()
					flatFile.close()
					searchResult = searchTerms.findall(flatData)
					if searchResult:
						for term in searchResult:
							if term not in outputTerm:
								outputTerm += term + '|'
					if outputTerm is not "":
						with open(outputPath, "a") as outfile:
							outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
							outfile.close()
			except Exception as e:
				#print(e)
				pass
	return


# Function to print status for number of files processed
def statustext(counter):
	CEND = '\33[0m'
	CBOLD = '\33[1m'
	CGREEN = '\33[32m'
	print(CBOLD + '\rFiles Processed: ' + CBOLD + CGREEN + str(counter) + CEND, end='')


if __name__ == "__main__":
	for root, dirs, files in os.walk(rootPath, topdown=True):
		for d in dirs[:]:
			if d in excludedirs:
				dirs.remove(d)
			for file in files:
				if file.lower().endswith(tuple(excludeExt)) or file in tuple(excludeFile):
					continue
				fullpath = os.path.join(root, file)
				executor = ProcessPoolExecutor(max_workers=1)
				worker = executor.map(do_work, [fullpath])
				filecount += 1
				statustext(filecount)
	print("\n--- %s seconds ---" % (time.time() - start_time))
