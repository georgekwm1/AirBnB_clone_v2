#!/usr/bin/python3
"""
web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime

env.hosts = ['34.201.161.6', '100.25.12.248']
env.user = 'ubuntu'


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

