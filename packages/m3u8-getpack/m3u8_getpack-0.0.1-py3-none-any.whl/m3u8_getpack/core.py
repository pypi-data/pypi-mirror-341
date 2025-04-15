from .fileman import Fileman
from .parser import Parser
from .downloader import Downloader
from .merger import Merger
from .utils import Args, Stopwatch


def core():
    input_file, output_file, quiet = Args().get()
    p_bar = False if quiet else True
    s_bar = False if quiet else True
    fm = Fileman(input_file)
    fm.rmdir()
    fm.mkdir()
    output_file = fm.parse_output(output_file)
    parser = Parser(input_file)
    urls, ext, total_segments = parser.enqueue_urls()
    parser.write_manifest()
    dl = Downloader(urls, ext, total_segments)
    dl.start(progress=p_bar)
    vm = Merger(output_file)
    vm.start(spinner=s_bar)
    fm.rmdir()


def main():
    st = Stopwatch(core)
    st.start()
    st.show()
