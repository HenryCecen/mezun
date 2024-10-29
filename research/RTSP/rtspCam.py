import cv2

# RTSP adresi
rtsp_url = "rtsp://admin:1234@192.168.1.100:554/cam/realmonitor?channel=1&subtype=1"

# RTSP bağlantısını açma
cap = cv2.VideoCapture(rtsp_url)

# Bağlantının başarılı olup olmadığını kontrol etme
if not cap.isOpened():
    print("Kamera bağlantısı başarısız!")
    exit()

# Video akışını okuma
while True:
    ret, frame = cap.read()

    if not ret:
        print("Video akışı alınamadı!")
        break

    # Frame'i görüntüleme
    cv2.imshow('RTSP Kamera', frame)

    # Çıkış için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakma
cap.release()
cv2.destroyAllWindows()
