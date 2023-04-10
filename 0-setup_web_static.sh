#!/usr/bin/env bash
# setup airbnb on a ubuntu 14.04 server
if ! command -v nginx &> /dev/null; then
  sudo apt-get update &> /dev/null
  sudo apt-get install nginx -y &> /dev/null
fi
# create dirs
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
# template html
echo "<html>
<head></head>
<body style='display: flex; height:100vh; width: 100vw; justify-content: center; align-items: center;'>
<div>Holberton School</div>
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html &>/dev/null
# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# Set ownership of /data folder recursively to ubuntu
sudo chown -R ubuntu:ubuntu /data/
if grep -q "location /hbnb_static {" /etc/nginx/sites-enabled/default; then
  :
else
  sudo sed -i "s+listen.*default_server;+&\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html;\n\t\terror_page 404 /404.html;\n\t}+" /etc/nginx/sites-enabled/default
fi
# Restart Nginx
sudo service nginx restart &>/dev/null
# test
