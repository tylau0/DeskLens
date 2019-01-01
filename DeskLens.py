import tkinter as tk
import tkinter.scrolledtext as tkst
#from googletrans import Translator
from mstrans import Translator
import numpy as np
import cv2
import PIL
from PIL import ImageGrab as ig
####from mscv import OCRDevice
from tesseractcv import OCRDevice
import time
import threading
import tempfile
import os, io

VERSION = "0.4"
DEBUG = True

MINWAIT = 3000
current_milli_time = lambda: int(round(time.time() * 1000))

class DeskLens(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.screenscanner = OCRDevice()
        self.translator = Translator()
        
        self.bboxLabelFrame = tk.LabelFrame(self, text="Capture area")
        self.bboxLeftLabelFrame = tk.LabelFrame(self.bboxLabelFrame, text="Top Left")
        self.bboxRightLabelFrame = tk.LabelFrame(self.bboxLabelFrame, text="Bottom Right")
        self.startX = tk.StringVar(root, value='10')
        self.startXEntry = tk.Entry(self.bboxLeftLabelFrame, textvariable=self.startX, width=4)
        self.startY = tk.StringVar(root, value='110')
        self.startYEntry = tk.Entry(self.bboxLeftLabelFrame,textvariable=self.startY, width=4)
        self.endX = tk.StringVar(root, value='650')
        self.endXEntry = tk.Entry(self.bboxRightLabelFrame, textvariable=self.endX, width=4)
        self.endY = tk.StringVar(root, value='580')
        self.endYEntry = tk.Entry(self.bboxRightLabelFrame, textvariable=self.endY, width=4)
        self.showCapButton = tk.Button(self.bboxLabelFrame, text="Preview", command=self.showCapToggle)
        
        self.langLabelFrame = tk.LabelFrame(self, text="Input and output languages")
        self.fromPrompt = tk.Label(self.langLabelFrame, text="from")
        ####self.fromItem = tk.StringVar(self, value='jpn')
        ####self.fromOptionMenu = tk.OptionMenu(self.langLabelFrame, self.fromItem, 'jpn', 'chi_tra', 'eng')
        self.fromItem = tk.StringVar(self, value='ja')
        self.fromOptionMenu = tk.OptionMenu(self.langLabelFrame, self.fromItem, 'en', 'zh-tw', 'ja')
        self.toPrompt = tk.Label(self.langLabelFrame, text="to")
        self.toItem = tk.StringVar(self, value='en')
        self.toOptionMenu = tk.OptionMenu(self.langLabelFrame, self.toItem, 'en', 'zh-tw', 'ja')
        
        self.actionLabelFrame = tk.LabelFrame(self, text="Actions")
        self.onetimeTransButton = tk.Button(self.actionLabelFrame, text="One-time translate", command=self.translate)
        self.startAutoTransButton = tk.Button(self.actionLabelFrame, text="Start auto-translate", command = self.startAutoTransToggle)
        
        self.translationLabelFrame = tk.LabelFrame(self, text="Output")
        self.origTextLabelFrame = tk.LabelFrame(self.translationLabelFrame, text="OCR input")
        self.translatedTextLabelFrame = tk.LabelFrame(self.translationLabelFrame, text="Translation")
        self.origText = tkst.ScrolledText(master=self.origTextLabelFrame, wrap = tk.WORD, width=28, height=12)
        self.translatedText = tkst.ScrolledText(master=self.translatedTextLabelFrame, wrap = tk.WORD, width=28, height=12)
        
        self.statusStr = tk.StringVar()
        self.statusLabel = tk.Label(self, textvariable=self.statusStr, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        
        # lay the widgets out on the screen.
        self.startXEntry.pack(side="left", padx=10, pady=10)
        self.startYEntry.pack(side="right", padx=10, pady=10)
        self.endXEntry.pack(side="left", padx=10, pady=10)
        self.endYEntry.pack(side="right", padx=10, pady=10)
        self.bboxLeftLabelFrame.pack(side="left", padx=10, pady=10)
        self.bboxRightLabelFrame.pack(side="left", padx=10, pady=10)
        self.showCapButton.pack(side="right", padx=10, pady=10)
        self.bboxLabelFrame.pack(side="top", fill="x", padx=10, pady=10)
        
        self.fromPrompt.pack(side="left", padx=10, pady=10)
        self.fromOptionMenu.pack(side="left", padx=10, pady=10)
        self.toPrompt.pack(side="left", padx=10, pady=10)
        self.toOptionMenu.pack(side="left", padx=10, pady=10)
        self.langLabelFrame.pack(side="top", fill="x", padx=10, pady=10)
        
        self.onetimeTransButton.pack(side="left", padx=10, pady=10)
        self.startAutoTransButton.pack(side="left", padx=10, pady=10)
        self.actionLabelFrame.pack(side="top", fill="x", padx=10, pady=10)
        
        self.origText.pack(fill="y", padx=10, pady=10)
        self.translatedText.pack(fill="y", padx=10, pady=10)
        self.origTextLabelFrame.pack(side="left", fill="x", padx=10, pady=10)
        self.translatedTextLabelFrame.pack(side="right", fill="x", padx=10, pady=10)
        self.translationLabelFrame.pack(side="top", fill="x", padx=10, pady=10, expand=True)
        
        self.statusLabel.pack(side="bottom", fill="x")

        
    def showCapToggle(self):
        if self.showCapButton.config('text')[-1] == 'Preview':
            self.showCapButton.config(text="Stop preview")
            # Run a thread to the capture and ui update
            t = threading.Thread(target=self.showPreviewWindow, args=())
            t.daemon = True
            t.start()
        else:
            cv2.destroyAllWindows()
            self.showCapButton.config(text="Preview")
        pass
    
    def showPreviewWindow(self):
        cv2.namedWindow("Preview")
        bRefreshWindow = True
        while(self.showCapButton.config('text')[-1] == 'Stop preview'):
            if cv2.getWindowProperty('Preview',cv2.WND_PROP_VISIBLE) < 1:    
                cv2.destroyAllWindows()
                self.showCapButton.config(text="Preview")            
                break
            try:
                startX = int(self.startX.get())
                startY = int(self.startY.get())
                endX = int(self.endX.get())
                endY = int(self.endY.get())
                if startX >=0 and endX > startX and startY >=0 and endY > startY:
                    screen = ig.grab(bbox=(startX, startY, endX, endY))
                    image = np.array(screen)
                    cv2.imshow("Preview", image)
            except ValueError as e:
                print(str(e))
            except Exception as e:
                print(str(e))
            finally:
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    self.showCapButton.config(text="Preview")
                    break
            
    
    def translate(self):
        try:
            starttime = current_milli_time()
            startX = int(self.startX.get())
            startY = int(self.startY.get())
            endX = int(self.endX.get())
            endY = int(self.endY.get())
            fromlang = self.fromItem.get()
            tolang = self.toItem.get()
            if not(startX >=0 and endX > startX and startY >=0 and endY > startY):
                raise Exception("Scan area is not valid.")
                
            ocrResult = self.screenscanner.scanScreen(startX, startY, endX, endY, fromlang)
            
            translateResult = ''
            if len(ocrResult) > 0: 
                translateResult = self.translator.translate(ocrResult, src=fromlang, dest=tolang).text
            else:
                if DEBUG:
                    print("No translation needed...")
        
            self.origText.delete('1.0', tk.END)
            self.origText.insert('insert', ocrResult)
            self.translatedText.delete('1.0', tk.END)
            self.translatedText.insert('insert', translateResult)
            elapsed_time = current_milli_time() - starttime
            self.statusStr.set("Last translation took " + str(elapsed_time) + 'ms')
        except ValueError as e:
            print(str(e))
        except Exception as e:
            print(str(e))
        pass
    
    def autoTranslate(self):
        prev_startX =  int(self.startXEntry.get())
        prev_startY = int(self.startYEntry.get())
        prev_endX = int(self.endXEntry.get())
        prev_endY = int(self.endYEntry.get())
        while(self.startAutoTransButton.config('text')[-1] == 'Stop auto-translate'):
            starttime = current_milli_time()   
            self.translate()
            elapsed_time = current_milli_time() - starttime
            if elapsed_time < MINWAIT:
                time.sleep((MINWAIT-elapsed_time)/1000.0)
    
    def startAutoTransToggle(self):     
        if self.startAutoTransButton.config('text')[-1] == 'Start auto-translate':
            self.startAutoTransButton.config(text="Stop auto-translate")
            # Run a thread to the capture and ui update
            t = threading.Thread(target=self.autoTranslate, args=())
            t.daemon = True
            t.start()
        else:
            self.startAutoTransButton.config(text="Start auto-translate")
        pass

# if this is run as a program (versus being imported),
# create a root window and an instance,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    root.title("DeskLens: Real-time screen text scanner and translator v" + VERSION)
    root.geometry('600x600')
    frame = DeskLens(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()