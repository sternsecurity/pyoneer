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
import gc
from concurrent.futures import ProcessPoolExecutor
import asyncio


# Search though file contents with the following extensions
xmlDocExt = [".docx", ".xlsx"]
oleDocExt = [".doc", ".xls"]
imgExt = [".jpg", ".tiff", ".png"]

# Exclude the following directories files and extensions
excludeExt = [".mp4", ".mpg", ".mov", ".bmp", ".iso", ".dmg", ".zip", ".exe", ".msi", ".mp3", ".pptx", ".ppt", ".jar",".gz", ".lock"]
excludeFile = ["desktop.ini", "thumbs.db", ".ds_store"]
excludedirs = ["windows", "program files", "program files (x86)", "users"]

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
resultsearch = re.compile('.*result=\((\d),\s.*>')

# Change this variable to the path to search
rootPath = "/YOUR/SEARCH/PATH/"
# Change this to the path for search results output.
outputPath = "/YOUR/OUTPUT/PATH/FILE.csv"

# Misc variables
start_time = time.time()
processedcount = 0
previousfile = ''
# Set this to 'true' if you need to restart the script
resumescript = ''
CEND = '\33[0m'
CBOLD = '\33[1m'
CGREEN = '\33[32m'
matchlimit = 10

# Worker function called by the asycio loop
# Exception is commented out for flat files because when a byte that isn't uft-8 can't be read
# it's caught as an exception and is very noisy.
# EG:
# 'utf-8' codec can't decode byte 0x## in position #####: invalid start byte
# 'utf-8' codec can't decode byte 0x## in position #####: invalid continuation byte
def do_work(filePath):
	matchext = ''
	filematch = 0
	if filePath.lower().endswith(tuple(xmlDocExt)) or filePath.lower().endswith(
			tuple(oleDocExt)) or filePath.lower().endswith('.pdf') or filePath.lower().endswith(tuple(imgExt)):
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
				if outputTerm is not "":
					dontcare, matchext = os.path.splitext(filePath)
					filematch = 1
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
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
					searchResult = searchTerms.findall(oleStr)
					if searchResult:
						for term in searchResult:
							if term not in outputTerm:
								outputTerm += term + '|'
				if outputTerm is not "":
					with open(outputPath, "a") as outfile:
						dontcare, matchext = os.path.splitext(filePath)
						filematch = 1
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
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
							continue
						searchResult = searchTerms.findall(pdfText)
						if searchResult:
							for term in searchResult:
								if term not in outputTerm:
									outputTerm += term + '|'
				if outputTerm is not "":
					dontcare, matchext = os.path.splitext(filePath)
					filematch = 1
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
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
					dontcare, matchext = os.path.splitext(filePath)
					filematch = 1
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
			except Exception as e:
				print(e)
				pass
	else:
		if filePath.lower().endswith(tuple(ransomExt)) or filePath.lower().endswith(
				tuple(dbExt)) or filePath.lower().endswith(tuple(vmExt)):
			if checkforransom == 'true':
				if filePath.lower().endswith(tuple(ransomExt)):
					filetype = "ransom"
					outputTerm = "Ransomware Extension Found\n"
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
			if checkfordb == 'true':
				if filePath.lower().endswith(tuple(dbExt)):
					filetype = "database"
					outputTerm = "Database File Found\n"
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
			if checkforvm == 'true':
				if filePath.lower().endswith(tuple(vmExt)):
					filetype = "vm"
					outputTerm = "Virtual Machine File Found\n"
					with open(outputPath, "a") as outfile:
						outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
		else:
			try:
				with open(filePath) as flatFile:
					filetype = "flatfile"
					outputTerm = ""
					flatData = flatFile.read()
					searchResult = searchTerms.findall(flatData)
					if searchResult:
						for term in searchResult:
							if term not in outputTerm:
								outputTerm += term + '|'
					if outputTerm is not "":
						dontcare, matchext = os.path.splitext(filePath)
						filematch = 1
						with open(outputPath, "a") as outfile:
							outfile.write(filePath + ',' + filetype + ',' + outputTerm + "\n")
			except Exception as e:
				#print(e)
				pass
	gc.collect()
	return filematch, matchext


# Function to print status
def statustext(filecounter, elapsed, matchcount):
	print(CBOLD + '\rFiles Processed: ' + CBOLD + CGREEN + str(filecounter) + CEND + ' Match Count: ' + CBOLD + CGREEN + str(matchcount) + CEND + ' Time elapsed: ' + str(elapsed), end='')

# AsyncIO function called by main
async def async_func():
	matchtotal = 0
	matchendswith = ''
	processedcount = 0
	global resumescript
	for root, dirs, files in os.walk(rootPath, topdown=True):
		for d in dirs[:]:
			if d.lower() in excludedirs:
				dirs.remove(d)
				print(' >>>DIR EXCLUDED: ' + root + "/" + d)
				continue
		for file in files:
			# USE FOR REAL STATUS BAR IN LATER DEV
			filecount = len(files)
			#print('Files in folder: ' + str(filecount))
			filename, fileext = os.path.splitext(file)
			# IF Statement to quit searching a directory if file extension match X times in a row, set by matchlimit variable
			if fileext in matchendswith and matchtotal == matchlimit:
				files.clear()
				print(CBOLD + CGREEN + ' >>> MATCHED ' + str(matchtotal) + ' files: MOVING ON!' + CEND)
				matchendswith = ''
				matchtotal = 0
				continue
			fullpath = os.path.join(root, file)
			# Exclude files
			if file.lower().endswith(tuple(excludeExt)) or file.lower() in tuple(excludeFile):
				continue
			# This will read the last line of the output file and begin searching through the file system
			# and resume the script from there.  If the search folder structure changes, files could be missed.  This code
			# simply reads the last line of the output and iterates through the filesystem till its found.
			if resumescript == 'true':
				with open(outputPath, 'rb') as f:
					f.seek(-2, os.SEEK_END)
					while f.read(1) != b'\n':
						f.seek(-2, os.SEEK_CUR)
					resultslastine = f.readline().decode()
				print(CBOLD + '\rResume Enabled >>> Searching for last file: ' + CEND + CBOLD + CGREEN + str(processedcount) + CEND, end='')
				processedcount += 1
				filesearch = re.findall(re.escape(str(fullpath)), str(resultslastine))
				if filesearch:
					resumescript = ''
					print(CBOLD + CGREEN + '\nLAST FILE FOUND: ' + str(filesearch) + CEND + CBOLD + '\nResuming Content Scan' + CEND)
			else:
				processedcount += 1
				elapsedtime = time.time() - start_time
				statustext(processedcount, elapsedtime, matchtotal)
				loop = asyncio.get_event_loop()
				with ProcessPoolExecutor(max_workers=2) as executor:
					runprocess = [loop.run_in_executor(executor, do_work, fullpath)]
					for item in asyncio.as_completed(runprocess):
						await item
						result = re.findall('.*result=.*(\d),\s\'(.*)\'.*', str(runprocess))
						# Used for the file match limit
						matchcount = int(result[0][0])
						if matchcount == 0:
							matchtotal = 0
							matchendswith = ''
						else:
							if matchendswith == '':
								matchendswith = str(list([result[0][1]]))
							if fileext in matchendswith:
								matchtotal = matchtotal + matchcount


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(async_func())
	loop.close()
	print("\n--- %s seconds ---" % (time.time() - start_time))
