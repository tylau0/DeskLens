import os, requests, uuid, json

subscriptionKey = 'xxxx'

base_url = 'https://api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'

headers = {
    'Ocp-Apim-Subscription-Key': subscriptionKey,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

class Translation:
    def __init__(self, text=''):
        self.text = text
        pass
        
    def setText(self, text):
        self.text = text

class Translator:
    def __init__(self):
        self.translation = Translation()
        pass
        
    def translate(self, origText, src, dest):
        ####params = '&from=' + src + '&to=' + dest
        params = '&to=' + dest
        constructed_url = base_url + path + params
        body = [{
            'text' : origText
        }]
        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()
        self.translation.setText(response[0]['translations'][0]['text'])
        return self.translation

        pass