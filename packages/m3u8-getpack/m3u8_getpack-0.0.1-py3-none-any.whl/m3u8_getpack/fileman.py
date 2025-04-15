import os
import re


class Fileman:
    def __init__(
            self, input_path, output_path=None,
            temp_path=".tmp"):
        self.input_path = input_path
        self.output_path = self.parse_output(output_path)
        self.temp_path = temp_path

    def parse_output(self, output_path):
        matcher = r"^(.+)\.[\w\d]+$"
        if output_path is None:
            match = re.search(matcher, self.input_path)
            if not match:
                return "default_video"
            else:
                return match.group(1)
        else:
            match = re.search(matcher, output_path).group(1)
            return match

    def rmdir(self, directory=None):
        directory = self.temp_path if directory is None else directory
        if os.path.isdir(directory):
            for root, dirs, files in os.walk(directory):
                for f in files:
                    path = os.path.join(root, f)
                    os.remove(path)
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(directory)

    def mkdir(self, directory=None):
        directory = self.temp_path if directory is None else directory
        os.makedirs(directory) if not os.path.isdir(directory) else None
