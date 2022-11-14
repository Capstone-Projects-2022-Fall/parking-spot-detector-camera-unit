import json
import os
import requests
from requests import Request
from requests.compat import urljoin
from utils.get_config import get_config

DOMAIN=get_config()["server_address"]
CAMERA_ID=get_config()["camera_id"]

# sends a temporary frame file
def send_frame(frame_file, frame_data={}):
    print("sending frame " + frame_file.name)
    METHOD="POST"
    PATH="/frames"
    URL = urljoin(DOMAIN, PATH)
    params = {"camera_id": CAMERA_ID}
    data = {"datetime": "sample", "bytes": 1999, "camera_id": CAMERA_ID}
    files = {"frame": frame_file}

    res = requests.post(URL, params=params, files=files)

    print(res.ok)

def update_camera_state(frame_data={}):
    print("updating camera state ")
    METHOD="PATCH"
    PATH="/cameras/" + CAMERA_ID
    URL = urljoin(DOMAIN, PATH)
    data = frame_data

    res = requests.patch(URL, json=data)

    print(res.ok)


def send_annotated_frame(frame_file):
    print("sending frame " + frame_file.name)
    METHOD="POST"
    PATH="/cameras/" + CAMERA_ID + "/annotated"
    URL = urljoin(DOMAIN, PATH)
    files = {"frame": frame_file}

    res = requests.post(URL, files=files)

    print(res.ok)
