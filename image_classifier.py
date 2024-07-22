# Import required modules
import cv2 as cv
import logging as log

# CV heuristics TODO: improve model functionality
CONF_THRESHOLD = 0.7
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Male', 'Female']

# Camera info
CAMERA_RESOLUTION = 720


# ----------------------CLASS----------------------
class Person:
    def __init__(self, age, gender, proximity, coords: tuple):
        """
        Person class
        :param age: Age of the person
        :param gender: Gender of the person
        :param proximity: Proximity to the camera
        """
        self.age = age
        self.gender = gender
        self.proximity = proximity
        self.coords = coords


# ----------------------FUNCTION----------------------
def classify_image(gender_net, age_net, frame_in):
    """
    Classifies faces in a given frame
    :param gender_net:
    :param age_net:
    :param frame_in:
    :return: List of People objects, frame with faces outlined and details annotated
    """

    frame = cv.flip(frame_in, 1)

    face_classifier = cv.CascadeClassifier(
        'opencv/data/haarcascades/haarcascade_frontalface_default.xml')  # Load the face classifier, SPECIFY PATH
    faces = face_classifier.detectMultiScale(frame, 1.3, 5, minSize=(30, 30))

    if len(faces) == 0:
        return None, frame

    log.info(f"Faces detected: {len(faces)}")

    people = []

    for (x, y, w, h) in faces:

        # log.info(f"Face {faces.index((x, y, w, h))} x: {x}, y: {y}, w: {w}, h: {h}")
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        face = frame[y:y + h, x:x + w].copy()
        log.info(face)

        blob = cv.dnn.blobFromImage(face, 1.0, (244, 244), MODEL_MEAN_VALUES, swapRB=True)
        # log.info(blob)

        # Predict gender
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()
        log.info(f"Gender preds size: {gender_preds.size}")
        if gender_preds.size > 0 and gender_preds[0].argmax() < len(GENDER_LIST):
            if gender_preds[0].max() > CONF_THRESHOLD:
                gender = GENDER_LIST[gender_preds[0].argmax()]
            else:
                gender = "Unknown"
        else:
            gender = "Unknown"

        log.info("Gender Output : {}".format(gender_preds))
        log.info("Gender : {}, conf = {:.3f}".format(gender, gender_preds[0].max()))

        # Predict age
        age_net.setInput(blob)
        age_preds = age_net.forward()
        age = AGE_LIST[age_preds[0].argmax()]

        # TODO: Improve proximity assessment
        proximity = w / CAMERA_RESOLUTION
        people.append(Person(age, gender, proximity, (x, y)))  # Create a person object and append it to the list

        log.info(f"Assumed gender: {gender_preds}\n Assumed age: {age_preds}")

        label = "{},{}".format(gender, age)
        text_size = cv.getTextSize(label, cv.FONT_HERSHEY_TRIPLEX, 0.5, 1)[0]
        text_x = x + (w - text_size[0]) / 2
        cv.putText(frame,
                   label,
                   (int(text_x), y - 10),
                   cv.FONT_HERSHEY_TRIPLEX,
                   0.5,
                   (0, 255, 0),
                   1,
                   cv.LINE_AA)

    return people, frame


# ----------------------FUNCTION----------------------
def load_caffe_models(args) -> tuple:
    """
    Loads models for age and genders
    :param args: bash args
    :return: calibrated networks for age and gender assessment
    """

    # face_proto = "opencv/samples/dnn/face_detector/opencv_face_detector.pbtxt"
    # face_model = "opencv_face_detector_uint8.pb"

    age_proto = "proto_values/deploy_age.prototxt"
    age_model = "proto_values/age_net.caffemodel"

    gender_proto = "proto_values/deploy_gender.prototxt"
    gender_model = "proto_values/gender_net.caffemodel"

    # face_net = cv.dnn.readNet(face_model, face_proto)
    age_net = cv.dnn.readNet(age_model, age_proto)
    gender_net = cv.dnn.readNet(gender_model, gender_proto)

    # ----------------------SETTINGS----------------------
    # Set device
    if args.device == "cpu":
        age_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)

        gender_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)

        # face_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)

        log.info("Using CPU device")
    elif args.device == "gpu":
        age_net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        age_net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

        gender_net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        gender_net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

        # face_net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        # face_net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        log.info("Using GPU device")

    # If device is not valid, default to CPU
    elif args.device != "cpu" and args.device != "gpu":
        log.info("Invalid device selected, defaulting to CPU")

        age_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
        gender_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
        # face_net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)

        log.info("Using CPU device")

    return age_net, gender_net

# cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_IN
# TALL_PREFIX=~/opencv_gpu -DINSTALL_PYTHON_EXAMPLES=OFF -DINSTALL_C_EXAMPLES=OFF -DOPENCV_ENABLE_NONFREE=ON -DOPENCV_EXTRA_MODULES_PATH=~/cv2_gpu/opencv_contrib/modules -DPYTHON_EXECUTABLE=~/env/bin/python3 -DBUILD_EXAMPLES=ON -DWITH_CUDA=ON -DWITH_CUDNN=ON -DOPENCV_DNN_CUDA=ON  -DENABLE_FAST_MATH=ON -DCUDA_FAST_MATH=ON  -DWITH_CUBLAS=ON -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-10.2 -DOpenCL_LIBRARY=/usr/local/cuda-10.2/lib64/libOpenCL.so -DOpenCL_INCLUDE_DIR=/usr/local/cuda-10.2/include/ ..
