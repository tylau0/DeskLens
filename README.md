# DeskLens
Real-time text recognition and translation of Desktop screen capture

## Prerequisites:
* Windows or MAC (Linux is not supported since the PIL library used in the program can't do desktop screen capture on that platform.)
* Python3
* OpenCV
* Tesseract OCR - make sure tesseract-ocr is in the PATH
* Python Pillow library
* Python googletrans library/Microsoft Cognitive Cloud text translation service subscription key
* Python pytesseractcv library/Microsoft Cognitive Cloud OCR service subscription key

## Customization:
### DeskLens.py
* You can switch between googletrans and mstrans for the translation service.
* You can switch between mscv and tesseractcv for the OCR service.
* The constant MINWAIT defines the wait time between successive translation attempt in milliseconds. You need to set 3000ms or higher if you are using the free tier of Microsoft cognitive cloud translation service.
### mscv/__init__.py
* Update the SUBSCRIPTION_KEY and SERVICE_URL.
### mstrans/__init__.py
* Update the subscriptionKey and base_url.

## Execution:
python DeskLens.py
