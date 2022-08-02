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
table = pd.read_csv('Abell2670_catalogue_test_final_class.csv') # Load in table

#### READ USUFUL COLUMNS
ra = table.ra_1
dec = table.dec_1
final_class = table.final_class
rps_conf = table.rps_conf
grav_conf = table.grav_conf
ni_conf = table.ni_conf


###################################################################################################################################################################################################		
############################################################################# HISTOGRAM OF CONFIDENCES ##################################################################################
###################################################################################################################################################################################################


# Plot the figure
plt.figure() 
plt.hist(rps_conf,bins=7,range=[0,1],facecolor='none',edgecolor='blue',label='rps conf') 
plt.hist(grav_conf,bins=7,range=[0,1],facecolor='none',edgecolor='red',label='grav conf') 
plt.hist(ni_conf,bins=7,range=[0,1],facecolor='none',edgecolor='black',label='nothing conf') 
plt.xlim(0,1) 
#plt.xticks([0.,0.25,0.5,0.75,1.0]) 
plt.xticks(list(np.arange(0.,1.+1/7.,1/7.))) 
plt.xlabel('Confidence (%)') 
plt.ylabel('counts') 
plt.title('Confidences for each group')
plt.tight_layout() 
plt.legend(loc='upper center',bbox_to_anchor=(0.5, 1.01),ncol=3, fancybox=True, shadow=True)
# Save it if you want
#plt.savefig('Example_JF_tail_offset_JC.eps') 
plt.savefig('Confidences_for_each_group.png')
#plt.show()
#plt.close()

###################################################################################################################################################################################################		
############################################################################# HISTOGRAM OF CONFIDENCES ONLY JF ##################################################################################
###################################################################################################################################################################################################


jellyfish = final_class[final_class == 'JF']
jelly_conf = rps_conf[final_class == 'JF']
merg_conf = grav_conf[final_class == 'JF']
nothing_conf = ni_conf[final_class == 'JF']

#print(jelly_conf)
# Plot the figure
plt.figure() 
plt.hist(jelly_conf,bins=7,range=[0,1],facecolor='none',edgecolor='blue',label='rps conf') 
plt.hist(merg_conf,bins=7,range=[0,1],facecolor='none',edgecolor='red',label='grav conf') 
plt.hist(nothing_conf,bins=7,range=[0,1],facecolor='none',edgecolor='black',label='nothing conf') 
plt.xlim(0,1) 
#plt.xticks([0.,0.25,0.5,0.75,1.0]) 
plt.xticks(list(np.arange(0.,1.+1/7.,1/7.))) 
plt.xlabel('Confidence (%)') 
plt.ylabel('counts') 
plt.title('Confidences for Final Class = JF')
plt.tight_layout() 
plt.legend(loc='upper center',bbox_to_anchor=(0.5, 1.01),ncol=3, fancybox=True, shadow=True)
# Save it if you want
#plt.savefig('Example_JF_tail_offset_JC.eps') 
plt.savefig('Confidences_for_Final_Class_JF.png')
#plt.show()       
#plt.close()


###################################################################################################################################################################################################		
############################################################################# CONF. FINAL ##################################################################################
###################################################################################################################################################################################################

final_conf = []
final_class_conf = []

for i in range(1,812):
	
	final_class_nth = table.loc[table["ID"] == i, "final_class"].tolist()[0]
	rps_conf_nth = table.loc[table["ID"] == i, "rps_conf"].tolist()[0] 
	grav_conf_nth = table.loc[table["ID"] == i, "grav_conf"].tolist()[0]
	ni_conf_nth = table.loc[table["ID"] == i, "ni_conf"].tolist()[0]
		
	#print(i,"|",final_class_nth,"|",rps_conf_nth,"|",grav_conf_nth,"|",ni_conf_nth)
	#print("---------------------------------------------------")
	
	confs = [rps_conf_nth,grav_conf_nth,ni_conf_nth]
	
	final_conf.append(np.max(confs))
	final_class_conf.append(final_class_nth)

filter_jf_confs = np.array(final_class_conf) == 'JF'
filter_m_confs = np.array(final_class_conf) == 'M'
filter_jm_confs = np.array(final_class_conf) == 'JM'
filter_pm_confs = np.array(final_class_conf) == 'PM'
filter_n_confs = np.array(final_class_conf) == 'N'


final_jf_confs = np.array(final_conf)[filter_jf_confs]
final_m_confs = np.array(final_conf)[filter_m_confs]
final_jm_confs = np.array(final_conf)[filter_jm_confs]
final_pm_confs = np.array(final_conf)[filter_pm_confs]
final_n_confs = np.array(final_conf)[filter_n_confs]

# Plot the figure
plt.figure() 
plt.hist(final_conf,bins=7,range=[0,1],facecolor='lightgray',edgecolor='lightgray',label='final conf') 
plt.hist(final_jf_confs,bins=7,range=[0,1],facecolor='none',edgecolor='darkblue',label='jfs')
plt.hist(final_m_confs,bins=7,range=[0,1],facecolor='none',edgecolor='darkred',label='m')
plt.hist(final_jm_confs,bins=7,range=[0,1],facecolor='none',edgecolor='darkorange',label='jm')
plt.hist(final_pm_confs,bins=7,range=[0,1],facecolor='none',edgecolor='darkgreen',label='pm')
plt.hist(final_n_confs,bins=7,range=[0,1],facecolor='none',edgecolor='black',label='n')
#plt.hist(final_n_confs,bins=7,range=[0,1],facecolor='none',edgecolor='black',label='n')
plt.xlim(0,1) 
#plt.xticks([0.,0.25,0.5,0.75,1.0]) 
plt.xticks(list(np.arange(0.,1.+1/7.,1/7.))) 
plt.xlabel('Confidence (%)') 
plt.ylabel('counts') 
plt.title('Final Conf')
plt.tight_layout() 
plt.legend(loc='upper center',bbox_to_anchor=(0.5, 1.01),ncol=3, fancybox=True, shadow=True)
# Save it if you want
#plt.savefig('Example_JF_tail_offset_JC.eps') 
plt.savefig("Final_Conf.png")
#plt.show()       
#plt.close()


###################################################################################################################################################################################################		
############################################################################# RA-DEC PLOT ##################################################################################
###################################################################################################################################################################################################

ra_jf, dec_jf  = ra[final_class == 'JF'], dec[final_class == 'JF']
ra_jm, dec_jm  = ra[final_class == 'JM'], dec[final_class == 'JM']
ra_m, dec_m = ra[final_class == 'M'], dec[final_class == 'M']
ra_pm, dec_pm = ra[final_class == 'PM'], dec[final_class == 'PM']

#jelly_rps_conf = rps_conf[final_class == 'JF']
#merg_grav_conf = grav_conf[final_class == 'M']
#jm_grav_conf = grav_conf[final_class == 'JM']

plt.figure(figsize=(8,8))
plt.gca().scatter(ra,dec,marker='.',s=150,c='gray',alpha=0.5)

#im = plt.gca().scatter(ra_jf, dec_jf,marker='*',s=250,c=jelly_rps_conf.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues)
#plt.gca().scatter(ra_m, dec_m,marker='p',s=100,c=merg_grav_conf.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues)
#plt.gca().scatter(ra_jm, dec_jm,marker='v',s=100,c=merg_grav_conf.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues)

im = plt.gca().scatter(ra_jf, dec_jf,marker='*',s=300,c=final_jf_confs.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues,label="JF")
plt.gca().scatter(ra_m, dec_m,marker='p',s=150,c=final_m_confs.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues,label="M")
plt.gca().scatter(ra_jm, dec_jm,marker='v',s=300,c=final_jm_confs.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues,label="JM")
plt.gca().scatter(ra_pm, dec_pm,marker='^',s=300,c=final_pm_confs.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues,label="PM")


plt.colorbar(im,label='conf')
#cbar.set_label('conf', size=20)
#cbar.ax.tick_params(labelsize='large')

## Plot BCG
# DATA OF CLUSTER A2670
z = 0.076 ## redshift
sigma = 686.62616 #km/s
r200_deg = 0.3616 ##degrees
r200_mpc = 1.9 ## Mpc
ra_bcg = 358.5571
dec_bcg = -10.41888
plt.scatter(ra_bcg,dec_bcg,marker="+",s=700,color='red',label='BCG')
theta = np.arange(0,2*np.pi+1,0.1)
plt.plot(r200_deg*np.cos(theta)+ra_bcg,r200_deg*np.sin(theta)+dec_bcg, linewidth=2, linestyle='--',color='black')
#plt.plot(4*r200_deg*np.cos(theta)+ra_bcg,4*r200_deg*np.sin(theta)+dec_bcg, linewidth=2, linestyle='--',color='black')
plt.plot(5*r200_deg*np.cos(theta)+ra_bcg,5*r200_deg*np.sin(theta)+dec_bcg, linewidth=2, linestyle='--',color='black')

#plt.scplot(ra_jm, dec_jm, '*',color='darkred',markersize=15)
plt.title("RA-Dec plane with interacting galaxies")
plt.xlabel("R.A. (degrees)")
plt.ylabel("Dec. (degrees)")
plt.xlim(360.4,356.5)
plt.ylim(-12.3,-8.3)
plt.legend(loc='upper center',bbox_to_anchor=(0.5, 1.02),ncol=5, fancybox=True, shadow=True)
plt.savefig("RA-Dec_plane_with_interacting_galaxies.png")
#plt.show()
#plt.close()

###################################################################################################################################################################################################		
############################################################################# RA-DEC PLOT only z ##################################################################################
###################################################################################################################################################################################################

ra_jf, dec_jf  = ra[final_class == 'JF'][table.redshift > 0], dec[final_class == 'JF'][table.redshift > 0]
ra_jm, dec_jm  = ra[final_class == 'JM'][table.redshift > 0], dec[final_class == 'JM'][table.redshift > 0]
ra_m, dec_m = ra[final_class == 'M'][table.redshift > 0], dec[final_class == 'M'][table.redshift > 0]
ra_pm, dec_pm = ra[final_class == 'PM'][table.redshift > 0], dec[final_class == 'PM'][table.redshift > 0]

jelly_rps_conf = rps_conf[final_class == 'JF'][table.redshift > 0]
merg_grav_conf = grav_conf[final_class == 'M'][table.redshift > 0]

plt.figure()
plt.gca().scatter(ra[table.redshift > 0],dec[table.redshift > 0],marker='.',s=150,c='gray',alpha=0.5)
im = plt.gca().scatter(ra_jf, dec_jf,marker='*',s=350,c=jelly_rps_conf.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues)
plt.gca().scatter(ra_m, dec_m,marker='p',s=300,c=merg_grav_conf.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues)


im = plt.gca().scatter(ra_jf, dec_jf,marker='*',s=300,c=final_jf_confs.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues,label="JF")
plt.gca().scatter(ra_m, dec_m,marker='p',s=150,c=final_m_confs.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues,label="M")
plt.gca().scatter(ra_jm, dec_jm,marker='v',s=300,c=final_jm_confs.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues,label="JM")
plt.gca().scatter(ra_pm, dec_pm,marker='^',s=300,c=final_pm_confs.tolist(),edgecolors='black',alpha=1.0,cmap=plt.cm.Blues,label="PM")


plt.colorbar(im,label='conf')
#cbar.set_label('conf', size=20)
#cbar.ax.tick_params(labelsize='large')

#plt.scplot(ra_jm, dec_jm, '*',color='darkred',markersize=15)
plt.xlim(360.1,356.5)
plt.show()
#plt.close()

