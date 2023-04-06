#!/usr/bin/env bash
# setup airbnb on a ubuntu 14.04 server

# install nginx
sudo apt-get update
sudo apt-get install nginx -y
# create dirs
sudo mkdir -p /data/web_static/releases/ /data/web_static/shared/ /data/web_static/releases/test/
# Set ownership of /data folder recursively to ubuntu
sudo chown -R ubuntu:ubuntu /data
# template html
echo "Hello World" > /data/web_static/releases/test/index.html
# Delete the symbolic link if it already exists
if [ -L /data/web_static/current ]; then
  rm /data/web_static/current
fi
# Create symbolic link
ln -s /data/web_static/releases/test /data/web_static/current
# backup
sudo cp /etc/nginx/sites-enabled/default /default.bak
# add location to nginx
if grep -q "location /hbnb_static {" /etc/nginx/sites-enabled/default; then
  echo "location exists"
else
  sudo sed -i "s+listen \[::\]:80.*default_server;+&\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html;\n\t\terror_page 404 /404.html;\n\t}+" /etc/nginx/sites-enabled/default
fi
# verify nginx conf
sudo nginx -t
# restart
sudo service nginx restart
