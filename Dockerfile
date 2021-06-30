FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV APP_HOME app

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y
RUN apt-get install poppler-utils -y
RUN apt-get install libtesseract-dev libleptonica-dev liblept5 -y
RUN apt-get install tesseract-ocr -y 
# ~git2288-10f4998a-2 -y
RUN apt-get install tesseract-ocr-deu -y
RUN apt-get install tesseract-ocr-fra -y
RUN apt-get install tesseract-ocr-rus -y


RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    #pip install -r requirements.txt && \
    rm -rf requirements.txt

COPY ./app /app

EXPOSE 8000

# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["python", "main.py"]

