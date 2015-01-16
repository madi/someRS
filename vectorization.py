#!/usr/bin/python

### Segmentation performed using orfeo toolbox
### The work flow is documented here: 
### http://www.orfeo-toolbox.org/CookBook/CookBooksu42.html
### Step 4 - Vectorization


from __future__ import print_function
import os
import glob
import argparse

parser = argparse.ArgumentParser(description = 'Segmentation performed \
using orfeo toolbox. The workflow is documented here: \
http://www.orfeo-toolbox.org/CookBook/CookBooksu42.html \
This module is the step 4 of the work flow and vectorizes the result. \
This operation is performed on a bunch of images \
stored in a folder. You need to indicate the input and the output folder. \
For tweacking the parameters, you need to look up into the code.')

parser.add_argument('--infolder', dest = "infolder",
help = "Folder where the original images (ortophoto) are. ")

parser.add_argument('--outfolder', dest = "outfolder",
help = "Folder where the segmented images are. \
Vector files will be written in this folder as well.")

args = parser.parse_args()

INPUT_FOLDER = args.infolder
DESTINATION_FOLDER = args.outfolder

os.chdir(INPUT_FOLDER)

# All the tif files in the folder are processed

images = []
for file in glob.glob("*.tif") :
	images.append(file.split(".")[0])


"""
The last step of the LSMS workflow consists in the vectorization of the 
segmented image into a GIS vector file. This vector file will contain one 
polygon per segment, and each of these polygons will hold additional 
attributes denoting the label of the original segment, the size of the 
segment in pixels, and the mean and variance of each band over the segment. 
The projection of the output GIS vector file will be the same as the 
projection from the input image (if input image has no projection, so 
does the output GIS file).

otbcli_LSMSVectorization -in input_image  
                         -inseg segmentation_merged.tif  
                         -out segmentation_merged.shp  
                         -tilesizex 256  
                         -tilesizey 256

This application will process the input images tile-wise to keep resources 
usage low, with the guarantee of identical results. You can set the tile 
size using the tilesizex and tilesizey parameters. However unlike the 
LSMSSegmentation application, it does not require to write any temporary 
file to disk. 
"""


for image in images :
	print(image)
	
	path_input = '"'INPUT_FOLDER + image + '.tif" '
	path_inseg = '"'DESTINATION_FOLDER + image + '_MERGED.tif" '
	path_out = '"'DESTINATION_FOLDER + image + '_SEG_VECT.shp" '

	cmdln1 = '/usr/bin/otbcli_LSMSVectorization -in ' + path_input
	cmdln2 = '-inseg ' + path_inseg
	cmdln3 = '-out ' + path_out + ' -tilesizex 256 -tilesizey 256 ' 
	
	cmdln = cmdln1 + cmdln2 + cmdln3 
	
	print(cmdln)
    
	os.system(cmdln)
	
print("Vectorization completed.")     
	
	
	
	
	
	
	
