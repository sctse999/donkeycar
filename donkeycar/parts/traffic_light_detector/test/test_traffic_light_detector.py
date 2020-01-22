import unittest

import pytest
from donkeycar.parts.traffic_light_detector.traffic_light_detector import TrafficLightDetector
import cv2
import hashlib
import numpy
import os
from edgetpu.detection.engine import DetectionCandidate


red_light_jpg_path = "red_light.jpg"
no_light_jpg_path = "no_light.jpg"

def test_convert_img_arr_to_img():
    tld = TrafficLightDetector()

    img_arr = cv2.cvtColor(cv2.imread(red_light_jpg_path),cv2.COLOR_BGR2RGB)
    img = tld.convertImageArrayToPILImage(img_arr)

    temp_file_path = "temp.jpg"
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
    img.save(temp_file_path)

    m = hashlib.md5()
    data = open(temp_file_path, 'rb').read()
    m.update(data)
    assert m.hexdigest() == "68754e35b1e12f7f9e05db5776efa76e"

# Test a picture with red traffic light
def test_detect_traffic_light_1():
    tld = TrafficLightDetector()

    img = cv2.imread(red_light_jpg_path)

    traffic_light_obj = tld.detect_traffic_light(img)

    assert traffic_light_obj is not None

    assert traffic_light_obj.score > 0.2
    assert traffic_light_obj.label_id == 9

# Test a picture with no traffic light
def test_detect_traffic_light_2():
    tld = TrafficLightDetector()

    img = cv2.imread(no_light_jpg_path)

    traffic_light_obj = tld.detect_traffic_light(img)

    assert traffic_light_obj is None


def test_is_light_on():
    tld = TrafficLightDetector()

    img = cv2.imread(red_light_jpg_path)

    traffic_light_obj = DetectionCandidate(9, 0.21, 277.77144909, 74.24615622, 301.41475201, 108.47412944)

    crop_img_arr = tld.crop_traffic_light(img, traffic_light_obj)
    cv2.imwrite("light_only.jpg", crop_img_arr)


    assert tld.is_light_on(crop_img_arr) == True

def test_crop_traffic_light():
    tld = TrafficLightDetector()

    img = cv2.imread(red_light_jpg_path)

    traffic_light_obj = DetectionCandidate(9, 0.21, 277.77144909, 74.24615622, 301.41475201, 108.47412944)

    crop_img_arr = tld.crop_traffic_light(img, traffic_light_obj)

    crop_img_arr_contiguous = crop_img_arr.copy(order='C')
    assert hashlib.sha1(crop_img_arr_contiguous).hexdigest() == "090d343943f4c2a08bbfe5edc461034f89e64a86"

def test_run():
    tld = TrafficLightDetector()
    img = cv2.imread(red_light_jpg_path)

    throttle, _ = tld.run(img,0.6)

    assert throttle == 0
