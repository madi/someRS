Segmentation with Orfeo Toolbox
===============================

What
----
This set of python scripts allows to run OTB tools over a folder.

Why
---
It's practical when you have several tiles and / or several bands to
process.

How
---
You can indicate an input folder and an output folder. The scripts will 
process all the images that are stored in the input folder. The scripts 
perform the workflow described in the OTB Cookbook at 
http://www.orfeo-toolbox.org/CookBook

To modify the parameters you should act on the code. It is recommended 
to tweak the parameters over a small subset before running the scripts

The work flow is composed of 4 steps:

1. Mean-Shift smoothing - alleviate image noise caused by sensor system 
(for very high image resolution)

2. Segmentation - will group together adjacent pixels whose range 
distance is below the ranger parameter and spatial distance  below the 
*spatialr* parameter

3. Merging small regions - filter out small segments

4. Vectorization - produce a vector file containing one polygon per 
segment, each of these polygons holding additional attributes denoting 
the label of the original segment, the size of the segment in pixels, 
and the mean and variance of each band over the segment.

The script **segmentation.py** performs steps 1 and 2. The **merging.py**
performs step 3 and finally **vectorization.py** performs the last step.

They are meant to be used via command line. To get more information on 
the usage, for example about **segmentation.py**, type in the terminal:

> python segmentation.py --help

Notes
-----

* When you type the folder, remember to put the final / character.
