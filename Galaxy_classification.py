# Required libraries
import math
from astropy.io import fits
import matplotlib.pyplot as plt
#from matplotlib import pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from astropy.visualization import MinMaxInterval, PercentileInterval, simple_norm
import glob
from PIL import Image
import pandas as pd
import random

### I AM EDITING

### Paths to read the photos
Image_path = 'DECam_cuts/' ## Cuts.fits from Deep DECam mosaics 
jpg_path = 'Legacy_cuts/'  ## Cuts from Legacy 
png_path = 'RGB_cuts/'    ## Cuts in rgb from photometric catalogue provided by Duho

### Read the table 
example_table = pd.read_csv('Abell2670_catalogue_test.csv')

### Taking the ID column
id_col = example_table['ID']  ## Take the ID column
### Definitio of two new columns
Class = np.array(['0']*len(id_col)) ## I create an array with zeros to save the classification 
example_table['Classification'] = Class ## Info of classification
example_table["Comments"] = Class ## Commennts about the classification

### A random seed for each classifier 
random.seed(0) ## Each time that you run the code, always it give you the id list in the same orden
id_list = id_col.tolist()
print(id_list)
random.shuffle(id_list) ## Here we unsort the list for one seed
k=0 ## to take the first object of the shuffle list when we start to classify
print(id_list)

## The code will ask you if you want to start from the begining or if the code stop during your classification, you can start where you stayed
print("Type the number of the options:")
print("1: Are you running for first time? or do you want to classify again?")
print("2: Continue where you stayed!")
Q = int(input("Type: "))

## If you want to continue in the part where you stayed
if Q == 2:
	example_table = pd.read_csv('class_results.csv') ## Read the saved table 
	checking_class = example_table['Classification'] == '0' ## Checking if the classification is complete
	true = not any(checking_class) ## If is True theres is no zeros so your classification is complete
	if true == True:
		check = input("Your classification is complete. Do you want to start again? ('y':yes, 'n':no): ").lower()
		if check == 'y':
			example_table = pd.read_csv('Abell2670_catalogue_testsample.csv')
			
			### Get the objects
			id_col = example_table['ID']  ## Take the ID column
			Class = np.array(['0']*len(id_col)) ## I create an array with zeros to save the classification 
			example_table['Classification'] = Class ## I put this array in the table
			example_table["Comments"] = Class
			
		else: ## If check = no, the code don't do anything
			id_list = []
		
	else: ### You'll start where you stayed
		for i in id_list: ## It read each id to check what object was classified
			cl = example_table['Classification'][id_col==i]  
			if cl.tolist()[0] == '0': 
				k = id_list.index(i)  #to take the first object of the shuffle list when we start to classify
				break

### Here start the classification
for i in id_list[k:]:
	
	## Definition of zero array as preliminar images to plot juts in case there is no image 
	image_data_r = np.zeros([256,256])
	image_data_g = np.zeros([256,256])
	Decals_image = np.zeros([256,256])
	RGB_image = np.zeros([256,256])
	
	## Now we have to check if there is image for each object in each folder 
	try: ## Fit g band DECam
		imlist_g = Image_path+str(i)+'_gband.fits' ## <<<<<<<<<<<<<<<<- You need to define according how you called your images
		hdu_list_g = fits.open(imlist_g) ## Open the fits
		image_data_g = hdu_list_g[0].data # Get the data from the fits
		image_data_g = np.rot90(image_data_g,3) # Dumb way of making North top in the image
	except(FileNotFoundError, IOError):
		image_data_g = np.zeros([256,256])
	
	try: ## Fit r band DECam	
		imlist_r = Image_path+str(i)+'_rband.fits' ## <<<<<<<<<<<<<<<<- You need to define according how you called your images
		hdu_list_r = fits.open(imlist_r) # Open the fits     
		image_data_r = hdu_list_r[0].data # Get the data from the fits
		image_data_r = np.rot90(image_data_r,3) # Dumb way of making North top in the image
	except(FileNotFoundError, IOError):								
		image_data_r = np.zeros([256,256])
	
	try: ## Legacy jpg
		jpglist = jpg_path+'L'+str(i)+'.jpg' ## <<<<<<<<<<<<<<<<- You need to define according how you called your images
		Decals_image = Image.open(jpglist) # Call the decals image from a file
	except(FileNotFoundError, IOError):								
		Decals_image = np.zeros([256,256])
		
	try: ## RGB png
		pnglist = png_path+str(i)+'_rgb_jar_3.png' ## <<<<<<<<<<<<<<<<- You need to define according how you called your images
		RGB_image = Image.open(pnglist)
	except (FileNotFoundError, IOError):
		RGB_image = np.zeros([256,256])
		
		
	
	coord_length = len(image_data_g)/2. # The range of values in the fits file extent, to define the scale
	FOV = coord_length # Field of view. Needs to be independent of the coord_length
			        	
	certain = False  ## Parameter to break the cicle
	while certain == False: 
		       	    
		        			     	
		# Create the plot figure to visualize the object and to classify
		fig, ((ax1, ax2), (ax3,ax4)) = plt.subplots(2, 2, gridspec_kw={'hspace': 0, 'wspace': 0}, figsize=(8,8))
				
		# Lognorm plot with flux values from min to max in g band
		norm_type = 'log'
		pp = 50. ## Here we choose the percent
		interval = PercentileInterval(pp)
	
		Pmin_g = interval.get_limits(np.sort(image_data_g.flatten()))[0]
		Pmax_g = np.max(image_data_g)
		norm_g= simple_norm(image_data_g, stretch=norm_type, min_cut=Pmin_g, max_cut=Pmax_g)
		
		if len(image_data_g[np.logical_not(np.isnan(image_data_g))])!= np.shape(image_data_g)[0]*np.shape(image_data_g)[1]:	
			img_without_nan = image_data_g[np.logical_not(np.isnan(image_data_g))]
			
			Pmin_g = interval.get_limits(np.sort(img_without_nan.flatten()))[0]
			Pmax_g = np.max(img_without_nan)
			norm_g = simple_norm(img_without_nan, stretch=norm_type, min_cut=Pmin_g, max_cut=Pmax_g)
			
			ax1.imshow(image_data_g, cmap='gray', norm=norm_g, extent=[-coord_length,coord_length,-coord_length,coord_length])
			ax1.annotate('g band',xy=[(-FOV + 0.1*FOV),(FOV - 0.2*FOV)],fontsize=18,color='red') # Label of the figure
			ax1.set_xlim(-FOV,FOV) # Ensure the field of view matches the requested zoom
			ax1.set_ylim(-FOV,FOV)
		else:
			ax1.imshow(image_data_g, cmap='gray', norm=norm_g, extent=[-coord_length,coord_length,-coord_length,coord_length])
			ax1.annotate('g band',xy=[(-FOV + 0.1*FOV),(FOV - 0.2*FOV)],fontsize=18,color='red') # Label of the figure
			ax1.set_xlim(-FOV,FOV) # Ensure the field of view matches the requested zoom
			ax1.set_ylim(-FOV,FOV)
      			
      		
		# Plot based in the Decals sourced image
		ax2.imshow(Decals_image,extent=[-180,180,-180,180]) 
		ax2.annotate('Legacy Survey',xy=[(-FOV + 0.1*FOV),(FOV - 0.2*FOV)],fontsize=18,color='red') # Label of the figure
		ax2.yaxis.tick_right() # Move the axis ticks to the right to keep things clean
		ax2.set_xlim(-FOV,FOV) # Ensure the field of view matches the requested zoom
		ax2.set_ylim(-FOV,FOV)
		
		
		
		# # Plot based in the RGB sourced image
		ax3.imshow(RGB_image,extent=[-280,280,-280,280]) 
		ax3.annotate('RGB',xy=[(-FOV + 0.1*FOV),(FOV - 0.2*FOV)],fontsize=18,color='red') # Label of the figure
		ax3.yaxis.tick_left() # Move the axis ticks to the right to keep things clean
		ax3.set_xlim(-FOV,FOV) # Ensure the field of view matches the requested zoom
		ax3.set_ylim(-FOV,FOV)
		
		# Lognorm plot with flux values from min to max in r band
		norm_type = 'log'
		pp = 50. ## Here we choose the percent
		interval = PercentileInterval(pp)
		
		Pmin_r = interval.get_limits(np.sort(image_data_r.flatten()))[0]
		Pmax_r = np.max(image_data_r)
		norm_r = simple_norm(image_data_r, stretch=norm_type, min_cut=Pmin_r, max_cut=Pmax_r)
		
		if len(image_data_r[np.logical_not(np.isnan(image_data_r))])!= np.shape(image_data_r)[0]*np.shape(image_data_r)[1]:	
			img_without_nan = image_data_r[np.logical_not(np.isnan(image_data_r))]
			
			Pmin_r = interval.get_limits(np.sort(img_without_nan.flatten()))[0]
			Pmax_r = np.max(img_without_nan.flatten())
			norm_r = simple_norm(img_without_nan, stretch=norm_type, min_cut=Pmin_r, max_cut=Pmax_r)
			
			ax4.imshow(image_data_r, cmap='gray', norm=norm_r, extent=[-coord_length,coord_length,-coord_length,coord_length])
			ax4.annotate('r band',xy=[(-FOV + 0.1*FOV),(FOV - 0.2*FOV)],fontsize=18,color='red') # Number the figure
			ax4.yaxis.tick_right() # Move the axis ticks to the right to keep things clean
			ax4.set_xlim(-FOV,FOV) # Ensure the field of view matches the requested zoom
			ax4.set_ylim(-FOV,FOV)
			
		else:
			ax4.imshow(image_data_r, cmap='gray', norm=norm_r, extent=[-coord_length,coord_length,-coord_length,coord_length])
			ax4.annotate('r band',xy=[(-FOV + 0.1*FOV),(FOV - 0.2*FOV)],fontsize=18,color='red') # Number the figure
			ax4.yaxis.tick_right() # Move the axis ticks to the right to keep things clean
			ax4.set_xlim(-FOV,FOV) # Ensure the field of view matches the requested zoom
			ax4.set_ylim(-FOV,FOV)
			
		
		plt.suptitle('ID Object: '+str(i), fontsize=16)
		plt.tight_layout()
		plt.pause(0.1) #Pause to highlight the line
		#plt.close(fig=None)
						
		#plt.close(fig=None) # Close the figure after the selection
		      	  
		
		#######################################################
            	
                                   
		plt.ion() # Ensure in interactive mode
       	
       	### Interactive mode with the user to start the classification
		print('---------------------------------------------------------------')	
		print("Classification N°", len(example_table['Classification'][example_table['Classification']!='0'])+1)
		print("ID for this object: ", i)
		print("Do you see any interaction? Type one of the following options and press <ENTER>")  # User input if the galaxy is a JF
		print('To comment add a space after the classification and type, e.g. "j ring galaxy"') 
		print("If you need to zoom, you can type 'i' to Zoom In or 'o' to Zoom Out ")
		print("'j': jellyfish")
		print("'m': merger")
		print("'pm': post merger")
		print("'jm': jellyfish+merger")
		print("'s': star")
		print("'n': no interaction ")
		print("'b': broken images")	
		
		
		InterQ = input("Type: ").lower() ## Input the interacting classification
		InterQ_list = list(InterQ) ## I convert the input in a list of words
		InterQ_array = np.array(InterQ_list,str) ## I convert the list in an array
		sep = np.where(InterQ_array == ' ')[0] ## Index value of the point where I separate the class and the comment
		
		## Whit this conditions I separete the coment from the classification
		if len(sep) == 0:
			InterQ_class = InterQ
			InterQ_comment = 'no comments'
		else:
			InterQ_class = InterQ[:sep[0]]
			InterQ_comment = InterQ[sep[0]+1:]
		
		## other option to comment
		#if MorphQ == 'j ' or MorphQ == 'm ' or MorphQ == 'pm ' or MorphQ == 'jm ' or MorphQ == 's ' or MorphQ == 'n ' or MorphQ == 'b ':
			#Comment = input("Comments: ").lower()
		
		## To zoom	
		ZoomQ = InterQ_class 
		
		### If classification = jellyfish
		if InterQ_class == 'j':
			               	
			# Ask to finish the classification
			FinishQ = input('Save and go next (y) or classify again (n)?: ' ).lower()
			if FinishQ == 'yes' or FinishQ =='y' or FinishQ == 's' or FinishQ == 'si':
				morph = InterQ_class
				comment = InterQ_comment
				certain = True # To leave the while loop 
					
		### If classification = merger
		elif InterQ_class == 'm':
			# Ask to finish the classification
			FinishQ = input('Save and go next (y) or classify again (n)?: ' ).lower()
			if FinishQ == 'yes' or FinishQ =='y' or FinishQ == 's' or FinishQ == 'si':
				morph = InterQ_class
				comment = InterQ_comment
				certain = True # To leave the while loop
				
		### If classification = post merger
		elif InterQ_class == 'pm':
			# Ask to finish the classification
			FinishQ = input('Save and go next (y) or classify again (n)?: ').lower()
			if FinishQ == 'yes' or FinishQ =='y' or FinishQ == 's' or FinishQ == 'si':
				morph = InterQ_class
				comment = InterQ_comment
				certain = True # To leave the while loop
		
		### If classification = jellyfish+merger		
		elif InterQ_class == 'jm':
			# Ask to finish the classification
			FinishQ = input('Save and go next (y) or classify again (n)?: ' ).lower()
			if FinishQ == 'yes' or FinishQ =='y' or FinishQ == 's' or FinishQ == 'si':
				morph = InterQ_class
				comment = InterQ_comment
				certain = True # To leave the while loop				

            	### If classification = star
		elif InterQ_class == 's':
			# Ask to finish the classification
			FinishQ = input('Save and go next (y) or classify again (n)?: ' ).lower()
			if FinishQ == 'yes' or FinishQ =='y' or FinishQ == 's' or FinishQ == 'si':
				morph = InterQ_class
				comment = InterQ_comment
				certain = True # To leave the while loop 
				
		### If classification = no interaction
		elif InterQ_class == 'n':
			# Ask to finish the classification
			FinishQ = input('Save and go next (y) or classify again (n)?: ' ).lower()
			if FinishQ == 'yes' or FinishQ =='y' or FinishQ == 's' or FinishQ == 'si':
				morph = InterQ_class
				comment = InterQ_comment
				certain = True # To leave the while loop 

		### If classification = broken images
		elif InterQ_class == 'b':
			# Ask to finish the classification
			FinishQ = input('Save and go next (y) or classify again (n)?: ' ).lower()
			if FinishQ == 'yes' or FinishQ =='y' or FinishQ == 's' or FinishQ == 'si':
				morph = InterQ_class
				comment = InterQ_comment
				certain = True # To leave the while loop 
				
						
		
		# Check the zoom user input
		elif ZoomQ == 'i':
			FOV = FOV-50 # FOV smaller
			plt.close(fig=None) # Close figure to refresh
			#plt.close() ## If you have problems with 'fig' use this line and comment the above line
			
		# If needing a bigger field of view/zoom out
		elif ZoomQ == 'o':
			FOV = FOV+50 # FOV bigger
			plt.close(fig=None) # Close figure to refresh
			#plt.close() ## If you have problems with 'fig' use this line and comment the above line

		plt.close(fig=None) # Close the figure to keep things clean
		#plt.close() ## If you have problems with 'fig' use this line and comment the above line
	
	### Here we save the classification and comments and we updated the new table each time that we classify an object
	example_table.loc[example_table["ID"] == i, "Classification"] = morph
	example_table.loc[example_table["ID"] == i, "Comments"] = comment
	example_table.to_csv('class_results.csv',index=False)





	
		

