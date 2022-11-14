import cv2
import time
from utils.latest_frame import LatestFrame

INTERVAL=0.5
END_OF_VIDEO=1


# thread for connecting to and fetching incoming frames

def connect_camera(latest_frame):

    # connect to IP Camera

    cap = cv2.VideoCapture(0)

    # cap.open('rtsp://admin:password123@68.82.174.34:554/cam/realmonitor?channel=1&subtype=1')

    # while stream is readable
    # grab the latest frame every INTERVAL
    # insert it into the latest frame

    while(cap.isOpened()):
        time.sleep(INTERVAL)
        cap.set(cv2.CAP_PROP_POS_AVI_RATIO, END_OF_VIDEO)
        ret, frame = cap.read()
        # cv2.imshow('frame', frame)

        # push the captured frame as the latest_frame

        latest_frame.update_frame(frame)

        # check for close condition

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # clean up camera resources

    cap.release()
    cv2.destroyAllWindows()
