import cv2 as cv

def line(img, point1, point2, color=(0, 255, 0), thickness=2):
    cv.line(img, point1, point2, color, thickness)

def point(img, point, color=(0, 0, 255), thickness=2):
    cv.circle(img, (point[0], point[1]), thickness, color)

def show(img):
    cv.imshow("output", img)
    cv.waitKey(0)
