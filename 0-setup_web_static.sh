#!/usr/bin/env bash
# setup airbnb on a ubuntu 14.04 server
if ! command -v nginx &> /dev/null; then
  sudo apt-get update &> /dev/null
  sudo apt-get install nginx -y &> /dev/null
fi
# create dirs
sudo mkdir -p /data/web_static/releases/ /data/web_static/shared/ /data/web_static/releases/test/
# Set ownership of /data folder recursively to ubuntu
sudo chown -hR ubuntu:ubuntu /data/
# template html
echo "<html><head><title>Test HTML File</title></head><body><h1>This is a test.</h1></body></html>" | sudo tee /data/web_static/releases/test/index.html &>/dev/null
# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# change root html location
# Configure Nginx to serve content from the current release
sudo sed -i '0,/^\(\s*\)server_name\s*.*$/s//\1server_name mb.tech www.mb.tech;/' /etc/nginx/sites-available/default
sudo sed -i '0,/^\(\s*\)server_name mb.tech www.mb.tech;$/s//&\n\n\1location \/hbnb_static {\n\1\1alias \/data\/web_static\/current\/;\n\1\1autoindex off;\n\1}/' /etc/nginx/sites-available/default
# verify nginx conf
# Restart Nginx
sudo service nginx stop &>/dev/null
sudo service nginx start &>/dev/null
