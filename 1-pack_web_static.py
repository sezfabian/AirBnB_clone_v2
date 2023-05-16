#!/usr/bin/python3
# Fabric script that generates a .tgz archive
# from the contents of the web_static folder in AirBnB Clone repo

import os.path
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
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
