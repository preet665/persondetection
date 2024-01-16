"""
File : gstreamer_decoder.py
Description : Class is responsible to Gstreamer Pipline and Processe frame decoding.
Created on : 
Author :
E-mail :

"""
from src.common.inference import Watcher
from src.constant.global_data import GlobalData
from src.exception.base_exception import GstreamerDecoderException, PipelineException
from src.constant.project_constant import Constant as constant
from src.common.handling_metadata import MetaDataHandler
import sys
import gi
gi.require_version(constant.GSTREAMER, constant.GST_VERSION)
from gi.repository import Gst, GLib
import threading
import time
import concurrent.futures
import cv2
import numpy as np
from datetime import datetime
import traceback


##waowza login : - diboje8093@avidapro.com
#pwd: India@12345
# rtsp://9aa6be958977.entrypoint.cloud.wowza.com:1935/app-45260S6Q/ac9b55a0


class VideoProcessing(object):
    def __init__(self) -> None:
        Gst.init()
        self.main_loop = GLib.MainLoop()
        GlobalData.gst_main_thread = threading.Thread(target=self.main_loop.run)
        GlobalData.gst_main_thread.start()
        self.success_event = threading.Event()
        self.running = True
        self.detections = []
        self.counter = 0
        self.inference = Watcher()
        self.last_frame_time = datetime.now()

    def start_stream(self, source):
        try:
            pipeline = Gst.parse_launch(source)
            appsink = pipeline.get_by_name(constant.GST_SINK)
            appsink.set_property(constant.GST_EMIT_SIGNAL, True)
            appsink.set_property(constant.GST_MAX_BUFFER, 1)
            appsink.connect(constant.GST_NEW_SAMPLE, self.on_new_sample)
            pipeline.set_state(Gst.State.PLAYING)

            while self.running:
                time.sleep(0.1)

                current_time = datetime.now()
                time_diff = (current_time - self.last_frame_time).total_seconds()
                if time_diff >= 10.0:
                    print("No frames received for 10 seconds. Stopping stream.")
                    break

            pipeline.set_state(Gst.State.NULL)
        except Exception as e:
            print('Exception in on_new_sample:', e)
            traceback.print_exc()
            
    def run(self):
        try:
            GlobalData.metadata_handling = MetaDataHandler()
            GlobalData.metadata_handling.read_camera_config()
            
            active_cameras = GlobalData.camera_metadata[constant.ACTIVE_CAMERA]
            camera_configs = GlobalData.camera_metadata[constant.CAMERAS]

            active_sources = [camera_configs[cam]['source'] for cam in active_cameras]
            GlobalData.total_active_camera = len(active_cameras)
            print('active source--', active_sources)
            if active_sources:
                with concurrent.futures.ThreadPoolExecutor(max_workers=len(active_sources)) as executor:
                    executor.map(self.start_stream, active_sources)
                #
                self.main_loop.quit()
                GlobalData.gst_main_thread.join()
            else:
                print('No active cameras found in the configuration.')
                
                self.main_loop.quit()
                GlobalData.gst_main_thread.join()
        except Exception as e:
            print(f"Thread encountered an error: {e}")
            self.success_event.clear()

    def stop(self):
        self.running = False

    def on_new_sample(self, appsink):
        try:
            sample = appsink.emit("pull-sample")
            if sample:
                buffer = sample.get_buffer()
                caps = sample.get_caps()
                width = caps.get_structure(0).get_value(constant.FRAME_BUFFER_WIDTH)
                height = caps.get_structure(0).get_value(constant.FRAME_BUFFER_HEIGHT)
                np_array = np.frombuffer(buffer.extract_dup(0, buffer.get_size()), dtype=np.uint8)
                frame = np_array.reshape((height, width, 3))
                
                self.counter += 1
                inference_status = self.inference.frame_processing(frame, self.counter)
                if not inference_status:
                    self.stop()
                    self.main_loop.quit()
                    #GlobalData.gst_main_thread.join()
                    sys.exit(0)
        except Exception as e:
            print('Exception in on_new_sample:', e)
            traceback.print_exc()
            
        return Gst.FlowReturn.OK
