# config.py

MODEL_PATH = "CV_models/model.pt"  # YOLOv8 gesture model
AUTH_USER_PATH = "FlaskAddUser/AuthUsers/"
FLASK = ["10.181.114.19",  # IP address of web server
          "Admin",          #Webserver username
        "Prometheus",       #Webserver password
    ]
GESTURE_MAP = {
    0: "blue",
    1: "bright",
    2: "dim",
    3: "down",
    4: "cap",
    5: "green",
    6: "left",
    7: "red",
    8: "right",
    9: "up"
}
