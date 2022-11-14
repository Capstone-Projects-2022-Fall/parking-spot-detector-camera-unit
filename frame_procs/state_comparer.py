import copy
import cv2
import hashlib
import os
from utils.create_temp_image import TempImage
from utils.get_config import get_config
from utils.find_open_segments import find_open_segments, find_mid_points_and_size

BUFF_SIZE = 65536

# initialize state
last_hash = ""

# mask uri
MASK_URI = get_config()["mask_uri"]
VECTOR_URI = get_config()["vector_uri"]

# instantiate the mask
parking_mask = cv2.imread(MASK_URI)

# function describes whether or not we
# should continue processing of this frame

def is_relevant(frame, proc_info={}):
    global last_hash

    # perform instance segmentation

    # redundant temp image

    output_image = None

    os.chdir("yolseg")

    with TempImage(frame) as temp_image:
        os.system("bin/Release/Yolact 0.3f " + temp_image.name)
        output_image = cv2.imread("result.png")

    os.chdir("../")

    instances = cv2.bitwise_not(output_image)

    # calculate current state
    # mask against parking spaces

    cv2.imwrite("instance.png", instances)

    # might want to XOR against open spots again to invert colors

    open_parking_spots = cv2.bitwise_and(parking_mask, instances)
    open_parking_spots = cv2.bitwise_not(open_parking_spots)
    open_parking_spots = cv2.bitwise_and(open_parking_spots, parking_mask)

    cv2.imwrite("./test.png", open_parking_spots)

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

    # calculate distances
    spot_vector = cv2.imread(VECTOR_URI)

    segments = find_open_segments(open_parking_spots, spot_vector)
    spot_sizes = find_mid_points_and_size(segments)


    proc_info.update(segments=segments, spot_sizes=spot_sizes)

    return True


"""
INPUT_FRAME_URI=get_config()["test_input_frame"]
test_image = cv2.imread(INPUT_FRAME_URI)
test = {}
is_relevant(test_image, proc_info=test)
print(test)

from utils.server_api import send_frame, update_camera_state, send_annotated_frame

with open(INPUT_FRAME_URI, "rb") as file:
    send_frame(file)
    update_camera_state(test)
    with open("./test.png", "rb") as result:
      send_annotated_frame(result)
"""
