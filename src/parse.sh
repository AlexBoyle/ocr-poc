#! /bin/bash

python3 proceser.py $1
tesseract ./output/output7.jpg  - --psm 6 quiet