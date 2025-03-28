FROM paiatech/paia-game-env:20250328
ADD . /game
WORKDIR /game

CMD ["bash"]
