"""
File : person_reid.py
Description : Class is responsible for Person re-identification
Created on : 
Author :
E-mail :

"""

from src.exception.base_exception import ImageConversionException, GstreamerDecoderException, FrameProcessingException
from src.common.config_manager import cfg
from src.utils.logger import Logger
from src.constant.project_constant import Constant as constant
from src.constant.global_data import GlobalData

import torchreid
from torchreid.reid.utils import FeatureExtractor
from torchreid import metrics
import torch
import os
import numpy as np 
import time
import glob
from PIL import Image
import queue
import threading

class PersonREID(object):

    def __init__(self) -> None:
        self.model_path = (constant.CURRENT_DIR_PATH / str(cfg.get_model_config(constant.CONFIG_MODEL_PERSONREID_WEIGHT_FILE))).resolve() 
        self.gallery_path = (constant.CURRENT_DIR_PATH / str(cfg.get_resource_config(constant.REID_GALLERY_DIR))).resolve() 
        self.query_path = (constant.CURRENT_DIR_PATH / str(cfg.get_resource_config(constant.REID_QUERY_DIR))).resolve() 
        self.output_file_name = "output003.txt"
        self.topK = 20
        self.image_queue = queue.Queue(maxsize=10)
        self.extractor = FeatureExtractor(model_name='resnet50',model_path=self.model_path, device=constant.CPU_DEVICE)
        self.stop_signal = threading.Event()
        

    def list_jpg_files(self, folder_path):
        search_pattern = os.path.join(folder_path, '*.jpg')    
        jpg_files = []
        jpg_files = glob.glob(search_pattern)    
        return jpg_files


    def get_topK_images_paths(self, top_k_indices, gallery_image_paths):
        
        top_k_gallery_images = []
        for row in top_k_indices:
            for ele in row:
                top_k_gallery_images.append(gallery_image_paths[int(ele)])
            break
        return top_k_gallery_images



    def get_topK_reID(self, query_image_path):
        query_image_feature = self.extractor(query_image_path)
        print("44444444444", query_image_feature)
        gallery_image_paths = self.list_jpg_files(self.gallery_path)
        query_image_paths = self.list_jpg_files(self.query_path)
        query_img_len = len(query_image_paths)
        gallary_img_len = len(gallery_image_paths)
        if query_img_len == 0:
            print("Please add query image(s).")
            return
        if gallary_img_len == 0:
            print("Please add gallery images.")
            return
        with open(self.output_file_name,"a") as file:
            file.write(f"{'The total number of images in query: '}: {query_img_len}\n")
            file.write(f"{'The total number of images in gallery: '}: {gallary_img_len}\n")
        print("$$$$$$$$$$$$________________________")
        # Extract features from the gallery images
        gallery_features = self.extractor(gallery_image_paths)
        #for filename in os.listdir(self.query_path):
        with open(self.output_file_name,"a") as file:
    
            # Record start time to process current image
            start = time.time()

            #query_features = self.extractor(query_image_path)

            similarity = torchreid.metrics.distance.euclidean_squared_distance(query_image_feature, gallery_features)
            sorted_distances_n, sorted_indices_n = torch.sort(similarity)

            # Get the indices of the top K gallery images
            top_k_indices_n = sorted_indices_n[:, :self.topK]
            end = time.time()
            query_time_cost = end - start

            # Return the top K gallery images
            topK_images_paths = self.get_topK_images_paths(top_k_indices_n, gallery_image_paths)
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            file.write(f"{'The time used for this query'}: {query_time_cost}\n")
            file.write(f"{'The query image is: '}: {query_image_path}\n")
            file.write(f"{'New Top k images are: '}: {topK_images_paths}\n")

    


    # def monitor_folder2(self):
    #     print("||||||||||||||||||| Inside Monitor ||||||||||||||||||")
        
    #     def process_images():
    #         while not self.stop_signal.is_set():
    #             try:
    #                 query_image_features = self.image_queue.get()
    #                 print("12121212121212")
    #                 self.get_topK_reID(query_image_features, query_image_path)
    #             except queue.Empty:
    #                 pass
        
    #     processing_thread = threading.Thread(target=process_images)
    #     processing_thread.start()
        
    #     while not self.stop_signal.is_set():
    #         folder2_images = os.listdir(self.query_path)
            
    #         for image_path in folder2_images:
    #             query_image_path = os.path.join(self.query_path, image_path)
    #             query_image_features = self.extractor(query_image_path)
                
    #             # Add the new image features to the queue
    #             self.image_queue.put(query_image_features)
                
    #             #os.remove(query_image_path)
    #             print('44444444444', self.image_queue.empty())
            
    #         time.sleep(1)  # Adjust the polling interval as needed
        
    #     # Stop the processing thread when the main thread exits
    #     self.stop_signal.set()
    #     processing_thread.join()



    def monitor_query_images(self, folder_path, image_queue, stop_event, ready_event):
        while not stop_event.is_set():
            for image_name in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image_name)
                #print('image_path', image_path)
                if os.path.isfile(image_path) and image_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_queue.put(image_path)
                    print('image_path', image_queue.qsize())
            time.sleep(1)  # Adjust the polling interval as needed
            ready_event.set()

    # Function to process images from the queue
    def process_images(self, query_queue, gallery_queue, stop_event):
        while not stop_event.is_set():
            try:
                query_image_path = query_queue.get()  # Wait for a query image
                gallery_image_path = gallery_queue.get()  # Wait for a gallery image
                #print('eererer--gallery_image_path',gallery_image_path )
                #print('34434344---query_image_path', query_image_path)
                query_image_features = self.extractor(query_image_path)
                #self.get_topK_reID(query_image_features, query_image_path)
              
                # gallery_image = load_and_process_image(gallery_image_path)

                # Calculate similarity between the two images
                #similarity = calculate_similarity(query_image, gallery_image)
                
                #print(f"Similarity between {query_image_path} and {gallery_image_path}: {similarity}")

            except queue.Empty:
                pass


