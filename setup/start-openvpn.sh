#!/bin/bash
docker run -d \
  --name=openvpn-as \
  --cap-add=NET_ADMIN \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/Calcutta \
  -p 943:943 \
  -p 9443:9443 \
  -p 1194:1194/udp \
  -v /home/ubuntu/vpn:/config \
  --restart unless-stopped \
  ghcr.io/linuxserver/openvpn-as
# refer to https://en.wikipedia.org/wiki/List_of_tz_database_time_zones for valid TZ
