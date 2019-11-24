import cv2
import imutils as imutils
import numpy as np
import test_rotation

# test
objects = 4
cap = cv2.VideoCapture(1)
FONT = cv2.FONT_HERSHEY_SIMPLEX
# Creating a window for later use
cv2.namedWindow('result')


def process_frame(frame, lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
    return result, thresh


def get_contours(thresh):
    """
    """
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    cnts.sort(reverse=True, key=cv2.contourArea)
    if len(cnts) == 0:
        return 0, 0
    c = cnts[0:min([objects, len(cnts)])]
    return c, result


def calc_centers(contours):
    centers = []
    for c in contours:
        # compute the center of the contour
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append((cX, cY))
    return centers


def draw_centers(centers, car):
    for i in range(len(centers)):
        cX, cY = centers[i]
        cv2.drawContours(result, [car[i]], -1, (0, 255, 0), 2)
        cv2.circle(result, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(result, "car", (cX - 20, cY - 20),
                    FONT, 0.5, (255, 255, 255), 2)
    # if len(centers) >= 2:
    #     cv2.rectangle(result, centers[0], centers[1], (0, 0, 255), 2)

lower_blue = np.array([60, 50, 40])
upper_blue = np.array([160, 150, 255])

while True:
    _, frame = cap.read()
    cv2.imshow("Original", frame)
    # converting to HSV
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    result, post_threshold = process_frame(frame, lower_blue, upper_blue)
    car, result = get_contours(post_threshold)

    if car is 0:
        cv2.imshow('result', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        continue

    else:
        centers = calc_centers(car)

    if len(centers) == 0:
        continue

    if len(centers) >= 4:
        points = np.array([np.array(centers[i]) for i in range(4)])
        warped = test_rotation.four_point_transform(frame, points)
        cv2.imshow('warped', warped)
    draw_centers(centers, car)
    cv2.imshow('result', result)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
