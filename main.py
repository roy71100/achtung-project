import cv2
import camera_object
import numpy as np
import init_constants

lower_car, upper_car, lower_corner, upper_corner, SLOW_RATIO = init_constants.init()
car = camera_object.Car(lower_car, upper_car, "CAR 1")
corners = [camera_object.Corner(lower_corner, upper_corner, "Corner") for i in range(4)]

cap = cv2.VideoCapture(1)

counter = 0

RESOLUTION = 500

while True:
    counter += 1
    _, frame = cap.read()
    cv2.imshow("Original", frame)

    corner_contours, corner_centers = corners[0].find_corners(frame)
    # print(corner_contours)
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

    if counter % SLOW_RATIO == 0:
        shape = warped.shape
        try:
            relative_x = car.x_location / shape[1]
            relative_y = 1 - (car.y_location / shape[0])
            # print(relative_x, relative_y)

            game_board = np.zeros((RESOLUTION, RESOLUTION, 3))

            x = int(np.floor(RESOLUTION * relative_x))
            y = int(np.floor(RESOLUTION * relative_y))
            # print(x, y)
            cv2.circle(game_board, (x, y), 7, (0, 0, 255), -1)

            cv2.imshow('gameboard', game_board)
        except Exception as a:
            print(a)

    cv2.imshow('warped', warped)
    cv2.imshow('result', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
