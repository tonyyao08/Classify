from cropping_func  import *
from os_func import *
from rotation_func import *

#need to be in the same folder as Coin_Images_labels
# use Coin_Images_Labels/test/train => 
#   => test_cropped/train_cropped
#     => test_rot/train_rot  
#       => test_folders/train_folders

base = "test"

dot_slash = "./"

new_dir_path = dot_slash + "new_dir/"
#all the files will go into the top_level folder = 
top_level = f"{new_dir_path}{base}_dir/"
#the source of the pics along with xml files 
pics_source = f"{dot_slash}Coin_Images_Labels/{base}/"

#pics source => crop => rotate/create more => and then bucket

#---------   Crop Images   ---------------#
from_folder = f"{pics_source}"
to_cropped_folder = f"{top_level}{base}_cropped/"

print(f"Cropping Images in {from_folder} and placing them in {to_cropped_folder}\n")
#xml = true means that it will copy over the xml files as well
#margin_ratio = margin of how big the box will be 
# as a ratio of the bounding box's hypotenuse
crop_all_images_in_folder(from_folder, to_cropped_folder,xml = True,margin_ratio = .4)

#---------   Rotate  Images   ---------------#
from_folder = to_cropped_folder
to_rot_folder = f"{top_level}{base}_rot/"

print(f"Rotating Images in {from_folder} and placing them in {to_rot_folder}\n")
#xml = true means that it will copy the xml files over as well
rot_images(10, from_folder, to_rot_folder,xml=True)

#---------   Bucket Images   ---------------#
#parent folder has label folders in it
from_folder = to_rot_folder
to_folder = f"{top_level}{base}_folders/"
print(f"Bucketting Images in {from_folder} and placing them in {to_folder}")
folder_to_label_buckets(from_folder,to_folder)

