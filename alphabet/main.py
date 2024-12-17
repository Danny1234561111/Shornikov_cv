import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label,regionprops, euler_number
from collections import defaultdict
from pathlib import Path


im=plt.imread('symbols.png')[:,:,:3].mean(2)
def recognize(region):
  if region.image.mean()==1.0:
    return "-"
  else:
    enumber = euler_number(region.image,2)
    if enumber==-1: #B ОТ 8
      have_vl = np.sum(np.mean(region.image[:,:region.image.shape[1]//2],0)==1)>3
      if have_vl:
        return "B"
      else:
        return "8"
    if enumber==0: #A ot 0
      image=region.image.copy()
      image[-1,:]=1
      enumber=euler_number(image)
      if enumber==-1:
        return "A"
      else:
        have_vl = np.sum(np.mean(region.image[:,:region.image.shape[1]//2],0)==1)>3
        if have_vl:
          top = region.image[:image.shape[0] // 2, :]
          bottom = region.image[(image.shape[0] // 2):, :]

                    # Сравниваем верхнюю и нижнюю части
          if (np.sum(top) > np.sum(bottom)):
            return "P"  # Если верхняя часть больше, это P
          else:
            return "D"
        else:
          return "0"
      # cy,cx = region.centroid_local
      # cy/=region.image.shape[0]
      # cx/=region.image.shape[1]
      # print(cy,cx)
    else: # / W X * 1
      have_vl = np.sum(np.mean(region.image[:,:region.image.shape[1]],0)==1)>3
      if have_vl:
        return "1"
      else:
        if region.eccentricity<0.4:
          return '*'
        else:
          image = region.image.copy()
          image[0,:]=1
          image[-1,:]=1
          image[:,0]=1
          image[:,-1]=1
          enumber=euler_number(image)
          if enumber ==-1:
            return "/"
          elif enumber ==-3:
            return "X"
          else:
            return "W"

  return "@"


im[im>0]=1
labeled=label(im)
regions=regionprops(labeled)
result=defaultdict(lambda: 0)
for region in regions:
  symbol=recognize(region)
  result[symbol]+=1
print(result)
plt.imshow(im)
