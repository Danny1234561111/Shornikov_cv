from scipy.ndimage import binary_dilation,binary_opening,binary_erosion,binary_closing
import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import disk


def neighbours2(y, x):
    return (y, x - 1), (y - 1, x)


def exist(B, nbs):
    left, top = nbs

    if left[0] >= 0 and left[0] <= B.shape[0] and left[1] >= 0 and left[1] < B.shape[1]:
        if B[left] == 0:
            left = None
    else:
        left = None


    if top[0] >= 0 and top[0] <= B.shape[0] and top[1] >= 0 and top[1] < B.shape[1]:
        if B[top] == 0:
            top = None
    else:
        top = None

    return left, top

def find(label, linked):
    j = label
    while linked[j].any() != 0:
        j = linked[j]

    return j


def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)

    if j != k:
        linked[k] = j

def two_pass(B):
    LB = np.zeros_like(B)
    linked = np.zeros(B.size // 2 + 1, dtype="int8")
    label = 1

    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                nbs = neighbours2(y, x)
                existed = exist(B, nbs)
                if existed[0] is None and existed[1] is None:
                    m = label
                    label += 1
                else:
                    lbs = [LB[n] for n in existed if n is not None]
                    m = min(lbs)

                LB[y, x] = m

                for n in existed:
                    if n is not None:
                        lb = LB[n]
                        if lb != m:
                            union(m, lb, linked)

    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                new_label = find(LB[y, x], linked)
                if new_label != LB[y, x]:
                    LB[y, x] = new_label

    uniques = np.unique(LB)[1:]

    for i, v in enumerate(uniques):
        LB[LB == v] = i + 1

    return LB,uniques.shape[0]


image = np.load('starsnpy.txt').astype('int8')
struct=np.zeros([5,5])
struct[:][2]=1
struct[:,2]=1

struct2=np.zeros([5,5])
for i in range(5):
  struct2[i, i] = 1
  struct2[i, 4 - i] = 1
image1 = binary_erosion(image, struct).astype('int')
image1,element = two_pass(image1)
image2 = binary_erosion(image, struct2).astype('int')
image2,element1 = two_pass(image2)

print(element+element1)
