import io
import os
import codecs
from PIL import ImageGrab as ig
import tempfile

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

class OCRDevice:

    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        pass
        
    def __exit__(self):
        pass
        
    def scanScreen(self, startX, startY, endX, endY, lang):
        screen = ig.grab(bbox=(startX, startY, endX, endY))
        tmpFileName = os.path.join(tempfile.gettempdir(), 'tmp.jpg')
        screen.save(tmpFileName, "JPEG")
        # Loads the image into memory
        with io.open(tmpFileName, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = self.client.document_text_detection(image=image)
        
        textList = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        textList.append(''.join([
                            symbol.text for symbol in word.symbols
                        ]))
                    textList.append('\n')
        return ''.join(textList)
