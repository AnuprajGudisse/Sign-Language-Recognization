import numpy as np
from keras.models import model_from_json
import operator
import cv2
import sys, os

# Loading the model
json_file = open("model-bw.json", "r")
model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(model_json)
# load weights into new model
loaded_model.load_weights("model-bw.h5")
print("Loaded model from disk")

cap = cv2.VideoCapture(0)

# Category dictionary
categories = {0: 'ZERO',
              1: 'ONE', 
              2: 'TWO', 
              3: 'THREE',
              4: 'FOUR',
              5: 'FIVE',
              6:'SIX',
              7:'SEVEN',
              8:'EIGHT',
              9:'NINE',
              'a':'A',
              'b':'B',
              'c':'C',
              'd':'D',
              'e':'E',
              'f':'F',
              'g':'G',
              'h':'H',
              'i':'I',
              'j':'J',
              'k':'K',
              'l':'L',
              'm':'M',
              'n':'N',
              'o':'O',
              'p':'P',
              'q':'Q',
              'r':'R',
              's':'S',
              't':'T',
              'u':'U',
              'v':'V',
              'w':'W',
              'x':'X',
              'y':'Y',
              'z':'Z'
              }

while True:
    _, frame = cap.read()
    # Simulating mirror image
    frame = cv2.flip(frame, 1)
    
    # Got this from collect-data.py
    # Coordinates of the ROI
    x1 = int(0.5*frame.shape[1])
    y1 = 10
    x2 = frame.shape[1]-10
    y2 = int(0.5*frame.shape[1])
    # Drawing the ROI
    # The increment/decrement by 1 is to compensate for the bounding box
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
    # Extracting the ROI
    roi = frame[y1:y2, x1:x2]
    
    # Resizing the ROI so it can be fed to the model for prediction
    roi = cv2.resize(roi, (64, 64)) 
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, test_image = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("test", test_image)
    # Batch of 1
    result = loaded_model.predict(test_image.reshape(1, 64, 64, 1))
    prediction = {'ZERO': result[0][0], 
                  'ONE': result[0][1], 
                  'TWO': result[0][2],
                  'THREE': result[0][3],
                  'FOUR': result[0][4],
                  'FIVE': result[0][5],
                  'SIX': result[0][6],
                  'SEVEN': result[0][7],
                  'EIGHT': result[0][8],
                  'NINE': result[0][9],
                  'A': result[0][10],
                  'B': result[0][11],
                  'C': result[0][12],
                  'D': result[0][13],
                  'E': result[0][14],
                  'F': result[0][15],
                  'G': result[0][16],
                  'H': result[0][17],
                  'I': result[0][18],
                  'J': result[0][19],
                  'K': result[0][20],
                  'L': result[0][21],
                  'M': result[0][22],
                  'N': result[0][23],
                  'O': result[0][24],
                  'P': result[0][25],
                  'Q': result[0][26],
                  'R': result[0][27],
                  'S': result[0][28],
                  'T': result[0][29],
                  'U': result[0][30],
                  'V': result[0][31],
                  'W': result[0][32],
                  'X': result[0][33],
                  'Y': result[0][34],
                  'Z': result[0][35]
                  
                  }
    # Sorting based on top prediction
    prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
    
    # Displaying the predictions
    cv2.putText(frame, prediction[0][0], (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)    
    cv2.imshow("Frame", frame)
    
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: # esc key
        break
        
 
cap.release()
cv2.destroyAllWindows()
