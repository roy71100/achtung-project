import cv2
import camera_object
import numpy as np
import init_constants

lower_car, upper_car, lower_corner, upper_corner, SLOW_RATIO = init_constants.init()
car = camera_object.Car(lower_car, upper_car, "CAR 1")
corners = [camera_object.Corner(lower_corner, upper_corner, "Corner") for i in range(4)]

cap = cv2.VideoCapture(0)

counter = 0
while True:
    counter += 1
    _, frame = cap.read()
    cv2.imshow("Original", frame)

    corner_contours, corner_centers = corners[0].find_corners(frame)
    # print(corner_contours)
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
            print(car.x_location / shape[1], 1 - (car.y_location / shape[0]))
        except:
            pass
    cv2.imshow('warped', warped)
    cv2.imshow('result', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
