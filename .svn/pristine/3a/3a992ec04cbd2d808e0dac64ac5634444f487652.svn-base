#pip install Pillow
from PIL import Image, ImageEnhance
directory1 = "originalimage/IMG_"
directory2 = "alteredimage/IMG_"
ending = ".jpg"
#start file number x
x= 0
# end file number y
y = 100
for i in range(x,y):
    imagename = directory1 + i + ending
    im = Image.open(imagename)

    #image brightness enhancer
    enhancer = ImageEnhance.Brightness(im)
    factor = 1 #gives original image
    im_output = enhancer.enhance(factor)
    name = directory2 + i + "original" + ending
    im_output.save(name)

    factor = 0.8 #darkens the image
    im_output = enhancer.enhance(factor)
    name = directory2 + i + "dark" + ending
    im_output.save(name)

    factor = 1.2 #brightens the image
    im_output = enhancer.enhance(factor)
    name = directory2 + i + "bright" + ending
    im_output.save(name)