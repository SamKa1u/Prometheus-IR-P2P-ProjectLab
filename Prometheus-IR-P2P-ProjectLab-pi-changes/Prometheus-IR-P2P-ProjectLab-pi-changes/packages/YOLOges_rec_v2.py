from ultralytics import YOLO
import cv2
from packages.facialAuthenticator import *

# Load a YOLOv8n model
mdl_path = "CV_MODELS/YOLOv8ngestureRec.pt"
model = YOLO(mdl_path)

#known names
knames = ['User0', 'User1', 'User2', 'User3', 'User4']

#call loaduser function from facialAuthenticator return known facial encodings from AuthUser database
def load():
    loaduser()
    return loaduser()[5]

#call processing function from facialAuthenticator return authentication status as boolean
def auth(frame, kfencodings):
    _,_,authenticated,_,_ = processing(frame, kfencodings, knames)
    print(authenticated)
    return authenticated


def gesture(gst):
#         '''
#     main function: gesture
#         Args:
#             gst (string or None): initialized as None by prometheus_lighting_system.py
#         Returns:
#             returns detected gestures to prometheus_lighting_system.py
#     '''
    #initialize some variables
    #kfencodings = load()   '''you can comment this out to speed up program start time'''
    gesture = gst
    process = 200
    authorized = False     #'''gesture rec wont run if not True'''
    AddAuthUserflag = False  # triggered when a user is added in AddAuthUser reload encodings to update kfencodings

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
# '''
#             error in this block set authorized = True to bypass
#         
#     #facial authenticator
#         #check if user encodings changed
#         if AddAuthUserflag:
#             kfencodings = load()
#             AddAuthUserflag = False
#         else:
#             pass
#         
#         #check if this frame should be processed for auth users      
#         if process == 200:
#             authorized = auth(frame, kfencodings)
#         elif process == 0:
#             process = 200
#         else:
#             process = process
#         print(process)
#         process = process - 1
# '''
        #run inference
        if authorized:
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
        else:
            print("No authorized users detected")
        # quit condition
        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()
    cam.release()

if __name__ == "__main__":
    gesture(None)
