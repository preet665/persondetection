"""
File : config_manager.py
Description : Reads configuration file and create getter functions for each
              parameter in config.
Created on : 
Author :
E-mail :
"""

import configparser
import os
from src.constant.project_constant import Constant as constant #pylint: disable = import-error
#from src.python.app.exceptions.base_exception import FileNotFoundException #pylint: disable = import-error
from src.constant.global_data import GlobalData

class ConfigManager:
    """
    This class opens the configuration file and
    reads all the configuration provided inside it
    """
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.file_name = os.path.join(constant.PROJECT_ROOT_DIR, constant.CONFIG_FILE_PATH)
            self.parser = configparser.ConfigParser()
            self.parser.optionxform = str
            self.config = self.parser

            if os.path.exists(self.file_name):
                self.config.read(self.file_name,encoding='utf-8')
            else:
                print('No Config file found!')

            self.instance = super(ConfigManager, self).__new__(self)

        return self.config


class ReadConfigFile:
    """
    This class reads specific configurations based on user requirement
    """

    objConfig = ''

    def __init__(self):
        self.obj_config = ConfigManager()

    def get_config_object(self):
        return self.objConfig

    def get_default_config(self, param):
        default_config = self.obj_config[constant.CONFIG_DEFAULT]
        return default_config[param]

    def get_environment_config(self, param):
        env_config = self.obj_config[GlobalData.exec_environment_config]
        return env_config[param]

    def get_json_data(self, param):
        json_data = self.obj_config[constant.CONFIG_RESOURCES]
        return json_data[param]

    def get_resource_config(self, param):
        resource_config = self.obj_config[constant.CONFIG_RESOURCES]
        return resource_config[param]

    def get_url_config(self, param):
        url_config = self.obj_config[constant.CONFIG_URL]
        return url_config[param]

    def get_library_config(self, param):
        resource_config = self.obj_config[constant.CONFIG_LIBRARY]
        return resource_config[param]

    def get_model_config(self, param):
        azure_service_config = self.obj_config[constant.CONFIG_MODEL]
        return azure_service_config[param]
    
    def get_camera_config(self, param):
        camera_config = self.obj_config[constant.CONFIG_RESOURCES]
        return camera_config[param]


# Create an instance of ReadConfigFile to be used throughout the program
cfg = ReadConfigFile()

