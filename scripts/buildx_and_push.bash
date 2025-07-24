export tag="1.6.4"
export game="swimming_squid_battle"
export pge_ver="PGE20250525"

docker buildx build --platform linux/amd64,linux/arm64 \
-t paiatech/${game}:${tag} -t paiatech/${game}:${tag}-${pge_ver} \
-f ./Dockerfile . --push