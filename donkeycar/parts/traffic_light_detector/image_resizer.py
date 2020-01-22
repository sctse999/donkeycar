import cv2


class ImageResizer(object):
    '''
    Resize image capture by camera and output the original and resize image

    Return original image and resized image
    '''


    def run(self, img_arr):
        if img_arr is None:
            return img_arr, img_arr

        resized_img_arr = cv2.resize(img_arr, (160,120))
        return img_arr, resized_img_arr
