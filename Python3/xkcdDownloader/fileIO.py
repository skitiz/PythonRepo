import os
import logging


def makeFolder(folder):
    try:
        os.mkdir(folder)
    except FileExistsError:
        logging.debug("Folder \'"+folder+"\' already present")


def getFiles(folder):
    # DO NOT USE os.chdir
    # logging.info(os.getcwd())
    # add to list
    files = []
    for i in os.scandir(folder):
        # logging.info(i.name)
        files.append(i.name.split('.')[0])

    return files
