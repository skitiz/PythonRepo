import requests
import bs4

import os
import logging
import re

# created
import fileIO

"""
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""


# logging.disable(logging.DEBUG)

# get site and input in filename
def get_site(url, filename):
    # logging.info("Inside the get_site function")
    siteData = requests.get(url)
    siteData.raise_for_status()

    site_file = open(filename, 'wb')
    for chunk in siteData.iter_content(100000):
        logging.debug("CHUNKSize: "+str(len(chunk)))
        site_file.write(chunk)
    site_file.close()
    # logging.info("Outside the get_site function")


# read the filename and output
# pic_url, prev_num, pic_num
def parse_site(filename):
    # logging.info("Inside parse_site function")
    read_d = open(filename, 'rb')
    parse_html = bs4.BeautifulSoup(read_d.read(),
                                   'html.parser')

    # get src
    try:
        find_img = parse_html.select('#comic img')[0].attrs
        img_src = find_img['src']
        logging.debug("image_url: "+img_src)
        # find the entire information
        # logging.info(find_img)

        # get previous link
        find_previous = parse_html.select('a[rel="prev"]')[0].attrs
        prev_src = find_previous['href']
        logging.debug("prev_num: "+prev_src)
        # logging.info(find_previous)

        # get Link number
        # WE might not need this
        # TODO, CHANGE THIS, it should work for 1, 2, 3, 4, etc digit nums
        linkNum = re.compile(r'/xkcd.com/(\d*)/')
        num = linkNum.search(parse_html.getText())
        # logging.debug(num.groups())
        # logging.info(len(num.groups()))
        # logging.info(num.group(0))

        # logging.info("Outside the parse_site function")
        # from num.group(1) we get the current imageNumber
        # img src is the downloadable img src of the curPage
        # prev src points to the url of the previous page
        return img_src, prev_src.strip("/"), num.group(1)
    except IndexError as e:
        logging.debug("Comic does not exist")
        return -1, -1, -1


# downloadas the comic from taking pic_url and pic_num as input
def download_comic(url, num, folder):
    # logging.info("Inside download_comic function")
    pic_name = os.path.basename(url)
    logging.info("Downloading "+pic_name)

    # WE get the pic data from here
    pic_data = requests.get('https:'+url)
    pic_data.raise_for_status()

    # logging.info("Outside download_comic function")
    # return pic_data.content
    # we write this to the fileStream

    pic_file = open(folder+"/"+str(num)+"."+pic_name, 'wb')
    pic_file.write(pic_data.content)
    pic_file.close()


# joins xkcd.com/<prev_num>
def site_join(prevUrl):
    return "https://xkcd.com/"+prevUrl+"/"


# combines both get_site and parse_site functions are returns:
# parse_site values
def get_schema(url, filename):
    get_site(url, filename)
    return parse_site(filename)


# NOTE, USE THIS FUNCTION AT YOUR OWN RISK
def start():
    logging.info("=================PROGRAM STARTS================\n")
    url = "https://xkcd.com"
    filename = "parse.html"
    folder = "Comic"

    # make folder
    fileIO.makeFolder(folder)
    files = fileIO.getFiles(folder)
    logging.info(str(files)+"\n\n")

    # get the first site url schema
    pic_url, prev_num, pic_num = get_schema(url, filename)
    if pic_num not in files:
        download_comic(pic_url, pic_num, folder)
        # pic_data = download_comic(pic_url, pic_num)
        # w_path = folder+"/"+str(pic_num)+"."+os.path.basename(pic_url)
        # fileIO.writeData(w_path, 'wb', pic_data)
    else:
        logging.info("Not Downloaded "+str(pic_num))
    logging.info(str(pic_num)+" DONE\n")
    print(str(pic_num)+" DONE\n")

    # replace with a while loop
    # for i in range(0, 20):
    while 1:
        logging.info(str(prev_num)+" is the cur DIR")
        if(str(prev_num) in '# 0'):
            logging.critical("Downloaded ALL")
            exit(0)

        if prev_num not in files:
            # do something here
            n_url = site_join(prev_num)
            pic_url, prev_num, pic_num = get_schema(n_url, filename)
            download_comic(pic_url, pic_num, folder)
            # pic_data = download_comic(pic_url, pic_num)
            # w_path = folder+"/"+str(pic_num)+"."+os.path.basename(pic_url)
            # fileIO.writeData(w_path, 'wb', pic_data)
        else:
            # do something else here
            logging.info("Not downloading "+str(prev_num))
            pic_num = prev_num
            prev_num = str(int(prev_num)-1)
        logging.info(str(pic_num)+" DONE\n")
        print(str(pic_num)+" DONE\n")
    logging.info("ALL DONE\n\n")


# start()
