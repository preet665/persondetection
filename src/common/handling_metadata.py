"""
File : handling_metadata.py
Description : Class is responsible for Active Camera handling
Created on : 
Author :
E-mail :

"""

from src.exception.base_exception import ImageConversionException, FileNotFoundException, MetaDataUpdationError
from src.common.config_manager import cfg
from src.utils.logger import Logger
from src.constant.project_constant import Constant as constant
from src.constant.global_data import GlobalData
from src.services.db_connection import RedisDatabaseHandler
import json
import time

class MetaDataHandler(object):
    def __init__(self):
        self.read_camera_config()
        self.read_metadata()
        self.db_handler = RedisDatabaseHandler()


    def read_camera_config(self):  
        try:
            camera_metadata = (constant.CURRENT_DIR_PATH / str(cfg.get_camera_config(constant.CAMERA_CONFIG_FILE))).resolve()  
        except Exception as e:
            raise FileNotFoundException("Camera config File not found : {0}".format(e))
        try:
            with open(camera_metadata) as f:
                config_data = json.load(f)
        except Exception as e:
            raise FileNotFoundException("Camera Json file not loaded : {0}".format(e))
        finally:
            f.close()
        GlobalData.camera_metadata = config_data

    def read_metadata(self):
        try:
            inference_metadata = (constant.CURRENT_DIR_PATH / str(cfg.get_json_data(constant.CONFIG_RESOURCES_METADATA_TEMPLATE_FILE))).resolve()
        except Exception as e:
            raise FileNotFoundException("Metadata file not found : {0} ". format(e))
        try:
            with open(inference_metadata) as f:
                metadata = json.load(f)
        except Exception as e:
            raise FileNotFoundException("Metadata Json file not loaded : {0}".format(e))
        finally:
            f.close()
        GlobalData.inference_metadata = metadata

    def set_all_metadata_attributes(self, output_data):
        try:
            data_template = GlobalData.inference_metadata

            for (x1, y1, x2, y2, person_id, conf, cls_id, ukw ) in output_data:
                data_template[constant.FRAME_METADATA][constant.TRACKER_TIME] = time.strftime("%Y-%m-%d %H:%M:%S")
                data_template[constant.FRAME_METADATA][constant.TRACKER_ID] = f"Person_{person_id}"
                data_template[constant.FRAME_METADATA][constant.CENTER] = (int((x1+x2)/2), int((y1+y2)/2))
                data_template[constant.FRAME_METADATA][constant.HEIGHT] = int(x2-x1)
                data_template[constant.FRAME_METADATA][constant.WIDTH] = int(y2-y1)
                data_template[constant.FRAME_METADATA][constant.X_CORD] = [int(x1), int(x2)]
                data_template[constant.FRAME_METADATA][constant.Y_CORD] = [int (y1),int(y2)]
                data_template[constant.FRAME_METADATA][constant.PRED_CLASS] = 'Person'
                data_template[constant.FRAME_METADATA][constant.PRED_SCORE] = "%.2f" % conf
            
            selected_data_insertion_keys = [constant.TRACKER_TIME, constant.X_CORD, constant.Y_CORD]
            redis_data_prep = {key: data_template[constant.FRAME_METADATA].get(key) for key in selected_data_insertion_keys}

            #print("Redis -Data",redis_data_prep)
            #self.db_handler.insert_data(data_template)
            self.db_handler.insert_data(redis_data_prep)
            return data_template, constant.SUCCESS_STATUS
        except Exception as e:
            raise MetaDataUpdationError("Exception occurred {0} in Metadata matching and updation".format(e)) from e