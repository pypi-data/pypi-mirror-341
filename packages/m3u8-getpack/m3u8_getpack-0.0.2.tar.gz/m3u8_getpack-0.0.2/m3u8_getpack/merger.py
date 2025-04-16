import ffmpeg
import os
import threading
from .notifier import Spinner


class Merger:
    def __init__(
            self, output_path,
            temp_path=".tmp",
            manifest_path=".manifest.txt",
            output_ext="mp4"):
        self.output_path = output_path
        self.output_ext = output_ext
        self.temp_path = temp_path
        self.manifest_path = os.path.join(
                                self.temp_path,
                                manifest_path)
        self.done_event = None

    def merge(self, loglevel="quiet"):
        ffmpeg.input(
            self.manifest_path,
            format='concat',
            safe=0
        ).output(
            f"{self.output_path}.{self.output_ext}",
            loglevel=loglevel,
            c='copy',
            y='-y'
        ).run()
        if self.done_event:
            self.done_event.set()

    def start(self, spinner=False):
        self.done_event = threading.Event() if spinner else None
        if spinner:
            spinner_thread = threading.Thread(
                                target=Spinner(
                                    "Joining clips",
                                    self.done_event).run)
            spinner_thread.daemon = True
            spinner_thread.start()
        merge_thread = threading.Thread(target=self.merge)
        merge_thread.daemon = True
        merge_thread.start()
        merge_thread.join()
