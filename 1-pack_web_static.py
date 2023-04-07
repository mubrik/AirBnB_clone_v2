#!/usr/bin/python3
""" do dsome packing"""
from fabric.api import local
from datetime import datetime
import os


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
