from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.generic import TextStringObject, NameObject
from PyPDF4.utils import b_
import os
import argparse
from io import BytesIO
from typing import Tuple
# Import the reportlab library
from reportlab.pdfgen import canvas
# The size of the page supposedly A4
from reportlab.lib.pagesizes import A4
# The color of the watermark
from reportlab.lib import colors

PAGESIZE = A4
FONTNAME = 'Helvetica-Bold'
FONTSIZE = 40
# using colors module
# COLOR = colors.lightgrey
# or simply RGB
# COLOR = (190, 190, 190)
COLOR = colors.red
# The position attributes of the watermark
X = 200
Y = 250
# The rotation angle in order to display the watermark diagonally if needed
ROTATION_ANGLE = 45

def create_watermark(wm_text: str):
    """
    Creates a watermark template.
    """
    if wm_text:
        # Generate the output to a memory buffer
        output_buffer = BytesIO()
        # Default Page Size = A4
        c = canvas.Canvas(output_buffer, pagesize=PAGESIZE)
        # you can also add image instead of text
        c.drawImage("image/watermark.png", X, Y, 160, 160,mask='auto')
        # Set the size and type of the font
        c.setFont(FONTNAME, FONTSIZE)
        # Set the color
        if isinstance(COLOR, tuple):
            color = (c/255 for c in COLOR)
            c.setFillColorRGB(*color)
        else:
            c.setFillColor(COLOR)
        # Rotate according to the configured parameter
        c.rotate(ROTATION_ANGLE)
        # Position according to the configured parameter
        # c.drawString(X, Y, wm_text)
        c.save()
        return True, output_buffer
    return False, None

def watermark_pdf(input_file: str, wm_text: str, pages: Tuple = None):
    """
    Adds watermark to a pdf file.
    """
    result, wm_buffer = create_watermark(wm_text)
    if result:
        wm_reader = PdfFileReader(wm_buffer)
        pdf_reader = PdfFileReader(open(input_file, 'rb'), strict=False)
        pdf_writer = PdfFileWriter()
        try:
            for page in range(pdf_reader.getNumPages()):
                # If required to watermark specific pages not all the document pages
                if pages:
                    if str(page) not in pages:
                        continue
                page = pdf_reader.getPage(page)
                page.mergePage(wm_reader.getPage(0))
                pdf_writer.addPage(page)
        except Exception as e:
            print("Exception = ", e)
            return False, None, None
        return True, pdf_reader, pdf_writer

def watermark_file(input_file,output_file):
        r,pdf_reader, pdf_writer = watermark_pdf(
            input_file=input_file, wm_text="Framalaundromat")
        
        
        with open(output_file, 'wb') as pdf_output_file:
            pdf_writer.write(pdf_output_file)
        pdf_output_file.close()
        pdf_reader.stream.close()