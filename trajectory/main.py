import numpy as np
import cv2
import matplotlib.pyplot as plt

input_directory = 'out'
loaded_images = []

for index in range(100):
    file_name = 'out/h_'+str(index)+'.npy'
    image_data = np.load(file_name).astype(np.uint8)
    loaded_images.append(image_data)

paths = {}

def find_closest_index(x, y,paths):

    closest_index = -1
    min_distance = 1000000000
    for idx in paths.keys():
        last_x, last_y = paths[idx][-1]
        distance = np.sqrt((last_x - x) ** 2 + (last_y - y) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_index = idx
    return closest_index


initial_contours, _ = cv2.findContours(loaded_images[0], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour_index, contour in enumerate(initial_contours):
    (centroid_x, centroid_y), _ = cv2.minEnclosingCircle(contour)
    paths[contour_index] = [(centroid_x, centroid_y)]

for current_image in loaded_images[1:]:
    current_contours, _ = cv2.findContours(current_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in current_contours:
        (centroid_x, centroid_y), _ = cv2.minEnclosingCircle(contour)

        closest_index = find_closest_index(centroid_x, centroid_y,paths)

        paths[closest_index].append((centroid_x, centroid_y))

plt.figure(figsize=(10, 10))
for trajectory_index in paths.keys():
    trajectory_points = np.array(paths[trajectory_index])
    plt.plot(trajectory_points[:, 0], trajectory_points[:, 1], label=f'Объект {trajectory_index + 1}')
plt.xlabel('X координаты')
plt.ylabel('Y координаты')
plt.title('Траектории объектов')
plt.legend()
plt.show()
