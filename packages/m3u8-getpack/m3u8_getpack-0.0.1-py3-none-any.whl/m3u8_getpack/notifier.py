import time
import sys


def show_error(msg):
    print(msg)


def cls():
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()


def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


class ProgressBar:
    def __init__(self, queue, total_segments, header):
        self.queue = queue
        self.total = total_segments
        self.header = header

    def draw_bar(self, current, total, header):
        spin = "─╲│╱"
        full = "■"
        null = "▫"
        left = "❪"
        right = "❫"
        percentage = (current * 100) / total
        label = f" {current} / {total} videos"
        width = len(label)
        indicator = int((current) / total * width) * f"{full}" if total else ""
        space = (len(label) - len(indicator)) * null
        center = (width//2 - (len(header)//2)) * " "
        bar = (f"{left}"
               f"{indicator}"
               f"{space}"
               f"{right}"
               f" {percentage:.1f}%"
               )

        for s in spin:
            cls()
            print(f"{center}{s}  {header}  {s}\n{bar}\n{label}")
            time.sleep(0.03)

    def run(self):
        hide_cursor()
        while not self.queue.empty():
            current = self.total - self.queue.qsize()
            self.draw_bar(current, self.total, f"{self.header}")

        self.draw_bar(self.total, self.total, f"{self.header} Complete")
        show_cursor()


class Spinner:
    def __init__(self, header, done_event):
        self.header = header
        self.done_event = done_event
        self.size = len(header)

    def draw_spinner(self):
        frag = "◥◤◢◣"
        done = "■▣□□"
        spin = "─╲│╱"
        null = "⎼"
        left = "❪"
        right = "❫"
        for occupied in range(self.size):
            for current in range(self.size-occupied):
                for mark in range(len(frag)):
                    if self.done_event.is_set():
                        cls()
                        return
                    line = (
                        f"  {spin[mark]} Joining clips {spin[mark]}\n"
                        f"  {left}"
                        f"{null*current}"
                        f"{frag[mark]}"
                        f"{null*(self.size-current-occupied)}"
                        f"{done[mark]*occupied}"
                        f"{right}"
                        )
                    cls()
                    print(line)
                    time.sleep(0.03)
        cls()

    def run(self):
        hide_cursor()
        while not self.done_event.is_set():
            self.draw_spinner()
        show_cursor()
