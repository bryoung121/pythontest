#trim the svg with imagemagick command line utitity
#find the correct image location in the pdf
#replace the pdf jpg with the svg and make sure the dimensions are correct


import sys
import os
import subprocess

from PIL import Image


def cleansvg(new_image):
    print 'Trimming the image so that it will fit on the pdf.'
    print subprocess.check_output(['convert',new_image, '-trim', '+repage','Documents/balfourtest/newimage.png'])
    return "Documents/balfourtest/newimage.png"

# Include the \n to ensure extact match and avoid partials from 111, 211...
OBJECT_ID = "\n9 0 obj"
def addimage(new_image, newpdf):
    #image = Image.open(new_image)
    print "trying to add the image to the pdf"
    print subprocess.check_output(['convert',newpdf, new_image, newpdf])

def replace_image(filepath, new_image):
    f = open(filepath, "r")
    contents = f.read()
    f.close()

    image = Image.open(new_image)
    width, height = image.size
    length = os.path.getsize(new_image)

    start = contents.find(OBJECT_ID)
    stream = contents.find("stream", start)
    image_beginning = stream + 7

    # Process the metadata and update with new image's details
    meta = contents[start: image_beginning]
    meta = meta.split("\n")
    new_meta = []
    for item in meta:
        if "/Width" in item:
            new_meta.append("/Width {0}".format(width))
        elif "/Height" in item:
            new_meta.append("/Height {0}".format(height))
        elif "/Length" in item:
            new_meta.append("/Length {0}".format(length))
        else:
            new_meta.append(item)
    new_meta = "\n".join(new_meta)
    # Find the end location
    image_end = contents.find("endstream", stream) - 1

    # read the image
    f = open(new_image, "r")
    new_image_data = f.read()
    f.close()

    # recreate the PDF file with the new_sign
    with open(filepath, "wb") as f:
        f.write(contents[:start])
        f.write("\n")
        f.write(new_meta)
        f.write(new_image_data)
        f.write(contents[image_end:])


if __name__ == "__main__":
    if len(sys.argv) == 3:
        myimage = cleansvg(sys.argv[2])
        #openimage("Documents/balfourtest/newimage.png")
        addimage(sys.argv[2], sys.argv[1])
        #replace_image(sys.argv[1], myimage)
    else:
        print("Usage: python process.py <pdfile> <new_image>")
