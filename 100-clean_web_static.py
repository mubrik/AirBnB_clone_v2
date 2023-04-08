#!/usr/bin/python3
""" do dsome packing"""
from fabric.api import env, put, run, local, cd, lcd
from datetime import datetime
import os

env.hosts = ['54.90.41.154', '52.91.160.206']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/alx'


def do_pack():
    """
    .tgz archive from the contents of the web_static
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
        # Upload archive to the /tmp/
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
        run("rm -f /data/web_static/current")
        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(folder_name))
        print("New version deployed!")
        return True
    except Exception as exc:
        return False


def deploy():
    """
    deploys
    """
    file_path = do_pack()
    if not file_path:
        return False
    return do_deploy(file_path)


def do_clean(number=0):
    """
    Deletes stuff
    """
    number = int(number)
    if not number or number == 1:
        number = 1

    with cd("/data/web_static/releases"):
        archives = run("ls -1tr").split("\n")

        for i in range(len(archives) - number):
            if archives[i].startswith("web_static_"):
                run("rm -f {}".format(archives[i]))

    archives = local("ls -1tr versions", capture=True).split("\n")
    for i in range(len(archives) - number):
        if archives[i].startswith("web_static_"):
            local("rm -f {}".format(archives[i]))


def do_cleaan(number=0):
    """
    Deletes stuff
    """
    number = int(number)
    if not number or number == 1:
        number = 1

    archives = local("ls -1tr testerss", capture=True).split("\n")
    for i in range(len(archives) - number):
        if archives[i].startswith("web_static_"):
            print(archives[i])
            """ local("rm -f {}".format(archives[i])) """
