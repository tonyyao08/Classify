import numpy as np
import cv2

# link to camera ip
# http://192.168.1.246:8081/video
# dim = 1280cols by 720 rows
# http://10.104.235.30:8081/video

cap = cv2.VideoCapture('rtsp://admin:1234@10.104.235.30:8554/live')
b = True
while True:
    ret, frame = cap.read()
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    belt = frame[200:700, 100: 900]
    gray_belt = cv2.cvtColor(belt, cv2.COLOR_BGR2GRAY)

    _, thresh_img = cv2.threshold(gray_belt, 80, 255, cv2.THRESH_BINARY)
    cv2.imshow('thresh_img', thresh_img)
    # DETECT COINS:
    contours, _ = cv2.findContours(
        thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        # if 200 < x+w < 400 and area > 1000:
        if area > 1000 and 200 < x+w < 400:
            # Put a rectangle around the object
            cv2.rectangle(belt, (x, y), (x + w, y + h), (0, 255, 0), 5)

            #cv2.putText(belt, coin_type, (x, y-7), 1, 1, (0, 255, 0))

    cv2.imshow('section', belt)
    key = cv2.waitKey(30)
    # if escape key is hit then exit
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
