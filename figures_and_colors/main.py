import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import threshold_otsu,sobel
from skimage.measure import label,regionprops
from skimage.segmentation import flood_fill
from skimage.color import rgb2hsv

im = plt.imread("balls.png")

binary = im.mean(2)
binary[binary>0]=1
labeled = label(binary)
region=regionprops(labeled)
print(np.max(labeled))
im_hsv = rgb2hsv(im)
colors=[]
arr=[]
for reg in region:


  shape=0
  
  area = reg.area
  perimeter = reg.perimeter
    
  # Получение координат ограничивающего прямоугольника
  minr, minc, maxr, maxc = reg.bbox
  bounding_box_area = (maxr - minr) * (maxc - minc)
    
  # Проверка, заполнен ли ограничивающий квадрат полностью
  if area == bounding_box_area:
    shape = 0
  else:
    shape = 1
  

  flag=True
  chet=0
  cy,cx = reg.centroid
  color = im_hsv[int(cy),int(cx)][0]
  if round(color,3) not in colors:
    for i in range(len(colors)):
      if ((colors[i]<round(color,3)+0.05) and (colors[i]>round(color,3)-0.05)):
        chet=i
        flag=False
    if (flag):
      colors.append(round(color,3))
      if shape:
        arr.append([1,0])
      else:
        arr.append([0,1])
    else:
      if shape:
        arr[chet][0]+=1
      else:
        arr[chet][1]+=1
  else:
    for i in range(len(colors)):
      if colors[i]==round(color,3):
        if shape:
          arr[i][0]+=1
        else:
          arr[i][1]+=1
    
  # colors.append(color)
plt.figure()
plt.imshow(im)
plt.figure()
print("[квадраты, круги - 1 цвета]")
print(len(colors))
print(arr)
