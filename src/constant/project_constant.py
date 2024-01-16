"""
File : project_constant.py
Description : Constant defined in this class to use across the project
Created on : 
Author : 
E-mail : 

"""
import os
from pathlib import Path

class Constant(object):
    """
    Description: variable declearation
    """
    CURRENT_DIR_PATH = Path(__file__).resolve().parent
    PROJECT_ROOT_DIR = os.path.abspath(os.curdir)
    CONFIG_FILE_PATH = 'configuration/config.ini'
    LOGGER_FILE_PATH = '../../log/logfiles.log'
    LOGGER_LEVEL = 'INFO'
    MAX_BYTES = 1024
    BACKUP_COUNT = 3

    CONFIG_URL = 'URL'

    REQUEST_DATA_PARAM = "data"

    CPU_DEVICE = 'cpu'
    MODEL_PATH = ''
    MODEL_CONFIG_PATH = 'COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'
    CURRENT_REQUEST_STATE = 'CURRENT_REQUEST_STATE'
    REQUEST_STATE_LAUNCH = 'launch'
    REQUEST_STATE_PAUSE = 'pause'
    REQUEST_STATE_STOP = 'stop'

    RESPONSE = 'response'
    STATUS = 'status'
    MIME_TYPE = 'mimetype'
    METADATA = 'metadata' 

    CONTENT_TYPE= 'application/json'
    API_HEADER = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    CONFIG_DEFAULT_API_HEADER = {'Content-type': 'application/json', 'Accept': 'text/plain'}


    PATH_SEPARATOR = '/'

    CONFIG_DEV_ENVIRONMENT = 'DEV_ENVIRONMENT'
    CONFIG_TEST_ENVIRONMENT = 'TEST_ENVIRONMENT'
    CONFIG_LOCAL_ENVIRONMENT = 'LOCAL_ENVIRONMENT'
    CONFIG_PROD_ENVIRONMENT = 'PROD_ENVIRONMENT'
    CONFIG_UAT_ENVIRONMENT = 'UAT_ENVIRONMENT'
    CONFIG_INT_ENVIRONMENT = 'INT_ENVIRONMENT'

    CONFIG_DEFAULT = 'DEFAULT'
    CONFIG_DEFAULT_OPERATING_SYSTEM = 'OperatingSystem'
    CONFIG_DEFAULT_EXECUTION_ENVIRONMENT = 'ExecutionEnvironment'
    CONFIG_DEFAULT_COMMUNICATION_PROTOCOL = 'CommunicationProtocol'

    CONFIG_ENVIRONMENT_SERVER_IP = 'ServerIP'
    CONFIG_ENVIRONMENT_SERVER_PORT = 'ServerPort'
    CONFIG_ENVIRONMENT_DATABASE_URI = 'DatabaseUri'
    CONFIG_ENVIRONMENT_DEBUG_MODE = 'DebugMode'
    CONFIG_ENVIRONMENT_DATABASE = 'RedisDB'
 

    # Values accepted by ExecutionEnvironment config
    EXECUTION_ENVIRONMENT_LOCAL = 'local'
    EXECUTION_ENVIRONMENT_DEV = 'dev'
    EXECUTION_ENVIRONMENT_PROD = 'prod'
    EXECUTION_ENVIRONMENT_TEST = 'test'
    EXECUTION_ENVIRONMENT_UAT = 'uat'
    EXECUTION_ENVIRONMENT_INT = 'int'


    CONFIG_MODEL = 'MODEL'
    CONFIG_MODEL_FILE_DIR = 'ModelFilesDirectory'
    CONFIG_MODEL_CONFIG_FILE = 'ModelConfigFile'
    CONFIG_MODEL_WEIGHT_FILE = 'ModelWeightFile'
    CONFIG_MODEL_PERSONREID_WEIGHT_FILE = 'PersonReIDModelWeightFile'
    CONFIG_MODEL_THRESH_VALUE = 'ModelThresholdValue'
    CONFIG_MODEL_OBJECTS = 'ModelObjects'
    CONFIG_MODEL_MARKING_COLOR = 'ModelMarkingColor'
    CONFIG_MODEL_MASK_RCNN_FPN_YAML =  'ModeMaskRcnnFPNYamlFile'
    ULTRALYTICS_YOLO = 'ultralytics/yolov5'

    DETECTION_CLASS = "class"
    X_MAX = "xmax"
    X_MIN = "xmin"
    Y_MAX = "ymax"
    Y_MIN = "ymin"
    DETECTION_CONF = 'confidence'

    FRAME_BUFFER_HEIGHT = "height"
    FRAME_BUFFER_WIDTH = "width"
    
    GSTREAMER = "Gst"
    GST_VERSION = "1.0"
    GST_EMIT_SIGNAL = "emit-signals"
    GST_SINK = "sink"
    GST_MAX_BUFFER = "max-buffers"
    GST_NEW_SAMPLE = "new-sample"

    DEBUG_MODE_ON = 'on'
    DEBUG_MODE_OFF = 'off'

    CONFIG_RESOURCES = 'RESOURCES'
    CONFIG_RESOURCES_METADATA_TEMPLATE_FILE = 'MetadataFilePath' 
    CAMERA_CONFIG_FILE = 'CameraConfigFile'
    ACTIVE_CAMERA = 'active_camera'
    CAMERAS = 'cameras'
    CAMERA_SOURCE = 'source'
    CAMEREA_SOURCE_FILE_PATH = 'source_src'

    REID_QUERY_DIR = 'ReidIDImageQueryDirectory'
    REID_GALLERY_DIR = 'ReidIDImageGalleryDirectory'

    IMAGE_DATA = 'image_data'
    HYPHEN = '-'
    DOT = '.'
    FORWARD_SLASH = '/'
    PIPE = '|'
    UNDER_SCORE = '_'
    AT_THE_RATE = '@'
    COMMA = ','
    EMPTY_STRING = ''
    COLON = ':'
    SPACE = ' '
    RIGHT_ARROW = '->'
    LEFT_ARROW = '<-'
    TIMES = 'x'

    SUCCESS_STATUS = True
    FAILURE_STATUS = False

    
    FRAME_METADATA = "frame_metadata"
    TRACKER_TIME = "time"
    TRACKER_ID = "tracker_id"
    CENTER = "center"
    HEIGHT = "height"
    WIDTH = "width"
    X_CORD = "X"
    Y_CORD = "Y"
    PRED_CLASS =  "pred_class"
    PRED_SCORE =  "pred_score"

    INFERENECE_METADATA_DB_TABLE = "inference_metadata"

