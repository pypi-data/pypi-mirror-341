import time
import argparse


class Stopwatch:
    def __init__(self, func):
        self.t0 = 0
        self.t1 = 0
        self.func = func

    def start(self):
        self.t0 = time.perf_counter()
        self.func()
        self.t1 = time.perf_counter() - self.t0

    def show(self):
        print(f"Elapsed time: {self.t1:.1f} seconds.")


class Args:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
                        description="",
                        usage=("python3 %(prog)s [OPTION] "
                                    "[FILE]\nexample: python3 %(prog)s "
                                    "-i playlist.m3u8 -o video.mp4")
        )
        self.parser.add_argument(
                    "-i",
                    "--input",
                    type=str,
                    metavar="",
                    required=True,
                    help="m3u8|txt file path. [REQUIRED]")
        self.parser.add_argument(
                    "-o",
                    "--output",
                    type=str,
                    metavar="",
                    help=("output file path."
                            "Default: same as input, "
                            "with .mp4 extension")
        )
        self.parser.add_argument(
                    "-q",
                    "--quiet",
                    action="store_true",
                    help="do not show progress bars")

    def get(self):
        args = self.parser.parse_args()
        return args.input, args.output, args.quiet
