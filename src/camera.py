# ----------------------IMPORTS----------------------
import platform

import cv2
import time
import subprocess
from controller import image_classifier as ic
from model import customer_picker as cp, product_picker as pp
import logging as log

# ----------------------MACROS----------------------
FPS = 5
LIST_FACES = False
PRODUCTS_LIST_FILENAME = "products.json"
CUSTOMER_COOLDOWN_THRESHOLD = 10
CUSTOMER_LIST_SIZE_THRESHOLD = 10


# ----------------------FUNCTION----------------------
def capture_video(camera_id: int) -> None:
    """
    Captures live video feed
    :param camera_id: Chosen input camera
    :return: None
    """
    picked_camera = cv2.VideoCapture(camera_id)
    t1 = time.time()
    while True:
        t2 = time.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if t2 - t1 < 1 / FPS:
            continue
        else:
            ret, frame = picked_camera.read()
            if not ret:
                log.error("Camera not available.")
                break
            t1 = t2
            # Display the resulting frame
            cv2.imshow(f"Camera {camera_id}", frame)
    picked_camera.release()
    cv2.destroyAllWindows()
    log.info("Camera released and windows destroyed.")


# ----------------------FUNCTION----------------------
def capture_video_classify(camera_id: int, demo) -> list:
    """
    Captures live video feed and classifies faces within its frame
    :param camera_id: Chosen input camera
    :param demo: Boolean value, if True, the frame will be annotated
    :return: None
    """
    products_list = init_products()
    picked_camera = cv2.VideoCapture(camera_id)
    t1 = time.time()
    cooldown_timer = t1
    picked_customers_list = []
    averaged_customer = None
    prev_averaged_customer = None
    log.info("Starting the camera, press 'q' to quit.")
    customer_cooldown = 0
    while True:
        t2 = time.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if t2 - t1 < 1 / FPS: #or (cooldown_timer is not None and t2 - cooldown_timer < 100):
            continue
        else:
            ret, frame = picked_camera.read()
            if not ret:
                log.error("Camera not available.")
                break
            t1 = t2
            # Display the resulting frame
        people, frame_out = ic.classify_image(frame, demo)  # Classify the frame
        if LIST_FACES:
            for person in people:
                log.info(f"Person: {person}")

        # Evaluate faces in the frame
        picked_customer = cp.evaluate_faces(people)  # Evaluate the customers
        if demo:
            if picked_customer is not None:
                log.info(f"Customer picked: {str(picked_customer)}")
            else:
                log.info("No faces detected.")

        if picked_customer is not None:
            picked_customers_list.append(picked_customer)
            log.info(f"Customer added to the list: {picked_customer}"
                      f"\nList size: {len(picked_customers_list)}")

        if len(picked_customers_list) > CUSTOMER_LIST_SIZE_THRESHOLD:
            picked_customers_list.pop(0)
        averaged_customer = cp.average_customers(picked_customers_list)

        if customer_cooldown == 0:
            prev_averaged_customer = averaged_customer
            customer_cooldown += 1
        elif prev_averaged_customer.__eq__(averaged_customer) and customer_cooldown > CUSTOMER_COOLDOWN_THRESHOLD:
            picked_products = pp.pick_products(averaged_customer.product_threshold, products_list)
            cooldown_timer = time.time()
            customer_cooldown = 0
            yield picked_products

        cv2.imshow(f"Camera {camera_id}", frame_out)
    picked_camera.release()
    cv2.destroyAllWindows()
    log.info("Camera released and windows destroyed.")


# ----------------------FUNCTION----------------------
def get_camera_list() -> list:
    """
    Scans the computer for all available video input devices
    :return: Dictionary of available cameras and their respective indices
    """
    cameras = []
    if platform.system().__eq__('Linux') or platform.system().__eq__('Darwin'):
        command = 'system_profiler SPCameraDataType | grep "^    [^ ]" | sed "s/    //" | sed "s/://"'
        cameras = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip().split('\n')
    elif platform.system().__eq__('Windows'):
        i = 10
        j = 0
        while i > 0:
            cap = cv2.VideoCapture(j)
            if cap.read()[0]:
                cameras.append(j)
                cap.release()
            j += 1
            i -= 1
    else:
        log.error("Unsupported OS, ending program.")
        exit(-1)
    return cameras


# ----------------------FUNCTION----------------------
def init_nets(args) -> None:
    ic.age_net, ic.gender_net = ic.load_caffe_models(args)
    log.info("Nets initialized.")


# ----------------------FUNCTION----------------------
def init_products() -> list:
    """
    Initializes products from a file
    :return: List of products
    """
    products = pp.deserialize_products(PRODUCTS_LIST_FILENAME)
    log.info("Products initialized.")
    return products
