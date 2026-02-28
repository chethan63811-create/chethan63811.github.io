import cv2
import os
import numpy as np

DATASET_PATH = "dataset"

# Create dataset folder if not exists
if not os.path.exists(DATASET_PATH):
    os.makedirs(DATASET_PATH)

# Function to capture image
def capture_image():
    name = input("Enter student/object name: ")

    cap = cv2.VideoCapture(0)
    print("Press 's' to save image")

    while True:
        ret, frame = cap.read()
        cv2.imshow("Capture Image", frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            img_path = os.path.join(DATASET_PATH, name + ".jpg")
            cv2.imwrite(img_path, frame)
            print(f"Image saved as {name}.jpg")
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to recognise image
def recognise_image():
    cap = cv2.VideoCapture(0)
    ret, test_img = cap.read()
    cap.release()

    test_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)

    min_diff = float("inf")
    recognised_name = "Unknown"

    for file in os.listdir(DATASET_PATH):
        img = cv2.imread(os.path.join(DATASET_PATH, file))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (test_gray.shape[1], test_gray.shape[0]))

        diff = np.sum(np.abs(test_gray - gray))

        if diff < min_diff:
            min_diff = diff
            recognised_name = file.split(".")[0]

    cv2.putText(test_img, recognised_name, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Recognised Image", test_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Recognised:", recognised_name)

# Menu-driven program
def main():
    while True:
        print("\n----- MENU -----")
        print("1. Capture Image")
        print("2. Recognise Image")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            capture_image()
        elif choice == '2':
            recognise_image()
        elif choice == '3':
            print("Program exited")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
