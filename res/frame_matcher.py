import cv2
import io
import sys
import time
from utils.server_api import send_annotated_frame
from utils.create_temp_image import TempImage

JPEG=".jpg"

NUM_ARGS=len(sys.argv)
NUM_REQ_ARGS=4

VID_FILE_IDX=1
TIMES_FILE_IDX=2
AN_DIR_PATH_IDX=3

if NUM_ARGS != NUM_REQ_ARGS:
    print("usage: python frame_matcher.py <video_file_path> <times_file> <annotated_vid>")
    exit()

VID_FILE=sys.argv[VID_FILE_IDX]
TIMES_FILE=sys.argv[TIMES_FILE_IDX]
AN_VID_FILE=sys.argv[AN_DIR_PATH_IDX]

CREATE_FLAG="--create"

create_images = False
if CREATE_FLAG in sys.argv:
    create_images = True

def get_annotated_frames(filename):
    temp=[]
    with open(filename, "r") as file:
        temp = file.readlines()

    annotated_frames=[]
    for frame_num in temp:
        annotated_frames.append(int(frame_num))

    return annotated_frames

annotated_frames = get_annotated_frames(TIMES_FILE)

print(annotated_frames)

# thread for reading from video

def connect_camera(latest_frame):

    # open video file

    cap = cv2.VideoCapture(VID_FILE)
    cap2 = cv2.VideoCapture(AN_VID_FILE)

    # check if there was an error openning file

    if(not cap.isOpened()):
        print("video file could not be opened")
        exit()

    if(not cap2.isOpened()):
        print("video file could not be opened")
        exit()

    # determine fps of video

    FPS=cap.get(cv2.CAP_PROP_FPS)

    last = 0
    for current in annotated_frames:
        # calculate time to wait
        interval = (current - last) / FPS
        print(interval)

        # wait that time
        time.sleep(interval)

        # seek to the approriate frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, current)
        ret, frame = cap.read()

        # display the current frame
        cv2.imshow('frame', frame)

        # calculate annotated URI
        cap2.set(cv2.CAP_PROP_POS_FRAMES, current)
        ret2, frame2 = cap2.read()

        if create_images:
            annotated_frame = cv2.imwrite(annotated_frame_uri, frame)
        else:
            with TempImage(frame2) as temp_image:
                send_annotated_frame(temp_image)

        # push the captured frame as the latest_frame
        latest_frame.update_frame(frame)

        # check for close condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        last = current

    # clean up camera resources
    cap.release()
    cv2.destroyAllWindows()
