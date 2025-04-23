import cv2
import face_recognition as fr

def loaduser():
    kfencodings = []
    try:
        User0 = fr.load_image_file('AuthUserDB/AuthUser0.jpg')
        UserEncoding0 = fr.face_encodings(User0)[0]
        kfencodings.append(UserEncoding0)
        encoding0 = True
    except:
        encoding0 = False

    try:
        User1 = fr.load_image_file('AuthUserDB/AuthUser1.jpg')
        UserEncoding1 = fr.face_encodings(User1)[0]
        kfencodings.append(UserEncoding1)
        encoding1 = True
    except:
        encoding1 = False

    try:
        User2 = fr.load_image_file('AuthUserDB/AuthUser2.jpg')
        UserEncoding2 = fr.face_encodings(User2)[0]
        kfencodings.append(UserEncoding2)
        encoding2 = True
    except:
        encoding2 = False

    try:
        User3 = fr.load_image_file('AuthUserDB/AuthUser3.jpg')
        UserEncoding3 = fr.face_encodings(User3)[0]
        kfencodings.append(UserEncoding3)
        encoding3 = True
    except:
        encoding3 = False

    try:
        User4 = fr.load_image_file('AuthUserDB/AuthUser4.jpg')
        UserEncoding4 = fr.face_encodings(User4)[0]
        kfencodings.append(UserEncoding4)
        encoding4 = True
        print("encoding4 =", encoding4)
    except:
        encoding4 = False
    return encoding0, encoding1, encoding2, encoding3, encoding4, kfencodings

def processing(frame, kfencodings, kfnames):
    authenticated = False
    # Speed up processing by resizing frame
    sml_frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)
    # color conversion for face rec
    rgbSml_frame = cv2.cvtColor(sml_frame, cv2.COLOR_BGR2RGB)
    # find face locations in refined frame
    face_locations = fr.face_locations(rgbSml_frame)
    # find encodings
    face_encodings = fr.face_encodings(rgbSml_frame, face_locations)
    name = None
    face_names = []
    for face_encoding in face_encodings:
        # try to find a match for known faces
        matches = fr.compare_faces(kfencodings, face_encoding, .4)
        name = "unknown"
        # if a match is found in known faces use the first one
        if True in matches:
            first_match_index = matches.index(True)
            name = kfnames[first_match_index]
        face_names.append(name)
        if name != "unknown":
            authenticated = True
    return name, frame, authenticated, face_locations, face_names

def display(frame, fnames, flocations):
    for (top, right, bottom, left), name in zip(flocations, fnames):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 5
        right *= 5
        bottom *= 5
        left *= 5

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    return frame

def main():
#Initilize Cam
    #Acces the camera
    cam = cv2.VideoCapture(0)
    # If camera is unavailable
    if not cam.isOpened():
        print("Sorry wasn't able to access camera.")
        exit()

    #Load and handle variations in number auth user of encodings
    encoding0, encoding1, encoding2, encoding3, encoding4, known_face_encodings = loaduser()
    if encoding0 is False and encoding1 is False and encoding2 is False and encoding3 is False and encoding4 is False:
        print("encodings were not available.")
    
    #Create arrays of known face encodings and their names
    known_face_names = [
        "Dylan", "Sam", "Ollie"
        ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    prcsframe = 5
    authenticated = False

    while True:
        #Capture frame by frame from the camera
        ret, frame = cam.read()
        #if frame is not captured
        if not ret:
            print("There was an issue capturing the frame.")
            continue

        #process every 6th frame
        if prcsframe == 5:
            name, frame, authenticated, face_locations, face_names = processing(frame, known_face_encodings, known_face_names)
        prcsframe -= 1
        if prcsframe == 0:
            prcsframe = 5

        #draw results on frame
        frame = display(frame, face_names, face_locations)
        cv2.imshow('Video', frame)
        print("auth user found:",authenticated)

        #exit program if q is pushed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #release the camera when done
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()