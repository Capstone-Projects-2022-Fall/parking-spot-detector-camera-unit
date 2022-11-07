from cv2 import imwrite
from contextlib import contextmanager
import os

START_FRAME_NUM=1
TEMP_DIR="/tmp/"
PREFIX="frame-"
SUFFIX=".jpg"

class TempImage:
    frame_number=START_FRAME_NUM
    def __init__(self, frame):
        self.frame = frame
        self.TEMP_IMAGE_URI=TEMP_DIR+PREFIX+str(TempImage.frame_number)+SUFFIX

    def __enter__(self):
        imwrite(self.TEMP_IMAGE_URI, self.frame)
        self.file = open(self.TEMP_IMAGE_URI, "rb")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.file.closed:
            self.file.close()

        if os.path.exists(self.TEMP_IMAGE_URI):
            os.remove(self.TEMP_IMAGE_URI)

        # consider adding modulus

        TempImage.frame_number += 1
