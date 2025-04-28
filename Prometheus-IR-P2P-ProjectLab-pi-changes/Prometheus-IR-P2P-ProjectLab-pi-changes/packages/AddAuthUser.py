import cv2
import os


def frameCap(Frame, i):
    path = 'AuthUserDB/'
    #display captured frame to user
    # cv2.imshow("Captured Frame", Frame)
    #save image
    cv2.imwrite(os.path.join(path, f"AuthUser{i}.jpg"), Frame)


def main():
    # Access the camera
    cam = cv2.VideoCapture(0)
    # If camera is unavailable
    if not cam.isOpened():
        print("Sorry wasn't able to access camera.")
        exit()

    NumUserEncodings = 0
    while True:
        #Capture frame by frame from the camera
        ret, frame = cam.read()
        #if frame is not captured
        if not ret:
            print("There was an issue capturing the frame.")
            continue

        cv2.imshow("Capture Camera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # call function to cap and store a frame
            frameCap(frame, NumUserEncodings)
            NumUserEncodings += 1

        elif NumUserEncodings > 4:
            NumUserEncodings = 0

        elif key == ord('q'):
            break

        else:
            continue

    # release the camera when done
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
