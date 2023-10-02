FROM ubuntu:22.04 as base

RUN apt-get update -y && apt-get upgrade -y
RUN apt install tesseract-ocr -y
RUN apt install libtesseract-dev -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt install libgl1-mesa-glx -y
RUN pip install numpy
RUN pip install opencv-python-headless
RUN pip install flask
RUN pip install pytesseract
RUN apt install curl -y
RUN apt-get install npm -y

RUN mkdir /main
WORKDIR /main
RUN mkdir ./client
RUN mkdir ./server

COPY ./client/public ./client/public
COPY ./client/src ./client/src
COPY ./client/.env ./client
COPY ./client/package.json ./client

COPY ./server ./server

COPY ./run.sh ./

WORKDIR /main/client

RUN npm install
FROM base as baseContainer

WORKDIR /main/client

RUN ls && npm run build





ENTRYPOINT ["/main/run.sh"]