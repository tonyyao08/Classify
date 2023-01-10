import cv2
import numpy as np
import math
import shutil
from os import filenames_in

def show_image(image):
    cv2.imshow(image)
    # c = cv2.waitKey()
    # if c >= 0 : return -1
    # return 0
###################################################################################
def save_cropped_img(img_path,save_path,write,margin_ratio):
  #if write == true, it will write over the image to save_path
  og_image = cv2.imread(img_path)
  img_gray = cv2.cvtColor(og_image, cv2.COLOR_BGR2GRAY)
  
  sz = 5
  kernel = np.ones((sz,sz),np.float32)/(sz**2)
  img_gray = cv2.filter2D(img_gray,-1,kernel)

  #ret, im = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY_INV)
  ret, thresh_img = cv2.threshold(img_gray, 88, 255, cv2.THRESH_BINARY_INV)
  sz = 5
  kernel = np.ones((sz,sz),np.float32)/(sz**2)
  thresh_img = cv2.filter2D(thresh_img,-1,kernel)

  cnt, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  #res_img = cv2.drawContours(thresh_img, cnt,-1, (255,255,255), 2)
  #get the largest contour by area
  mx = 0
  largest_cnt = 0
  for c in cnt:
    area = cv2.contourArea(c)
    if mx < area:
      mx = area
      largest_cnt = c

  #x,y is the top coordinate
  x,y,w,h = cv2.boundingRect(largest_cnt)
  
  #scale the box size a bit bigger
  r = math.sqrt(w**2 + h**2)
  margin = int(r*margin_ratio)
  # print(f"r = {r} margin = {margin}")
  # print(f"x = {x} y = {y} w = {w} h = {h}")
  w = w+margin
  h = h+margin
  #1 - 2
  #3 - 4
  im_height_index = og_image.shape[0] - 1
  im_width_index = og_image.shape[1] - 1

  xabove = max(x - margin,0)
  xbelow = min(x+w,im_width_index)

  yabove = max(y - margin,0)
  ybelow = min(y+h,im_height_index)

  box_rows_cols = (yabove,ybelow, xabove,xbelow)
  #print(f"x_above = {xabove}\n x_below = {xbelow}\n y_below = {ybelow}\n y_above = {yabove}\n")
  #this actually draws a bounding box around the coin
  #res_img = cv2.rectangle(thresh_img,(xabove,yabove),(xbelow,ybelow),(255,255,255),5)
  cropped_image = og_image[yabove:ybelow, xabove:xbelow]
  #cv2_imshow(cropped_image)
  #cv2_imshow(cropped_image)
  if write:
    cv2.imwrite(save_path, cropped_image)
  return cropped_image

###################################################################################
def crop_all_images_in_folder(from_folder, to_folder,xml,margin_ratio):
#if xml == True, then copy the xml files to that folder as well
#margin ratio of about .4 is good
  file_names_list = filenames_in(from_folder,jpg = True)
  for f in file_names_list:
    img_path = f"{from_folder}{f}.jpg" 
    #copy the original image to the desired folder
    img_save_path = f"{to_folder}{f}.jpg"
    cropped = save_cropped_img(img_path,img_save_path,write = True, margin_ratio = .3)
    if xml == True:
      xml_path = f"{from_folder}{f}.xml"
      xml_save_path = f"{to_folder}{f}.xml"
      shutil.copyfile(xml_path, xml_save_path)
###################################################################################