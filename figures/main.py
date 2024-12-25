import cv2
import numpy as np
chet=[0 for i in range(1,13)]
for i in range(0,12):
    image = cv2.imread(f"images/img ({i+1}).jpg")
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,10,255,cv2.THRESH_BINARY)

    contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    chet[i]=0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cactus_coords = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Если площадь больше 100
            x, y, w, h = cv2.boundingRect(contour)

            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            width = int(rect[1][0])
            height = int(rect[1][1])
            # print(box)
            box = np.int64(box)
            if (height>width*7 or width>height*7) and height>100 and width>100:  # Проверяем ширину
                chet[i]+=1
for i in range(0,12):
    print(f"{i+1} : {chet[i]}")
print(f"Всего элементов -{np.sum(chet)}")

# print(len(contours))
#
# arrow=contours[0]
# cv2.drawContours(image,contours,0,(255,0,0),3)
#
#
# print(f"area ={cv2.contourArea(arrow)}")
# print(f"Perimeter = {cv2.arcLength(arrow,False)}")
#
# moments = cv2.moments(arrow)
# print(f"Moments = {moments}")
# centroid = (int(moments['m10']/(moments['m00'])),int(moments['m01']/moments['m00']))
# print(f"Centroid - {centroid}")
#
# cv2.circle(image,centroid,4,(0,255,0),4)
# eps=0.001 *cv2.arcLength(arrow,True)
# approx = cv2.approxPolyDP(arrow,eps,True)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cactus_coords = []
#     for contour in contours:
#         area = cv2.contourArea(contour)
#         if area > 60:  # Если площадь больше 60
#             x, y, w, h = cv2.boundingRect(contour)
#             if w > 10:  # Проверяем ширину
#                 cactus_coords.append((x, y, w, h))