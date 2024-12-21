import re
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label
from pathlib import Path

def calculate_distance(point1: tuple, point2: tuple) -> float:
    y1, x1 = point1
    x2, y2 = point2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def find_closest_center(centroids: tuple, regions, processed: list) -> tuple:
    min_distance = float('inf')
    closest_index = None
    
    for i, region in enumerate(regions):
        if i not in processed:
            distances = np.array([calculate_distance(centroid, region.centroid) for centroid in centroids])
            if distances.mean() < min_distance:
                min_distance = distances.mean()
                closest_index = i
    
    return regions[closest_index].centroid, closest_index

def plot_changes(trajectory):
    differences = np.abs(trajectory[1:] - trajectory[:-1])
    plt.plot(differences, 'o')
    plt.show()

def display_images(trajectories, image_list):
    plt.ion()
    for idx, img in enumerate(image_list):
        plt.clf()
        plt.title(idx)
        plt.imshow(img)
        for j, trajectory in enumerate(trajectories):
            plt.scatter(trajectory[idx][0],
                        trajectory[idx][1],
                        c=['blue', 'red', 'green'][j],
                        s=3)
        
        plt.pause(1)

def plot_trajectory_paths(trajectories):
    for idx, trajectory in enumerate(trajectories):
        plt.plot(trajectory[:, 0], trajectory[:, 1], label=f"Path {idx + 1}")

    plt.legend()
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()

data_path = Path(__file__).parent / "motion/"
data_files = sorted([str(file) for file in data_path.glob("*.npy")],
                    key=lambda s: int(re.findall(r'\d+', s)[-1]))

image_list = [np.load(file).astype(int) for file in data_files]
trajectories = []

for frame_index, frame in enumerate(image_list):
    labeled_frame = label(frame)
    regions = regionprops(labeled_frame)
    processed_indices = []

    if not trajectories:
        for region in regions:
            cy, cx = region.centroid
            trajectories.append([(float(cx), float(cy))])
    else:
        for trajectory_index, obj_trajectory in enumerate(trajectories):
            depth = 3
            recent_centroids = obj_trajectory[-depth:]
            (new_y, new_x), closest_index = find_closest_center(recent_centroids, regions, processed_indices)

            trajectories[trajectory_index].append((float(new_x), float(new_y)))
            processed_indices.append(closest_index)

trajectories = np.array(trajectories)

plot_trajectory_paths(trajectories
