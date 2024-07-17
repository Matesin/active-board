import cv2
import time
import subprocess

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
        cv2.imshow(f"Camera {camera_id}", frame)
    picked_camera.release()
    cv2.destroyAllWindows()
    print("Camera released and windows destroyed.")


def get_camera_dict() -> dict:
    # Get all camera names
    index = 0
    cameras = {}
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_ANY)
        if not cap.read()[0]:
            break
        else:
            command = f'system_profiler SPCameraDataType | grep "^    [^ ]" | sed "s/    //" | sed "s/://"'
            camera_name = subprocess.run(command, shell=True, capture_output=True, text=True).stdout
            cameras[index] = camera_name[index]
            print(f"Camera {index}: {camera_name[index]}")
        cap.release()
        index += 1
    return cameras


if __name__ == "__main__":
    cameras = get_camera_dict()
    if len(cameras) == 0:
        print("There are no cameras available, ending program")
        exit(-1)
    print(f"The following cameras are available:")
    i = 0
    for camera in cameras:
        print(f"{i}: {camera}")
        i += 1
    camera_index = input("Input the camera index: ")
    while not camera_index.isdigit() or int(camera_index) not in cameras:
        camera_index = input("Input a valid camera index: ")
    print(f"Opening camera {camera_index}...")
    capture_video(int(camera_index))
    print("Ending program, jebuto.")
