import cv2
import time
import subprocess
import image_classifier as ic
import argparse
import logging as log

# ----------------------MACROS----------------------
FPS = 10


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
def capture_video_classify(camera_id: int, age_net, gender_net) -> None:
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
        people, frame_out = ic.classify_image(gender_net, age_net, frame)  # Classify the frame
        cv2.imshow(f"Camera {camera_id}", frame_out)
    picked_camera.release()
    cv2.destroyAllWindows()
    log.info("Camera released and windows destroyed.")


# ----------------------FUNCTION----------------------
def get_camera_dict() -> dict:
    """
    Scans the computer for all available video input devices
    :return: Dictionary of available cameras and their respective indices
    """
    # Get all camera names
    # TODO: add Windows compatibility
    index = 0
    cameras = {}
    while True:
        try:
            cap = cv2.VideoCapture(index, cv2.CAP_ANY)
            if not cap.read()[0]:
                break
            else:
                command = 'system_profiler SPCameraDataType | awk \'/Model ID/{log substr($0, index($0,$6))}\''
                camera_name = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip()
                camera_names = camera_name.split('\n')
                if index < len(camera_names):
                    cameras[index] = camera_names[0]
                    # log(f"Camera {index}: {cameras[index]}")
                else:
                    break
            cap.release()
        except Exception as e:
            log.error(e) # Jebat tuhle exception, zkousim mutnout OpenCV errors, zkus najit jiny reseni pls
            break
        index += 1
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
    cameras = get_camera_dict()
    if len(cameras) == 0:
        log.error("There are no cameras available, ending program")
        exit(-1)
    print(f"The following cameras are available:")
    for index, camera_name in cameras.items():
        print(f"Camera {index}: {camera_name}")
    camera_index = input("Input the camera index: ")
    while not camera_index.isdigit() or int(camera_index) not in cameras.keys():
        camera_index = input("Input a valid camera index: ")
    print(f"Opening camera {camera_index}...")
    age_net, gender_net = ic.load_caffe_models(args)
    # capture_video(int(camera_index))
    capture_video_classify(int(camera_index), age_net, gender_net)
    log.info("Ending program, jebuto.")
