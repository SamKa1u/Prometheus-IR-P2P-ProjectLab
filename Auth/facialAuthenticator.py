import cv2
import time
import face_recognition as fr


class Authenticator:
    def __init__(self, shared, auth_path):
        self.shared = shared
        self.auth_path = auth_path
        self.knames = ['User0','User1','User2','User3','User4']
        self.kEncodings = []

    def load_encodings(self):
        encoding0,encoding1,encoding2,encoding3,encoding4 = False,False,False,False,False
        try:
            User0 = fr.load_image_file(f'{self.auth_path}AuthUser0.jpg')
            UserEncoding0 = fr.face_encodings(User0)[0]
            self.kEncodings.append(UserEncoding0)
            encoding0 = True
        except:
            pass

        try:
            User1 = fr.load_image_file(f'{self.auth_path}AuthUser1.jpg')
            UserEncoding1 = fr.face_encodings(User1)[0]
            self.kEncodings.append(UserEncoding1)
            encoding1 = True
        except:
            pass

        try:
            User2 = fr.load_image_file(f'{self.auth_path}AuthUser2.jpg')
            UserEncoding2 = fr.face_encodings(User2)[0]
            self.kEncodings.append(UserEncoding2)
            encoding2 = True
        except:
            pass

        try:
            User3 = fr.load_image_file(f'{self.auth_path}AuthUser3.jpg')
            UserEncoding3 = fr.face_encodings(User3)[0]
            self.kEncodings.append(UserEncoding3)
            encoding3 = True
        except:
            pass

        try:
            User4 = fr.load_image_file(f'{self.auth_path}AuthUser4.jpg')
            UserEncoding4 = fr.face_encodings(User4)[0]
            self.kEncodings.append(UserEncoding4)
            encoding4 = True
        except:
            pass
        self.shared["encodingBools"] = [encoding0, encoding1, encoding2, encoding3, encoding4]

    def processing(self):
        p = 100
        while True:
            if p == 100:
                self.load_encodings()
                p = p - 1
            elif p == 0:
                p = 100
            else:
                p = p - 1
            print('[Facial Auth] ',p)
            frame = self.shared.get("frame")
            if frame is None:
                time.sleep(.01)
                continue
            # Speed up processing by resizing frame
            # sml_frame = cv2.resize(frame, (128, 96))
            # color conversion for face rec
            rgbSml_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # # find face locations in refined frame
            face_locations = fr.face_locations(rgbSml_frame)
            # find encodings
            face_encodings = fr.face_encodings(rgbSml_frame, face_locations)
            name = None
            matches = [False]
            for face_encoding in face_encodings:
                # try to find a match for known faces
                matches = fr.compare_faces(self.kEncodings, face_encoding)
                # if a match is found in known faces authenticated is True
            if True in matches:
                self.shared['authenticated'] = True
            else:
                self.shared['authenticated'] = False
            print(f"[Facial Auth] Status: {self.shared['authenticated']}")


#test Auth
if __name__ == '__main__':

    shared_state = {
        "frame": None,
        "gesture": None,
        "encodingBools": [False, False, False, False, False],
        "authenticated": False,
    }
    a = Authenticator(shared_state, '')
    a.load_encodings()
    print(a.shared.get("encodingBools"))