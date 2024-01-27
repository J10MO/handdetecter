import cv2
import mediapipe
import numpy
import autopy
import numpy as np
import math
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast,POINTER


######################### voice 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volumRange=volume.GetVolumeRange()
#print(volumRange)
minvol=volumRange[0]
maxvol=volumRange[1]
######################################
cap = cv2.VideoCapture(0)
initHand = mediapipe.solutions.hands  # Initializing mediapipe
# Object of mediapipe with "arguments for the hands module"
mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
draw = mediapipe.solutions.drawing_utils  # Object to draw the connections between each finger index
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
    check, img = cap.read()  # Reads frames from the camera
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Changes the format of the frames from BGR to RGB7
    lmList = handLandmarks(imgRGB)
    # cv2.rectangle(img, (75, 75), (640 - 75, 480 - 75), (255, 0, 255), 2)
                   
              
    if len(lmList) != 0: #Confidence between Frequent Itemsets:It is another event handler in C# that is triggered when button9 is clicked.

        x1, y1 = lmList[8][1:]  # Gets index 8s x and y values (skips index value because it starts from 1)
        x2, y2 = lmList[4][1:]  # Gets index 12s x and y values (skips index value because it starts from 1)
        x3,y3=lmList[12][1:]
        finger = fingers(lmList)  # Calling the fingers function to check which fingers are up
        
        if finger[1] == 1 and finger[0] == 0:  # Checks to see if the pointing finger is up and thumb finger is down
            x3 = numpy.interp(x1, (75, 650 - 75), (0, wScr))  # Converts the width of the window relative to the screen width
            y3 = numpy.interp(y1, (75, 500 - 75), (0, hScr))
            cX = pX + (x3 - pX) / 7  # Stores previous x locations to update current x location
            cY = pY + (y3 - pY) / 7  # Stores previous y locations to update current y location
            cv2.circle(img,(x1,y1),10,(0,255,255),cv2.FILLED)
            autopy.mouse.move(wScr-cX, cY)  # Function to move the mouse to the x3 and y3 values (wSrc inverts the direction)
            pX, pY = cX, cY  # Stores the current x and y location as previous x and y location for next loop

        if finger[1] == 0 and finger[0] == 1:  # Checks to see if the pointer finger is down and thumb finger is up
            autopy.mouse.click()  # Left click
            cv2.circle(img,(x2,y2),10,(0,255,0),cv2.FILLED)

        if finger[1]==1 and finger[2]==1 and finger[0] == 0:
            autopy.mouse.click(autopy.mouse.Button.RIGHT)
            #cv2.circle(img,(x3,y3),10,(0,0,255),cv2.FILLED)
            


        if finger[1] == 1 and finger[0] == 1:

            x4, y4 = lmList[4][1:]
            x5, y5 = lmList[8][1:]
            cx,cy=(x4+x5)//2,(y4+y5)//2

            cv2.circle(img,(x4,y4),10,(200,0,0),cv2.FILLED)
            cv2.circle(img,(x5,y5),10,(200,0,0),cv2.FILLED)
            cv2.line(img,(x4,y4),(x5,y5),(0,100,100),3)  
            cv2.circle(img,(cx,cy),6,(200,0,0),cv2.FILLED)

            length=math.hypot(x5-x4,y5-y4)
                    #print(length)
                    #length 200-50
            if length<50:
              cv2.circle(img,(cx,cy),6,(0,0,255),cv2.FILLED)
            if length>200:
                cv2.circle(img,(cx,cy),6,(0,255,0),cv2.FILLED)
                     
            vol= np.interp(length,[50,200],[minvol,maxvol]) 
            volume.SetMasterVolumeLevel(vol,None)
         
            
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break