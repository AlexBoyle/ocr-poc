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
    top = int(0.05 * image.shape[0]) # shape[0] = rows
    bottom = top
    left = int(0.05 * image.shape[1]) # shape[1] = cols
    right = left
    value = [0,0,0,0]
    image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, None, value)
    ogImage1 = cv2.copyMakeBorder(ogImage, top, bottom, left, right, cv2.BORDER_CONSTANT, None, value)
    cv2.imwrite("output/output1.jpg", image)
    # detect edges
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = 127
    image = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite("output/output2.jpg", image)
    image = cv2.blur(image, (5, 5), 0)
    cv2.imwrite("output/output3.jpg", image)
    image = cv2.Canny(image, 10, 200)
    cv2.imwrite("output/output4.jpg", image)
    image = cv2.dilate(image, np.ones((20, 20), np.uint8))
    cv2.imwrite("output/output5.jpg", image)
    # detect contours and sort them according to contour area
    contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    receipt_contour = None
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        # approximate a polygonal curve with the specified precision
        # function uses Ramer–Douglas–Peucker algorithm
        approx_curve = cv2.approxPolyDP(contour, 0.05 * perimeter, True) # contour, epsilon, closed? 
        if len(approx_curve) == 4:
            receipt_contour = approx_curve
            break
    mask = np.zeros_like(ogImage1)
    mask = cv2.drawContours(image=mask, contours=contours, contourIdx=0, color=(255, 255, 255), thickness=cv2.FILLED, lineType=cv2.LINE_AA)
    out = np.zeros_like(mask)
    out[mask == 255] = ogImage1[mask == 255]
    cv2.imwrite("output/output6.jpg", mask)
    out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    #out = cv2.threshold(out, thresh, 255, cv2.THRESH_BINARY)[1]
    out = cv2.resize(out, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    kernel = np.ones((1, 1), np.uint8)
    out = cv2.dilate(out, kernel, iterations=10)
    out = cv2.erode(out, kernel, iterations=10)
    out = cv2.medianBlur(out, 3)
    #out = cv2.adaptiveThreshold(out, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    se=cv2.getStructuringElement(cv2.MORPH_RECT , (30,30))
    bg=cv2.morphologyEx(out, cv2.MORPH_DILATE, se)
    #out=cv2.divide(out, bg, scale=255)
    #out=cv2.threshold(out, 0, 255, cv2.THRESH_OTSU )[1] 
    cv2.imwrite("output/output7.jpg", out)
if __name__ == "__main__":
    TEST1 = sys.argv[1]
    img = cv2.imread(TEST1)
    c = find_conturs(img)
        


    