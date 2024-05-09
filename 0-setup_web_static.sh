#!/usr/bin/env bash
# Write a Bash script that sets up your web servers for the deployment of web_static

# Check if nginx is installed and install it if not
if ! command -v nginx &> /dev/null; then
    echo "Nginx is not installed. Installing..."
    sudo apt-get update || { echo "Failed to update packages."; exit 1; }
    sudo apt-get install nginx -y || { echo "Failed to install nginx."; exit 1; }
    echo "Nginx has been installed."
else
    echo "Nginx is already installed."
fi

# Create the necessary directories if they don't already exist
directories=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/")

for directory in "${directories[@]}"; do
    if [ ! -d "$directory" ]; then
        echo "Creating $directory"
        sudo mkdir -p "$directory" || { echo "Failed to create directory $directory"; exit 1; }
        echo "The $directory directory has been created."
    else
        echo "The $directory directory already exists."
    fi
done

# Check if the symbolic link already exists; if so, remove it
if [ -e "${directories[1]}current" ]; then
    echo "Removing existing symlink"
    sudo rm -f "${directories[1]}current" || { echo "Failed to remove symlink"; exit 1; }
fi

# Create a new symbolic link
echo "Creating symlink"
sudo ln -s "${directories[4]}" "${directories[1]}current" || { echo "Failed to create symlink"; exit 1; }

# Create a fake HTML file /data/web_static/releases/test/index.html
html_file="/data/web_static/releases/test/index.html"
if [ ! -f "$html_file" ]; then
    echo "<html>
  <head>
  </head>
  <body>
    Holberton School
    </body>
  </html>" | sudo tee "$html_file" || { echo "Failed to create HTML file"; exit 1; }
fi

# Update the Nginx configuration to serve the content of /data/web_static/releases/test/ to hbnb
nginx_config="/etc/nginx/sites-available/default"
if [ ! -f "$nginx_config" ]; then
    echo "Creating $nginx_config"
    sudo mkdir -p /etc/nginx/sites-available/ || { echo "Failed to create directory /etc/nginx/sites-available/"; exit 1; }
    sudo touch "$nginx_config" || { echo "Failed to create $nginx_config"; exit 1; }
else
    echo "$nginx_config already exists"
fi

nginx_config_content="server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$HOSTNAME;
    root /data/web_static/releases/test/;
    index index.html;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current/;
    }
}"
echo "$nginx_config_content" | sudo tee "$nginx_config" || { echo "Failed to write to $nginx_config"; exit 1; }

# Enable the site by creating a symlink in sites-enabled
sites_enabled="/etc/nginx/sites-enabled/default"
if [ ! -L "$sites_enabled" ]; then
    echo "Creating symlink in /etc/nginx/sites-enabled/"
    sudo ln -sf "$nginx_config" "$sites_enabled" || { echo "Failed to create symlink"; exit 1; }
else
    echo "Symlink already exists in /etc/nginx/sites-enabled/"
fi

# Change owner of directory
echo "Changing owner to ubuntu"
sudo chown -R ubuntu:ubuntu "${directories[0]}" || { echo "Failed to change owner to ubuntu"; exit 1; }
echo "Owner changed to ubuntu"

# Check nginx configuration syntax
echo "Checking Nginx configuration syntax"
sudo nginx -t || { echo "Nginx configuration syntax test failed"; exit 1; }

# Restart Nginx
echo "Restarting Nginx"
sudo service nginx restart || { echo "Failed to restart Nginx"; exit 1; }

echo "Setup completed successfully."

