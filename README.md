# create docker image 
docker build -t ocr-de-en .


# create docker container 
docker rm ocr && docker run  -d --name ocr -p 8001:8001 ocr-de-en

# open app
open  http://127.0.0.1:8001/docs 