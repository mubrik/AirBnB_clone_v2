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
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_root = os.path.splitext(archive_name)[0]
        releases_path = "/data/web_static/releases/{}/".format(archive_root)

        # Upload archive
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, releases_path))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))

        # Update symlink
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))

        print("New version deployed!")
        return True
    except Exception as exc:
        return False
