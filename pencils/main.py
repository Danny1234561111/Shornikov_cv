import cv2
import numpy as np
chet=[0 for i in range(1,13)]
for i in range(0,12):
    chet[i] = 0
    image = cv2.imread(f"images/img ({i+1}).jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Если площадь больше 100
            rect = cv2.minAreaRect(contour)
            width = int(rect[1][0])
            height = int(rect[1][1])
            if (height>width*7 or width>height*7) and height>100 and width>100:  # Проверяем ширину
                chet[i]+=1
for i in range(0,12):
    print(f"{i+1} : {chet[i]}")
print(f"Всего элементов -{np.sum(chet)}")