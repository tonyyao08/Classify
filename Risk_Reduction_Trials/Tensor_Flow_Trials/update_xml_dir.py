import math
import os
import re
import xml.etree.ElementTree as ET
import cv2

###################################################################################
def filenames_in(source,jpg_bool):
    #if jpg = true, just return the list of jpg files in the folder
    files = []
    #try:
    path, dirs, files = next(os.walk(source))
    #except StopIteration:
    #    pass
    lst = []
    if jpg_bool and len(files) > 0:
        for f in files:
            m = re.match(r"^([A-za-z\d]+).jpg$", f)
            if m:
                lst.append(m.group(1))
        return lst

    return files
###################################################################################
# define function to take in file, and create .txt file
def edit_xml(xml_name, new_val, param):
    # param will be either of the following: xmin, xmax, ymin, ymax, or filename, or path
    tree = ET.parse(xml_name)
    bnd_box_params = ["xmin", "xmax", "ymin", "ymax"]

    #print(tree.getroot())

    if param in bnd_box_params: # it's xmin xmax ymin ymax
        for name in tree.getroot().iterfind('object'):
            bnd_box = name.find('bndbox')
            attribute = bnd_box.find(param)
            attribute.text = str(new_val)
    else:
        # go for filename/path
        root = tree.getroot()
        tags = root.find(param)
        tags.text = new_val
    
    tree.write(xml_name)
###################################################################################
"""
files = filenames_in(coin_folder_path,jpg=True)
for f in files:
xml_path = main_path + f + ".xml" -> MAKE THIS ITS OWN FUNCTION AND RUN THAT


#function to edit xml files

go through files and edit the xml versions to change the path, title and bounding box

bounding box of most should be the boundary of the image but can drop it by a margin if want a smaller box

-drop the margin by .25
"""
def reduce_margins(img_path): # pass in path WITHOUT JPG EXTENSION
    
    # import jpg
    original_image = cv2.imread(img_path + ".jpg") #Get grayscale image 
    img_height,img_width = original_image.shape[:2]
    
   
    r = math.sqrt(img_height**2 + img_width**2)
    margin = int(r*.25)
    # margin is a distance scaled with the length of the hypotenuse

    xmax = margin
    xmin = img_width - margin
    ymax = img_height - margin
    ymin = margin

    # now overwrite the image's xml (same directory, same name)
    edit_xml(img_path + ".xml", xmax, "xmax")
    edit_xml(img_path + ".xml", ymax, "ymax")
    edit_xml(img_path + ".xml", xmin, "xmin")
    edit_xml(img_path + ".xml", ymin, "ymin")
###################################################################################
def mod_directory(dir_path):
    file_list = filenames_in(path, True)

    # for every file, reduce the margin
    for file in file_list:
        new_path = os.path.join(path, file)
        # call reduce_margins on each path
        reduce_margins(new_path)
###################################################################################
# Execute function
path = "../tensor_coin/test"
mod_directory(path)

    