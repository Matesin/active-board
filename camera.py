import platform


import cv2
import time
import subprocess
import image_classifier as ic
import argparse
import logging as log

# ----------------------MACROS----------------------
FPS = 5


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
def capture_video_classify(camera_id: int, demo) -> None:
    """
    Captures live video feed and classifies faces within its frame
    :param camera_id: Chosen input camera
    :param age_net: Network to determine age from a given image
    :param gender_net: Network to determine gender from a given image
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
        people, frame_out = ic.classify_image(frame, demo)  # Classify the frame
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

# ----------------------MAIN----------------------
if __name__ == "__main__":

    # ----------------------BASH ARGS----------------------
    parser = argparse.ArgumentParser(description='Use this script to run age and gender recognition using OpenCV.')

    parser.add_argument('--input',
                        help='Path to input image or video file. Skip this argument to capture frames from a camera.')

    parser.add_argument("--device", default="cpu", help="Device to inference on")

    parser.add_argument('--fps', type=int, default=10, help='Frames per second that the camera will capture')

    # Parse args
    args = parser.parse_args()

    # Set FPS
    FPS = args.fps if args.fps in args else FPS
    camera_list = get_camera_list()
    if len(camera_list) == 0:
        log.error("There are no cameras available, ending program")
        exit(-1)
    print(f"The following cameras are available:")
    index = 1
    for camera_name in camera_list:
        print(f"Camera {index}: {camera_name}")
        index += 1
    camera_index = input("Input the camera index: ")
    while not camera_index.isdigit() or int(camera_index) - 1 > len(camera_list):
        camera_index = input("Input a valid camera index: ")
    demo = input("Do you want to run the demo? (y/n): ")
    while demo.lower() != 'y' and demo.lower() != 'n':
        demo = input("Input a valid answer: ")
    if demo.lower() == 'y':
        demo = True
    else: demo = False
    print(f"Opening camera {camera_index}...")
    age_net, gender_net = ic.load_caffe_models(args)
    # capture_video(int(camera_index))
    capture_video_classify(int(camera_index), demo)
    log.info("Ending program, jebuto.")
