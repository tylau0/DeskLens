# DeskLens
Real-time text recognition and translation of Desktop screen

## Prerequisites:
### Basic
* Windows or MAC (Linux is not supported since the PIL library used in the program can't do desktop screen capture on that platform.)
* OpenCV
* Python3
* Python cv2 library
* Python Pillow library
### OCR
* If you choose Tesseract OCR, make sure you install Tesseract OCR, and tesseract-ocr is in the PATH. Also install Python pytesseractcv library.
* If you choose Google Cloud Vision API, make sure you apply for the cloud service and obtain the service credential file. Before you run the program, set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of that file.
* If you choose Microsoft Cognitive Cloud OCR service, make sure you apply for the cloud service and obtain a subscription key.
### Translation
* If you choose Google translation service, install Python googletrans library
* If you choose Microsoft Cognitive Cloud text translation service, make sure you apply for the cloud service and obtain a subscription key

## Customization:
### DeskLens.py
* In the "import" part, you can switch between gcv, mscv and tesseractcv for the OCR service. You can switch between googletrans and mstrans for the translation service.
* The constant MINWAIT defines the wait time between successive translation attempt in milliseconds. You need to set 3000ms or higher if you are using the free tier of Microsoft cognitive cloud translation service.
### mscv/__init__.py (for using Microsoft Cognitive Cloud OCR service)
* Update the SUBSCRIPTION_KEY and if needed, SERVICE_URL.
### mstrans/__init__.py (for using Microsoft Cognitive Cloud translation service)
* Update the subscriptionKey and if needed, base_url.

## Execution:
Run this in the command line: python DeskLens.py
Use the UI to define the capture area, and click on any translate button to trigger the translation.
