
# importing OpenCV library
import cv2
# initialize the camera
#camera port =0 because i have labtop camera
cap = cv2.VideoCapture(0)

while True:
    check, img = cap.read()  # Reads frames from the camera
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Changes the format of the frames from BGR to RGB

    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): #stop condition
        break