"""
Provides functionality for cropping, cutting out receipt from raw picture
"""
import cv2
import numpy as np
import sys

MAX_COLOR_VALUE = 255
MIN_COLOR_VALUE = 0
def cutOnBrightness(ogImage):
    image = ogImage.copy()
    
    # Preprocesing for image simplification
    processedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avrBrightness = np.average(processedImage)
    print(avrBrightness)
    processedImage = cv2.threshold(processedImage, 100, MAX_COLOR_VALUE, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(processedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )[0]
    contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    
    a = cv2.drawContours(image=processedImage.copy(), contours=[contour], contourIdx=-1, color=(MAX_COLOR_VALUE, MAX_COLOR_VALUE, MIN_COLOR_VALUE), thickness=1  , lineType=cv2.LINE_AA)
    cv2.imwrite("./output/a.jpg", a)
   
    # Simplify bounding box
    #peri = cv2.arcLength(contour, True)
    #contour = cv2.approxPolyDP(contour, .05 * peri, True)
    
    # Create mask to cut out image
    mask = np.zeros_like(image)
    mask = cv2.drawContours(image=mask, contours=[contour], contourIdx=0, color=(MAX_COLOR_VALUE, MAX_COLOR_VALUE, MAX_COLOR_VALUE), thickness=cv2.FILLED  , lineType=cv2.LINE_4)
    out = np.zeros_like(mask)
    out[mask == MAX_COLOR_VALUE] = image[mask == MAX_COLOR_VALUE]
    
    # Crop as much of the mask as possible
    x,y,w,h = cv2.boundingRect(contour)
    out = out[y:y+h,x:x+w]
    return out

def preprocess(ogImage):
    image = ogImage.copy()
    # add border
    image = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_CONSTANT, None, [MIN_COLOR_VALUE,MIN_COLOR_VALUE,MIN_COLOR_VALUE,MIN_COLOR_VALUE])
    cut = cutOnBrightness(image)
    cv2.imwrite("./output/cut.jpg", cut)
    #reduce noise
    out = cv2.cvtColor(cut, cv2.COLOR_BGR2GRAY)
    out = np.abs(np.subtract(out,1))
    out = cv2.adaptiveThreshold(src=out, maxValue=MAX_COLOR_VALUE, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C , thresholdType=cv2.THRESH_BINARY, blockSize=13, C=10)
    cv2.imwrite("./output/final.jpg", out)
if __name__ == "__main__":
    print(sys.argv[1])
    img = cv2.imread(sys.argv[1])
    cv2.imwrite("./output/inital.jpg", img)
    c = preprocess(img)
    
        


    