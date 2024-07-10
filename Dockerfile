FROM paiatech/mlgame:10.4.6a2-slim
ADD . /game
WORKDIR /game
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    build-essential \
    cmake \
    git \
    pkg-config \
    libjpeg-dev \
    libtiff5-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    gfortran \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt --no-cache-dir

CMD ["bash"]
