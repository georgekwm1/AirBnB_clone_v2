#!/usr/bin/python3
"""
A Fabric script that distributes an archive to your web servers
using the function do_deploy.
"""
from fabric.api import *
from fabric.contrib.files import exists
from datetime import datetime

env.hosts = ['34.201.161.6', '100.25.12.248']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

@task
def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not exists(archive_path):
        print("Archive path does not exist.")
        return False
    try:
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))

        # Create the release folder on the web server
        run("mkdir -p /data/web_static/releases/{}".format(folder_name))

        # Uncompress the archive to the release folder
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(file_name, folder_name))

        # Remove the archive from the /tmp/ directory
        run("rm /tmp/{}".format(file_name))

        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{} /data/web_static/current".format(folder_name))
        
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False

