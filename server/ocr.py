pytesseract = None
try:
    import pytesseract
except:
    print("Cant find pytesseract")






def runTesseract(ogImage, ocrOptions):
    if pytesseract is not None:
        custom_oem_psm_config = r'--oem 3 --psm 7 -l eng'
        #custom_oem_psm_config = r'--oem 3 --psm 13 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.\ $*@[]{}()'
        #custom_oem_psm_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789.\ '
        if ocrOptions is not None:
            custom_oem_psm_config = repr(ocrOptions)
        print(custom_oem_psm_config)
        return str(pytesseract.image_to_string(ogImage, config=custom_oem_psm_config)).strip()
    return ""