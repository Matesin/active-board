import cv2

print(f"OpenCV version: {cv2.__version__}")
build_info = cv2.getBuildInformation()
print("OpenCV build information:")
print(build_info)