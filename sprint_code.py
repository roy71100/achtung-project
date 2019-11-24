import cv2
import imutils as imutils
import numpy as np

#test
objects = 3
cap = cv2.VideoCapture(1)

# Creating a window for later use
cv2.namedWindow('result')


def get_center(hsv, lower, upper):
    """
    get info from track bar and appy to result
    :param hsv:
    :param lower:
    :param upper:
    :return:
    """
    # Normal masking algorithm
    mask = cv2.inRange(hsv, lower, upper)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("thresh", thresh)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    cnts.sort(reverse=True, key=cv2.contourArea)
    if len(cnts) == 0:
        return 0, 0
    c = cnts[0:min([objects, len(cnts)])]

    return c, result


lower_blue = np.array([60, 50, 120])
upper_blue = np.array([160, 150, 255])

x_array = []
y_array = []

while True:
    _, frame = cap.read()
    print("frame")
    cv2.imshow("Original", frame)
    # converting to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    car, result = get_center(hsv, lower_blue, upper_blue)
    centers = []
    to_draw_car = True
    if car is 0:
        cv2.imshow('result', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        continue
    # elif not (car is 0):
    #     print("cant find car")
    #     to_draw_car = False
    #     c = car
    #     M = cv2.moments(c)
    #     if M["m00"] != 0:
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])
    #         centers.append((cX, cY))
    else:
        for c in car:
            # compute the center of the contour
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers.append((cX, cY))

    if len(centers) < 1:
        continue
    for i in range(len(centers)):
        cX, cY = centers[i]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.drawContours(result, [car[i]], -1, (0, 255, 0), 2)
        cv2.circle(result, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(result, "car", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow('result', result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()