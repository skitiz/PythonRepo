import sys
import logging

import xkcdDownloader as downloader
import fileIO


# Init the folder and return the filename present in folder
def initFolders(folder):
    fileIO.makeFolder(folder)
    downloaded = fileIO.getFiles(folder)
    logging.info(str(downloaded)+"\n\n")
    return downloaded


# check to see command line args and return arglist
def cli_args():
    if len(sys.argv) <= 1:
        # this is for people who cannot use command line and run from there
        get_commands = input("Do you want to input commands? y/n\n> ")
        # for some reason get_commands.lower() doesnt work with is
        # no match happens
        if get_commands.lower() in 'y':
            commands = input("ex. -s 100 -e 90\ninput> ")
            command_list = commands.split(" ")
            # print(command_list)
            # this was the problem, logging.basicConfig
            # logging.debug(command_list)
            for i in command_list:
                sys.argv.append(i)
    return sys.argv  # We get list from here


# logging to file or console, even disable is possible
def output_options(arglist):
    if '-vf' in arglist:
        print("Log to file active")
        f_name = arglist[arglist.index('-vf')+1]
        logging.basicConfig(filename=f_name,
                            level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
    # elif '-v' in sys.argv or len(sys.argv) <= 1:
    else:
        # automatically start the logs
        print("Log to console active")
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')

    if '-nl' in arglist:
        print("Logging disabled")
        logging.disable(logging.CRITICAL)


# set -s and -e from here
def args_options(arglist, url, filename, folder, downloaded):
    # get start_num. FIRST
    # if -s is specified we dont need to init
    # sys.argv
    if '-s' in arglist:
        pic_num = arglist[arglist.index('-s')+1]
        # downloader.site_join(start_num)
        # pic_url, prev_num, pic_num = downloader.get_schema(start_num, filename)
        # downloader.download_comic(pic_url, pic_num, folder)
    else:
        # start from starting, FIRST
        pic_url, prev_num, pic_num = downloader.get_schema(url, filename)
        if pic_url is not -1:
            if pic_num not in downloaded:
                downloader.download_comic(pic_url, pic_num, folder)
            else:
                logging.info("Not Downloaded "+str(pic_num))
        else:
            logging.debug("Comic does not exist")
    # NOTE, from here we get pic_num properly so use that ahead
    pic_num = int(pic_num)

    if '-e' in arglist:
        end_num = arglist[arglist.index('-e')+1]
    else:
        # end at 1;
        end_num = '1'
        pass
    # NOTE, from here we get end_num properly so use that
    end_num = int(end_num)-1  # -1 so that we go till that number

    return [pic_num, end_num]  # WE return start and stop num


# download all the files now
def run(r, filename, folder, downloaded):
    pic_num, end_num = r
    for pnum in range(pic_num, end_num, -1):
        # check for pic_num
        snum = str(pnum)
        if snum not in downloaded:
            logging.info("Downloading "+snum)
            url = downloader.site_join(snum)
            pic_url, prev_num, pic_num = downloader.get_schema(url, filename)
            if pic_url is not -1:
                downloader.download_comic(pic_url, pic_num, folder)
                logging.info("Finished download "+snum+"\n")
            else:
                print("Comic does not exist")
                continue
            # NOTE, We do not use prev_num since we are manually checking
        else:
            logging.info("Already downloaded "+snum)
        # if there in files then do not download
        # else download


# Code runs here
def main():
    # Main function starts here
    url = "https://xkcd.com"
    filename = "parse.html"
    folder = "Comic"

    # Get args
    arglist = cli_args()
    # debugging
    # print("args: "+str(arglist))

    # set logging
    output_options(arglist)
    # NOTE, We can use logging now

    # downloaded files
    downloaded = initFolders(folder)

    # set range
    range = args_options(arglist, url, filename, folder, downloaded)
    logging.info(range)

    # run
    run(range, filename, folder, downloaded)


# start program
main()
