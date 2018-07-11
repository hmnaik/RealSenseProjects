import cv2 as cv
import numpy as np
from datetime import datetime
import os


class testClass:
    """"A simple example for class"""

def getDateTimeInfo():

    dateTime = datetime.now()
    # String for date
    dateString = dateTime.strftime("%m%d%Y") # Format : MMDDYYYY
    #dateString = str(dateInfo.year) + str(dateInfo.month) + str(dateInfo.day)
    # String for time
    timeString = dateTime.strftime("%H%M%S")

    return dateString, timeString

# Get date time info
dateStr, timeStr = getDateTimeInfo()


cap = cv.VideoCapture(0)
capture = False

if os.path.exists(os.path.join(os.getcwd(),dateStr)):
    print("Folder Exists Dumping Data")
else:
    os.mkdir(os.path.join(os.getcwd(),dateStr))

counter = 0

while True :
    ret, frame = cap.read()
    if frame is not None:
        cv.imshow("test",frame)
        counter = counter+1

        fileName = os.path.join(dateStr,"img_" + str(counter) + ".jpg")
        if capture is True:
            cv.imwrite(fileName, frame)


    k = cv.waitKey(1)
    if k == ord('q'):
        break

    if k == ord('c'):
        capture = not capture
        print("Capture Status : " , capture)
cap.release()
cv.destroyWindow("test")

