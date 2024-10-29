import cv2


def cam2():
    # Open the default camera (usually the first one)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Main loop to capture frames from the camera
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # openInterface.displayImage(frame, 1)
        # cv2.waitKey()
        # Display the frame
        cv2.imshow('Camera', frame)
        #
        # Check for key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cam2()
