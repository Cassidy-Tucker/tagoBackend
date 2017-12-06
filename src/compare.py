import cv2
import numpy as np

def getDiff(base_image, current_image):
    base_image = cv2.GaussianBlur(base_image, (17, 17), 0)
    current_image = cv2.GaussianBlur(current_image, (17, 17), 0)

    diff = cv2.absdiff(base_image, current_image)

    _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    return diff


