# adjust all attributes of an xml file, and update it
# Edit points in xml file
import xml.etree.ElementTree as ET

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


edit_xml("IMG_3395.xml", "794", "xmin")
