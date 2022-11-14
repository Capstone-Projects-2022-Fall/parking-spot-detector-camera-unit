from threading import Thread
from utils.read_from_camera import connect_camera
# from res.frame_matcher import connect_camera
from utils.frame_consumer import frame_consumer
from utils.latest_frame import LatestFrame
from utils.get_config import get_config

exit(0)

# config camera unit properties

NUM_FRAME_CONSUMER=get_config()["num_consumer_threads"]

# create global vars

latest_frame = LatestFrame()

# create and start frame_consumer worker threads

worker_threads = []

for i in range(NUM_FRAME_CONSUMER):
    new_thread = Thread(target=frame_consumer, kwargs={"latest_frame": latest_frame})
    new_thread.daemon = True
    worker_threads.append(new_thread)
    new_thread.start()

# create and start configuration thread

# connect to camera

connect_camera(latest_frame=latest_frame)
