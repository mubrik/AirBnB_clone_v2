#!/usr/bin/python3
""" do dsome packing"""
from fabric.api import env, put, run, local
from datetime import datetime
import os

env.hosts = ['localhost']
env.user = 'mubrik'
env.key_filename = '~/.ssh/alx'


def do_pack():
    """
    packs archive
    """
    try:
        # create
        if not os.path.exists("versions"):
            local("mkdir versions")
        # create the archive filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        print("Packing web_static to {}".format(archive_path))
        # create the archive
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as exc:
        return None


def do_deploy(archive_path):
    """
    deploys archive
    """
    archive_name = os.path.basename(archive_path).split(".")[0]
    if not os.path.exists(archive_path):
        return False

    temp_archive, = put(local_path=archive_path, remote_path="/tmp")
    folder_name = "/data/web_static/releases/{}".format(archive_name)
    r1 = run("mkdir -p {}".format(folder_name))
    r2 = run("tar -xzf {} -C {}".format(temp_archive, folder_name))
    r6 = run("rm {}".format(temp_archive))
    r3 = run("mv {}/web_static/* {}".format(folder_name, folder_name))
    r4 = run("rm -rf {}/web_static".format(folder_name))
    r5 = run("rm -r  /data/web_static/current".format(folder_name))
    r7 = run("ln -s {} /data/web_static/current".format(folder_name))

    if r1.failed and r2.failed and r3.failed and r4.failed and r5.failed \
            and r6.failed and r7.failed:
        return False
    return True
