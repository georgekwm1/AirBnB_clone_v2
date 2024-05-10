#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime

# env.hosts = ['34.74.176.159', '3.89.210.18']


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
