import numpy as np
import cv2
import time
import random

class FinishLineDetector(object):
    '''
    Detect the finishing line of a track. Assuming the finishing line is red and if the car
    pass the finish line, the lower portion of the frame should contain a certain percentage of red color

    Use opencv to find out the percentage of red color covering the lower portion of the frame and return
    whether the car has passed the finishing line

    '''
    def run(self, img, debug = False):
        if img is None:
            return False, img

        if debug:
            cv2.imshow("img {}".format(random.randint(1,10000)), img)
            cv2.waitKey()

        font = cv2.FONT_HERSHEY_SIMPLEX
        img_hsv=cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        # lower mask (0-10)
        # lower_red = np.array([0,50,50])
        lower_red = np.array([0,100,100])
        upper_red = np.array([10,255,255])
        mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

        if debug:
            cv2.imshow("Mask 0 {}".format(random.randint(1,10000)), mask0)
            cv2.waitKey()

        # upper mask (170-180)
        # lower_red = np.array([170,50,50])
        lower_red = np.array([170,100,100])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

        if debug:
            cv2.imshow("Mask 1  {}".format(random.randint(1,10000)), mask1)
            cv2.waitKey()

        # join my masks
        mask = mask0+mask1

        # Mask top 3/4 portion
        mask_percent = 0.75
        # print (mask.shape)
        # print(mask)
        height, width = mask.shape
        # print (mask.shape)
        # print("height, width", height * mask_percent, width)
        # cv2.rectangle(mask, (0, 0), (160, 90), 255, -1)
        cv2.rectangle(mask, (0, 0), (width, int(height * mask_percent)), 0, -1)

        if debug:
            cv2.imshow("Mask  {}".format(random.randint(1,10000)), mask)
            cv2.waitKey()

        tot_pixel = int(height * (1-mask_percent)) * width  # total pixel of the ROI (Region of Interest)
        red_pixel = np.count_nonzero(mask)

        if (red_pixel > 1000):
            print("red_pixel / tot_pixel = {} / {}".format(red_pixel, tot_pixel))

        if ((red_pixel / tot_pixel) > 0.2):
            # if debug:
            print("{} finishing line detected".format(time.time()))
            cv2.putText(img,'finish line',(0,30), font, 1,(255,0, 0),2,cv2.LINE_AA)
            return True, img
        else:
            return False, img

    # def shutdown(self):
        # if self.fps_list is not None:
        #     print("fps (min/max) = {:2d} / {:2d}".format(min(self.fps_list), max(self.fps_list)))
        #     print("fps list {}".format(self.fps_list))
        # self.running = False
        # time.sleep(0.1)
