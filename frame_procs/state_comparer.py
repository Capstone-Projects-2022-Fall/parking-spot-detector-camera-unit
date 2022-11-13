import cv2
import hashlib
from utils.create_temp_image import TempImage

BUFF_SIZE = 65536

# initialize state
last_hash = ""

# mask uri
MASK_URI = "./res/mask.jpg"

# instantiate the mask
parking_mask = cv2.imread(MASK_URI)

# function describes whether or not we
# should continue processing of this frame

def is_relevant(frame):
    # perform instance segmentation
    instances = frame

    # calculate current state
    # mask against parking spaces

    # might want to XOR against open spots again to invert colors
    open_parking_spots = cv2.bitwise_and(parking_mask, instances)
    cv2.imwrite("./test.jpg", open_parking_spots)

    # calculate state

    # reduce resolution

    p = 0.10 # should be correlated to P/M

    # make a copy of open parking spots

    new_width = int(open_parking_spots.shape[1] * p)
    new_height = int(open_parking_spots.shape[0] * p)

    resized = cv2.resize(open_parking_spots, (new_width, new_height))

    # take a hash of the open parking spaces

    md5 = hashlib.md5()

    with TempImage(resized) as temp_resized:
        data = temp_resized.read(BUFF_SIZE)
        while data:
            md5.update(data)
            data = temp_resized.read(BUFF_SIZE)


    curr_hash = md5.hexdigest()
    print(curr_hash)

    # compare against last state

    if(curr_hash == last_hash):
        return False

    # if different, send to server

    last_hash = curr_hash

    return True;

test_image = cv2.imread("./res/img1.jpg")
is_relevant(test_image)
