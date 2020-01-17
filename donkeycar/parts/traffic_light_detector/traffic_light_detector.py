import numpy as np
import cv2
import time
import random
import collections
from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils
from PIL import Image
from matplotlib import cm
import os
import urllib.request


class TrafficLightDetector(object):
    '''
    Requires an EdgeTPU for this part to work

    This part will run a EdgeTPU optimized model to run object detection to detect a traffic light.
    We are just using a pre-trained model (MobileNet V2 SSD) provided by Google.

    After we identified the


    We override the throttle


    Detect the finishing line of a track. Assuming the finishing line is red and if the car
    pass the finish line, the lower portion of the frame should contain a certain percentage of red color

    Use opencv to find out the percentage of red color covering the lower portion of the frame and return
    whether the car has passed the finishing line

    '''

    def download_file(self, url, filename):
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(url, filename)


    def __init__(self, debug):
        MODEL_FILE_NAME = "mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
        LABEL_FILE_NAME = "coco_labels.txt"

        MODEL_URL = "https://github.com/google-coral/edgetpu/raw/master/test_data/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"

        LABEL_URL = "https://dl.google.com/coral/canned_models/coco_labels.txt"


        self.download_file(MODEL_URL, MODEL_FILE_NAME)
        self.download_file(LABEL_URL, LABEL_FILE_NAME)


        self.last_5_scores = collections.deque(np.zeros(5), maxlen=5)
        self.engine = DetectionEngine(MODEL_FILE_NAME)
        self.labels = dataset_utils.read_label_file(LABEL_FILE_NAME)

        self.TRAFFIC_LIGHT_CLASS = 9
        self.LAST_5_SCORE_THRESHOLD = 0.4
        self.MIN_SCORE = 0.2
        self.debug = debug
        self.stop_count = 20

    def convertImageArrayToPILImage(self, img_arr):
        img = Image.fromarray(img_arr.astype('uint8'), 'RGB')



        # cropped_img = img.crop((50,0,350,300))
        # cropped_img.show()

        # img = Image.fromarray(np.uint8(cm.gist_earth(img_arr)*255))
        return img

    '''
    Return an object if there is a traffic light in the frame
    '''
    def detect_traffic_light(self, img_arr):
        img = self.convertImageArrayToPILImage(img_arr)

        ans = self.engine.detect_with_image(img,
                                          threshold=self.MIN_SCORE,
                                          keep_aspect_ratio=True,
                                          relative_coord=False,
                                          top_k=3)
        max_score = 0
        traffic_light_obj = None
        if ans:
            for obj in ans:
                if (obj.label_id == self.TRAFFIC_LIGHT_CLASS or obj.label_id == 12):
                    if self.debug:
                        print("traffic light detected, score = {}".format(obj.score))
                    if (obj.score > max_score):
                        print(obj.bounding_box)
                        traffic_light_obj = obj
                        max_score = obj.score

        if traffic_light_obj:
            self.last_5_scores.append(traffic_light_obj.score)
            sum_of_last_5_score = sum(list(self.last_5_scores))
            # print("sum of last 5 score = ", sum_of_last_5_score)

            if sum_of_last_5_score > self.LAST_5_SCORE_THRESHOLD:
                return traffic_light_obj
            else:
                print("Not reaching last 5 score threshold")
                return None
        else:
            self.last_5_scores.append(0)
            return None

        return traffic_light_obj

    '''
    Return a traffic light image array based on the traffic light obj bounding box
    '''
    def crop_traffic_light(self, img_arr, traffic_light_obj):
        bbox = traffic_light_obj.bounding_box

        x1 = int(bbox[0][0])
        x2 = int(bbox[1][0])

        y1 = int(bbox[0][1])
        y2 = int(bbox[1][1])

        return img_arr[y1:y2, x1:x2]

    def is_light_on(self, img_arr):

        cv2.imwrite("upper_red_light.jpg",img_arr)
        img_gray = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
        ret, img_thresh = cv2.threshold(img_gray, 210, 255, cv2.THRESH_BINARY)

        cv2.imwrite("upper_red_light_thresh.jpg",img_thresh)

        print("cv2.countNonZero = ", cv2.countNonZero(img_thresh))

        if cv2.countNonZero(img_thresh) > 0:
            return True
        else:
            return False

    def crop_upper_half(self, img_arr):
        h, w, channels = img_arr.shape
        upper_half_img_arr = img_arr[
            0:h // 2, 0:w, :]  # Upper part of image refer to red light

        return upper_half_img_arr

    def run(self, img_arr, throttle, debug=False):
        if img_arr is None:
            return throttle, img_arr

        # if debug:
        #     cv2.imshow("img {}".format(random.randint(1, 10000)), img_arr)

        # Detect traffic light object
        traffic_light_obj = self.detect_traffic_light(img_arr)

        if traffic_light_obj:
            xmargin  =( traffic_light_obj.bounding_box[1][0] - traffic_light_obj.bounding_box[0][0]) *0.1

            traffic_light_obj.bounding_box[0][0] = traffic_light_obj.bounding_box[0][0] + xmargin
            traffic_light_obj.bounding_box[1][0] = traffic_light_obj.bounding_box[1][0] - xmargin

            ymargin = ( traffic_light_obj.bounding_box[1][1] - traffic_light_obj.bounding_box[0][1]) *0.05

            traffic_light_obj.bounding_box[0][1] = traffic_light_obj.bounding_box[0][1] + ymargin
            traffic_light_obj.bounding_box[1][1] = traffic_light_obj.bounding_box[1][1] - ymargin


            cv2.rectangle(img_arr, tuple(traffic_light_obj.bounding_box[0].astype(int)),
                          tuple(traffic_light_obj.bounding_box[1].astype(int)), (0, 255, 0), 2)

            # traffic_light_img = self.crop_traffic_light(
            #     img_arr, traffic_light_obj)

            # upper_half_img_arr = self.crop_upper_half(traffic_light_img)

            # if self.is_light_on(upper_half_img_arr):
            #     # print("Red light detected, overriding throttle to 0")
            #     throttle = 0
            self.stop_count = 20
            return 0, img_arr
        else:
            if self.stop_count > 0:
                self.stop_count -= 1
                return 0, img_arr
            return throttle, img_arr

    # def shutdown(self):
    # if self.fps_list is not None:
    #     print("fps (min/max) = {:2d} / {:2d}".format(min(self.fps_list), max(self.fps_list)))
    #     print("fps list {}".format(self.fps_list))
    # self.running = False
    # time.sleep(0.1)
