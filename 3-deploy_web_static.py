#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime

env.hosts = ['34.201.161.6', '100.25.12.248']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder
    of your AirBnB Clone repo"""
    local("mkdir -p versions")
    date = datetime.now()
    file_name = "versions/web_static_{}.tgz"\
                .format(date.strftime("%Y%m%d%H%M%S"))
    result = local("tar -cvzf {} web_static".format(file_name))
    if result.failed:
        return None
    return file_name

def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    file_name = archive_path.split("/")[-1]
    folder_name = file_name.split(".")[0]
    result = put(archive_path, "/tmp/")
    if result.failed:
        return False
    result = run("mkdir -p /data/web_static/releases/{}/"\
             .format(folder_name))
    if result.failed:
        return False
