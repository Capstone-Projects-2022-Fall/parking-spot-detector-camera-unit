from utils.create_temp_image import TempImage
from utils.server_api import send_frame
from frame_procs import state_comparer

def frame_consumer(latest_frame):
    while True:
        print("ready to recieve frame")
        frame = latest_frame.recieve_frame()
        with TempImage(frame) as temp_image_file:
            if(state_comparer.is_relevant(frame)):
                send_frame(temp_image_file, frame)
