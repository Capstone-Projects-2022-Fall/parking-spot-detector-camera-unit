import cv2

import cv2
cap = cv2.VideoCapture()
cap.open('rtsp://admin:password123@192.168.1.169:554/cam/realmonitor?channel=1&subtype=1')

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
