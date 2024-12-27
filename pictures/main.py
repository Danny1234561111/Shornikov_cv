import cv2
import numpy as np

video_path = 'output (1).avi'
cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.namedWindow("Threshold", cv2.WINDOW_NORMAL)

video = cv2.VideoCapture(video_path)
count = 0

while video.isOpened():
    ret, frame = video.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)


    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sum=0

    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        area = cv2.contourArea(contour)

        circle_area = np.pi * (radius ** 2)

        if(area / circle_area > 0.8):
            sum +=1

    if sum >= 6 and len(contours) > 12 and len(contours) <= 18:
        cv2.imshow("Video", frame)
        cv2.imshow("Threshold", thresh)
        count += 1

    key = cv2.waitKey(1)
    if key == ord('q'): 
        break

video.release()
cv2.destroyAllWindows()
print(count)
