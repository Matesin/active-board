# visual recognition API key: AALtVzXYrmnUq4Rma4qERYrbFLBXQm-8yefjM--FPAVa

import cv2 as cv
from picamera import PiCamera
from io import BytesIO
import requests as req
import numpy as np
import json
from datetime import datetime


def capture_image():
    # Create the in-memory stream
    stream = BytesIO()
    camera = cv.VideoCapture(0)
    frame = camera.read()
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)

    return stream


if __name__ == "__main__":

    url = "https://gateway.watsonplatform.net/visual-recognition/api/v3/detect_faces?version=2018-03-19"
    username = "apikey"
    password = "AALtVzXYrmnUq4Rma4qERYrbFLBXQm-8yefjM--FPAVa"
    image_stream = capture_image()
    files = {'file':('camera', image_stream.getvalue(), 'image/jpg')}
    resp = req.post(url, files=files, auth=(username, password))
    print("code: {}\n\nresponse:\n{}".format(resp.status_code, json.dumps(resp.json(), indent=4)))
    result = resp.json()
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    decoded_image = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
    img = decoded_image if decoded_image is not None else 'default.jpg'

    for face in result['images'][0]['faces']:

        top_left = (face['face_location']['left'], face['face_location']['top'])
        bottom_right = (top_left[0] + face['face_location']['width'], top_left[1] + face['face_location']['height'])
        print(f"top_left {i + 1}: {top_left}, bottom_right: {bottom_right}")
        cv.rectangle(img, top_left, bottom_right, (0, 0, 200), 3)
        i += 1

        font = cv.FONT_HERSHEY_SIMPLEX
        bottom_left = top_left
        bottomLeftCornerOfText = (bottom_left[0]-100, bottom_left[1]-30)
        fontScale = 0.5
        fontColor = (0,0,0)
        lineType = 1
        gender = face['gender']['gender_label']
        age_min = face['age']['min']
        age_max = face['age']['max']
        cv.putText(img,'gender: {} age: {}-{}'.format(gender, age_min, age_max),
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            lineType)

cv.imwrite('image-obdelnik-{}.jpg'.format(datetime.now().strftime("%Y %H:%M:%S")), img)