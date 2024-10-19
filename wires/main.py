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

struct=np.array([[1],[1],[1]])
image = np.load('wires3npy.txt').astype('int8')
spisok=[]
chet=0
open=0
for i in range(image.shape[0]):
    if not(np.all(image[i] == 0)):
        if (open==0):
            spisok.append([])
        spisok[chet].append(image[i])
        open =1
    elif(open==1):
        chet+=1
        open=0

number = 1*100+(len(spisok)+1)*10+1
plt.subplot(number)
plt.imshow(image)
for i in range(len(spisok)):
    number = 1*100+(len(spisok)+1)*10+2+i
    spisok[i] = binary_erosion(spisok[i], struct).astype('int')
    spisok[i],element = two_pass(spisok[i])
    if (element==0):
        print("Элемента слишком поврежден")
    elif (element==1):
        print("Провод целый")
    else:
        print("Провод разделен на ", element," частей")
    print("")
    plt.subplot(number)
    plt.imshow(spisok[i])



image=binary_erosion(image,struct)


plt.show()
