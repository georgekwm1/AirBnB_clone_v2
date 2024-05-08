#!/usr/bin/env bash
#Write a Bash script that sets up your web servers for the deployment of web_static

#Checks if nginx is installed and installs it
sudo apt-get update
sudo apt-get -y install nginx 
echo "Nginx has been installed."

#Create the folder /data/ if it doesn’t already exist
directory=("/data/" "/data/web_static/"
 "/data/web_static/releases/" "/data/web_static/shared/"
 "/data/web_static/releases/test/")

for folder in "${directory[@]}"; do
    if [ ! -d "$folder" ]; then
        echo "Creating $folder"
        sudo mkdir "$folder"
        echo "The "$folder" directory has been created."

    else
        echo "The "$folder" directory already exists."
    fi
    done


#Check if the symbolic link already exists, it should be deleted and recreated every time the script is ran.

sudo ln -sf "${directory[4]}" "${directory[1]}"current

#Create a fake HTML file /data/webstatic/releases/test/index.html
sudo echo "<html> 
  <head> 
  </head> 
  <body> 
    Holberton School
    </body>
  </html>" | sudo tee /data/web_static/releases/test/index.html

#Change owner of directory
echo "Changing owner to ubuntu"
sudo chown -R ubuntu:ubuntu "${directory[0]}"
echo "Owner changed to ubuntu"

sudo echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /var/www/html;
    index index.html;
    server_name ;
    location /hbnb_static {
        alias /data/web_static/current/; 
    }
} " | sudo tee /etc/nginx/sites_available/default

sudo ln -sf /etc/nginx/sites_available/default /etc/nginx/sites-enabled/default

sudo service nginx restart
