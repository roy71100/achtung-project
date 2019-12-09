import cv2
import imutils
import numpy as np
import image_rotation

CORNERS_COUNT = 4


class CameraObject:
    """
    A general class to represent an object which is located in a frame.
    """

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
        """
        :return: A string containing the object name and location in x,y
        """
        return "{0} current location: {1}, {2}".format(self.name, self.x_location, self.y_location)

    def draw(self, frame):
        """
        Marks current object in given frame, including perimeter and name.
        :param frame: A frame containing current object
         (you should check that the latest location of the object is indeed in current frame)
        :return: None
        """
        if not (self.contour is 0):
            cv2.drawContours(frame, [self.contour], -1, self.GREEN, 2)
            cv2.circle(frame, (self.x_location, self.y_location), 7, self.WHITE, -1)
            cv2.putText(frame, self.name, (self.x_location - 20, self.y_location - 20),
                        self.FONT, 0.5, self.WHITE, 2)

    def activate_mask_threshold(self, frame):
        """
        Receives a frame and activates the threshold relevant to current object.
        :param frame: A frame containing current object
        :return: A frame in grayscale which is received after threshold.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
        return thresh

    @staticmethod
    def find_contours(threshold, contour_count):
        """
        A static method which finds requested number of top-sized contours in a given frame.
        :param threshold: A frame after threshold to a given color.
        :param contour_count: Integer. The number of requested contours in current frame.
        :return: A list of all relevant contours in threshold.
        """
        contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours.sort(reverse=True, key=cv2.contourArea)
        if len(contours) == 0:
            return 0
        return contours[0:min([contour_count, len(contours)])]

    @staticmethod
    def contours_to_centers(contours):
        """
        Finds (x,y) centers of each contour in given list.
        :param contours: A list of contours.
        :return: A list of (x,y) tuples containing the center of each given contour.
        """
        centers = []
        if contours is 0:
            return 0
        for cont in contours:
            # compute the center of the contour
            M = cv2.moments(cont)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                centers.append((center_x, center_y))
        return centers


class Car(CameraObject):
    """
    A class that inherits from CameraObject.
    Represents a car located in given frame.
    """
    def find_car(self, frame):
        """
        Finds current car in given frame.
        Updates current car's location fields according to the frame.
        :param frame: A frame that may contain current car.
        :return: None
        """
        threshold = self.activate_mask_threshold(frame)
        self.contour = CameraObject.find_contours(threshold, 1)
        if not (self.contour is 0):
            self.contour = self.contour[0]
            centers = CameraObject.contours_to_centers([self.contour])
            if len(centers) == 1:
                self.x_location, self.y_location = centers[0]


class Corner(CameraObject):
    """
    A class that inherits from CameraObject.
    Represents a corner of the board.
    """
    def find_corners(self, frame):
        """
        Find the 4 corners of the board.
        :param frame: A frame in which we want to look for the corners of the game board.
        :return: A list of the contours, A list of the contour centers.
        """
        threshold = self.activate_mask_threshold(frame)
        corner_contours = CameraObject.find_contours(threshold, CORNERS_COUNT)
        corner_centers = CameraObject.contours_to_centers(corner_contours)
        return corner_contours, corner_centers

    @staticmethod
    def warp_if_possible(corners, frame):
        """
        A static method.
        If we have 4 corners of the board recognized, warp the given frame so they will be the edges of the frame.
        Uses file image_rotation.py.
        :param corners: A list of Corner objects
        :param frame:
        :return:
        """
        if len(corners) != CORNERS_COUNT:
            return -1
        points = np.array([np.array([corners[i].x_location, corners[i].y_location]) for i in range(CORNERS_COUNT)])
        warp = image_rotation.four_point_transform(frame, points)
        return warp
