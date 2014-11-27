#!/usr/bin/python

### Segmentation performed using orfeo toolbox
### The workflow is documented here
### http://www.orfeo-toolbox.org/CookBook/CookBooksu42.html

from __future__ import print_function
import os,sys
import glob
import argparse

parser = argparse.ArgumentParser(description = 'Segmentation performed using orfeo toolbox. \
The workflow is documented here: http://www.orfeo-toolbox.org/CookBook/CookBooksu42.html')

parser.add_argument('--infolder', dest = "infolder",
help = "Folder where the images to be processed are. All the tif files in the folder will be processed.")

parser.add_argument('--outfolder', dest = "outfolder",
help = "Destination folder, where the results will be written.")

args = parser.parse_args()

INPUT_FOLDER = args.infolder
DESTINATION_FOLDER = args.outfolder

os.chdir(INPUT_FOLDER)

images = []
for file in glob.glob("*.tif") :
	images.append(file.split(".")[0])



""" The first step of the workflow is to perform Mean-Shift smoothing 
with the MeanShiftSmoothing application:

otbcli_MeanShiftSmoothing -in input_image  
                          -fout filtered_range.tif  
                          -foutpos filtered_spat.tif  
                          -ranger 30  
                          -spatialr 5  
                          -maxiter 10  
                          -modesearch 0

Note that the modesearch option should be disabled, and that the foutpos 
parameter is optional: it can be activated if you want to perform the 
segmentation based on both spatial and range modes. 
"""


for image in images :
	print(image)
	
	path_input = '"' + INPUT_FOLDER + image + '.tif" '
	path_output = '"' + DESTINATION_FOLDER + image + '_FILTERED_RANGE_010.tif" '
	path_outpos = '"' + DESTINATION_FOLDER + image + '_FILTERED_SPATIAL_010.tif" '

	cmdln1 = '/usr/bin/otbcli_MeanShiftSmoothing -in ' + path_input
	cmdln2 = '-spatialr 5 -ranger 15 -thres 0.1 -maxiter 100 -rangeramp 0 -modesearch false ' 
	cmdln3 = '-fout ' + path_output + ' -foutpos ' + path_outpos
	
	cmdln = cmdln1 + cmdln2 + cmdln3 
	
	print(cmdln)
    
	os.system(cmdln)
    
print("Filtering completed")
print("Starting LSMS Segmentation")


"""The next step is to produce an initial segmentation based on the smoothed 
images produced by the MeanShiftSmoothing application. To do so, the LSMSSegmentation 
will process them by tiles whose dimensions are defined by the tilesizex and tilesizey 
parameters, and by writing intermediate images to disk, thus keeping the memory 
consumption very low throughout the process. The segmentation will group together 
adjacent pixels whose range distance is below the ranger parameter and (optionally) 
spatial distance is below the spatialr parameter.

otbcli_LSMSSegmentation -in filtered_range.tif  
                        -inpos filtered_spatial.tif  
                        -out  segmentation.tif uint32  
                        -ranger 30  
                        -spatialr 5  
                        -minsize 0  
                        -tilesizex 256  
                        -tilesizey 256

Note that the final segmentation image may contains a very large number of segments, 
and the uint32 image type should therefore be used to ensure that there will be 
enough labels to index those segments. The minsize parameter will filter segments 
whose size in pixels is below its value, and their labels will be set to 0 (nodata).

Please note that the output segmented image may look patchy, as if there were 
tiling artifacts: this is because segments are numbered sequentially with respect 
to the order in which tiles are processed. You will see after the result of the 
vectorization step that there are no artifacts in the results.

The LSMSSegmentation application will write as many intermediate files as tiles 
needed during processing. As such, it may require twice as free disk space as 
the final size of the final image. The cleanup option (active by default) will 
clear the intermediate files during the processing as soon as they are not 
needed anymore. By default, files will be written to the current directory. 
The tmpdir option allows to specify a different directory for these intermediate files. 
"""


for image in images :
	
	print(image)
	
	path_input1 = '"' + DESTINATION_FOLDER + image + '_FILTERED_RANGE_010.tif" '
	path_input2 = '"' + DESTINATION_FOLDER + image + '_FILTERED_SPATIAL_010.tif" '
	path_output = '"' + DESTINATION_FOLDER + image + '_SEG.tif" '

	cmdln1 = '/usr/bin/otbcli_LSMSSegmentation -in ' + path_input1 + ' -inpos ' + path_input2
	cmdln2 = '-out ' + path_output + ' -ranger 30 -spatialr 5 -minsize 0 -tilesizex 256 -tilesizey 256 '

	cmdln = cmdln1 + cmdln2
    
	print(cmdln)
    
	os.system(cmdln)
    
print("Segmentation completed") 






