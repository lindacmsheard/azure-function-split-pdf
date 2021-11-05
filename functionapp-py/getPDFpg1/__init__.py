import logging
import os

import azure.functions as func

from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO


def main(fullpdf: func.InputStream, page1: func.Out[func.InputStream]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {fullpdf.name}\n"
                 f"Blob Size: {fullpdf.length} bytes")


    pdfbytes = fullpdf.read()                                 # returns bytes

    # create intermediary input stream
    fullpdfstream = BytesIO(pdfbytes)                         # returns seekable stream

    pages = os.getenv('PAGES').split(',')

    adj = 0 if "0" in pages else 1
    
    if adj==1:
        logging.info(f"No '0' included in page specification: Assuming page numbering starts from '1'.")

    pages = [int(p)-adj for p in pages]

    pdf = PdfFileReader(fullpdfstream)

    pdfWriter = PdfFileWriter()

    for page_num in pages:
        pdfWriter.addPage(pdf.getPage(page_num))
    
    # create intermediary output stream
    page1stream = BytesIO()                                   # empty stream object that pyPDF2 class method can write to

    pdfWriter.write(page1stream)
    
    page1.set(page1stream.getvalue())                         # set the func.Out[func.InputStream] object to stream out
                                                              #     out the bytes object returned by .getvalue() to blob storage
    page1stream.close()
   




#https://github.com/Azure/azure-functions-python-worker/issues/832