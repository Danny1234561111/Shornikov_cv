import cv2
import numpy as np
import mss
import pyautogui
import time

def capture_screen():
    with mss.mss() as sct:
        bbox = {"top": 230, "left": 645, "width": 500, "height": 170}
        screenshot = sct.grab(bbox)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

def detect_cactus(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cactus_coords = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 60:  # Если площадь больше 60
            x, y, w, h = cv2.boundingRect(contour)
            if w > 10:  # Проверяем ширину
                cactus_coords.append((x, y, w, h))
    return cactus_coords

def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
def main():
    print("Начинаем игру через 3 секунды!")
    time.sleep(3)
    last_jump_time = 0  # Время последнего прыжка
    distit = 40 # Начальное расстояние
    distit1=0
    jump_delay  = 0.1  # Базовая задержка, увеличено для предотвращения быстрых прыжков
    last_jump_time1 = time.time()
    while True:
        screen = capture_screen()
        cactus_coords = detect_cactus(screen)
        dino_x = 0 # Приблизительное расположение динозавра по X. Настройте!
        dino_y = 150

        if cactus_coords:
            closest_cactus = min(cactus_coords, key=lambda c: calculate_distance(dino_x, dino_y, c[0], c[1]))
            cx, cy, cw, ch = closest_cactus
            distance = calculate_distance(dino_x, dino_y, cx, cy)

            # Адаптивная настройка distit (оставьте или удалите, в зависимости от необходимости)
            # distit += 0.2
            distit1=distit
            if ch > 100:
                distit1 *= distit*1.1
            elif cw > 30:
                distit1 *=distit* 0.9

            # Адаптивная настройка jump_delay (оставьте или удалите, в зависимости от необходимости)
            jump_delay = 0.2
            if (time.time() - last_jump_time1) > 0.1:
                distit += 0.56671
                last_jump_time1 =  time.time()  # Прыжок если кактус близко и прошло достаточно времени
            # Условие прыжка с корректным обновлением last_jump_time
            if cx < dino_x + distit-(cw-15) and (time.time() - last_jump_time) > jump_delay and cy>125:
                print(f"Препятствие найдено! Прыжок! Расстояние: {distance:.2f}, distit: {distit:.2f}")
                pyautogui.press('space')
                time.sleep(jump_delay*cw/70+0.1)
                pyautogui.press('down')
                last_jump_time = time.time()  # Обновление last_jump_time ВНУТРИ условия
                jump_delay *= 0.9999
            elif(cx < dino_x + distit-(cw-10) and (time.time() - last_jump_time) > jump_delay):
                pyautogui.keyDown('down')
                time.sleep(jump_delay*2)
                pyautogui.keyUp('down')
                jump_delay *= 0.9999

        else:
            print("Нет препятствий.")

if __name__ == "__main__":
    main()
