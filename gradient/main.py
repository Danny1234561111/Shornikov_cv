import numpy as np
import matplotlib.pyplot as plt

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

size = 100
image = np.zeros((size, size, 3), dtype="uint8")
assert image.shape[0] == image.shape[1]

color1 = [255, 128, 0]
color2 = [0, 128, 255]

for i, v in enumerate(np.linspace(0.5, 0, image.shape[0])):
  for j, s in enumerate(np.linspace(0.5, 0, image.shape[1])):
      r = lerp(color1[0], color2[0], v+s)
      g = lerp(color1[1], color2[1], v+s)
      b = lerp(color1[2], color2[2], v+s)
      image[i, j, :] = [r, g, b]

plt.figure(1)
plt.imshow(image)
plt.show()
