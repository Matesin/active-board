import cv2
import time
import subprocess
import image_classifier as ic
import argparse

# define fps
FPS = 20


# capture video from camera
def capture_video(camera_id: int) -> None:
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
                print("Camera not available.")
                break
            t1 = t2
            # Display the resulting frame
        cv2.imshow(f"Camera {camera_id}", frame)
    picked_camera.release()
    cv2.destroyAllWindows()
    print("Camera released and windows destroyed.")


def capture_video_classify(camera_id: int, age_net, gender_net) -> None:
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
                print("Camera not available.")
                break
            t1 = t2
            # Display the resulting frame
        faces, frame_out = ic.classify_image(gender_net, age_net, frame)  # Classify the frame
        cv2.imshow(f"Camera {camera_id}", frame_out)
    picked_camera.release()
    cv2.destroyAllWindows()
    print("Camera released and windows destroyed.")


def get_camera_dict() -> dict:
    # Get all camera names
    index = 0
    cameras = {}
    while True:
        try:
            cap = cv2.VideoCapture(index, cv2.CAP_ANY)
            if not cap.read()[0]:
                break
            else:
                command = 'system_profiler SPCameraDataType | awk \'/Model ID/{print substr($0, index($0,$3))}\''
                camera_name = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip()
                camera_names = camera_name.split('\n')
                if index < len(camera_names):
                    cameras[index] = camera_names[index]
                    # print(f"Camera {index}: {cameras[index]}")
                else:
                    break
            cap.release()
        except Exception as e:
            print(f"Error: {e}") # Jebat tuhle exception, zkousim mutnout OpenCV errors, zkus najit jiny reseni pls
            break
        index += 1
    return cameras


if __name__ == "__main__":
    # Parse bash args TODO: implement FPS argument to code
    parser = argparse.ArgumentParser(description='Use this script to run age and gender recognition using OpenCV.')

    parser.add_argument('--input',
                        help='Path to input image or video file. Skip this argument to capture frames from a camera.')

    parser.add_argument("--device", default="cpu", help="Device to inference on")

    parser.add_argument('--fps', type=int, default=10, help='Frames per second that the camera will capture')
    args = parser.parse_args()

    cameras = get_camera_dict()
    if len(cameras) == 0:
        print("There are no cameras available, ending program")
        exit(-1)
    print(f"The following cameras are available:")
    for index, camera_name in cameras.items():
        print(f"Camera {index + 1}: {camera_name}")
    camera_index = input("Input the camera index: ")
    while not camera_index.isdigit() or int(camera_index) not in cameras.keys():
        camera_index = input("Input a valid camera index: ")
    print(f"Opening camera {camera_index}...")
    age_net, gender_net = ic.load_caffe_models(args)
    # capture_video(int(camera_index))
    capture_video_classify(int(camera_index), age_net, gender_net)
    print("Ending program, jebuto.")
