import numpy as np
from image_handeling import camera_object
import cv2

# Green car in light
lower_car = np.array([45, 60, 50])
upper_car = np.array([90, 140, 140])


class Camera:
    counter = 0
    RESOLUTION = 500
    cap = cv2.VideoCapture(1)
    lower_corner = np.array([10, 55, 90])
    upper_corner = np.array([30, 255, 200])

    def __init__(self):
        # Orange in light
        self.cars = [camera_object.Car(lower_car, upper_car, "CAR 1")]
        self.corners, self.corner_contours, self.corner_centers = self.init_corners()

    def init_corners(self):
        corners = [camera_object.Corner(self.lower_corner, self.upper_corner, "Corner") for _ in range(4)]
        _, frame = self.cap.read()
        corner_contours, corner_centers = corners[0].find_corners(frame)
        for i in range(len(corner_centers)):
            corners[i].contour = corner_contours[i]
            corners[i].x_location, corners[i].y_location = corner_centers[i]
        return corners, corner_contours, corner_centers

    def get_location(self, car_index):
        self.counter += 1
        if self.counter % 30 == 0:
            self.corners, self.corner_contours, self.corner_centers = self.init_corners()
        car = self.cars[car_index]
        _, frame = self.cap.read()
        warped = camera_object.Corner.warp_if_possible(self.corners, frame)
        if warped is -1:
            return -1
        car.find_car(warped)
        shape = warped.shape
        # if car.x_location < 0 or car.y_location < 0:
        #     return 0.05, 0.05
        relative_x = 1 - (car.x_location / shape[1])
        relative_y = (car.y_location / shape[0])
        return relative_x, relative_y


