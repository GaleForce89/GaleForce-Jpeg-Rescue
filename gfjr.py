#!/usr/bin/env python3
"""
Project: GaleForce Jpeg Rescue AKA GFJR
By: Galeforce
GITHUB: github.com/galeforce89

Description: 
Attempt to recover jpegs embedded in a binary file with bad exif. 

Shout out to the fam, I hope this helps.
"""

#built in libraries
import binascii  # convert hex
import datetime as DT
import os
from pathlib import Path  # deals with paths between operating systems
import sys

# 3rd party
# N/A


def main():
    '''main function, set variables and get file name
    '''


    # get file from user
    fileName = getFile("Name of file to dump (may require full path): ")

    # get filesize in bytes
    fileSize = os.path.getsize(fileName)

    # read in whole file
    try:
        with open(fileName, "rb") as f:
            rescue = f.read()
    except IOError:  # catch any random errors
        print("File IO error, exiting...")
        sys.exit(1)

    # filesize and len should match so controlled loop
    x = 0
    imgFound = 0
    while x < fileSize:  # NOTE-> reading in nibbles it seems so 4 bits
        if rescue[x:x+1] == b'\xFF':  # if we hit F check if FFD8FF matches
            if rescue[x:x+3] == b'\xFF\xD8\xFF':  # if match try to extract jpeg

                # Return X so we don't repeat
                x = jRescue(rescue, x, imgFound, fileSize)
                imgFound += 1  # update images

        x += 1  # iterate our loop

    # need to fix image paths etc..
    print("\nDone, images saved in jSave dir.\nFound: {} image(s).".format(imgFound))


# attempt jpeg rescue
def jRescue(rescue, x, imgFound, fileSize):
    # local vars
    y = x + 1  # set y to x
    while y < fileSize:  # could of set as true, but did not want a random loop situation so fileSize
        # if F check if its the bad data and restart or determine if trailer
        if rescue[y:y+1] == b'\xFF':
            #remove this statement to recover those with valid exif.
            if rescue[y:y+3] == b'\xFF\xD8\xFF':  # new sig found, update x and repeat
                x = y
                # repeat after strping exif
                jRescue(rescue, x, imgFound, fileSize)
            elif rescue[y:y+2] == b'\xFF\xD9':  # trailer found, save jpeg img update x
                x = jSave(rescue, x, y+2, imgFound)  # save
                return x  # return new x
        y += 1

    return y  # fallback

# save jpeg if found, return updated x
def jSave(rescue, x, y, imgFound):
    saveFile = Path(os.getcwd()+"/jSave/" + str(imgFound) + ".jpeg")

    dirCheck = os.path.exists(Path(os.getcwd() + "/jSave"))

    if not dirCheck:
        os.mkdir(Path(os.getcwd() + "/jSave"))

    with open(saveFile, "wb") as jpeg:
        jpeg.write(rescue[x:y])
    return y


# able to concat integers
# NOTE->Not needed but keeping for future
def concat(a, b, c=None):
    if c:
        return int(f"{a}{b}{c}")
    return int(f"{a}{b}")


# verify provided file
def getFile(text):
    '''
    Get file to be analyzed
    '''
    fileName = input(text)

    while True:  # check file
        fileName = Path(fileName)  # set file to work for current os
        if fileName.is_file():  # return a valid file
            return fileName
        else:
            print("You entered: ", fileName, " which does not seem to exist")
            fileName = input("enter new path or 0 to exit: ")

            if fileName == "0":
                sys.exit(0)


# call main at the end
if __name__ == '__main__':
    main()
