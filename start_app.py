"""
File : infernce.py
Description : Class is responsible for custom exception handling
Created on : 
Author :
E-mail :

"""

from src.common.gstreamer_decoder import VideoProcessing
from src.constant.project_constant import Constant as constant
from src.common.config_manager import cfg
from src.utils.logger import Logger
from src.constant.global_data import GlobalData
from src.exception.base_exception import MediaProcessingEngineException
from src.common.initiate_services import InitiateServices
import signal, sys
import multiprocessing as mp

def set_execution_environment():
    # Setting up environment configuration
    execution_env = cfg.get_default_config(constant.CONFIG_DEFAULT_EXECUTION_ENVIRONMENT)
    if execution_env.lower() == constant.EXECUTION_ENVIRONMENT_LOCAL:
        GlobalData.exec_environment_config = constant.CONFIG_LOCAL_ENVIRONMENT
    elif execution_env.lower() == constant.EXECUTION_ENVIRONMENT_DEV:
        GlobalData.exec_environment_config = constant.CONFIG_DEV_ENVIRONMENT
    (Logger.get_logger()).info("Execution environment is {}".format(GlobalData.exec_environment_config))


def signal_handler(signum, frame):
    print("Keyboard interruption detected. Terminating processes...")
    
    if hasattr(service_initializatio, 'video_processor_process'):
        GlobalData.video_processor_process.terminate()
    if hasattr(service_initializatio, 'person_reid_process'):
        GlobalData.person_reid_process.terminate()
    sys.exit(1)


if __name__ == "__main__":
    mp.set_start_method('spawn')
    set_execution_environment()
    print(f'Execution Environment set to: {GlobalData.exec_environment_config}')
    (Logger.get_logger()).info("Initializing app...")
    if GlobalData.exec_environment_config is None:
        raise MediaProcessingEngineException("Execution Environment not set. Select from local, dev, prod, test, int or uat "
                        "as ExecutionEnvironment in config.ini.")
    
    try:
        #stream = 'person.mp4'
        #processor = VideoProcessing()
        # GlobalData.streaming_status = constant.SUCCESS_STATUS
        # processor.run()
        #GlobalData.gst_main_thread.join()
        service_initializatio = InitiateServices()
        metahandler_service_status = service_initializatio.init_metadata_handler()
        print(f'Meta Handler Service Inition Status:{metahandler_service_status}')
        video_processing_status = service_initializatio.init_videoprocessing_pipeline()
        print(f'Video Processing Service Inition Status:{video_processing_status}')
        #person_reid_service_status = service_initializatio.init_person_reidentification()
        #print(f'Person REID Service Inition Status:{person_reid_service_status}')
        
        signal_status = signal.signal(signal.SIGINT, signal_handler)

        
    
    except Exception as e:
        print("Exception:", e)

        