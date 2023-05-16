#!/usr/bin/python3
"""Creates an archive for the web_static folder"""
from fabric.api import local, task, runs_once
from datetime import datetime
from fabric.api import run, put, env, with_settings


# Remote servers
env.hosts = ['52.86.36.245', '100.25.45.160']


@runs_once
@with_settings(warn_only=True)
def do_pack():
    """Executes commands locally to create archive"""
    try:
        time = datetime.now()
        str_time = time.strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_name = "versions/web_static_{}.tgz".format(str_time)
        execute = local("tar -czvf {} web_static".format(archive_name))
        return archive_name
    except Exception:
        return None


@with_settings(warn_only=True)
def do_deploy(archive_path):
    """ships and unpacks the .tgv file"""
    file_name = archive_path.split('/')[-1]
    folder_extract = file_name.replace(".tgz", "")

    put(archive_path, '/tmp')
    run('mkdir -p /data/web_static/releases/{}'.format(folder_extract))
    run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(file_name, folder_extract))

    run('rm /tmp/{}'.format(file_name))
    run('mv -f /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}'.format(folder_extract, folder_extract))
    run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_extract))
    run('rm -rf /data/web_static/current')
    run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_extract))


@task
def deploy():
    """_summary_

    Returns:
        _type_: _description_
    """
    archive_name = do_pack()

    if archive_name == None:
        return False
    else:
        do_deploy(archive_name)
