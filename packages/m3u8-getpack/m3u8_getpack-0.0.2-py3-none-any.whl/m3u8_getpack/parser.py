import os
import queue
import re
from .notifier import show_error


class Parser:
    def __init__(self, input_path, temp_path=".tmp"):
        self.input_path = input_path
        self.temp_path = temp_path
        self.urls = queue.Queue()
        self.total_segments = 0
        self.ext = None

    def enqueue_urls(self):
        with open(self.input_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            if "https://" in line:
                self.urls.put(line.strip())
                if self.ext is None:
                    matcher = r"(\.[^.]+)$"
                    self.ext = re.search(matcher, line).group(1)
                    self.ext = self.ext.strip("\n")
        self.total_segments = self.urls.qsize()
        return self.urls, self.ext, self.total_segments

    def write_manifest(self):
        directory = os.path.join(self.temp_path, ".manifest.txt")
        try:
            with open(directory, "w") as manifest:
                for i in range(self.total_segments):
                    manifest.write(f"file {i}{self.ext}\n")
        except OSError as e:
            show_error(f"Failed to write manifest: {e}")
