"""
Provides functionality for cropping, cutting out receipt from raw picture
"""
import cv2
import numpy as np
import sys
import math
import ocr
pytesseract = None
try:
    import pytesseract
except:
    print("Cant find pytesseract")
MAX_COLOR_VALUE = 255
MIN_COLOR_VALUE = 0
DEBUG = True


def saveImage(img, name, compression=100):
    cv2.imwrite(name + ".webp", img, [cv2.IMWRITE_WEBP_QUALITY, compression])

def crop(ogImage):
    image = ogImage.copy()
    image1 = ogImage.copy()
    image = cv2.bitwise_not(image)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
    image = cv2.dilate(image, rect_kernel, iterations=1)
    contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    x, y, w, h = cv2.boundingRect(contour)
    image1 = image1[y:y + h, x:x + w]
    image1 = cv2.copyMakeBorder(image1, 1, 1, 1, 1, cv2.BORDER_CONSTANT, None,
                                [MAX_COLOR_VALUE, MAX_COLOR_VALUE, MAX_COLOR_VALUE, MIN_COLOR_VALUE])
    return image1


def cutOnBrightness(ogImage):
    image = ogImage.copy()

    # Preprocesing for image simplification
    processedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avrBrightness = np.average(processedImage)
    if avrBrightness > 100:
        avrBrightness = 100
    processedImage = cv2.threshold(processedImage, avrBrightness, MAX_COLOR_VALUE, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(processedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    a = cv2.drawContours(image=processedImage.copy(), contours=[contour], contourIdx=-1,
                         color=(MAX_COLOR_VALUE, MAX_COLOR_VALUE, MIN_COLOR_VALUE), thickness=1, lineType=cv2.LINE_AA)
    if DEBUG: saveImage(a, "./output/a")
    # Simplify bounding box
    peri = cv2.arcLength(contour, True)
    # contour = cv2.approxPolyDP(contour, .05* peri, True)

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
    if DEBUG: saveImage(cut, "./output/cut")
    # Reduce noise
    out = cv2.cvtColor(cut, cv2.COLOR_BGR2GRAY)
    out = np.abs(np.subtract(out, 1))
    out = cv2.adaptiveThreshold(src=out, maxValue=MAX_COLOR_VALUE, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                thresholdType=cv2.THRESH_BINARY, blockSize=13, C=10)
    #cv2.floodFill(out, None, (0, 0), 0)
    #cv2.floodFill(out, None, (0, 0), 255)
    # out = remove_isolated_pixels(out)
    if DEBUG: saveImage(out, "./output/final")

    return out


def procesing(ogImage):
    image = ogImage.copy()
    ogImageCopy = ogImage.copy()

    ret, thresh1 = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if DEBUG: saveImage(dilation, "./output/dilation")
    # Creating a copy of image
    wordLocation = []
    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h <= 500: continue
        if w * h >= 20000: continue
        rect = cv2.rectangle(ogImageCopy, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cropped = ogImage[y:y + h, x:x + w]
        cropped = crop(cropped)
        cropped = cv2.resize(cropped, (0, 0), fx = 3, fy = 3)
        cropped = cv2.threshold(cropped, 125, MAX_COLOR_VALUE, cv2.THRESH_BINARY)[1]
        ocrOutput = ocr.runTesseract(cropped)
        if ocrOutput == "": ocrOutput = str(i)
        saveImage(cropped, "./output/cropped-"+str(i))
        wordLocation.append([x, y, str(ocrOutput)])
    wordLocation = sorted(wordLocation, key=lambda x: x[1])
    if DEBUG: saveImage(ogImageCopy, "./output/ogImageCopy")
    diff = 0
    for i, word in enumerate(wordLocation):
        if i != 0:
            diff = diff + (wordLocation[i][1] - wordLocation[i - 1][1])
    diff = math.floor(diff / (len(wordLocation) - 1) / 2)
    currentHeight = 0
    wordGrouping = [[]]
    output = ""
    for i, word in enumerate(wordLocation):
        if (currentHeight + diff) < word[1]:
            wordGrouping[-1] = sorted(wordGrouping[-1], key=lambda x: x[0])
            for word1 in wordGrouping[-1]:
                output = output + str.ljust(word1[2], 15) + " | "
            output = output + "\n"
            print(wordGrouping[-1])
            wordGrouping.append([])
            currentHeight = word[1]
        wordGrouping[-1].append(word)
    print(wordGrouping)

    return output


def process(imageName):
    output = ""
    img = cv2.imread(imageName)
    if DEBUG: saveImage(img, "./output/inital")
    preprocessed = preprocess(img)
    output = procesing(preprocessed)
    return output


if __name__ == "__main__":
    print(sys.argv[1])
    print(process(sys.argv[1]))
