import numpy as np
from PIL import Image 
import shutil
import numpy as np
from random import seed
from random import random
from os import filenames_in

def rotated(A,angle):
#rotates the point A by the degrees given
#angle = 0-360
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    A = [0,1]
    rotated_A = A @ R.T
    return np.around(rotated_A)

###################################################################################
#go through all image files in a folder 
#if xml is true then it will also copy the xml files wherever the jpg files are
#going
def rot_images(num_times, from_folder, to_folder,xml):
  file_names_list = filenames_in(from_folder,jpg = True)
  new_file_count = 0

  for f in file_names_list:
    img_path = f"{from_folder}{f}.jpg"
    xml_path = f"{from_folder}{f}.xml"  
    try:
          img = Image.open(img_path) 
    except Exception:
          print(f"failed to open img: {i}")

    #copy the original image to the desired folder
    img_save_path = f"{to_folder}IMG_{new_file_count}.jpg"
    shutil.copyfile(img_path, img_save_path)
    if xml:
      #also copy the xml file cooresponding with this image
      xml_save_path = f"{to_folder}IMG_{new_file_count}.xml"
      shutil.copyfile(xml_path,xml_save_path)
    #added 2 new files
    new_file_count += 1

    angles = np.linspace(0,300,num_times)
    angles = np.around(angles)
    #build the angle buckets
    seed()
    for i in range(len(angles)):
      r = round(10*random())
      angles[i] += r

    for x in angles:
      rot_img = img.rotate(x)
      img_save_path = f"{to_folder}IMG_{new_file_count}.jpg"
      rot_img.save(img_save_path)
      if xml:
        #also copy the xml file cooresponding with this image
        xml_save_path = f"{to_folder}IMG_{new_file_count}.xml"
        shutil.copyfile(xml_path, xml_save_path)
        #added 2 new files, jpg and xml
      new_file_count += 1
###################################################################################