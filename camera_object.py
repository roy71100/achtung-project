import cv2
import imutils
import numpy as np
import image_rotation

CORNERS_COUNT = 4


class CameraObject:
    def __init__(self, lower_hsv, upper_hsv, name, contour=0, x_location=-1, y_location=-1):
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv
        self.name = name
        self.contour = contour
        self.x_location = x_location
        self.y_location = y_location

        self.FONT = cv2.FONT_HERSHEY_SIMPLEX
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)

    def __str__(self):
        return "{0} current location: {1}, {2}".format(self.name, self.x_location, self.y_location)

    def draw(self, frame):
        if not (self.contour is 0):
            cv2.drawContours(frame, [self.contour], -1, self.GREEN, 2)
            cv2.circle(frame, (self.x_location, self.y_location), 7, self.WHITE, -1)
            cv2.putText(frame, self.name, (self.x_location - 20, self.y_location - 20),
                        self.FONT, 0.5, self.WHITE, 2)

    def activate_mask_threshold(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
        return result, thresh

    @staticmethod
    def find_contours(threshold, contour_count):
        contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours.sort(reverse=True, key=cv2.contourArea)
        if len(contours) == 0:
            return 0
        return contours[0:min([contour_count, len(contours)])]

    @staticmethod
    def contours_to_centers(contours):
        centers = []
        for cont in contours:
            # compute the center of the contour
            M = cv2.moments(cont)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                centers.append((center_x, center_y))
        return centers


class Car(CameraObject):
    def find_car(self, frame):
        result, threshold = self.activate_mask_threshold(frame)
        self.contour = CameraObject.find_contours(threshold, 1)
        if not (self.contour is 0):
            self.contour = self.contour[0]
            #try:
            centers = CameraObject.contours_to_centers([self.contour])
            if len(centers) == 1:
                self.x_location, self.y_location = centers[0]
            # print("p", CameraObject.contours_to_centers([self.contour]))
            # except:
            #     print(self.contour)
            #     exit()


class Corner(CameraObject):
    def find_corners(self, frame):
        result, threshold = self.activate_mask_threshold(frame)
        corner_contours = CameraObject.find_contours(threshold, CORNERS_COUNT)
        corner_centers = CameraObject.contours_to_centers(corner_contours)
        return corner_contours, corner_centers

    @staticmethod
    def warp_if_possible(corners, frame):
        if len(corners) != CORNERS_COUNT:
            return -1
        points = np.array([np.array([corners[i].x_location, corners[i].y_location]) for i in range(CORNERS_COUNT)])
        warp = image_rotation.four_point_transform(frame, points)
        return warp
