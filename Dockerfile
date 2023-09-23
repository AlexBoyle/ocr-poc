FROM ubuntu:22.04
RUN apt-get update -y && apt-get upgrade -y
RUN apt install tesseract-ocr -y
RUN apt install libtesseract-dev -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt install libgl1-mesa-glx -y
RUN pip install numpy
RUN pip install opencv-python-headless
RUN pip install flask 
RUN apt install curl -y


RUN mkdir /main

WORKDIR /main
COPY ./src .






ENTRYPOINT ["./run.sh"]