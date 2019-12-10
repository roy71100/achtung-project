import cv2
from image_handeling import camera_object, init_constants, proj
import numpy as np

lower_car, upper_car, lower_corner, upper_corner, SLOW_RATIO = init_constants.init()
car = camera_object.Car(lower_car, upper_car, "CAR 1")
corners = [camera_object.Corner(lower_corner, upper_corner, "Corner") for i in range(4)]

cap = cv2.VideoCapture(1)

counter = 0

RESOLUTION = 500
white = 255 * np.ones((RESOLUTION, RESOLUTION, 3))
count_errors = 0
while True:
    counter += 1
    _, frame = cap.read()
    cv2.imshow("Original", frame)

    corner_contours, corner_centers = corners[0].find_corners(frame)
    # print(corner_contours)
    count_errors += 1
    if corner_centers is 0:
        continue
    for i in range(len(corner_centers)):
        corners[i].contour = corner_contours[i]
        corners[i].x_location, corners[i].y_location = corner_centers[i]
        corners[i].draw(frame)

    warped = camera_object.Corner.warp_if_possible(corners, frame)

    if warped is -1:
        continue

    car.find_car(warped)
    car.draw(warped)
    if car.contour is 0:
        if count_errors > 100:
            proj.show_full_screen(white)
            k = cv2.waitKey(5) & 0xFF
            continue
        count_errors += 1
        continue
    else:
        if cv2.contourArea(car.contour) < 5:
            if count_errors > 100:
                proj.show_full_screen(white)
                k = cv2.waitKey(5) & 0xFF
                count_errors += 1
                continue
            count_errors += 1
            continue
    count_errors = 0
    if counter % SLOW_RATIO == 0:
        shape = warped.shape
        try:
            relative_x = 1 - car.x_location / shape[1]
            relative_y = (car.y_location / shape[0])
            # print(relative_x, relative_y)

            game_board = np.zeros((RESOLUTION, RESOLUTION, 3))

            x = int(np.floor(RESOLUTION * relative_x))
            y = int(np.floor(RESOLUTION * relative_y))
            # print(x, y)
            cv2.circle(game_board, (x, y), 70, (255, 255, 255), -1)
            cv2.circle(game_board, (0, RESOLUTION - 50), 70, (255, 255, 255), -1)
            cv2.circle(game_board, (0, 0), 70, (255, 255, 255), -1)
            cv2.circle(game_board, (RESOLUTION-1, 0), 70, (255, 255, 255), -1)
            cv2.circle(game_board, (RESOLUTION-1, RESOLUTION-1), 70, (255, 255, 255), -1)

            proj.show_projection(game_board)
            # cv2.imshow('gameboard', game_board)
        except Exception as a:
            print(a)

    cv2.imshow('warped', warped)
    cv2.imshow('result', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
