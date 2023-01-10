import sys
from capture_v3 import *
from os.path import exists

# This file is the command line interpreter. It is the file that will actually be executed from the user.
# It is necessary to look at the README.txt to run the program properly.

n = len(sys.argv)
user_file_path = ""
want_scaling = ""
scaling_input = ""
print()

if n == 1:
    # print(n)
    # ******call function******
    bucket = "mycoins"
    in_bucket_prefix = ""
    path_for_local_imgs = "/home/pi/Desktop/local_images/"
    num_objects = 5
    projID = "83e8e92a-c299-437c-aaca-57225a737afe"
    train = False

    mode = input('Is this for training? (True/False): ')
    if mode == 'T' or mode == 't' or mode == 'true' or mode == 'True' or mode == 'TRUE':
        train = True

    proj_input = input("What is the id of this project?: ")
    if proj_input:
        projID = proj_input.strip()
#     tempbucket = input('What bucket would you like?(press enter for default): ')
#     if tempbucket != '':
#         bucket = tempbucket
#
#     tempinbucket = input('What in_bucket_prefix would you like?(press enter for default): ')
#     if tempbucket != '':
#         in_bucket_prefix = tempinbucket
#
#     temppath = input('What path would you like for local images?(press enter for default): ')
#     if temppath != '':
#         path_for_local_imgs = temppath

    tempnum = input(
        'What number of object would you like?(press enter for default=4): ')
    if tempnum != '':
        num_objects = tempnum

    # print(bucket+in_bucket_prefix+path_for_local_imgs+num_objects)
    conveyor_belt(bucket, in_bucket_prefix, num_objects,
                  path_for_local_imgs, train, projID)
    # ******call function******
else:
    print("Something looks wrong.")
    print("Please make sure to look at the README.txt to properly use this application.")


# sample input:
# ScrimmageData/01.txt
