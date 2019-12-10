import numpy as np


def init():
    # Green dots
    # lower_corner = np.array([60, 90, 70])
    # upper_corner = np.array([170, 255, 255])

    # Red dot
    # lower_car = np.array([0, 110, 90])
    # upper_car = np.array([50, 255, 230])

    # CAR
    # lower_car = np.array([40, 30, 30])
    # upper_car = np.array([90, 130, 190])

    # Orange infi books for corners
    # lower_corner = np.array([10, 100, 50])
    # upper_corner = np.array([60, 255, 255])

    # Orange in light
    lower_corner = np.array([10, 55, 90])
    upper_corner = np.array([30, 200, 200])

    # Green car in light
    lower_car = np.array([45, 60, 50])
    upper_car = np.array([90, 140, 140])

    SLOW_RATIO = 1

    return lower_car, upper_car, lower_corner, upper_corner, SLOW_RATIO
