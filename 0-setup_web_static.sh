#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static
sudo apt-get update -y
sudo apt-get install nginx -y
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
echo -e "<html>\n <head>\n </head>\n <body>\n  Holberton School\n </body>\n</html>" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data
hbnb_location="\n\tlocation /hbnb_static {\n\
\t\t# hbnb web_static\n\
\t\talias /data/web_static/current;\n\
\t\tindex index.html;\n\
\t}\n"
sudo sed -i "53i\\$hbnb_location" /etc/nginx/sites-available/default

sudo service nginx restart
