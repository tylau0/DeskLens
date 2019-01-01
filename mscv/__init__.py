import os, requests, uuid, json
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, io
from PIL import ImageGrab as ig
import tempfile

SUBSCRIPTION_KEY = 'xxxx'
SERVICE_URL = 'westus.api.cognitive.microsoft.com'

class OCRDevice:

    def __init__(self):
        self.headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        }
        self.conn = http.client.HTTPSConnection(SERVICE_URL)
     
    def __exit__(self):
        self.conn.close()
        
    def scanScreen(self, startX, startY, endX, endY, lang):
        
        params = urllib.parse.urlencode({
            # Request parameters
            'language': lang,
            'detectOrientation ': 'true',
        })
        
        screen = ig.grab(bbox=(startX, startY, endX, endY))
        tmpFileName = os.path.join(tempfile.gettempdir(), 'tmp.jpg')
        screen.save(tmpFileName, "JPEG")
        f = io.open(tmpFileName, 'rb')
        self.conn.request("POST", "/vision/v1.0/ocr?%s" % params, f, self.headers)
        f.close()
        os.remove(tmpFileName)
        response = self.conn.getresponse()
        data = response.read()
        json_obj = json.loads(data.decode('utf-8'))
        textList = []
        
        for region in json_obj['regions']:
            for line in region['lines']:
                for word in line['words']:
                    textList.append(word['text'])
                textList.append('\n')
            textList.append('\n\n')
        return ''.join(textList)
        
