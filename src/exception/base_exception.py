"""
File : base_exception.py
Description : Class is responsible for custom exception handling
Created on :
Author :
E-mail :
"""

from src.utils.logger import Logger


class MediaProcessingEngineException(Exception):
    """
    This class is responsible for custom exception handling
    """

    message = ''

    def __init__(self, message):
        self.message = message
        (Logger.get_logger()).error(self.message)

    def __str__(self):
        return repr(self.message)


class FileNotFoundException(MediaProcessingEngineException):
    def __init__(self, message):
        super(FileNotFoundException,self).__init__(message)

class GstreamerDecoderException(MediaProcessingEngineException):
    def __init__(self, message):
        super(GstreamerDecoderException, self).__init__(message)

class PipelineException(MediaProcessingEngineException):
    def __init__(self, message):
        super(PipelineException, self).__init__(message)


class StreamDecodeManagerException(MediaProcessingEngineException):
    def __init__(self, message):
        super(StreamDecodeManagerException,self).__init__(message)


class ImageConversionException(MediaProcessingEngineException):
    def __init__(self, message):
        super(ImageConversionException,self).__init__(message)

class ServiceInitiateException(MediaProcessingEngineException):
    def __init__(self, message):
        super(ServiceInitiateException,self).__init__(message)


class SensorInitiationException(MediaProcessingEngineException):
    def __init__(self, message):
        super(SensorInitiationException,self).__init__(message)


class SensorProcessingHandlerException(MediaProcessingEngineException):
    def __init__(self, message):
        super(SensorProcessingHandlerException,self).__init__(message)


class SensorMetadataHandlerException(MediaProcessingEngineException):
    def __init__(self, message):
        super(SensorMetadataHandlerException,self).__init__(message)

class MetaDataUpdationError(MediaProcessingEngineException):
    def __init__(self, message):
        super(MetaDataUpdationError,self).__init__(message)

class RequestStateHandlerException(MediaProcessingEngineException):
    def __init__(self, message):
        super(RequestStateHandlerException,self).__init__(message)

class NotifyGenerationHandlerError(MediaProcessingEngineException):
    def __init__(self, message):
        super(NotifyGenerationHandlerError,self).__init__(message)

class FrameProcessingException(MediaProcessingEngineException):
    def __init__(self, message):
        super(FrameProcessingException,self).__init__(message)
