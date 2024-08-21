from controller import camera
from controller.camera import get_camera_list, capture_video_classify, init_nets
import logging as log
import argparse


def main() -> None:
    # Demo program for the product
    # Made for macOS, Windows and Linux

    # ----------------------BASH ARGS----------------------
    parser = argparse.ArgumentParser(description='Use this script to run age and gender recognition using OpenCV.')

    parser.add_argument('--input',
                        help='Path to input image or video file. Skip this argument to capture frames from a camera.')

    parser.add_argument("--device", default="cpu", help="Device to inference on")

    parser.add_argument('--fps', type=int, default=10, help='Frames per second that the camera will capture')

    # Parse args
    args = parser.parse_args()

    # Set FPS
    FPS = args.fps if args.fps in args else camera.FPS
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
    # capture_video(int(camera_index))
    init_nets(args)
    capture_video_classify(int(camera_index), demo)
    log.info("Ending program, jebuto.")


if __name__ == "__main__":
    main()