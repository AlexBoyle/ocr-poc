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
    cv2.imwrite("./output/init.jpg", image)


    #try to cut out non-important parts
    Mimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("./output/g.jpg", Mimage)
    Mimage = cv2.threshold(Mimage, 150, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(Mimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

    cv2.imwrite("./output/Mimage.jpg", Mimage)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    temp = cv2.drawContours(image=image, contours=contours, contourIdx=0, color=(255, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    cv2.imwrite("./output/temp.jpg", temp)

    #cut out targeted area
    mask = np.zeros_like(image)
    mask = cv2.drawContours(image=mask, contours=contours, contourIdx=0, color=(255, 255, 255), thickness=-1, lineType=cv2.LINE_AA)
    out = np.zeros_like(mask)
    out[mask == 255] = image[mask == 255]
    cv2.imwrite("./output/mask.jpg", mask)
    cv2.imwrite("./output/crop-b.jpg", out)
    
    #crop
    gray = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
    contours = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    out = out[y:y+h,x:x+w]
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
    
        


    