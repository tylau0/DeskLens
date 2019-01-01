import pytesseract
from PIL import ImageGrab as ig

class OCRDevice:

    def __init__(self):
        pass
        
    def scanScreen(self, startX, startY, endX, endY, lang):
        # Change the tesseract one to standard one
        if lang == 'ja':
            lang = 'jpn'
        elif lang == 'zh-tw':
            lang = 'chi_tra'
        elif lang == 'en':
            lang = 'eng'
        
        screen = ig.grab(bbox=(startX, startY, endX, endY))
        ocrResult = pytesseract.image_to_string(screen, lang=lang).strip()
        return " ".join(ocrResult.split())
    