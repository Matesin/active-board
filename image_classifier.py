# Import required modules
import cv2 as cv
import time
import argparse

# CV heuristics
CONF_THRESHOLD = 0.7
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Male', 'Female']

# Camera settings
global CAMERA_FPS

def get_face_box(net, frame):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > CONF_THRESHOLD:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, faceBoxes


def load_caffe_models(args) -> tuple:
    age_proto = "proto_values/deploy_age.prototxt"
    age_model = "proto_values/age_net.caffemodel"

    gender_proto = "proto_values/deploy_gender.prototxt"
    gender_model = "proto_values/gender_net.caffemodel"

    face_proto = "opencv/samples/dnn/face_detector/opencv_face_detector.pbtxt"
    face_model = "opencv_face_detector_uint8.pb"

    face_net = cv.dnn.readNet(face_model, face_proto)
    age_net = cv.dnn.readNet(age_model, age_proto)
    gender_net = cv.dnn.readNet(gender_model, gender_proto)

    # ----------------------SETTINGS----------------------
    # Set device
    if args.device == "cpu":
        age_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)

        gender_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)

        face_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)

        print("Using CPU device")
    elif args.device == "gpu":
        age_net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        age_net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

        gender_net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        gender_net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

        gender_net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        gender_net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        print("Using GPU device")

    # If device is not valid, default to CPU
    elif args.device != "cpu" and args.device != "gpu":
        print("Invalid device selected, defaulting to CPU")
        
        age_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
        gender_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
        face_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)

        print("Using CPU device")

    return age_net, gender_net, face_net


def video_detector(age_net, gender_net, face_net, args) -> None:
    # Open a video file or an image file or a camera stream
    cap = cv.VideoCapture(args.input if args.input else 0)
    padding = 20
    t1 = time.time()
    while cv.waitKey(1) < 0:
        # Read frame
        t2 = time.time()
        # Limit FPS
        if t2 - t1 < 1 / args.fps:
            continue
        has_frame, frame = cap.read()
        if not has_frame:
            cv.waitKey()
            break

        frame_face, bboxes = get_face_box(face_net, frame)
        if not bboxes:
            print("No face Detected, Checking next frame")
            continue

        for bbox in bboxes:
            # print(bbox)
            face = frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1),
                   max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]

            blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = GENDER_LIST[gender_preds[0].argmax()]
            print("Gender Output : {}".format(gender_preds))
            print("Gender : {}, conf = {:.3f}".format(gender, gender_preds[0].max()))

            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = AGE_LIST[age_preds[0].argmax()]
            print("Age Output : {}".format(age_preds))
            print("Age : {}, conf = {:.3f}".format(age, age_preds[0].max()))

            label = "{},{}".format(gender, age)
            cv.putText(frame_face, label, (bbox[0], bbox[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2,
                       cv.LINE_AA)
            cv.imshow("Age Gender Demo", frame_face)
            # cv.imwrite("age-gender-out-{}".format(args.input),frameFace)
        print("time : {:.3f}".format(time.time() - t1))


def main(args) -> None:

    video_detector(*load_caffe_models(args), args)

if __name__ == "__main__":
    # Parse bash arguments
    parser = argparse.ArgumentParser(description='Use this script to run age and gender recognition using OpenCV.')

    parser.add_argument('--input',
                        help='Path to input image or video file. Skip this argument to capture frames from a camera.')

    parser.add_argument("--device", default="cpu", help="Device to inference on")

    parser.add_argument('--fps', type=int, default=10, help='Frames per second that the camera will capture')

    args = parser.parse_args()
    main(args)


# cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_IN
# TALL_PREFIX=~/opencv_gpu -DINSTALL_PYTHON_EXAMPLES=OFF -DINSTALL_C_EXAMPLES=OFF -DOPENCV_ENABLE_NONFREE=ON -DOPENCV_EXTRA_MODULES_PATH=~/cv2_gpu/opencv_contrib/modules -DPYTHON_EXECUTABLE=~/env/bin/python3 -DBUILD_EXAMPLES=ON -DWITH_CUDA=ON -DWITH_CUDNN=ON -DOPENCV_DNN_CUDA=ON  -DENABLE_FAST_MATH=ON -DCUDA_FAST_MATH=ON  -DWITH_CUBLAS=ON -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-10.2 -DOpenCL_LIBRARY=/usr/local/cuda-10.2/lib64/libOpenCL.so -DOpenCL_INCLUDE_DIR=/usr/local/cuda-10.2/include/ ..
