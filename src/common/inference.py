"""
File : infernce.py
Description : Class is responsible for custom exception handling
Created on : 
Author :
E-mail :

"""


from src.exception.base_exception import ImageConversionException, GstreamerDecoderException, FrameProcessingException
from src.common.config_manager import cfg
from src.utils.logger import Logger
from src.constant.project_constant import Constant as constant
from src.constant.global_data import GlobalData 
from src.utils.image_resize import resize_image
from src.services.person_reid import PersonREID

import os
#export DISPLAY=192.168.56.1:0
#source ~/.bashrc
import cv2
import json
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from boxmot import DeepOCSORT
import logging
import threading, time 



class Watcher:
    def __init__(self):
       
       
        model_path = (constant.CURRENT_DIR_PATH / str(cfg.get_model_config(constant.CONFIG_MODEL_WEIGHT_FILE))).resolve() 
        self.tracker = DeepOCSORT(model_weights=model_path, device=constant.CPU_DEVICE,fp16=False)
        self.detector = torch.hub.load(constant.ULTRALYTICS_YOLO, 'yolov5s', force_reload=True, verbose=False).to(constant.CPU_DEVICE)
        self.colors = np.random.randint(0, 255, size=(100, 3), dtype=np.uint8).tolist()
        self.updated_unique_person_list = False
        self.detection = []
        
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.logger = self.setup_logger('first_logger', 'first_logfile.log')
        self.logger.info('This is just info message')
        self.gallery_path = (constant.CURRENT_DIR_PATH / str(cfg.get_resource_config(constant.REID_GALLERY_DIR))).resolve() 
        self.query_path = (constant.CURRENT_DIR_PATH / str(cfg.get_resource_config(constant.REID_QUERY_DIR))).resolve() 
        self.skip_factor = 5
        #self.person_reid = PersonREID()
    
            

    def setup_logger(self, name, log_file, level=logging.INFO):
        """To setup as many loggers as you want"""
    
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(self.formatter)
    
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    
    def detect_person(self, img):
        results = self.detector(img).pandas().xyxy[0]
        boxes = [] #(x, y, x, y, conf, cls_id)
        for idx in results.index:
            cls_id = results[constant.DETECTION_CLASS][idx]
            if cls_id == 0:
                x1 = results[constant.X_MIN][idx]; y1 = results[constant.Y_MIN][idx] 
                x2 = results[constant.X_MAX][idx]; y2 = results[constant.Y_MAX][idx]
                
                conf = results[constant.DETECTION_CONF][idx]
                boxes.append([x1, y1, x2, y2, conf, cls_id]) 
        return np.array(boxes)
    

    def crop_detected_person(self, frame, boxes, counter):
        try:
            frame_bgr = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            cropped_images = []

            if not GlobalData.unique_person_list:
                if counter == 1 and not self.updated_unique_person_list:
                    GlobalData.unique_person_list.extend([box[4] for box in boxes])
                    self.updated_unique_person_list = True 
                for box in boxes:
                    x1, y1, x2, y2, person_id, conf, cls_id, ukn = box
                    if person_id in GlobalData.unique_person_list:
                        crop = frame_bgr[int(y1):int(y2), int(x1):int(x2)]
                        cropped_images.append(crop) 

            else:   
                intersection = [x for x in GlobalData.set_person_id if x not in GlobalData.unique_person_list]
                GlobalData.unique_person_list.extend(intersection)

                for box in boxes:
                    x1, y1, x2, y2, person_id, conf, cls_id, ukn = box
                    if person_id in GlobalData.set_person_id and person_id in intersection:
                        crop = frame_bgr[int(y1):int(y2), int(x1):int(x2)]
                        cropped_images.append(crop)

            # Save cropped images if needed
            if cropped_images:
                for i, cropped_image in enumerate(cropped_images):
                    print("counter ---:", counter)
                    image = resize_image.resize_and_save_image(cropped_image)
                    image_save_path = f'{self.query_path}/frame_{counter:04d}.jpg'
                    cv2.imwrite(image_save_path, image)
                    #self.person_reid.get_topK_reID(image_save_path)

            
            for box_id, box in enumerate(boxes):  
                croped_image = frame_bgr[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                image = resize_image.resize_and_save_image(croped_image)
                image_save_path = f'{self.gallery_path}/frame_{counter:04d}_{box_id:04d}.jpg'
                if counter % self.skip_factor ==0:
                    cv2.imwrite(image_save_path, image)

            #person_reId = PersonREID()
            return frame_bgr

        except Exception as e:
            (Logger.get_logger()).info(f"Exception occurred: {e}")

    

    def draw_boxes(self, frame, boxes, image_path):
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        try:
            for box in boxes:
                x1, y1, x2, y2, person_id, conf, cls_id, ukn = box
                #cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), self.colors[int(person_id)], 2)
                #cv2.putText(frame, f'id: {int(person_id)}', (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors[int(person_id)], 2)
                #cv2.imwrite(image_path, frame)
            return frame
        except IndexError as e:
            (Logger.get_logger()).info(" Exception occured due to {} Index error".format(e))
    
    def visualize(self, frame, boxes, counter):
        image_path = f'{self.query_path}/frame_{counter:04d}.jpg'
        frame = self.draw_boxes(frame, boxes, image_path)
        self.crop_detected_person(frame, boxes, counter)
        
        #cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        # cv2.imshow('frame', frame)
        # cv2.waitKey(1)
            

    def frame_processing(self, frame, counter):
        try:
            print("Inside frame Proceiing")
            frame = Image.fromarray(frame)
            boxes = self.detect_person(frame)

            if boxes.shape[0] != 0:
                tracked_boxes = self.tracker.update(boxes, np.array(frame)) # --> (x, y, x, y, id, conf, cls_id, Uknw)
                
                GlobalData.set_person_id.extend([box[4] for box in tracked_boxes if box[4] not in GlobalData.set_person_id])
                
                # if counter == 1 and not self.updated_unique_person_list:
                #     GlobalData.unique_person_list.extend([box[4] for box in tracked_boxes])
                #     self.updated_unique_person_list = True 
            else:
                return False
   
            metadata, metadata_updation_status = GlobalData.metadata_handling.set_all_metadata_attributes(tracked_boxes)
 
            self.visualize(frame, tracked_boxes, counter)
            print(metadata)
            #GlobalData.app_logger.info("MetaData:  {}".format(metadata))
            self.logger.info(json.dumps(metadata))
            return constant.SUCCESS_STATUS
        except FrameProcessingException as e:
            raise GstreamerDecoderException(e)