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
NGINX_CONFIG=\
"
server {
 	listen	80;
  server_name rubbish rubbish;
	location /hbnb_static/ {
		alias /data/web_static/current/;
		autoindex off;
	}
}
"
echo -e "$NGINX_CONFIG" > /etc/nginx/sites-enabled/default
# verify nginx conf
# Restart Nginx
sudo service nginx restart &>/dev/null
# test
# echo $? && ls -l /data && ls -l /data/web_static && ls /data/web_static/current && echo "cating" && cat /data/web_static/current/index.html && echo "curling" && curl localhost/hbnb_static/index.html
