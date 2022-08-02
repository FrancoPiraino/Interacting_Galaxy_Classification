#######################################################################################################################################################################################################				
### IMPORT SOME PACKAGES
import glob
import re

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
from  scipy import stats 
from  scipy.stats import norm

from astropy.io import fits, ascii  ### import fits from astropy.io
from astropy.table import Table  ## import Table from astropy.table

#Units and constants
from astropy import units as u
import astropy.constants as cons
from PIL import Image

#pandas
import pandas as pd


#### READ TABLE RESULTS
name_table = 'class_results_' ## Common name of your tables
test_tables = glob.glob(name_table+'*.csv') ## Read the result table of each inspector
#colors = ['yellow','red','green','blue','cyan'] ## We choose some color for each inspector
N = len(test_tables) # People that ran the code

print("--------------------------------------------------------------------------")
print("--------------------------------------------------------------------------")
print('N = ',N,' people ran the code to classify interacting galaxies')
print("--------------------------------------------------------------------------")
print("--------------------------------------------------------------------------")

## Function to sort the images label (linux doesn't sort correctly the name of the images when there are numbers)
def num_sort(test_string):
	return list(map(int,re.findall(r'\d+',test_string)))[0]

jpglist = sorted(glob.glob('Legacy_cuts/L*.jpg')) ## Read the Legacy Survey Images 
jpglist.sort(key=num_sort) ## Sort the images to assign the final class by row
length = len(jpglist) ## Number of the galaxies classified

###################################################################################################################################################################################################		
############################################################################# CHECK FINAL CLASS FOR EACH OBJECT ##################################################################################
###################################################################################################################################################################################################


JF_final, M_final, PM_final, JM_final, N_final, S_final, B_final, NC_final = [], [], [], [], [], [], [], []

Final_Class = []
RPS_Conf = []
GRAV_Conf = []
NI_Conf = []

### Cycle for to review each galaxy classified
for i in jpglist:
	
	id_num = int(re.findall(r'\d+', i)[0]) ## to extract the id number
	
	### Do at least n=1 person of N people classified the nth galaxy?
	print("Do at least n=1 person of ",N," people classified the galaxy number",id_num," ?")
	
	n_list = []
	JF, M, PM, JM, NO, S, B, NC = [], [], [], [], [], [], [], []
	Comments = []
	for tablename in test_tables:
		table = pd.read_csv(tablename)
		
		Id = table.loc[table["ID"] == id_num, "ID"].tolist()[0]
		classif = table.loc[table["ID"] == id_num, "Classification"].tolist()[0]
		comment = table.loc[table["ID"] == id_num, "Comments"].tolist()[0]
		
		if comment != "no comments" and comment!="0" and comment!=" " and comment!="  ":
			Comments.append(comment) 
		
		
		if classif != '0':
			n_list.append(classif)
			
			## For one side, we have classfications to flag that the galaxy is interacting
			## j: jellyfish, jm: jellyfish+merger, m: merger, pm: post-merger
			if classif == 'j' or classif == 'jm' or classif == 'm' or classif == 'pm':
				#Inter_class.append(classif)	
				
				if classif == 'j':
					JF.append('JF')
										
				elif classif == 'm':
					M.append('M')
											
				elif classif == 'pm':
					PM.append('PM')
								
				elif classif == 'jm':
					JM.append('JM')
									
			## On the other side, we have classification to flag that the galaxy is not interacting
			## n: nothing, s: star, b: broken
			else:
				#NoInter_class.append(classif)
				
				if classif == 'n':
					NO.append('N')
										
				elif classif == 's':
					S.append('S')
									
				elif classif == 'b':
					B.append('B')
		else:
			NC.append('NC')
	
	
			
	n = len(n_list)
	if n>0: ### Yes
		print("Yes, ",n," people of ",N," classified the galaxy")
		print("Now we'll check the classification performed by each one the ",n," people") ### Check the classfication performed by each one of the n people
		print(n_list)
		
	else:  #### No
		print("No Classified")   ### No CLassified
		final_class  = 'NC'
		NC_final.append(final_class)		
			
	
	### Count the votes of each classification

	
	Class = ['JF','JM','M','PM','S','B','N']
	Votes = [len(JF),len(JM),len(M),len(PM),len(S),len(B),len(NO)]
		
	RPS  = (Votes[0]+0.5*Votes[1])/float(n)
	GRAV = (Votes[2]+Votes[3]+0.5*Votes[1])/float(n)
	NI = (Votes[4]+Votes[5]+Votes[6])/float(n)
	
	### Choose the final class among the groups with more confidence
	groups_name = ['RPS','GRAV','NI']
	groups = [RPS,GRAV,NI]
	
	max_prob = np.max(groups)
	filter_max = np.where(groups==max_prob)
	
	confidences = np.array(groups)[filter_max]
	group_confidences = np.array(['RPS','GRAV','N.I.'])[filter_max]
	
	print('JF:',Votes[0],'| JM:',Votes[1],'| M:',Votes[2],'| PM:',Votes[3],'| S:',Votes[4],'| B:',Votes[5],'| N:',Votes[6] )
	print('RPS(%):',round(RPS,3),'('+str(RPS*n)+'/'+str(n)+')| '+' GRAV(%):',round(GRAV,3),'('+str(GRAV*n)+'/'+str(n)+')| '+' N.I.(%):',round(NI,3),'('+str(NI*n)+'/'+str(n)+')')
	print('The group/s with more confidence is/are: ',group_confidences,"with",confidences, "%")
	
	
	rps_class, rps_votes = ['JF','JM'], [Votes[0],Votes[1]]
	grav_class, grav_votes = ['M','PM'], [Votes[2],Votes[3]]
	ni_class, ni_votes = ['S','B','N'], [Votes[4],Votes[5],Votes[6]]
	
	if len(group_confidences) == 1:  ## RPS or GRAV or NI
		
		if group_confidences == ['RPS']:
			Class = rps_class
			Votes = rps_votes
			Max = np.max(Votes)
			Filter_votes = np.where(Votes==Max)
			
			Max_Votes = len(Filter_votes[0])
			Class_max = np.array(Class)[Filter_votes]
			Length_Votes = np.array(Votes)[Filter_votes]
			
			print("So, we have to choose between JF:",Votes[0],"| JM:",Votes[1])
			if len(Class_max)==1: 
				print("The classification with more votes is",Class_max[0]," with ",Length_Votes[0], "votes of ",n)
				final_class = Class_max[0]
				
				
			elif len(Class_max)>1: 											
				print("There are ",Max_Votes," classifications with the same votes, they are ",Class_max," with",Length_Votes[0]," votes each one")
				
				### Are there only classifications = ?
				if any(ele == 'JF' for ele in Class_max) == True and any(ele == 'JM' for ele in Class_max) == True:
					#print("Are there only classifications = JF?: No")
					#print("Are there classifications = JF + sth with gravitationl interacting?: Yes")
					final_class = 'JM'
					print("The priority for the final class is JM")
				
				
		elif group_confidences == ['GRAV']:
			Class = grav_class
			Votes = grav_votes
			Max = np.max(Votes)
			Filter_votes = np.where(Votes==Max)
			
			Max_Votes = len(Filter_votes[0])
			Class_max = np.array(Class)[Filter_votes]
			Length_Votes = np.array(Votes)[Filter_votes]
			
			print("So, we have to choose between M:",Votes[0],"| PM:",Votes[1])
			if len(Class_max)==1: 
				print("The classification with more votes is",Class_max[0]," with ",Length_Votes[0], "votes of ",n)
				final_class = Class_max[0]
				
			elif len(Class_max)>1: 											
				print("There are ",Max_Votes," classifications with the same votes, they are ",Class_max," with",Length_Votes[0]," votes each one")
			
				### Are there only classifications = ?
				if any(ele == 'M' for ele in Class_max) == True and any(ele == 'PM' for ele in Class_max) == True:
					#print("Are there only classifications = M?: No")
					#print("Are there classifications = M+ PM?: Yes")
					final_class = 'M'
					print("The priority for the final class is M")
			
		
		elif group_confidences == ['N.I.']:
			Class = ni_class
			Votes = ni_votes
			Max = np.max(Votes)
			Filter_votes = np.where(Votes==Max)
			
			Max_Votes = len(Filter_votes[0])
			Class_max = np.array(Class)[Filter_votes]
			Length_Votes = np.array(Votes)[Filter_votes]
			
			print("So, we have to choose between S:",Votes[0],"| B:",Votes[1],"| N:",Votes[2])
			if len(Class_max)==1: 
				print("The classification with more votes is",Class_max[0]," with ",Length_Votes[0], "votes of ",n)
				final_class = Class_max[0]
				
			elif len(Class_max)>1: 											
				print("There are ",Max_Votes," classifications with the same votes, they are ",Class_max," with",Length_Votes[0]," votes each one")
			
				## Are there only classifications = ?
				if any(ele == 'S' for ele in Class_max) == True and any(ele == 'B' for ele in Class_max) == True:
					#print("Are there classifications = S + B?: Yes")
					final_class = 'S'
					print("The priority for the final class is S")
				elif any(ele == 'S' for ele in Class_max) == True and any(ele == 'N' for ele in Class_max) == True:
					#print("Are there classifications = S + N?: Yes")
					final_class = 'S'
					print("The priority for the final class is S")
				elif any(ele == 'B' for ele in Class_max) == True and any(ele == 'N' for ele in Class_max) == True:
					#print("Are there classifications = B + N?: Yes")
					final_class = 'B'
					print("The priority for the final class is B")
				elif any(ele == 'S' for ele in Class_max) == True and any(ele == 'B' for ele in Class_max) and any(ele == 'N' for ele in Class_max) == True:
					#print("Are there classifications = S + B + N?: Yes")
					final_class = 'S'
					print("The priority for the final class is S")
							
					
		
	elif len(group_confidences) == 2: ## RPS+GRAV or RPS+NI or GRAV+NI
		
		if list(group_confidences) == ['RPS','GRAV']:
			Class = rps_class + grav_class
			Votes = rps_votes + grav_votes
			Max = np.max(Votes)
			Filter_votes = np.where(Votes==Max)
			
			Max_Votes = len(Filter_votes[0])
			Class_max = np.array(Class)[Filter_votes]
			Length_Votes = np.array(Votes)[Filter_votes]
			
			print("So, we have to choose between JF:",Votes[0],"| JM:",Votes[1],"| M:",Votes[2],"| PM:",Votes[3])
			
			if len(Class_max)==1: 
				print("The classification with more votes is",Class_max[0]," with ",Length_Votes[0], "votes of ",n)
				final_class = Class_max[0]
			
			elif len(Class_max)>1: 											
				print("There are ",Max_Votes," classifications with the same votes, they are ",Class_max," with",Length_Votes[0]," votes each one")
											
				if any(ele == 'JF' for ele in Class_max) == True and any(ele == 'JM' or ele == 'M' or ele == 'PM' for ele in Class_max) == True:
					final_class = 'JM'
					print("The priority for the final class is JM")
							
				elif any(ele == 'JM' for ele in Class_max) == True and any(ele == 'M' or ele == 'PM' for ele in Class_max) == True:
					final_class = 'JM'
					print("The priority for the final class is JM")
				
				elif any(ele == 'M' and ele == 'PM' for ele in Class_max) == True:
					final_class = 'M'
					print("The priority for the final class is M")
			
						
		elif list(group_confidences) == ['RPS','N.I.']:
			Class = rps_class + ni_class
			Votes = rps_votes + ni_votes
			Max = np.max(Votes)
			Filter_votes = np.where(Votes==Max)
			
			Max_Votes = len(Filter_votes[0])
			Class_max = np.array(Class)[Filter_votes]
			Length_Votes = np.array(Votes)[Filter_votes]
			
			print("So, we have to choose between JF:",Votes[0],"| JM:",Votes[1],"| S:",Votes[2],"| B:",Votes[3],"| N:",Votes[4])
			
			if len(Class_max)==1: 
				print("The classification with more votes is",Class_max[0]," with ",Length_Votes[0], "votes of ",n)
				final_class = Class_max[0]
			
			elif len(Class_max)>1: 											
				print("There are ",Max_Votes," classifications with the same votes, they are ",Class_max," with",Length_Votes[0]," votes each one")
											
				if any(ele == 'JM' for ele in Class_max) == True:
					final_class = 'JM'
					print("The priority for the final class is JM")
				
				elif any(ele == 'JF' for ele in Class_max) and any(ele == 'S' or ele == 'B' or ele == 'N' for ele in Class_max) == True:
					final_class = 'JF'
					print("The priority for the final class is JF")
				
				"""	
				elif any(ele == 'S' or ele == 'B' or ele == 'N' for ele in Class_max) == True:
					
					## Are there only classifications = ?
					if any(ele == 'S' for ele in Class_max) == True and any(ele == 'B' for ele in Class_max) == True:
						final_class = 'S'
						print("The priority for the final class is S")
					elif any(ele == 'S' for ele in Class_max) == True and any(ele == 'N' for ele in Class_max) == True:
						final_class = 'S'
						print("The priority for the final class is S")
					elif any(ele == 'B' for ele in Class_max) == True and any(ele == 'N' for ele in Class_max) == True:
						final_class = 'B'
						print("The priority for the final class is B")
					elif any(ele == 'S' for ele in Class_max) == True and any(ele == 'B' for ele in Class_max) and any(ele == 'N' for ele in Class_max) == True:
						final_class = 'S'
						print("The priority for the final class is S")
				"""	
					
			
		elif list(group_confidences) == ['GRAV','N.I.']:
			Class = grav_class + ni_class
			Votes = grav_votes + ni_votes
			Max = np.max(Votes)
			Filter_votes = np.where(Votes==Max)
			
			Max_Votes = len(Filter_votes[0])
			Class_max = np.array(Class)[Filter_votes]
			Length_Votes = np.array(Votes)[Filter_votes]
			
			print("So, we have to choose between M:",Votes[0],"| PM:",Votes[1],"| S:",Votes[2],"| B:",Votes[3],"| N:",Votes[4])
		
			if len(Class_max)==1: 
				print("The classification with more votes is",Class_max[0]," with ",Length_Votes[0], "votes of ",n)
				final_class = Class_max[0]
			
			elif len(Class_max)>1: 											
				print("There are ",Max_Votes," classifications with the same votes, they are ",Class_max," with",Length_Votes[0]," votes each one")
											
				if any(ele == 'M' for ele in Class_max) == True:
					final_class = 'M'
					print("The priority for the final class is M")
				
				elif any(ele == 'PM' for ele in Class_max) and any(ele == 'S' or ele == 'B' or ele == 'N' for ele in Class_max) == True:
					final_class = 'PM'
					print("The priority for the final class is PM")
				
				"""	
				elif any(ele == 'S' or ele == 'B' or ele == 'N' for ele in Class_max) == True:
					
					## Are there only classifications = ?
					if any(ele == 'S' for ele in Class_max) == True and any(ele == 'B' for ele in Class_max) == True:
						final_class = 'S'
						print("The priority for the final class is S")
					elif any(ele == 'S' for ele in Class_max) == True and any(ele == 'N' for ele in Class_max) == True:
						final_class = 'S'
						print("The priority for the final class is S")
					elif any(ele == 'B' for ele in Class_max) == True and any(ele == 'N' for ele in Class_max) == True:
						final_class = 'B'
						print("The priority for the final class is B")
					elif any(ele == 'S' for ele in Class_max) == True and any(ele == 'B' for ele in Class_max) and any(ele == 'N' for ele in Class_max) == True:
						final_class = 'S'
						print("The priority for the final class is S")
				"""
	
	
				
	elif len(group_confidences) == 3: ## RPS+GRAV+NI
		Class = rps_class + grav_class + ni_class
		Votes = rps_votes + grav_votes + ni_votes
		Max = np.max(Votes)
		Filter_votes = np.where(Votes==Max)
	
		Max_Votes = len(Filter_votes[0])
		Class_max = np.array(Class)[Filter_votes]
		Length_Votes = np.array(Votes)[Filter_votes]
			
		print("So, we have to choose between JF:",Votes[0],"| JM:,",Votes[1],"| M:",Votes[2],"| PM:",Votes[3],"| S:",Votes[4],"| B:",Votes[5],"| N:",Votes[6]) 
	
		if len(Class_max)==1: 
				print("The classification with more votes is",Class_max[0]," with ",Length_Votes[0], "votes of ",n)
				final_class = Class_max[0]
		
		elif len(Class_max)>1: 											
				print("There are ",Max_Votes," classifications with the same votes, they are ",Class_max," with",Length_Votes[0]," votes each one")
											
				if any(ele == 'JM' for ele in Class_max) == True:
					final_class = 'JM'
					print("The priority for the final class is JM")
				
				elif any(ele == 'JF' for ele in Class_max) and any(ele == 'M' or ele == 'PM' for ele in Class_max) == True:
					final_class = 'JM'
					print("The priority for the final class is JM")
				
				elif any(ele == 'JF' for ele in Class_max) and any(ele == 'M' or ele == 'PM' for ele in Class_max) == False and any(ele == 'S' or ele == 'B' or ele == 'N' for ele in Class_max)==True:
					final_class = 'JF'
					print("The priority for the final class is JF")
	
	Final_Class.append(final_class)
	RPS_Conf.append(round(RPS,3))
	GRAV_Conf.append(round(GRAV,3))
	NI_Conf.append(round(NI,3))
	
	
	if final_class == 'JF':
		JF_final.append(final_class)
		
	elif final_class == 'M':
		M_final.append(final_class)
		
	elif final_class == 'PM':
		PM_final.append(final_class)
		
	elif final_class == 'JM':
		JM_final.append(final_class)
	
	elif final_class == 'N':
		N_final.append(final_class)	
	
	elif classif == 'S':
		S_final.append(final_class)
	
	elif classif == 'B':
		B_final.append(final_class)					
			
	#### PLOT THE INFO IN THE IMAGES -----------------------------------------------------------------------------------------------------------------------
			
	### Pre-classifications
	rps = table.loc[table["ID"] == id_num, "RPS"].tolist()[0]
	merg = table.loc[table["ID"] == id_num, "Merger"].tolist()[0]
					
	imagename = i
	Decals_image = Image.open(imagename) # Call the decals image from a file	
	plt.imshow(Decals_image)
	plt.annotate('JF: '+str(len(JF)),(210,10),fontsize=10,color='red')
	plt.annotate('JM: '+str(len(JM)),(210,20),fontsize=10,color='red')
	plt.annotate('M: '+str(len(M)),(210,30),fontsize=10,color='red')
	plt.annotate('PM: '+str(len(PM)),(210,40),fontsize=10,color='red')
	plt.annotate('S: '+str(len(S)),(210,50),fontsize=10,color='red')
	plt.annotate('B: '+str(len(B)),(210,60),fontsize=10,color='red')
	plt.annotate('N: '+str(len(NO)),(210,70),fontsize=10,color='red')	
	plt.annotate('NC: '+str(len(NC)),(210,80),fontsize=10,color='red')
	plt.annotate(str(id_num)+': '+final_class,(10,20),fontsize=20,color='red')
	plt.annotate('RPS (%): '+str(round(RPS,2))+' ('+str(int(RPS*n))+'/'+str(n)+')',(10,40),fontsize=11,color='red')
	plt.annotate('GRAV (%): '+str(round(GRAV,2))+' ('+str(int(GRAV*n))+'/'+str(n)+')',(10,60),fontsize=11,color='red')
	plt.annotate('N.I. (%): '+str(round(NI,2))+' ('+str(int(NI*n))+'/'+str(n)+')',(10,80),fontsize=11,color='red')
	
	
	k = 210
	for i in Comments:
		plt.annotate(i,(10,k),fontsize=10,color='red')
		k-=10
		
	if rps >= 1.0 and merg >= 1.0:
		plt.annotate('PC: JM',(210,90),fontsize=10,color='red')
		plt.annotate('('+str(int(rps))+'+'+str(int(merg))+')',(220,100),fontsize=10,color='red')
		
	elif rps == 0.0 and merg >= 1.0:
		plt.annotate('PC: M'+'('+str(int(merg))+')',(210,90),fontsize=10,color='red')
					
	elif rps >= 1.0 and merg == 0.0:
		plt.annotate('PC: JF'+'('+str(int(rps))+')',(210,90),fontsize=10,color='red')
			
	elif rps == 0.0 and merg == 0.0:
		plt.annotate('PC: N',(210,90),fontsize=10,color='red')
		
	else:
		plt.annotate('PC: NC',(210,90),fontsize=10,color='red')
	
	plt.axis('off')
	plt.savefig('class_final_legacy_cuts/L'+str(id_num)+'.png')
	#plt.show()
	plt.close()
	
	#### PLOT THE INFO IN THE IMAGES -----------------------------------------------------------------------------------------------------------------------
	
	#print("FINAL CLASS", final_class)	

	print("-----------------------------------------------------------------------------------------------------")


example_table = pd.read_csv('Abell2670_catalogue_test.csv') # Load in table
example_table['final_class'] = Final_Class
example_table['rps_conf'] = RPS_Conf
example_table['grav_conf'] = GRAV_Conf
example_table['ni_conf'] = NI_Conf

for tablename in test_tables:
	table = pd.read_csv(tablename)
	classifier = tablename.replace(name_table,'')
	classifier = classifier.replace('.csv','')
	example_table["Class_"+str(classifier)] = table["Classification"].tolist()
	example_table["Comment_"+str(classifier)] = table["Comments"].tolist()

example_table.to_csv('Abell2670_catalogue_test_final_class.csv',index=False)

#############
x = np.arange(0.,0.5,0.1)

plt.gca().bar_label(plt.gca().bar(x[0],len(JF_final),0.1,alpha=0.5))
plt.gca().bar_label(plt.gca().bar(x[1],len(M_final),0.1,alpha=0.5))
plt.gca().bar_label(plt.gca().bar(x[2],len(PM_final),0.1,alpha=0.5))
plt.gca().bar_label(plt.gca().bar(x[3],len(JM_final),0.1,alpha=0.5))
plt.gca().bar_label(plt.gca().bar(x[4],len(NC_final),0.1,alpha=0.5,color='gray'))
	
plt.xticks(x,['JF','M','PM','JM','NoClassified'])
plt.ylabel('Counts')
#plt.legend(['JF','M','PM','JM','NoClassified'])
#plt.show()
plt.savefig('bar_char_final.png')
plt.close()



