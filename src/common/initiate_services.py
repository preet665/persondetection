"""
File : initiate_services.py
Description : Class is responsible to Initiate all services
Created on : 
Author :
E-mail :

"""


from src.exception.base_exception import ServiceInitiateException, GstreamerDecoderException, FrameProcessingException
from src.common.config_manager import cfg
from src.utils.logger import Logger
from src.constant.project_constant import Constant as constant
from src.constant.global_data import GlobalData 
from src.common.gstreamer_decoder import VideoProcessing
from src.services.person_reid import PersonREID
from src.common.handling_metadata import MetaDataHandler
import threading 
import multiprocessing
import sys, queue, time


class InitiateServices(object):
    def __init__(self) -> None:
        self.videoprocessing_status = constant.SUCCESS_STATUS
        self.person_reid_status = constant.SUCCESS_STATUS
        self.metadata_status = constant.SUCCESS_STATUS
        self.gallery_path = (constant.CURRENT_DIR_PATH / str(cfg.get_resource_config(constant.REID_GALLERY_DIR))).resolve() 
        self.query_path = (constant.CURRENT_DIR_PATH / str(cfg.get_resource_config(constant.REID_QUERY_DIR))).resolve() 

    def init_metadata_handler(self):
        try:
            print("inside metadata")
            GlobalData.metadata_handling = MetaDataHandler()
            GlobalData.metadata_handling.read_camera_config()
            return self.metadata_status
        except Exception as e:
            raise ServiceInitiateException(f'Exception Occured in Metadatae Service Inition: {e}.')

    def init_videoprocessing_pipeline(self):
        try:
            print("inside video processing")
            # Create a separate process for VideoProcessing
            GlobalData.video_processor_process = multiprocessing.Process(target=self.init_video_processing)
            GlobalData.video_processor_process.start()
            return self.videoprocessing_status
        except Exception as e:
            raise ServiceInitiateException(f'Exception Occurred in Video Processing Service Initialization: {e}.')

    def init_person_reidentification(self):
        try:
            print("inside person reid")
            # # Create a separate process for PersonREID
            # GlobalData.person_reid_process = multiprocessing.Process(target=self.init_person_reid)
            # GlobalData.person_reid_process.start()
            # return self.person_reid_status
            frame_processing_person_reid = PersonREID()
            
            
            query_folder = self.query_path
            gallery_folder = self.gallery_path
            
            stop_event = threading.Event()
            query_ready_event = threading.Event()
            gallery_ready_event = threading.Event()
            
            query_monitor_thread = threading.Thread(target=frame_processing_person_reid.monitor_query_images, args=(query_folder, GlobalData.query_queue, stop_event, query_ready_event))
            gallery_monitor_thread = threading.Thread(target=frame_processing_person_reid.monitor_query_images, args=(gallery_folder, GlobalData.gallery_queue, stop_event, gallery_ready_event))
            
            query_monitor_thread.start()
            gallery_monitor_thread.start()
            
            # Create multiple image processing processes (adjust the number as needed)
            num_threads = 2
            threads = []
            
            for _ in range(num_threads):
                thread = threading.Thread(target=frame_processing_person_reid.process_images, args=(GlobalData.query_queue, GlobalData.gallery_queue, stop_event))
                thread.start()
                threads.append(thread)
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                # Stop monitoring and processing threads and processes on Ctrl+C
                stop_event.set()
                query_monitor_thread.join()
                gallery_monitor_thread.join()
                for thread in threads:
                    thread.join()
        except Exception as e:
            raise ServiceInitiateException(f'Exception Occurred in Person REID Service Initialization: {e}.')
        

    def init_video_processing(self):
        # global video_processor
        video_processor = None
        try:
            # global video_proccessor
            video_processor = VideoProcessing()
            video_processor.run()
        except Exception as e:
            video_processor.stop()
            GlobalData.gst_main_thread.join()
            GlobalData.video_processor_process.join()
            print(f'Exception Occured: {e}')
        except KeyboardInterrupt:
            video_processor.stop()
            GlobalData.gst_main_thread.join()
            GlobalData.video_processor_process.join()
            print(f'Exception Keyboard Intruption: {e}')

    def init_person_reid(self):
        try:
            frame_processing_person_reid = PersonREID()
            frame_processing_person_reid.monitor_query_images()            
        except Exception as e:
            GlobalData.person_reid_process.join()
            print(f'Exception Occured: {e}')
        except KeyboardInterrupt:
            GlobalData.person_reid_process.join()
            print(f'Exception Keyboard Intruption: {e}')



    



    