import cv2 as cv
from picamera import PiCamera
from io import BytesIO
import requests as req
import numpy as np
import json
import time
import image_classifier

FPS = 5


def capture_image():
    # Create the in-memory stream
    stream = BytesIO()
    with PiCamera() as camera:
        camera.rotation = 180
        camera.capture(stream, format='jpeg')
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)

    return stream
