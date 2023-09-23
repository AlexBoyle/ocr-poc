"""
Provides functionality for cropping, cutting out receipt from raw picture
"""
import cv2
import numpy as np
import sys

def find_conturs(ogImage):
    """
    Find receipt contours

    Returns None if no contours were found
    """
    image = ogImage.copy()
    
    # add border
    image = cv2.copyMakeBorder(image, 100, 100, 100, 100, cv2.BORDER_CONSTANT, None, [0,0,0,0])
    ogImage1 = cv2.copyMakeBorder(ogImage, 100, 100, 100, 100, cv2.BORDER_CONSTANT, None, [0,0,0,0])
    cv2.imwrite("./output/inital.jpg", ogImage1)

    #try to cut out non-important parts
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
    image = cv2.dilate(image, np.ones((20, 20), np.uint8))
    cv2.imwrite("./output/test.jpg", image)
    contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    receipt_contour = None
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx_curve = cv2.approxPolyDP(contour, 0.05 * perimeter, True)
        if len(approx_curve) == 4:
            receipt_contour = approx_curve
            break
            
    #cut out targeted area
    mask = np.zeros_like(ogImage1)
    mask = cv2.drawContours(image=mask, contours=contours, contourIdx=0, color=(255, 255, 255), thickness=cv2.FILLED, lineType=cv2.LINE_AA)
    out = np.zeros_like(mask)
    out[mask == 255] = ogImage1[mask == 255]
    cv2.imwrite("./output/mask.jpg", mask)
    
    #crop
    leeway = 30
    gray = cv2.cvtColor(out,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    out = img[y-leeway:y+h+leeway,x-leeway:x+w+leeway]
    cv2.imwrite('./output/crop.jpg',out)
    
    #reduce noise
    out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    #out = cv2.resize(out, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    out = cv2.adaptiveThreshold(out, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 20)
    #out = cv2.threshold(out, 250, 255, cv2.THRESH_BINARY)[1]

    cv2.imwrite("./output/final.jpg", out)
if __name__ == "__main__":
    print(sys.argv[1])
    img = cv2.imread(sys.argv[1])
    c = find_conturs(img)
    
        


    