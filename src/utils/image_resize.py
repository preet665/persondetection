from src.exception.base_exception import ImageConversionException, GstreamerDecoderException, FrameProcessingException
from src.utils.logger import Logger
from src.constant.project_constant import Constant as constant
import cv2

class ResizeImage(object):
    def __init__(self) -> None:
        self.desired_height = 128
        self.desired_width = 64
       

    def resize_and_save_image(self, image):
        try:

            height, width, _ = image.shape
            if height != self.desired_height or width != self.desired_width:
                resized_image = cv2.resize(image, (self.desired_width, self.desired_height))
                return resized_image  
            else:
                return image

        except Exception as e:
            print(f"Error processing image : {str(e)}")


resize_image = ResizeImage()

