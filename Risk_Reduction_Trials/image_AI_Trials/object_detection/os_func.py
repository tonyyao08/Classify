#function for reading xml file and return the class from it 
from bs4 import BeautifulSoup as bs
import re
import numpy as np
import os
import shutil
from PIL import Image  
import os
import shutil

###################################################################################
def xml_to_class(filepath):
  #<name>quarter</name>
  with open(filepath, 'r') as f:
    data = f.read()

  Bs_data = bs(data, "xml")
  tagline = str(Bs_data.find('name'))
  m = re.match(r"^<name>([A-za-z\d ]+)</name>$", tagline)
  class_val = m.group(1)

  if class_val and class_val == "1 dollar":
    class_val = "dollar"

  if class_val:
    return class_val
  else:
    return "Unknown"
# xml_to_class(training_path)
###################################################################################
def filenames_in(source,jpg):
#if jpg = true, just return the list of jpg files in the folder
  path, dirs, files = next(os.walk(source))
  lst = []
  if jpg:
    for f in files:
      m = re.match(r"^([A-za-z\d]+).jpg$", f)
      if m:
        lst.append(m.group(1))
    return lst

  return files
###################################################################################
def make_folders(folder_names_list,parent_path):
  #folders = ["penny","nickel","dime","quarter","dollar","Unknown"]
  for f in folder_names_list:
    path = parent_path + f
    try:
        os.mkdir(path)
    except OSError:
        print (f"Could not create {path}")
    else:
        print ("Successfully created the directory %s " % path)
###################################################################################
def remove_all_folders(folder_path):
      shutil.rmtree(folder_path)
###################################################################################
#Reorganizing the JPGs into proper label buckets
def folder_to_label_buckets(from_folder,to_parent_folder):
  
  file_names_list = filenames_in(from_folder,jpg = True)
  
  folder = "Unknown"
  for f in file_names_list:
    img_path = f"{from_folder}{f}.jpg"
    xml_path = f"{from_folder}{f}.xml"
    try:
          img = Image.open(img_path) 
    except Exception:
          print(f"folder to label failed to place img: {i}")
    folder = xml_to_class(xml_path)  
    #print(f"img {i} goes in {folder}")
    img_save_path = f"{to_parent_folder}{folder}/{f}.jpg"
    shutil.copyfile(img_path, img_save_path)
###################################################################################