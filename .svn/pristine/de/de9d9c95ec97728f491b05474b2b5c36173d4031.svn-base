from os_func import *

#if you want to delete new_dir and start over 
# dot_slash = "./"
# new_dir_path = dot_slash + "new_dir/"
# remove_all_folders(new_dir_path)

#Set Up proper directory structure
#need to be in the same folder as Coin_Images_labels
#Create One folder where everything is located
dot_slash = "./"

new_dir_path = dot_slash + "new_dir/"

#if you want to recursively delete new_dir, run: remove_all_folders(new_dir_path)
if not os.path.isdir(new_dir_path):
  os.mkdir(new_dir_path)

#remake directory structure:
base = "test"
#top_level is the folder where we will do everything
top_level = f"{new_dir_path}{base}_dir/"
#first remove all files in new_dir if there are any
if os.path.isdir(top_level):
  # delete all folders in the top_level directory
  remove_all_folders(top_level)
else:
  os.mkdir(top_level)

#create main_folders
dir_folders = [f"{base}_rot",f"{base}_cropped",f"{base}_folders"]
make_folders(dir_folders,top_level)

#create label_folders
folders = ["penny","nickel","dime","quarter","dollar","Unknown"]
label_folders_parent = f"{top_level}{base}_folders/"

make_folders(folders,label_folders_parent)