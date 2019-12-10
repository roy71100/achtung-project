import cv2 as cv2
import numpy as np
from image_handeling import camera_object, init_constants

_, _, lower_corner, upper_corner, _ = init_constants.init()
RESOLUTION = 700
lower_projection = (0, 0, 70)
upper_projection = (180, 45, 155)
homography = [0]

def show_full_screen(frame):
    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('window', frame)


def automated_corner_detection():
    white = 255 * np.ones((RESOLUTION, RESOLUTION, 3))
    show_full_screen(white)
    k = cv2.waitKey(500) & 0xFF
    ret, light_frame = cap.read()
    k = cv2.waitKey(500) & 0xFF
    lower_dist_from_floor = 200
    up_left_x = 100
    up_right_x = 140
    upper_y = 50
    pDst = [(up_right_x, upper_y), (RESOLUTION - up_left_x, upper_y), (0, RESOLUTION - lower_dist_from_floor),
            (RESOLUTION, RESOLUTION - lower_dist_from_floor)]
    test_project = np.zeros((RESOLUTION, RESOLUTION, 3))
    for i in range(4):
        cv2.circle(test_project, pDst[i], 30, (255, 255, 255), -1)
    count = 0
    count += 1
    if count == 1:
        show_full_screen(test_project)
        k = cv2.waitKey(6000) & 0xFF

    ret, dark_frame = cap.read()
    real_corners = [camera_object.Corner(lower_corner, upper_corner, "Corner") for i in range(4)]
    projected_corners = [camera_object.Corner(lower_projection, upper_projection, "Corner") for i in range(4)]

    real_corner_contours, real_corner_centers = real_corners[0].find_corners(light_frame)
    projected_corner_contours, projected_corner_centers = projected_corners[0].find_corners(dark_frame)

    received_game_board = np.zeros((RESOLUTION, RESOLUTION, 3))
    for i in range(4):
        cv2.circle(received_game_board, real_corner_centers[i], 30, (0, 0, 255), -1)
        cv2.circle(received_game_board, projected_corner_centers[i], 30, (255, 255, 255), -1)

    k = cv2.waitKey(5) & 0xFF
    show_full_screen(received_game_board)
    while True:
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break


def calculate_projection(width, height):
    # im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    # print(im)
    channels = 3
    s = (width, height, channels)
    # dst = np.zeros(s, dtype=np.uint8)
    # a, b = input("enter the horizontal and vertical factors (0-100):\n").split(",")
    # alpha = 1 - float(a)/100
    # beta = 1 - float(b)/100
    # (x,y)
    # upper left, upper right, lower left, lower right
    pSrc = [(0, 0), (width, 0), (0, height), (width, height)]
    # pDst = [(int(width * alpha), 0), (int(width*(1 - alpha)), 0), (int(width * alpha), int(height*beta)), (int(width*(1 - alpha)), int(height*beta))]
    # pDst = [(21, 0), (width - 21, 0), (0, height-200),
    #         (width, height - 200)]
    # width_shrink = int(((horizontal_factor / 100) / 2) * width)
    # height_shrink = int((vertical_factor / 100) * height)
    lower_dist_from_floor = 200
    up_left_x = 100
    up_right_x = 140
    upper_y = 50
    pDst = [(up_right_x, upper_y), (width - up_left_x, upper_y), (0, height - lower_dist_from_floor),
            (width, height - lower_dist_from_floor)]

    # imD = im.copy()
    # dstD = dst.copy()
    # for p in pSrc:
    #     cv2.circle(imD, p, 2, (255, 0, 0), -1)
    # for p in pDst:
    #     cv2.circle(dstD, p, 2, (255, 0, 0), -1)
    global homography
    homography = cv2.findHomography(np.array(pSrc, dtype=np.float32), np.array(pDst, dtype=np.float32), cv2.LMEDS)


def stretch_projection(im, homography):
    """
    Takes an image and warps it so it looks normal after projecting by an angle.
    :param image: opencv2 image opject (BGR format).
    :param horizontal_factor: the horizontal factor to compress the upper part by.
    :param vertical_factor: The vertical factor to compress lower part by.
    :return opencv2 image object (BGR) of the transformed image.
    """
    dstD = cv2.warpPerspective(im, homography[0], (im.shape[1], im.shape[0])) # TODO: mendi it is weird shapes are opposite here is it on purpose?
    return dstD
    # im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    # print(im)
    # dst = np.zeros(im.shape, dtype=np.uint8)
    # (height, width, channels) = im.shape
    # a, b = input("enter the horizontal and vertical factors (0-100):\n").split(",")
    # alpha = 1 - float(a)/100
    # beta = 1 - float(b)/100
    # (x,y)
    # upper left, upper right, lower left, lower right
    # # pDst = [(int(width * alpha), 0), (int(width*(1 - alpha)), 0), (int(width * alpha), int(height*beta)), (int(width*(1 - alpha)), int(height*beta))]
    # # pDst = [(21, 0), (width - 21, 0), (0, height-200),
    # #         (width, height - 200)]
    # # width_shrink = int(((horizontal_factor / 100) / 2) * width)
    # # height_shrink = int((vertical_factor / 100) * height)
    # lower_dist_from_floor = 200
    # up_left_x = 100
    # up_right_x = 140
    # upper_y = 50
    # pDst = [(up_right_x, upper_y), (width - up_left_x, upper_y), (0, height - lower_dist_from_floor),
    #         (width, height - lower_dist_from_floor)]

    # imD = im.copy()
    # for p in pSrc:
    #     cv2.circle(imD, p, 2, (255, 0, 0), -1)
    # for p in pDst:
    #     cv2.circle(dstD, p, 2, (255, 0, 0), -1)
    # M = cv2.getRotationMatrix2D((width/2, height/2), 180, 1.0)
    # dstD = cv2.warpAffine(dstD, M, (dstD.shape[1], dstD.shape[0]))


def show_projection(frame_to_project):
    projected = stretch_projection(frame_to_project, homography)
    projected = cv2.flip(projected, 0) # todo: VERY IMPORTANT - put this in holomography so we wont need this cuz it slow code MUCH/////
    # Display the resulting frame
    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('window', projected)


"""Old program, warps single image from file"""
# image = cv2.imread("large_image.png")
# warped = stretch_projection(image, 30, 70)
#
# while True:
#     cv2.imshow("warped!", warped)
#     cv2.waitKey(3)


"""New program for live video"""
# cap = cv2.VideoCapture(1)

# while (True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     shape = frame.shape
#
#     frame = 255 * np.ones(shape)
#
#     # Our operations on the frame come here
#     # warped = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     warped = stretch_projection(frame, 30, 70)
#
#     warped = cv2.flip(warped, 0)
#     # Display the resulting frame
#     cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
#     cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     cv2.imshow('window', warped)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# When everything done, release the capture
# ret, frame = cap.read()
# automated_corner_detection()

# cap.release()
# cv2.destroyAllWindows()
