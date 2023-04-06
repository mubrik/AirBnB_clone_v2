#!/usr/bin/env bash
# setup airbnb on a ubuntu 14.04 server

# install nginx
sudo apt-get update
sudo apt-get install nginx -y
# cretae dirs
mkdir -p /data/web_static/releases/ /data/web_static/shared/ /data/web_static/releases/test/
# template html
echo "Hello World" > /data/web_static/releases/test/index.html
# Delete the symbolic link if it already exists
if [ -L /data/web_static/current ]; then
  rm /data/web_static/current
fi
# Create symbolic link
ln -s /data/web_static/releases/test /data/web_static/current
# Set ownership of /data folder recursively to ubuntu
chown -R ubuntu:ubuntu /data
# look for
sed -i 's/listen [::]:80 default_server;'
