FROM paiatech/mlgame:10.4.6a2-slim
ADD . /game
WORKDIR /game
RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN pip install -r requirements.txt --no-cache-dir
RUN apt-get update && apt-get install -y libglib2.0-0

CMD ["bash"]
