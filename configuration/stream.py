import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import threading
import time
import concurrent.futures
import cv2
import numpy as np
from datetime import datetime
import os
import traceback
import json
Gst.init(None)

class StreamHandler:
    def __init__(self, source, stream_name, output_folder):
        self.source = source
        self.stream_name = stream_name
        self.output_folder = output_folder
        self.pipeline = None
        self.appsink = None
        self.counter = 0
        self.last_frame_time = datetime.now()  

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def frame_processing(self, frame):
        stream_id = self.stream_name.replace(" ", "_")
        filename = os.path.join(self.output_folder, f"{stream_id}_frame_{self.counter}.jpg")
        cv2.imwrite(filename, frame)
        self.counter += 1
        return True  

    def start_stream(self):
        try:
            self.pipeline = Gst.parse_launch(self.source)
            self.pipeline.set_state(Gst.State.PLAYING)
            bus = self.pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect("message::error", self.on_error)

            self.appsink = self.pipeline.get_by_name("sink")
            self.appsink.set_property("emit-signals", True)
            self.appsink.set_property("max-buffers", 1)
            self.appsink.connect("new-sample", self.on_new_sample)
        except Exception as e:
            print(f"Error while starting stream {self.stream_name}: {e}")


   

    def stop_stream(self):
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
            self.pipeline = None

    def on_error(self, bus, message):
        error, debug_info = message.parse_error()
        print(f"Error on stream {self.stream_name}: {error.message}")
        self.stop_stream()


    def on_new_sample(self, appsink):
        try:
            sample = appsink.emit("pull-sample")
            if sample:
                buffer = sample.get_buffer()
                caps = sample.get_caps()
                width = caps.get_structure(0).get_value('width')
                height = caps.get_structure(0).get_value('height')
                np_array = np.frombuffer(buffer.extract_dup(0, buffer.get_size()), dtype=np.uint8)
                frame = np_array.reshape((height, width, 3))
                
                self.counter += 1
                inference_status = self.frame_processing(frame)
                if not inference_status:
                    self.stop()
                    self.main_loop.quit()
                    #GlobalData.gst_main_thread.join()
                    sys.exit(0)
        except Exception as e:
            print('Exception in on_new_sample:', e)
            traceback.print_exc()
            
        return Gst.FlowReturn.OK


def stop_application(handlers, main_loop):
    while True:
        time.sleep(10)
        current_time = datetime.now()
        for handler in handlers:
            time_diff = (current_time - handler.last_frame_time).total_seconds()
            if time_diff >= 10:
                handler.stop_stream()
        # Stop the main loop after all handlers have been stopped
        if all(handler.pipeline is None for handler in handlers):
            main_loop.quit()
            break

def load_camera_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def main():
    sources = [
        "filesrc location=input_vid1.mp4 ! qtdemux name=demux demux.video_0 ! decodebin ! videoconvert ! video/x-raw,format=BGR ! appsink name=sink", 
        "filesrc location=input_vid2.mp4 ! qtdemux name=demux demux.video_0 ! decodebin ! videoconvert ! video/x-raw,format=BGR ! appsink name=sink"
    ]
    config_path = 'camera_config.json'  # Path to your camera_config.json file
    camera_configs = load_camera_config(config_path)

    output_folder = "output_frames"

    handlers = []

    # Assuming 'cameras' key in JSON file contains the camera configurations
    for camera_id, camera_config in camera_configs['cameras'].items():
        source = camera_config['source']
        handler = StreamHandler(source, f"Stream {camera_id}", output_folder)
        handlers.append(handler)

    # for i, source in enumerate(sources):
    #     handler = StreamHandler(source, f"Stream {i + 1}", output_folder)
    #     handlers.append(handler)

    main_loop = GLib.MainLoop()

    stop_thread = threading.Thread(target=stop_application, args=(handlers,main_loop))
    stop_thread.daemon = True
    stop_thread.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(sources)) as executor:
        futures = [executor.submit(handler.start_stream) for handler in handlers]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    try:
        main_loop.run()
    except KeyboardInterrupt:
        pass
    finally:
        for handler in handlers:
            handler.stop_stream()

if __name__ == '__main__':
    main()



