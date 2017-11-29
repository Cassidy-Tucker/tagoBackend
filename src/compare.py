import cv2
import numpy as np

def getDiff(base_image, current_image):
    base_image = cv2.GaussianBlur(base_image, (9,9), 0)
    current_image = cv2.GaussianBlur(current_image, (9,9), 0)

    base_image_gray = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
    current_image_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(base_image_gray, current_image_gray)

    _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    return diff


