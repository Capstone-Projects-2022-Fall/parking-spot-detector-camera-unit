from utils.create_temp_image import TempImage
from utils.server_api import send_frame, update_camera_state, send_annotated_frame
from frame_procs import state_comparer

def frame_consumer(latest_frame):
    while True:
        print("ready to recieve frame")
        frame = latest_frame.recieve_frame()
        with TempImage(frame) as temp_image_file:
            proc_info = {}
            if(state_comparer.is_relevant(frame, proc_info=proc_info)):
                send_frame(temp_image_file)
                update_camera_state(proc_info)
                with open("test.png", "rb") as annot:
                    send_annotated_frame(annot)
