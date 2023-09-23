#! /bin/bash

python3 proceser.py $1
tesseract ./output/final.jpg  - --psm 3 quiet --load_system_dawg false