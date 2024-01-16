"""
File : status_code.py
Description : Status codes defined in this class to use across the project
Created on :
Author :
E-mail :
"""


class StatusCode(object):
    """
    Status codes defined in this class to use across the project
    """
    STATUS_SUCCESS = 20000
    STATUS_STREAM_ALREADY_ACTIVE = 20001
    STATUS_STREAM_ALREADY_INACTIVE = 20002
    STATUS_STREAM_STOP_ALREADY_INITIATED = 20003
    STATUS_SENSOR_ID_NOT_FOUND = 20004

    HTTP_SUCCESS_STATUS = 200
    HTTP_BAD_REQUEST_STATUS = 400
    HTTP_NOT_FOUND_STATUS = 404
    HTTP_MISSING_PARAMETER_STATUS = 409
    HTTP_INTERNAL_SERVER_ERROR = 500

