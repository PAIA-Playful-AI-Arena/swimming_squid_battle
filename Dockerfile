FROM paiatech/paia-game-env:20250522
ADD . /game
WORKDIR /game

CMD ["bash"]
