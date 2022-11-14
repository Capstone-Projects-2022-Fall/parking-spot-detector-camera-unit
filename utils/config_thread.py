from utils.create_temp_image import TempImage
from utils.server_api import send_frame

def frame_consumer(latest_frame):
    while True:
        frame = latest_frame.recieve_frame()
        with TempImage(frame) as temp_image_file:
            send_frame(temp_image_file)
