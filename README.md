# GaleForce-Jpeg-Rescue
GaleForce Jpeg Rescue (GFJR) a free tool used to extract jpegs from binary data, especially those with bad exif due to class design.

# Screenshots
# Example run
![Screenshot](/img/gfjr-example.png)

# True jpeg start
![Screenshot](/img/true-jpeg-start.png)

# Exif
![Screenshot](/img/exif-data.png)



# NOTES
Need to optimize and add generator for large files, rework the loop as it took much trial and error understanding why python produces different output for bytes such as test[x] vs test[x:y].

# How to use
Use shell/cmd and run the script python gfjr.py and follow on screen instructions. It is best at this time to put the executable or any other file in the same directory. Jpegs saved in ./jSave directory.
