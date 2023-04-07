#!/usr/bin/python3
""" do dsome packing"""
from fabric.api import env, put, run
import os

env.hosts = ['54.90.41.154', '52.91.160.206']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and sets up the symbolic links
    """
    if not os.path.exists(archive_path):
        return False
    try:
        print("Executing task 'do_deploy'")
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
