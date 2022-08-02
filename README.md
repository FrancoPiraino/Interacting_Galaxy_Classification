

# Interacting_Galaxy_Classification



########################### Galaxy Classification Code #############################
		
This code is used to classify galaxies and check if they have some interaction,
through the visualization of cut images from Legacy Survey, Deep Mosaic FITS files
from DECam in r and g band and available rgb images from a photometric catalogue.

To run the code you need a csv table with a column for the ID of each object and three folders 
which contain the cuts to classify them

The folders that you should have are:
	
	``Legacy_cuts``: Here we should have a catalogue of images from Legacy Survey
	``DECam_cuts`` : Here we should have some cutout fits from Deep Mosaic FITS DECam 
	                 in two bands (r,g). 
	``RGB_cuts``   : Here we should have rgb images from the photometric
			  catalogue.
			
The code is edited to read the images from those folders such that the name of the cuts 
should contain the ID value. You decide how you call your files but in this case, they are 
called in the following way:

``Legacy_cuts`` --> ``L+ID+.jpg``
``DECam_cuts`` --> ``ID+_rband.fits``
``Legacy_cuts`` --> ``ID+_gband.fits``
``RGB_cuts`` --> ``ID+_rgb_jar_3.png`` 

So, into the code, you need to define how you call from the folders.
In this repository we only have a small sample to test the code.
	
The code is written in python3, so maybe you should run it using ``python3 Galaxy_classification.py``

The code has the option to put a seed to classify in a random way.

Then, it will ask us if we want to start from the beginning or if we want to start where
 we stayed, in the case of the code stopping or failing during our classification:
..
	Type the number of the options:
	1: Are you running for the first time? or do you want to classify again?
	2: Continue where you stayed!
	Type: |

Just in case, if our classification is complete and we type ``2``, the
code will ask us if we want to start again or not:
..
	Your classification is complete. Do you want to start again? ('y':yes, 'n':no):

In that case, if you type ``n`` the code won't do anything. 

After that, the code will ask us for the classification while a figure is plotted with
four images from the folders (``Legacy survey``, ``r band``, ``g band`` & ``rgb image``):

..
	Classification N° #
	ID for this object:  #
	Do you see any interaction? Type one of the following options and press <ENTER>
	If you want comment sth, press <space> and write -> 'j ring galaxy', 'j unwinding', ... etc
	If you need to zoom, you can type 'i' to Zoom In or 'o' to Zoom Out 
	'j': jellyfish
	'm': merger
	'pm': post merger
	'jm': jellyfish+merger
	's': star
	'n': no interaction 
	'b': broken images
	Type: |
	
The number of the classification that we are performing is showed by screen and
also the ID of the object.

If you see some interaction, the options to choose are the following:
	
	``j`` : For jellyfish galaxies. Any galaxy with ram-pressure stripping effect and that
	        seems to have some evidence of gas remotion without evidence of mergers 
	        or tidal interaction. We can include unwinding galaxies.
	
	``m`` : When two or more galaxies are interacting gravitationally. Evidence of bridges, 
	        or tidal interactions. We can include pre-merger or mergers where 
	        we can distinguish both galaxies. 
	
	``pm``: Any galaxy that looked to have been involved in a past gravitational
	        interaction (merger etc.). It 's difficult to see the progenitors.
	        Galaxies with a big shell can be considered as post-mergers galaxies.
	      
	``jm``: Similar to 'j' but also they seem to be interacting with other galaxies, with 
	        evidence of bridges and tidal interactions.	        
	
	``s`` : For object type stars, very bright points.
	
	``n`` : You cannot see a galaxy interacting. Galaxies without any particular feature,
	        and normal or symmetric galaxies.
	        
	``b`` : The four images are broken


Adding a space after to type an option, if you want, you can write some comment 
about the classification in the galaxy.
For example, 'j ring galaxy', 'j unwinding', .... etc

If you need to zoom, you can type 'i' to Zoom In or 'o' to Zoom Out.

Finally, the code will ask us if we want to save the classification or not
..
	Save and go next (y) or classify again (n)?: 
	
For the first time that we run the code, when we save the first classification,
a table will be created ``class_results.csv`` with two new columns called:
``Classification`` and ``Comments ``

Each time that you save a classification, this table will be updated.

OBSERVATION:
Just in case when you start to run the code, the next error could happen:

..
 Traceback (most recent call last):
   File "Galaxy_classification_Franco.py", line 311, in <module>
     plt.close(fig=None) # Close figure to refresh
 TypeError: close() got an unexpected keyword argument 'fig'

You can comment all the line where it says 'plt.close(fig=None)',they are in the end 
of the script, and uncomment the other line 'plt.close()' since the fig argument 
is the problem, I don't why this happen but it could be the python3 version 
that you are using.


################### Final Classifcation v3 Code ##########################

This code was created to assign a final class for each galaxy 

Its structure is based in the flowchart attached in this repository

The code will need the table with the classification for each galaxy
of each classifier that run the code to classify.


#################### Plot for results code ###############################

Here we can obtain some results from the final classifications as:

Histogram of confidence for each group and each classification,
Histogram of the final confidences and a plot of the ra vs dec plane 
to see each interacting galaxy distributed in the sky









