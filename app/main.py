import os
from PIL import Image
from pdf2image import convert_from_path
import pdf2image
import pytesseract
from pytesseract import image_to_string
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import shutil
from typing import Optional, List, Tuple
import platform
import re

# в зависимости от платформы загружаем бибилиотеки и настрйоки 
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

os.makedirs(temp_path, exist_ok=True)
print('OCR Version: ',pytesseract.get_tesseract_version())

# разрешенные расширения
ALLOWED_EXTENSIONS_PAGE = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
ALLOWED_EXTENSIONS_PAGES = {'pdf'}

app = FastAPI()

# стартовая страница
@app.get("/")
async def main():
    return {"Status": "Ok"}

# распознаем страницу
def ocr_image(image, config):
    text = pytesseract.image_to_string(Image.open(image), config=config)
    return text

# удаляем из текста лишние символы
def preprocessing_text(text):
    text = re.sub('[!@#$]', ' ', text)
    text = re.sub('\n\n}', '\n', text)
    text = re.sub('\s{2,}', ' ', text)
    text = re.sub('^\s$', ' ', text)
    return text

def run(image, config):
    text_source = ocr_image(image, config)
    text = preprocessing_text(text_source)

    result = []
    id = 0
    doc = text.split('\n')
    for s in doc:
        id += 1
        if re.search('\|', s):
            rows = s.split('|')
            result.append({"id": id, "table_string": rows})
        else:
            result.append({"id": id, "text": s})    

    return {"result": result}

@app.post("/page/")
async def image(image: UploadFile = File(...),
                language: str = Query("eng", enum=["eng", "deu", "rus"], description='Choice language OCR'),
                ):

    if image.filename and image.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PAGE:
        with open("temp", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)        

        custom_config = f'-l {language} --psm 3'    

        if image.filename.rsplit('.', 1)[1].lower() == 'pdf':
            images = convert_from_path(
            os.path.abspath('temp'), 
            poppler_path=poppler_path, 
            )

            results = []

            for image in images:
                filename = f'{temp_path}/{images.index(image)}.jpg'
                image.save(filename, 'JPEG')
                result = run(filename, custom_config)
                results.append(result)
            return results

        result = run('temp', custom_config)
        return [result]

    return 'Not correct file'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    uvicorn.run("main:app", 
                host='0.0.0.0', 
                port=port,
                log_level="info", 
                reload=True, 
                workers=3,
                )
