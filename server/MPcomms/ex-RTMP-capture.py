import cv2

myrtmp_addr = 'rtmp://localhost/live/rgb'

cap = cv2.VideoCapture(myrtmp_addr)

while(True):
    ret, frame = cap.read()

    cv2.imshow('client', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
