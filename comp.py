#! python3
# comp.py - splits PDF files for Computability HW and uploads them to moodle


import sys
import PyPDF2

"""
Receives array of tuples representing new files to create
"""
def split(pdfName, pages):
    pdfFile = open(pdfName, 'rb')
    reader = PyPDF2.PdfFileReader(pdfFile)

    for i in range(len(pages)):
        firstPage = int(pages[i][0])
        lastPage = int(pages[i][1])
        writer = PyPDF2.PdfFileWriter()
        #subName = pdfName[:-4]+"("+str(firstPage)+"-"+str(lastPage)+").pdf"
        subName = pdfName[:-4]+"#"+str(i)+".pdf"
        with open(subName, 'wb') as f:
            for j in range(firstPage-1,lastPage):
                writer.addPage(reader.getPage(j))
            writer.write(f)

    pdfFile.close()

args = sys.argv
pdfName = args[1]
pages = []
for i in range(2,len(args)):
    if len(args[i])==1:
        pages.append([args[i],args[i]])
    else: pages.append(args[i].split('-'))

split(pdfName,pages)
