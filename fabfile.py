#!/usr/bin/python3
# Fabric script that generates a .tgz archive
# from the contents of the web_static folder in AirBnB Clone repo

from os import path
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Create a tar.gz archive of the directory web_static.
    """
    timestamp = datetime.utcnow()
    filename = "versions/web_static_{}{}{}{}{}{}.tgz".format(timestamp.year,
                                                             timestamp.month,
                                                             timestamp.day,
                                                             timestamp.hour,
                                                             timestamp.minute,
                                                             timestamp.second)
    if path.isdir("versions") is False:
        if local("mkdir versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(filename)).failed is True:
        return None
    return filename
