import functools
#threading  from threading import Thread, Event           
from packages.facialAuthenticator import *
from PIL import Image, ImageTk
#threading
from packages.YOLOges_rec_v2 import gesture as gst       
from packages.AddAuthUser import *
import tkinter as tk
import cv2
import threading
import random #test threading without camera stuff
import time #test threading without camera stuff
#threading  event = Event()         
"""
class App
    Positional Args:
        window (Tkinter object)
        cap (boolean): turns vid stream on or off will get Attribute error no vid if True for wrong window
        page (dictionary): passes page information 
        gesture (string or None): passes current gesture supposed to be from YOLOges_rec
    Keyword Args:
        video_source (int): set to default cam index usually 0
        window_title (string)
        
    Returns:
        GUI elements
"""
class App:
    def __init__(self, window, cap, page, gesture, video_source=0, window_title = "Prometheus Lighting Systems: Control Center"):
        #-------------------add prometheus icon----------------------#
        self.window = window
        self.window.title(window_title)
        self.width = 480
        self.height = 272
        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()
        self.page = page
        self.gesture = gesture
        self.current = self.page["current_page"]
        self.index = None
        self.overwrite = False
        if self.index is None:
            self.index = self.open_user()
        
        if cap:
            self.video_source = video_source
            self.vid = cv2.VideoCapture(self.video_source)
            if not self.vid.isOpened():
                raise ValueError("Unable to open video source", video_source)
            self.update()
        self.text()
        self.button()
        self.window.mainloop()
        return
    """
    update
        Positional Args:
            self (App class Attributes)
        
        Returns:
            updated frame for video feed resized to fit in Adduser page
    """
    def update(self):
        ret, frame = self.vid.read()
        w = int(self.width*.6)
        h = int(self.height*.7)
        self.resized_frame = cv2.resize(frame, (w, h))
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self.resized_frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(340, 100, image=self.photo)
    """
    button
        Positional Args:
            self (App class Attributes)
        
        Returns:
            the required buttons depending on what page self.current points to
    """
    def button(self):
        light_btn = tk.Button(self.window, text="GO", command=self.change_window0)
        light_btn.place(relx=0.09, rely=0.225)

        Users_btn = tk.Button(self.window, text="GO", command=self.change_window1)
        Users_btn.place(relx=0.09, rely=0.725)

        if self.gesture == 'light':
            light_btn.invoke()
        elif self.gesture == 'add':
            Users_btn.invoke()
        
        #place buttons according to current page
        match self.current:
            case 0: #0-light ctrl
                self.canvas.create_rectangle(192,85,440,190, fill="grey")
                red_btn = tk.Button(self.window, text = self.page["button_names"][0], command =self.button_red)
                red_btn.place(relx=0.45,rely=0.35)

                green_btn = tk.Button(self.window, text=self.page["button_names"][1], command=self.button_green)
                green_btn.place(relx=0.58,rely=0.35)

                blue_btn = tk.Button(self.window, text=self.page["button_names"][2], command=self.button_blue)
                blue_btn.place(relx=0.75,rely=0.35)

                bright_btn = tk.Button(self.window, text=self.page["button_names"][4],command=self.button_bright)
                bright_btn.place(relx=0.5,rely=0.55)

                dim_btn = tk.Button(self.window, text=self.page["button_names"][3], command=self.button_dim)
                dim_btn.place(relx=0.70,rely=.55)
                
                #gesture integration
                if self.gesture == 'r':
                    red_btn.invoke()
                elif self.gesture == 'g':
                    green_btn.invoke()
                elif self.gesture == 'b':
                    blue_btn.invoke()
                elif self.gesture == 'bright':
                    bright_btn.invoke()
                elif self.gesture == 'dim':
                    dim_btn.invoke()

            case 1: #1-add users
                user0_btn = tk.Button(self.window, text=self.page["button_names"][1],
                                 command=functools.partial(self.button_user, 0))
                user0_btn.place(relx=0.3, rely=0.025)

                user1_btn = tk.Button(self.window, text=self.page["button_names"][2],
                                 command= functools.partial(self.button_user, 1))
                user1_btn.place(relx=0.3, rely=0.17)

                user2_btn = tk.Button(self.window, text=self.page["button_names"][3],
                                 command=functools.partial(self.button_user, 2))
                user2_btn.place(relx=0.3, rely=0.32)

                user3_btn = tk.Button(self.window, text=self.page["button_names"][4],
                                 command=functools.partial(self.button_user, 3))
                user3_btn.place(relx=0.3, rely=0.47)

                user4_btn = tk.Button(self.window, text=self.page["button_names"][5],
                                 command=functools.partial(self.button_user, 4))
                user4_btn.place(relx=0.3, rely=0.61)

                cap_btn = tk.Button(self.window, text=self.page["button_names"][0],
                                    command=self.button_cap)
                cap_btn.place(relx=0.67, rely=0.6)

                #gesture integration
                if self.gesture == 'cap':
                    cap_btn.invoke()
                elif self.gesture == 'inc':
                    pass
                elif self.gesture == 'dec':
                    pass

    """
    text
        Positional Args:
            self (App class Attributes)
        
        Returns:
            renders menu text
    """
    def text(self):
    #side bar backgrd
        self.canvas.create_rectangle(0, 0, 132, 272, fill="grey")
    #side bar text
        # lights text pos
        menu1 = tk.Text(self.window, height=1, width=16)
        menu1.place(relx=0, rely=0)
        # light text pos
        menu1.insert(tk.END, "Light System\n")
        # disable text editing for side menu
        menu1.config(state="disabled")

        # Add Users text pos
        menu2 = tk.Text(self.window, height=1, width=16)
        menu2.place(relx=0, rely=.5)
        # Add user text pos
        menu2.insert(tk.END, "Add Users\n")
        # disable text editing for side menu
        menu2.config(state="disabled")

    """
    change_window(0/1)
        Positional Args:
            self (App class Attributes)
        
        Returns:
            destroys current window calls nav button to respective page
    """
    def change_window0(self):
        self.window.destroy()
        lightcntrl()

    def change_window1(self):
        self.window.destroy()
        adduser()

#page 0 buttons
    """
        button_red :
            Args: None
            function: sends 100hz freq
            
        button_green :
            Args: None
            function: sends 200hz freq
            
        button_blue:
            Args: None
            function: sends 300hz freq
            
        button_bright :
            Args: None
            function: sends 400hz freq
            
        button_dim :
            Args: None
            function: sends 500hz freq
    """
    def button_red(self):
        print("red")
        
    def button_green(self):
        print("green")

    def button_blue(self):
        print("blue")

    def button_bright(self):
        print("brighten")
        
    def button_dim(self):
        print("dim")
        
    
#page 1 buttons
    """
    button_cap
        Positional Args:
            self (App class Attributes)
        
        Returns:
            calls frameCap from AddAuthUser warns user and overwrites when out of bounds
    """
    def button_cap(self):
        if self.overwrite:
            self.overwrite_warning()
            self.index = 0
            self.overwrite = False
        frameCap(self.resized_frame,self.index)
        self.index = self.index + 1
        if self.index > 4:
            self.overwrite = True
        print("after cap:",self.index)
    """
    open_user
        Positional Args:
            self (App class Attributes)
        
        Returns:
            i (int): the index of the first open user profile
    """
    
    def open_user(self):
        i = 0
        enc0, enc1, enc2, enc3, enc4, _ = loaduser()
        encodings = [enc0, enc1, enc2, enc3, enc4]
        for i in range(0, 5):
            if not encodings:
                break
        return i
    """
    overwrite_warning
        Positional Args:
            self (App class Attributes)
        
        Returns:
            warns user overwrite is imminient 
    """
    def overwrite_warning(self):
        self.canvas.create_rectangle(212, 215, 450, 260, fill="grey")
        # user input pos
        txt = tk.Text(self.window, height=1, width=22, font=('', 10))
        txt.place(relx=.525, rely=.815)
        txt.insert(tk.END, 'All users full overwriting from User0')
        txt.config(state="disabled")
    """
    button_user
        Positional Args:
            self (App class Attributes)
            index (int): the user encoding being queried
        Returns:
            renders rectangle with encoding status of the user profile 
    """
    def button_user(self,index):
        encoding = loaduser()[index]
        self.canvas.create_rectangle(212, 215, 450, 260, fill="grey")
        # user input pos
        txt = tk.Text(self.window, height=1, width=22, font=('',10))
        txt.place(relx=.525, rely=.815)
        if encoding:
            text = f'User{index} holds an encoding'
            # user input text
            txt.insert(tk.END, f'{text}')
            txt.config(state="disabled")
        else:
            text = f'User{index} encoding is missing or invalid'
            txt.insert(tk.END, f'{text}')
            txt.config(state="disabled")

    #camera cleanup
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            
    # 4/27/25 always run gest rec in back to make sure ui doesnt freeze
    def run_gesture_control(self):
        while True:
            result = self.gesture()

            if result == "r":
                self.button_red()
            elif result == "g":
                self.button_green()
            elif result == "b":
                self.button_blue()
            elif result == "bright":
                self.button_brighten()
            elif result == "dim":
                self.button_dim()

 



#Nav buttons
def lightcntrl():
    current = App(tk.Tk(), cap=False, page = Ctrl_page, gesture = gesture)
    
    # start a thread for gesture detection, doing this blind 4/27/25
    gesture_thread = threading.Thread(target=current.run_gesture_control)
    gesture_thread.daemon = True  # ensure thread ends when app closes
    gesture_thread.start()



def adduser():
    current = App(tk.Tk(), cap=False,page=AddUser_page, gesture = gesture)   #enable vid with cap = True


def page_info(select):
    match select:
        case 0:
            info = {
                "current_page": 0,                                                                  #0: Control page
                "button_names": ["red","green","blue","dim","brighten"],
                "text": [[],],
            }
        case 1:
            info = {
                "current_page": 1,                                                                  # 1: Add Users page
                "button_names": ["cap", "user0", "user1" ,"user2", "user3", "user4", "confirm", "discard"],
                "text": [[],],
            }
        case _:
            info = None
    return info

#threading def get_gesture(gesture):
 #threading   gst(gesture)


if __name__ == "__main__":
    #gesture = None
    
    gesture = gst
    
    
    # initializes page info
    Ctrl_page = page_info(0)
    AddUser_page = page_info(1)
#threading     gesture_thread = Thread(target=get_gesture, daemon = True, args=(gesture,))
#threading     gesture_thread.start()
    while True:
        try:
        #landing page call
            current = App(tk.Tk(), cap=False, page=Ctrl_page, gesture=gesture)
            #threading print(gesture)
        except Exception as e:
            print(e)
# threading        gesture_thread.join()
