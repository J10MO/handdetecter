import cv2
import mediapipe as mp 
import autopy
import numpy as np
import math
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast,POINTER

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volumRange=volume.GetVolumeRange()
#print(volumRange)
minvol=volumRange[0]
maxvol=volumRange[1]

cap = cv2.VideoCapture(0)
initHand = mp.solutions.hands  # Initializing mediapipe
# Object of mediapipe with "arguments for the hands module"
mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
draw = mp.solutions.drawing_utils  # Object to draw the connections between each finger index
wScr, hScr = autopy.screen.size()  # Outputs the high and width of the screen (1920 x 1080)
pX, pY = 0, 0  # Previous x and y location
cX, cY = 0, 0  # Current x and y location


def handLandmarks(colorImg):
    landmarkList = []  # Default values if no landmarks are tracked

    landmarkPositions = mainHand.process(colorImg)  # Object for processing the video input
    landmarkCheck = landmarkPositions.multi_hand_landmarks  # Stores the out of the processing object (returns False on empty)
    if landmarkCheck:  # Checks if landmarks are tracked
        for hand in landmarkCheck:  # Landmarks for each hand
            for index, landmark in enumerate(hand.landmark):  # Loops through the 21 indexes and outputs their landmark coordinates (x, y, & z)
                draw.draw_landmarks(img, hand, initHand.HAND_CONNECTIONS)  # Draws each individual index on the hand with connections
                h, w, c = img.shape  # Height, width and channel on the image
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)  # Converts the decimal coordinates relative to the image for each index
                landmarkList.append([index, centerX, centerY])  # Adding index and its coordinates to a list
                
    return landmarkList


def fingers(landmarks):
    fingerTips = []  # To store 4 sets of 1s or 0s
    tipIds = [4, 8, 12, 16, 20]  # Indexes for the tips of each finger
    
    # Check if thumb is up
    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)
    
    # Check if fingers are up except the thumb
    for id in range(1, 5):
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:  # Checks to see if the tip of the finger is higher than the joint
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips 

while True:
     success, img =cap.read()
     img =cv2.flip(img,1)
     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
     lmlist = handLandmarks(imgRGB)
#     result=hands.process(imgRGB)
    
     #lmlist=[]
     #if result.multi_hand_landmarks:
        #for handlms in result.multi_hand_landmarks:
            #for id,lm in enumerate(handlms.landmark):
                #h,w,c=img.shape
                #cx, cy=int(lm.x * w), int(lm.y * h)
               # lmlist.append([id,cx,cy])
                #print(lmlist)
                #mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)

                
                
     if len(lmlist)!=0:
                   x1, y1 = lmlist[4][1],lmlist[4][2] 
                   x2, y2 = lmlist[8][1],lmlist[8][2]
                   cx,cy=(x1+x2)//2,(y1+y2)//2

                


                   cv2.circle(img,(x1,y1),10,(200,0,0),cv2.FILLED)
                   cv2.circle(img,(x2,y2),10,(200,0,0),cv2.FILLED)
                   cv2.line(img,(x1,y1),(x2,y2),(0,100,100),3)  
                   cv2.circle(img,(cx,cy),6,(200,0,0),cv2.FILLED)

                   length=math.hypot(x2-x1,y2-y1)
                    #print(length)
                    #length 200-50
                   if length<50:
                      cv2.circle(img,(cx,cy),6,(0,0,255),cv2.FILLED)
                   if length>200:
                      cv2.circle(img,(cx,cy),6,(0,255,0),cv2.FILLED)
                     
                   vol= np.interp(length,[50,200],[minvol,maxvol]) 
                   volume.SetMasterVolumeLevel(vol,None)
                   
     cv2.imshow('hand tracker', img)
     if cv2.waitKey(5)& 0xff == 27 :
        break            