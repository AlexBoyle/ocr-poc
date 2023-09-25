"""
Provides functionality for cropping, cutting out receipt from raw picture
"""
import cv2
import numpy as np
import sys
pytesseract = None
try:
    import pytesseract
except:
    print("Cant find pytesseract")
MAX_COLOR_VALUE = 255
MIN_COLOR_VALUE = 0
DEBUG = True
def saveImage(img, name, compression = 100):
    cv2.imwrite(name+".webp", img, [cv2.IMWRITE_WEBP_QUALITY, compression])
def cutOnBrightness(ogImage):
    image = ogImage.copy()

    # Preprocesing for image simplification
    processedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avrBrightness = np.average(processedImage)
    if avrBrightness > 100 :
        avrBrightness = 100
    processedImage = cv2.threshold(processedImage, avrBrightness, MAX_COLOR_VALUE, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(processedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    a = cv2.drawContours(image=processedImage.copy(), contours=[contour], contourIdx=-1, color=(MAX_COLOR_VALUE, MAX_COLOR_VALUE, MIN_COLOR_VALUE), thickness=1, lineType=cv2.LINE_AA)
    if DEBUG : saveImage(a, "./output/a")
    # Simplify bounding box
    peri = cv2.arcLength(contour, True)
    #contour = cv2.approxPolyDP(contour, .05* peri, True)

    # Create mask to cut out image
    mask = np.zeros_like(image)
    mask = cv2.drawContours(image=mask, contours=[contour], contourIdx=0,
                            color=(MAX_COLOR_VALUE, MAX_COLOR_VALUE, MAX_COLOR_VALUE), thickness=cv2.FILLED,
                            lineType=cv2.LINE_4)
    out = np.zeros_like(mask)
    out[mask == MAX_COLOR_VALUE] = image[mask == MAX_COLOR_VALUE]

    # Crop as much of the mask as possible
    x, y, w, h = cv2.boundingRect(contour)
    out = out[y:y + h, x:x + w]
    return out


def preprocess(ogImage):
    image = ogImage.copy()
    # Add border
    image = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_CONSTANT, None,
                               [MIN_COLOR_VALUE, MIN_COLOR_VALUE, MIN_COLOR_VALUE, MIN_COLOR_VALUE])
    cut = cutOnBrightness(image)
    if DEBUG : saveImage(cut, "./output/cut")
    # Reduce noise
    out = cv2.cvtColor(cut, cv2.COLOR_BGR2GRAY)
    out = np.abs(np.subtract(out, 1))
    out = cv2.adaptiveThreshold(src=out, maxValue=MAX_COLOR_VALUE, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                thresholdType=cv2.THRESH_BINARY, blockSize=13, C=10)
    if DEBUG : saveImage(out, "./output/final")

    return out
def func(conro):
    x, y, w, h = cv2.boundingRect(conro)
    return y
def procesing(ogImage):
    image = ogImage.copy()

    ret, thresh1 = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=func)
    if DEBUG : saveImage(dilation, "./output/dilation")
    # Creating a copy of image
    im2 = ogImage.copy()
    text = ""
    i = 0
    lastHeight = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        i = i+1
        if w*h <= 500: continue
        if w*h >= 10000: continue

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cropped = ogImage[y:y + h, x:x + w]
        # Apply OCR on the cropped image
        if lastHeight - x > 6: text = text + "\n"
        tesseractOutput = ""
        custom_oem_psm_config = r'--oem 3 --psm 13'
        if pytesseract is not None: tesseractOutput =  pytesseract.image_to_string(cropped, config=custom_oem_psm_config)
        saveImage(cropped, "./output/cropped-"+str(i)+"-"+str(tesseractOutput))
        lastHeight = y
        print(tesseractOutput)
        text = text + " " + str(tesseractOutput)
    if DEBUG : saveImage(im2, "./output/im2")
    return text
def process(imageName):
    output = ""
    output1 = ""
    img = cv2.imread(imageName)
    if DEBUG : saveImage(img, "./output/inital")
    preprocessed = preprocess(img)
    output = procesing(preprocessed)
    return output
if __name__ == "__main__":
    print(sys.argv[1])
    process(sys.argv[1])