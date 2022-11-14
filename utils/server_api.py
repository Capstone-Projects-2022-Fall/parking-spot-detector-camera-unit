import os
import requests
from requests import Request
from requests.compat import urljoin

DOMAIN=os.environ.get('DOMAIN_NAME')
CAMERA_ID=os.environ.get('CAMERA_ID')

# sends a temporary frame file
def send_frame(frame_file, frame_data):
    print("sending frame " + frame_file.name)
    METHOD="POST"
    PATH="/frames"
    URL = urljoin(DOMAIN, PATH)
    params = {"camera_id": CAMERA_ID}
    data = {"datetime": "sample", "bytes": 1999, "camera_id": CAMERA_ID} | frame_data
    files = {"frame": frame_file}

    res = requests.post(URL, params=params, files=files, data=data)

    print(res.ok)

def send_annotated_frame(frame_file):
    print("sending frame " + frame_file.name)
    METHOD="POST"
    PATH="/annotated/" + CAMERA_ID
    URL = urljoin(DOMAIN, PATH)
    files = {"frame": frame_file}

    res = requests.post(URL, files=files)

    print(res.ok)
