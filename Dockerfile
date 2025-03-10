FROM paiatech/paia-game-env:20250310
ADD . /game
WORKDIR /game

CMD ["bash"]
