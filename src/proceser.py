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
    #cv2.imwrite("./output/init.jpg", image)


    #try to cut out non-important parts
    Mimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite("./output/g.jpg", Mimage)
    Mimage = cv2.threshold(Mimage, 100, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(Mimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

    #cv2.imwrite("./output/Mimage.jpg", Mimage)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    temp = cv2.drawContours(image=image, contours=contours, contourIdx=0, color=(255, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    #cv2.imwrite("./output/temp.jpg", temp)

    #cut out targeted area
    mask = np.zeros_like(image)
    mask = cv2.drawContours(image=mask, contours=contours, contourIdx=0, color=(255, 255, 255), thickness=-1, lineType=cv2.LINE_AA)
    out = np.zeros_like(mask)
    out[mask == 255] = image[mask == 255]
    #cv2.imwrite("./output/mask.jpg", mask)
    #cv2.imwrite("./output/crop-b.jpg", out)
    
    #crop
    gray = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
    contours = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    out = out[y:y+h,x:x+w]
    #cv2.imwrite('./output/crop.jpg',out)
    
    
    #reduce noise
    out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    #out = cv2.resize(out, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    out = cv2.adaptiveThreshold(out, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 20)
    #out = cv2.threshold(out, 250, 255, cv2.THRESH_BINARY)[1]

    cv2.imwrite("./output/final.jpg", out)
def find_conturs_alt(ogImage):
    image = ogImage.copy()
    original = image.copy()
    #Find the relevent parts of the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilated = cv2.dilate(blurred, rectKernel)
    edged = cv2.Canny(dilated, 100, 200, apertureSize=3)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image_with_contours = cv2.drawContours(image.copy(), contours, -1, (0,255,0), 3)
    #cv2.imwrite("./output/image_with_contours.jpg", image_with_contours)
    largest_contours = sorted(contours, key = cv2.contourArea, reverse = True)[:1]
    receipt_contour = largest_contours[0]#get_receipt_contour(largest_contours)
    image_with_receipt_contour = cv2.drawContours(image.copy(), [receipt_contour], -1, (0, 255, 0), 2)
    #cv2.imwrite("./output/image_with_receipt_contour.jpg", image_with_receipt_contour)
    mask = np.zeros_like(image)
    mask = cv2.drawContours(image=mask, contours=[receipt_contour], contourIdx=-1, color=(255, 255, 255), thickness=-1, lineType=cv2.LINE_AA)
    out = np.zeros_like(mask)
    out[mask == 255] = image[mask == 255]
    #cv2.imwrite("./output/mask.jpg", mask)
    #cv2.imwrite("./output/cut.jpg", out)
    gray = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
    contours = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    out = out[y:y+h,x:x+w]
    #cv2.imwrite('./output/crop.jpg',out)
    final = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    #out = cv2.resize(out, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    final = cv2.adaptiveThreshold(final, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 20)
    cv2.imwrite("./output/final_alt.jpg", final)
if __name__ == "__main__":
    print(sys.argv[1])
    img = cv2.imread(sys.argv[1])
    c = find_conturs(img)
    c = find_conturs_alt(img)
    
        


    