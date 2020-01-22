import unittest

import pytest
from donkeycar.parts.traffic_light_detector.image_resizer import ImageResizer
import cv2


red_light_jpg_path = "red_light.jpg"

def test_run():
    ir = ImageResizer()
    img_arr = cv2.imread(red_light_jpg_path)


    original_img_arr, resized_img_arr = ir.run(img_arr)

    cv2.imwrite("1.jpg", original_img_arr)
    cv2.imwrite("2.jpg", resized_img_arr)
