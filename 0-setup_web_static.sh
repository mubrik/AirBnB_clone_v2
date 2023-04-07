#!/usr/bin/env bash
# setup airbnb on a ubuntu 14.04 server
# install nginx
sudo apt-get update &> /dev/null
sudo apt-get install nginx -qq --force-yes &> /dev/null
# create dirs
sudo mkdir -p /data/web_static/releases/ /data/web_static/shared/ /data/web_static/releases/test/
# Set ownership of /data folder recursively to ubuntu
sudo chown -R ubuntu:ubuntu /data
# template html
echo "<html>
<head></head>
<body style='display: flex; height:100vh; width: 100vw; justify-content: center; align-items: center;'>
<div>Holberton School</div>
</body>
</html>" > /data/web_static/releases/test/index.html
# Delete the symbolic link if it already exists
if [ -L /data/web_static/current ]; then
  rm /data/web_static/current
fi
# Create symbolic link
ln -s /data/web_static/releases/test /data/web_static/current
# create backup
sudo cp /etc/nginx/sites-enabled/default /default.bak
# change root html location
sudo sed -i "s+root .*html;+root /var/www/html;+" /etc/nginx/sites-enabled/default
# add location to nginx
if grep -q "location /hbnb_static {" /etc/nginx/sites-enabled/default; then
  :
else
  sudo sed -i "s+listen.*default_server;+&\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html;\n\t\terror_page 404 /404.html;\n\t}+" /etc/nginx/sites-enabled/default
fi
# verify nginx conf
# sudo nginx -t
# restart
sudo service nginx restart > /dev/null
# test
echo $? && ls -l /data && ls -l /data/web_static && ls /data/web_static/current && echo "cating" && cat /data/web_static/current/index.html && echo "curling" && curl localhost/hbnb_static/index.html
