#!/usr/bin/python3
""" do dsome packing"""
from fabric.api import env, put, run, local
from datetime import datetime
import os

env.hosts = ['54.90.41.154', '52.91.160.206']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static
    """
    try:
        # create the versions directory if it doesn't exist
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
    Distributes an archive to the web servers and sets up the symbolic links
    """
    if not os.path.exists(archive_path):
        return False
    try:
        # Upload the archive to the /tmp/
        put(archive_path, "/tmp/")
        # Uncompress
        filename = os.path.basename(archive_path)
        file_ext = os.path.splitext(filename)[0]
        folder_name = "/data/web_static/releases/" + file_ext
        run("mkdir -p {}".format(folder_name))
        run(
            "tar -xzf /tmp/{} -C {} --strip-components=1".format(
                filename, folder_name))
        # Delete the archive from server
        run("rm /tmp/{}".format(filename))
        # Delete the symbolic link
        run("sudo rm -f /data/web_static/current")
        # Create a new symbolic link
        run("sudo ln -s {} /data/web_static/current".format(folder_name))
        return True
    except Exception as exc:
        return False
