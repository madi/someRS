#!/usr/bin/python

### Segmentation performed using orfeo toolbox
### The work flow is documented here: 
### http://www.orfeo-toolbox.org/CookBook/CookBooksu42.html
### Step 3 - (Optional) Merging small regions

from __future__ import print_function
import os
import glob
import argparse


parser = argparse.ArgumentParser(description = 'Segmentation performed \
using orfeo toolbox. The workflow is documented here: \
http://www.orfeo-toolbox.org/CookBook/CookBooksu42.html \
This module is the step 3 of the work flow and performs Mean-Shift \
smoothing and consequent segmentation on a bunch of images \
stored in a folder. You need to indicate the input and the output folder. \
For tweacking the parameters, you need to look up into the code.')

parser.add_argument('--infolder', dest = "infolder",
help = "Folder where the original images (ortophoto) are. ")

parser.add_argument('--outfolder', dest = "outfolder",
help = "Folder where the segmented images are. \
Merged files will be written in this folder as well.")

args = parser.parse_args()

INPUT_FOLDER = args.infolder
DESTINATION_FOLDER = args.outfolder

os.chdir(INPUT_FOLDER)

# All the tif files in the folder are processed

images = []
for file in glob.glob("*.tif") :
	images.append(file.split(".")[0])
	
"""
The LSMSSegmentation application allows to filter out small segments. 
In the output segmented image, those segments will be removed and replaced 
by the background label (0). Another solution to deal with the small regions 
is to merge them with the closest big enough adjacent region in terms of 
radiometry. This is handled by the LSMSSmallRegionsMerging application, 
which will output a segmented image where small regions have been merged. 
Again, the uint32 image type is advised for this output image.

otbcli_LSMSSmallRegionsMerging -in filtered_range.tif  
                               -inseg segementation.tif  
                               -out segmentation_merged.tif uint32  
                               -minsize 10  
                               -tilesizex 256  
                               -tilesizey 256

The minsize parameter allows to specify the threshold on the size of the 
regions to be merged. Like the LSMSSegmentation application, this application 
will process the input images tile-wise to keep resources usage low, with 
the guarantee of identical results. You can set the tile size using the 
tilesizex and tilesizey parameters. However unlike the LSMSSegmentation 
application, it does not require to write any temporary file to disk. 
"""


for image in images :
	
	print(image)
	
	path_input = '"' + DESTINATION_FOLDER + image + '_FILTERED_RANGE_010.tif" '
	path_inseg = '"' + DESTINATION_FOLDER + image + '_SEG.tif" '
	path_output = '"' + DESTINATION_FOLDER + image + '_MERGED.tif" '

	cmdln1 = '/usr/bin/otbcli_LSMSSmallRegionsMerging -in ' + path_input + ' -inseg ' + path_inseg
	cmdln2 = '-out ' + path_output + ' uint32 -minsize 10 -tilesizex 256 -tilesizey 256 '


	cmdln = cmdln1 + cmdln2
    
	print(cmdln)
    
	os.system(cmdln)
    
print("Merge completed.") 

