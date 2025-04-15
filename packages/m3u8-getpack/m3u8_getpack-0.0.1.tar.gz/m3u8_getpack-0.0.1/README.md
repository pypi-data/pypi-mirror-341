
# m3u8-getpack

![m3u8-getpack](https://img.shields.io/badge/pip_install-m3u8--getpack-gold) ![MIT License](https://img.shields.io/badge/License-MIT-gold.svg) ![Linux](https://img.shields.io/badge/Linux-Support-blue?logo=linux&logoColor=white) ![FFMPEG Support](https://img.shields.io/badge/FFMPEG-Support-blue) ![Python](https://img.shields.io/badge/Python-blue?logo=python&logoColor=yellow)

**m3u8-getpack** (also **m3gp**) is a fast command-line tool and Python library. 

It **gets** video segments (.ts files) from .m3u8 playlists and **packs** them into a single .mp4 video file.

Perfect for handling HLS (HTTP Live Streaming) content, **m3u8-getpack** provides both a streamlined CLI for easy use and a modular API for integration into your own projects.

## ✨ Features
#### ⚡ Fast and simple CLI for quick use directly from the terminal.
#### 🧩 Modular Python API for seamless integration into your own scripts and tools.
#### 🚀 Multithreaded downloading for high-speed performance.
#### 🎞️ Uses [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) as a backend for accurate video merging.
#### 📡 Designed to handle HLS (HTTP Live Streaming) content efficiently.
#### 📌 Currently supports only static HLS playlists — direct .m3u8 files .containing segment .ts links (not master playlists or nested CDN manifests).

## 📦 Installation
### ⚙️ Requirements
#### Make sure python3 and pip are installed:
```bash
    python3 --version
    pip --version
```
#### If needed:
```bash
    sudo apt install python3
    sudo apt install python3-pip
```
### ✅ Install via pip (Recommended-CLI)

```bash
    pip install m3u8-getpack
```

### 🛠️ Install via GitHub (dev mode)

#### For development or direct usage from source:
```bash
    git clone https://github.com/yourusername/m3u8-getpack.git
    cd m3u8-getpack
    pip install -e .
```

## Running
### ✅ Recommended-CLI
```bash
    m3u8-getpack -i video.m3u8 -o myvideo.mp4
    # Or alternatively:
    m3gp -i video.m3u8 -o myvideo.mp4
    mgp -i video.m3u8 -o myvideo.mp4
```

### 🛠️ Run the package directly from source (without installation, live changes reflected):
```bash
    python3 -m m3u3-getpack -i video.m3u8 -o myvideo.mp4
```
