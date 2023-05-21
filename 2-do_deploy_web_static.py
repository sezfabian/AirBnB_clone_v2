#!/usr/bin/python3
# a fabric script that creates and distributes an archive
# to your web servers, using the function deploy

from fabric.api import *
from os.path import exists
import os

# Remote servers
env.hosts = ['100.26.223.28']


def do_deploy(archive_path):
    """
    Function to deploy_distribute an archive to web servers
    """
    if not exists(archive_path):
        return False

    # Get base file name from archive
    filename = archive_path.split('/')[-1]
    filename_no_ext = filename.replace(".tgz", "")

    try:
        # Upload archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Create the folder /data/web_static/releases/<filename_no_ext>
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(filename_no_ext))

        # Uncompress the archive to the folder
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(filename, filename_no_ext))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(filename))
        run('sudo mv -f /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}'.format(filename_no_ext, filename_no_ext))
        run('sudo rm -rf /data/web_static/releases/{}/web_static'.format(filename_no_ext))
        
        # Delete symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new the symbolic link /data/web_static/current
        run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(filename_no_ext))
        run('sudo systemctl restart nginx')
        
        print('New version deployed!')
        return True
    except Exception as e:
        print(e)
        return False
