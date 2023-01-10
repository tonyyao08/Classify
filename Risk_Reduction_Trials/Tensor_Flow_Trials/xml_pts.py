# Edit points in xml file
import xml.etree.ElementTree as ET


# define function to take in file, and create .txt file
def edit_xml(xml_name, new_val, param):
    # param will be either of the following: xmin, xmax, ymin, ymax
    tree = ET.parse(xml_name)

    
    #print(tree.getroot['object'])
    for name in tree.getroot().iterfind('object'):
        bnd_box = name.find('bndbox')
        attribute = bnd_box.find(param)
        #print(new_val)
        #print(attribute.text)
        attribute.text = str(new_val)
        
    
    #    if name.attrib['search'].startswith('select ARG'):
    #        name.attrib['search'] = name.attrib['search'].replace(
    #            'select ARG', 'selected ARG')

    #k = str(7340)
    #print(k)

    tree.write(xml_name)


""" parsing directly.
tree = ET.parse('xmldocument.xml')
root = tree.getroot()
# parsing using the string.
stringroot = ET.fromstring(XMLexample_stored_in_a_string)
# printing the root.
print(root)
print(stringroot)"""



edit_xml("IMG_3395.xml", 694, "ymin")



