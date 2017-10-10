import os
import logging


# Make folder if it doesnt exist
def makeFolder(folder):
    try:
        os.mkdir(folder)
    except FileExistsError:
        # Make sure logging.basicConfig is defined before calling this
        logging.debug("Folder \'"+folder+"\' already present")
        # print("Folder\'"+folder+"\' already present")


# Get files from a relative folder path
def getFiles(folder):
    # DO NOT USE os.chdir
    # logging.info(os.getcwd())
    # add to list
    files = []
    for i in os.scandir(folder):
        # logging.info(i.name)
        files.append(i.name.split('.')[0])

    return files
