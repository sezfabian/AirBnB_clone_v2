#!/usr/bin/python3
"""Pack web static module"""
from datetime import datetime
from os import path
from fabric import api


def do_pack():
    """
    Generates a .tgz archive from the contents of
    the web_static folder of AirBnB Clone repo
    """
    if not path.isdir("versions"):
        api.local("mkdir versions")
    date = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date)
    result = api.local("tar -czvf {} web_static".format(file_name))
    if result.failed:
        return None
    return file_name
