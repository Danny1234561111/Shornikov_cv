import numpy as np
import matplotlib.pyplot as plt


def counts(B, figures):
    height, width = B.shape

    for y in range(height - 5):
        for x in range(width - 3):
            for i in range(len(figures)):
                figure_shape = figures[i][0].shape

                if figure_shape == (6, 4) and (y + 6 <= height) and (x + 4 <= width):
                    if np.array_equal(B[x:x + 6, y:y + 4], figures[i][0]):
                        figures[i][2] += 1

                if figure_shape == (4, 6) and (y + 4 <= height) and (x + 6 <= width):
                    if np.array_equal(B[x:x + 4, y:y + 6], figures[i][0]):
                        figures[i][2] += 1


# Загрузка изображения
image = np.load("ps.npy (2).txt").astype("int")

# Определение фигур
bottom = np.array([[1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1],
                   [1, 1, 0, 0, 1, 1],
                   [1, 1, 0, 0, 1, 1]])

rect = np.array([[1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1]])

massiv = ["left", "top", "right"]
figures = [[bottom, "bottom", 0], [rect, "rect", 0]]

for i in range(len(massiv)):
    bottom = np.rot90(bottom)
    figures.append([bottom, massiv[i], 0])

counts(image, figures)
sum=0

for i in range(len(figures)):
    print(f"Форма - {figures[i][1]}, количество - {figures[i][2]}")
    sum+=figures[i][2]
print(f"Сумма - {sum}")
