#!/usr/bin/env bash
# setup airbnb on a ubuntu 14.04 server
# install nginx
sudo apt-get update &> /dev/null
sudo apt-get install nginx -y &> /dev/null
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
#!/usr/bin/env bash
# installs Nginx if not already installed
# creates several directories as well as a sym link

# Install Nginx if not already installed
if [ ! -x "$(command -v nginx)" ]; then
    sudo service "$(sudo lsof -i :80 | grep LISTEN | awk '{print $1}' | head -n 1)" stop &/dev/null;
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create required directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file to test Nginx
echo "<html><head><title>Test HTML File</title></head><body><h1>This is a test.</h1></body></html>" | sudo tee /data/web_static/releases/test/index.html &>/dev/null

# Create symbolic link to the test release
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership to ubuntu user and group
sudo chown -hR ubuntu:ubuntu /data/

# Configure Nginx to serve content from the current release
sudo sed -i '0,/^\(\s*\)server_name\s*.*$/s//\1server_name cheezaram.tech www.cheezaram.tech;/' /etc/nginx/sites-available/default
sudo sed -i '0,/^\(\s*\)server_name cheezaram.tech www.cheezaram.tech;$/s//&\n\n\1location \/hbnb_static {\n\1\1alias \/data\/web_static\/current\/;\n\1\1autoindex off;\n\1}/' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx stop &>/dev/null
sudo service nginx start &>/dev/null
# test
# echo $? && ls -l /data && ls -l /data/web_static && ls /data/web_static/current && echo "cating" && cat /data/web_static/current/index.html && echo "curling" && curl localhost/hbnb_static/index.html
