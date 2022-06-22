# Galaxy_Classification
This repository contain 

===========================
Galaxy Classification Code
===========================
		
This code is used to classify galaxies, visualizing them with cut images
from Legacy Survey, Deep Mosaic FITS files from DECam in r and g band and available rgb 
images from a photometric catalogue.

To run the code you need a table with the ID of each object and three folders 
which contain the cuts to classify them

The folders that you should have are:
	
	``Legacy_cuts``: Here we should have the complete catalogue of
			images from Legacy Survey
	``DECam_cuts`` : Here we should have some cutout fits from Deep Mosaic FITS DECam 
			in two bands (r,g). 
	``RGB_cuts``   : Here we should have rgb images from the photometric
			catalogue.
	
The code is written in python3, so maybe you should run it using ``python3 Galaxy_classification.py``

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
Just in case when you start to run the code, the nexte error
could appear:

..
 Traceback (most recent call last):
   File "Galaxy_classification_Franco.py", line 311, in <module>
     plt.close(fig=None) # Close figure to refresh
 TypeError: close() got an unexpected keyword argument 'fig'

You can comment all the line where it says 'plt.close(fig=None)', 
they are in the end of the script, and uncooment the other line 
'plt.close()' since the fig argument is the problem, 
I don't why but it could be the python3 version
that you are using.


