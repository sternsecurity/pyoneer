'''
Written by Peter Nelson
Stern Security
www.sternsecurity.com
'''

import os
import zipfile
import olefile
import re
import PyPDF2
import textract

#Search file contents for terms with the following extensions
xmlExt = [".docx", ".xlsx"]
oleExt = [".doc", ".xls"]
flatExt = [".csv", ".txt"]
pdfExt = [".pdf"]

#Search for the below extensions only 
dbExt = [".mdf", ".db", ".sql", ".sqlite"]
ransomExt = [".nozelesn"]

#Change as needed, search is case insensitive
searchTerms = ["SSN", "DOB", "mrn", "password", "patient", "pt number", "diagnosis", "phone", "address", "name"]
#Change this variable to the path to search
rootPath = "/SEARCH/PATH"
#Change this to the path for search results output.  Results are pipe (|) separated 
outputPath = "/OUTPUT/PATH/results.csv"

#Check file extensions in the 'rootPath' and perform search based on file type.
#'print' statements have been left in for debug purposes
#Try statments are below to continue the script in the event of an error/exception
for root, dirs, files in os.walk(rootPath):
    for file in files:
		if file.endswith(tuple(xmlExt)) and "~$" not in file:
			if file.endswith(".docx"):
				try:
					document = zipfile.ZipFile(os.path.join(root, file))
					outputTerm = ""
					#print(document.namelist())
					xmlContent = document.read('word/document.xml')
					document.close()
					xmlStr = str(xmlContent)
					text_re = re.findall('<w:t>.*?<\/w:t>',xmlStr)[1:]
					for item in text_re:
						#print(item)
						for term in searchTerms:
							searchResult = ""
							searchResult = re.findall('^.*'+term+'.*',item, re.I)
							if searchResult:
								outputTerm += term+','
								#print outputTerm
								#print(os.path.join(root, file))
								#print term
								#print(searchResult)
							else:
								continue
					if outputTerm is not "":
						with open(outputPath, "a") as outfile:
							outfile.write(os.path.join(root, file)+'|'+outputTerm+"\n")
				except Exception:
					pass
			if file.endswith(".xlsx"):
				try:
					document = zipfile.ZipFile(os.path.join(root, file))
					outputTerm = ""
					xmlDocs = document.namelist()
					#print(xmlDocs)
					for docs in xmlDocs:
						workSheets = re.findall('xl/worksheets/.heet.*',docs)
						#print workSheets
						if workSheets:
							#print docs
							xmlContent = document.read(docs)
							document.close()
							#print xmlContent
							xmlContentStr = str(xmlContent)
							text_re = re.findall('<v>.*?<\/v>',xmlContentStr)[1:]
							for item in text_re:
								#print(item)
								for term in searchTerms:
									#print(term)
									searchResult = ""
									searchResult = re.findall('^.*'+term+'.*',item, re.I)
									if searchResult:
										outputTerm += term+','
										#print outputTerm
										#print(os.path.join(root, file))
										#print term
										#print(searchResult)
									else:
										continue
					if outputTerm is not "":
						with open(outputPath, "a") as outfile:
							outfile.write(os.path.join(root, file)+'|'+outputTerm+"\n")
				except Exception:
					pass
		if file.endswith(tuple(oleExt)) and "~$" not in file:
			if file.endswith(".doc"):
				try:
					#print(os.path.join(root, file))
					with olefile.OleFileIO(os.path.join(root, file)) as oleDoc:
						outputTerm = ""
						#print(oleDoc.listdir())
						oleContent = oleDoc.openstream('WordDocument')
						oleData = oleContent.read()
						oleStr = str(oleData)
						#print oleData
						for term in searchTerms:
							#print term
							searchResult = ""
							searchResult = re.findall('^.*'+term+'.*',oleStr, re.I)
							if searchResult:
								outputTerm += term+','
								#print outputTerm
								#print(os.path.join(root, file))
								#print term
								#print(searchResult)
							else:
								continue
					if outputTerm is not "":
						with open(outputPath, "a") as outfile:
							outfile.write(os.path.join(root, file)+'|'+outputTerm+"\n")
				except Exception:
					pass
			if file.endswith(".xls"):
				try:
					#print(os.path.join(root, file))
					with olefile.OleFileIO(os.path.join(root, file)) as oleDoc:
						outputTerm = ""
						#oleStreams = oleDoc.listdir()
						#print(oleStreams)
						#for streams in oleStreams:
							#sheets = re.findall('sheet.*'
						oleContent = oleDoc.openstream('Workbook')
						oleData = oleContent.read()
						oleStr = str(oleData)
						#print oleStr
						output = os.path.join(root, file)
						for term in searchTerms:
							#print term
							searchResult = ""
							searchResult = re.findall('^.*'+term+'.*',oleStr, re.I)
							if searchResult:
								outputTerm += term+','
								#print outputTerm
								#print(os.path.join(root, file))
								#print term
								#print(searchResult)
							else:
								continue
					if outputTerm is not "":
						with open(outputPath, "a") as outfile:
							outfile.write(os.path.join(root, file)+'|'+outputTerm+"\n")
				except Exception:
					pass
		if file.endswith(tuple(flatExt)):
			try:
				with open(os.path.join(root, file)) as flatFile:
					outputTerm = ""
					flatData = flatFile.read()
					#print flatData
					for term in searchTerms:
							#print term
							searchResult = ""
							searchResult = re.findall('^.*'+term+'.*',flatData, re.I)
							if searchResult:
								outputTerm += term+','
								#print outputTerm
								#print(os.path.join(root, file))
								#print term
								#print(searchResult)
							else:
								continue
					if outputTerm is not "":
						with open(outputPath, "a") as outfile:
							outfile.write(os.path.join(root, file)+'|'+outputTerm+"\n")
			except Exception:
					pass
		if file.endswith(tuple(pdfExt)):
			try:
				with open(os.path.join(root, file), 'rb') as pdfFile:
					pdfReader = PyPDF2.PdfFileReader(pdfFile)
					numPages = pdfReader.numPages
					count = 0
					pdfText = ""
					outputTerm = ""
					while count < numPages:
						pdfPage = pdfReader.getPage(count)
						count += 1
						pdfText += pdfPage.extractText()
					if pdfText != "":
						pdfText = pdfText
						#print pdfText
					else:
						#print pdfFile
						pdfText = textract.process(os.path.join(root, file), method='tesseract', language='eng')
						#print('#############\n\nOCROCROCROCROCROCROCR\n\n##############')
						#print (pdfText)
					for term in searchTerms:
							#print term
							searchResult = ""
							searchResult = re.findall('^.*'+term+'.*',pdfText, re.I)
							if searchResult:
								outputTerm += term+','
								#print outputTerm
								#print(os.path.join(root, file))
								#print term
								#print(searchResult)
							else:
								continue
					if outputTerm is not "":
						with open(outputPath, "a") as outfile:
							outfile.write(os.path.join(root, file)+'|'+outputTerm+"\n")
			except Exception:
					pass
		if file.endswith(tuple(ransomExt)):
			try:
				ransomFile = os.path.join(root, file)+"|Ransomware Extension\n"
				with open(outputPath, "a") as outfile:
					outfile.write(ransomFile)
			except Exception:
				pass
		else:
			if file.endswith(tuple(dbExt)):
				try:
					dbFile = os.path.join(root, file)+"|Database File\n" 
					with open(outputPath, "a") as outfile:
						outfile.write(dbFile)
				except Exception:
					pass
			else:
				continue
