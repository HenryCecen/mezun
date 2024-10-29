import cv2
import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()

# Open the video file (replace 'video.mp4' with your actual video file)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the audio from the current frame to text
    with sr.Microphone() as source:
        audio_data = r.listen(source)
        try:
            text = r.recognize_google(audio_data)
            print(f"Detected speech: {text}")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error during speech recognition: {e}")

    # Display the frame with the detected text
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()