#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['34.201.161.6', '100.25.12.248']


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder
    of your AirBnB Clone repo"""
    try:
        date = datetime.now()
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz"\
                    .format(date.strftime("%Y%m%d%H%M%S"))
        result = local("tar -cvzf {} web_static".format(file_name))
        result
        return file_name
    except:
        return None
            

def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/"\
        .format(folder_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"\
        .format(file_name, folder_name))
