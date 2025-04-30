# add_user.py
import cv2
import os

SAVE_DIR = "data/users"
MAX_USERS = 5
os.makedirs(SAVE_DIR, exist_ok=True)

def get_next_index():
    for i in range(MAX_USERS):
        path = os.path.join(SAVE_DIR, f"AuthUser{i}.jpg")
        if not os.path.exists(path):
            return i
    return None

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not available.")
        return

    print("Press 'c' to capture your face. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        cv2.imshow("Add Auth User", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            index = get_next_index()
            if index is None:
                print(f"User limit reached ({MAX_USERS}).")
                break

            save_path = os.path.join(SAVE_DIR, f"AuthUser{index}.jpg")
            cv2.imwrite(save_path, frame)
            print(f"Saved {save_path}")

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
