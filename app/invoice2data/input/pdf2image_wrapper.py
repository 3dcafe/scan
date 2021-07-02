# -*- coding: utf-8 -*-
import shutil
import os
from pdf2image import convert_from_path
import pytesseract
from pytesseract import image_to_string
import platform
plt = platform.system()

if plt == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    poppler_path = r'C:/Python38/Lib/poppler/Library/bin'
    temp_path = r'c:/tmp'
elif plt == "Linux":
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    poppler_path = None
    temp_path = r'/tmp'
else:
    print("Unidentified system")



def to_text(path, language='eng'):
    """Wraps PDF2image with custom language model.

    Parameters
    ----------
    path : str
        path of electronic invoice in PDF format

    Returns
    -------
    extracted_str : str
        returns extracted text from image in JPG or PNG format

    """
    #language_list = {"en": "eng", "de": "deu", "ru": "rus", "fr": "fra", }

    config = f'-l {language} --psm 3'
    if path.rsplit('.', 1)[1].lower() == 'pdf':
        images = convert_from_path(
            os.path.abspath(path),
            poppler_path=poppler_path,
            dpi=300,
            fmt="tiff"
        )

        results = []

        for image in images:
            #filename = 'temp.tiff'
            #image.save(filename, 'TIFF')
            result = pytesseract.image_to_string(
                image, config=config)
            results.append(result)
        return "\n".join(results)

    result = pytesseract.image_to_string(
            os.path.abspath(path), config=config
            )
    return result
