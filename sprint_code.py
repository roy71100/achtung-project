import cv2
import imutils as imutils
import numpy as np
import image_rotation

# test
green_objects = 4
red_objects = 1
cap = cv2.VideoCapture(1)
FONT = cv2.FONT_HERSHEY_SIMPLEX
# Creating a window for later use
cv2.namedWindow('result')


def process_frame(frame, lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    # except:
    #     print("hsv")
    #     mask = cv2.inRange(frame, lower, upper)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("thresh", thresh)
    return result, thresh


def get_contours(thresh, objects_count):
    """
    """
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    cnts.sort(reverse=True, key=cv2.contourArea)
    if len(cnts) == 0:
        return 0, 0
    c = cnts[0:min([objects_count, len(cnts)])]
    return c


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


def draw_centers(centers, text, contours, pic):
    for i in range(len(centers)):
        cX, cY = centers[i]
        cv2.drawContours(pic, [contours[i]], -1, (0, 255, 0), 2)
        cv2.circle(pic, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(pic, text, (cX - 20, cY - 20),
                    FONT, 0.5, (255, 255, 255), 2)
    # if len(centers) >= 2:
    #     cv2.rectangle(result, centers[0], centers[1], (0, 0, 255), 2)


def get_color_contours(frame, lower, upper, color):
    result, post_threshold = process_frame(frame, lower, upper)
    if color == "green":
        color_contours = get_contours(post_threshold, green_objects)
    elif color == "red":
        color_contours = get_contours(post_threshold, red_objects)
    return color_contours


def calc_corners(corners, frame):
    if corners is 0:
        cv2.imshow('result', frame)
        return 0

    else:
        centers = calc_centers(corners)

    if len(centers) == 0:
        return 0

    draw_centers(centers, "corner", corners, frame)

    if len(centers) >= 4:
        points = np.array([np.array(centers[i]) for i in range(4)])
        warp = image_rotation.four_point_transform(frame, points)
        return warp
    return 1


lower_green = np.array([60, 90, 70])
upper_green = np.array([170, 180, 255])

lower_red = np.array([0, 205, 90])
upper_red = np.array([50, 255, 150])
counter = 0
while True:
    counter += 1
    _, frame = cap.read()
    cv2.imshow("Original", frame)

    corner_contours = get_color_contours(frame, lower_green, upper_green, "green")

    warped = calc_corners(corner_contours, frame)

    if warped is 0:
        continue

    if not (warped is 1):
        red_contours = get_color_contours(warped, lower_red, upper_red, "red")

        red_centers = calc_centers(red_contours)

        draw_centers(red_centers, "PLAYER 1", red_contours, warped)

        if counter % 50 == 0:
            shape = warped.shape
            try:
                print(red_centers[0][0] / shape[1], red_centers[0][1] / shape[0])
                # print(red_centers[0][0], red_centers[0][1])
                # print(shape)
            except:
                pass
    cv2.imshow('warped', warped)
    cv2.imshow('result', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
