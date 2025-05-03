# config.py

MODEL_PATH = "CV_models/YOLOv8nFinal.pt"  # YOLOv8 gesture model
AUTH_USER_PATH = "FlaskAddUser/AuthUsers/"
FLASK = ["10.181.114.19",  # IP address of web server
          "Admin",          #Webserver username
        "Prometheus",       #Webserver password
    ]
GESTURE_MAP = {
    0: "blue",
    1: "bright",
    2: "dim",
    3: "green",
    4: "red",
}
