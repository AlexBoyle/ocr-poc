#! /bin/bash

python3 proceser.py $1
tesseract ./output/final.jpg  - --psm 3 quiet --load_system_dawg false
echo "~~~~~~~"
tesseract ./output/final.jpg  - --psm 6 quiet --load_system_dawg false
echo "~~~~~~~"
tesseract ./output/final.jpg  - --psm 11 quiet --load_system_dawg false
echo "~~~~~~~"
tesseract ./output/final.jpg  - --psm 12 quiet --load_system_dawg false
echo "~~~~~~~"