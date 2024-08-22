# ----------------------IMPORTS----------------------
import camera
from camera import get_camera_list, capture_video_classify, init_nets
import logging as log
import argparse

# ----------------------LOGGING CONFIG----------------------
log.basicConfig(level=log.INFO)


def get_bool_response(user_input: str) -> bool:
    output = False
    while user_input.lower() != 'y' and user_input.lower() != 'n':
        user_input = input("Input a valid answer: ")
    if user_input.lower() == 'y':
        output = True
    return output


def main() -> None:
    # Demo program for the product
    # Made for macOS, Windows and Linux

    # ----------------------BASH ARGS----------------------
    parser = argparse.ArgumentParser(description='Use this script to run age and gender recognition using OpenCV.')

    parser.add_argument("--device", default="cpu", help="Device to inference on")

    parser.add_argument('--fps', type=int, default=10, help='Frames per second that the camera will capture')

    parser.add_argument('--list_faces', type=bool, default=False, help='List all faces in the frame')

    # Parse args
    args = parser.parse_args()

    # Set FPS
    camera.FPS = args.fps if args.fps in args else camera.FPS
    camera.LIST_FACES = args.list_faces if args.list_faces in args else camera.LIST_FACES

    camera_list = get_camera_list()
    if len(camera_list) == 0:
        log.error("There are no cameras available, ending program")
        exit(-1)

    # List all available cameras
    print(f"The following cameras are available:")
    index = 1
    for camera_name in camera_list:
        print(f"Camera {index}: {camera_name}")
        index += 1
    camera_index = input("Input the camera index: ")
    while not camera_index.isdigit() or int(camera_index) - 1 > len(camera_list):
        camera_index = input("Input a valid camera index: ")

    # Ask user if they want to run the demo
    demo = input("Do you want to run the demo? (y/n): ")
    demo = get_bool_response(demo)

    log.info(f"Opening camera {camera_index}...")

    init_nets(args)
    capture_video_classify(int(camera_index), demo)
    log.info("Ending program, jebuto.")


if __name__ == "__main__":
    main()
