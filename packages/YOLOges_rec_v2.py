from ultralytics import YOLO
import cv2
# from threading import  Event
# from Nav import *

# Load a YOLOv8n model
mdl_path = "CV_MODELS/YOLOv8ngestureRec.pt"
model = YOLO(mdl_path)

# def up():
#     translation('w')
#     # time.sleep(1)
# def down():
#     translation('s')
#     # time.sleep(1)
# def left():
#     translation('a')
#     # time.sleep(1)
# def right():
#     translation('d')
#     # time.sleep(1)

def gesture(gst):
    gesture = gst
    # initilize cam
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Camera unavailable")
        exit()
    while True:
        ret, frame = cam.read()
        #frame error check
        if not ret:
            print("Frame could not be read")
            continue
        #run inference
        results = model.predict(frame,conf=.5,imgsz= 480, max_det=1)

        #process results list
        for result in results:
            boxes = result.boxes.cls.tolist()
            while boxes:
                label = boxes[0]
                print(label)

                match label:
                    case 0:
                        gesture = 'b'
                                              ##blue
                    case 1:
                        gesture = 'bright'
                                                   ##brighten
                    case 2:
                        gesture = 'dim'
                                                   ##dim
                    case 3:
                        gesture =  'dec'   #'down'
                    case 4:
                        gesture = 'cap'            #enter
                    case 5:
                        gesture = 'g'
                                                   ##green
                    case 6:
                        gesture = 'light'  #'left'
                    case 7:
                        gesture = 'r'
                                                    ##red
                    case 8:
                        gesture =  'add'  #'right'
                    case 9:
                        gesture = 'inc'  #up
                    case _: print('unrecognized gesture')
                break

        #annotate frame
        bound_frame = results[0].plot()
        #display frame
        cv2.imshow("Bounding Boxes", bound_frame)
        # quit condition
        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()
    cam.release()

if __name__ == "__main__":
    gesture(None)
