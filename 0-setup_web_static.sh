#!/usr/bin/env bash
#Write a Bash script that sets up your web servers for the deployment of web_static

#Checks if nginx is installed and installs it
if ! command -v nginx &> /dev/null; then
    echo "Nginx is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install nginx -y
    echo "Nginx has been installed."
else
    echo "Nginx is already installed."
fi
#Create the folder /data/ if it doesn’t already exist
directory=("/data/" "/data/web_static/"
 "/data/web_static/releases/" "/data/web_static/shared/"
 "/data/web_static/releases/test/")

for folder in "${directory[@]}"; do
    if [ ! -d "$folder" ]; then
        echo "Creating $folder"
        sudo mkdir $folder
        echo "The $folder directory has been created."
    else
        echo "The $folder directory already exists."
    fi
    done

#Check if the symbolic link already exists, it should be deleted and recreated every time the script is ran.
link= "/data/web_static/current"
if [! -f"$link" ]; then
    echo "Creating symlink"
    ln -sfn $link $directory[4]current
else
    echo "The symlink already exists."
    echo "Removing symlink and recreating a new symlink"
    rm -r $link
    ln -sfn $link $directory[4]current

#Create a fake HTML file /data/web_static/releases/test/index.html
touch /data/web_static/releases/test/index.html
echo "<html> 
  <head> 
  </head> 
  <body> 
    Holberton School
    </body>
  </html>" | sudo tee /data/web_static/releases/test/index.html

#Update the Nginx configuration to serve the content of /data/web_static/releases/test/
#to hbnb
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /data/web_static/releases/test/;
    index index.html;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current/; 
    }
} ">>/etc/nginx/conf.d/holberton.conf

#Restart Nginx
sudo service nginx restart
