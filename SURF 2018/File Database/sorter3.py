#sorter3.py
#call using 'python sorter3.py'



#================================================
#================================================
#Imports
import numpy as np
from astropy.io import fits

import wirc_drp.wirc_object as wo
from wirc_drp.utils import calibration

from sets import Set
from itertools import groupby
from operator import itemgetter
from collections import Counter


import os
import glob

import sys

import pdb #python debugger

#================================================
#================================================
#maybe make it so that user iputs data_path +typ_basename i.e:
#glob_string = raw_input ('User enters data_path + typ_basename, i.e /hcig1-nas/wircpol/data/20170613/wirc????.fits)

wircpol_dir = os.environ['WIRC_DRP'] # Your WIRCPOL_DRP directory (with a "/" at the end!)

default_data_dir = '/hcig1-nas/wircpol/data/'


date = '20170222'
#date = '20170409'
#date = '20170714'
#date = '20170712'

#for testing on hcig1
#data_path = default_data_dir + date +'/'

#for testing on personal computer
# data_path = date + '/'


# fn_prefix = 'wirc' #usually 'wirc'?
# len_prefix = len(fn_prefix)
# frame_n_digits = 4 #number of digits left open in frame number ie 0003 is 4, while 004 is 3, etc
# frame_n_placeholder = '?' * frame_n_digits #makes place holder of ?'s as long as frame_n_digits, so '????'
# f_type = '.fits' #file type (always '.fits')
# typ_basename = fn_prefix + frame_n_placeholder + f_type
# print ('Grabbing raw data from: ' + data_path + typ_basename)
# #print ('Grabbing raw data from: ' + data_path_style)

# path_fn_list = sorted(glob.glob(data_path + typ_basename)) #ordered list of add on with file name, like 'sample_data/wirc0001.fits'

# #path_fn_list = sorted(glob.glob(data_path_style)) #ordered list of add on with file name, like 'sample_data/wirc0001.fits'
# fn_list= [os.path.basename(string) for string in path_fn_list] #list comprehension for file name, like 'wirc0001.fits'
# frame_n = [int(fn[len_prefix:len_prefix+frame_n_digits]) for fn in fn_list] #list comprehension of frame number, derived from file name

# #-----------------------------------------------------------

# #initiate lists of header values from fits files
# exp = []   #exposure time list
# fore = []     #fore filter list
# aft = []      #aft filter list
# focus = []        #telefocus position list #used to determine focus_grouping and after_new_focus
# airmass = []      # listairmass  number >=1 which for some reason is a string
# HA = []            #hour angle string list #used to determine whether not tracking, HA grouping
# RA = []       #right ascension #used to determine if no slew has happened, RA_grouping
# DEC = []    #declination
# TIME = []   #local time for some reason
# UTSHUT = []  #weird string for date and time

# #initializing values, including defaults
# for i in range(len(fn_list)):


#     #initializing values from header
#     hdu = fits.open(path_fn_list[i])
#     exp.append(hdu[0].header["EXPTIME"])
#     fore.append(hdu[0].header["FORE"].split(' ')[0]) #split may not be necessary
#     aft.append(hdu[0].header["AFT"].split(' ')[0]) #split may not be necessary
#     focus.append(float(hdu[0].header["TELFOCUS"].split(' ')[0]))
#     airmass.append(hdu[0].header["AIRMASS"])
#     HA.append(hdu[0].header["HA"])
#     RA.append(hdu[0].header["RA"])
#     DEC.append(hdu[0].header["DEC"])
#     TIME.append(hdu[0].header["TIME"])
#     UTSHUT.append(hdu[0].header["UTSHUT"])
#     hdu.close()

# #============================================================================
# #stuff for finding observation type

#-----------------------------------------------------------
#function delta_arcsec
def delta_arcsec(angle2_string,angle1_string,angle_type):
    #finds total difference in arcseconds between angle2 and angle1
    #called by id_angular_groupings (using either method) (typically for RA and HA, but also works for DEC)
    #for obvious reasons, if using RA and angle2-angle1 > 2*pi, this function doesnt make sense
    #for obvious reasons, if using HA or DEC and abs(angle2 or angle1) are >pi/2 or on the horizon, this function doesnt make sense
    #24 hours = 86400 arcseconds
    #360 decrees = 324000 arcseconds
    d_arcsec = 0
    if (angle_type == 'HA'):
        #pdb.set_trace()
        if (angle1_string[0] == 'W'):
            sign = 1.0
            #print ("did W")
        elif (angle1_string[0] == 'E'):
            sign = -1.0
            #print ("did E")
        HA1_h = float(angle1_string.split(':')[0][1:3])
        HA1_m = float(angle1_string.split(':')[1])
        HA1_s = float(angle1_string.split(':')[2])
        arcsec1 = sign*float((60*60*HA1_h) + (60*HA1_m) + HA1_s)

        if (angle2_string[0] == 'W'):
            sign = 1.0
        elif (angle2_string[0] == 'E'):
            sign = -1.0
        HA2_h = float(angle2_string.split(':')[0][1:3])
        HA2_m = float(angle2_string.split(':')[1])
        HA2_s = float(angle2_string.split(':')[2])
        arcsec2 = sign*float((60*60*HA2_h) + (60*HA2_m) + HA2_s)

        ####????
        d_arcsec = arcsec2-arcsec1





    elif (angle_type == 'RA'):
        RA1_h = float(angle1_string.split(':')[0])
        RA1_m = float(angle1_string.split(':')[1])
        RA1_s = float(angle1_string.split(':')[2])
        arcsec1 = float((60*60*RA1_h) + (60*RA1_m) + RA1_s)

        RA2_h = float(angle2_string.split(':')[0])
        RA2_m = float(angle2_string.split(':')[1])
        RA2_s = float(angle2_string.split(':')[2])
        arcsec2 = float((60*60*RA2_h) + (60*RA2_m) + RA2_s)

        d_arcsec = arcsec2-arcsec1



    elif (angle_type == 'DEC'):
        sign = 1.0
        if (angle1_string[0] == '-'):
            sign = -1.0
            DEC1_d = float(angle1_string.split(':')[0][1:3])
        else:
            DEC1_d = float(angle1_string.split(':')[0])
        DEC1_m = float(angle1_string.split(':')[1])
        DEC1_s = float(angle1_string.split(':')[2])
        arcsec1 = sign*float((60*60*DEC1_d) + (60*DEC1_m) + DEC1_s)

        if (angle2_string[0] == '-'):
            sign = -1.0
            DEC2_d = float(angle2_string.split(':')[0][1:3])
        else:
            DEC2_d = float(angle2_string.split(':')[0])
        DEC2_m = float(angle2_string.split(':')[1])
        DEC2_s = float(angle2_string.split(':')[2])
        arcsec2 = sign*float((60*60*DEC2_d) + (60*DEC2_m) + DEC2_s)

        d_arcsec = arcsec2-arcsec1
    else:
        print ("improper angle_type designated, returning 0")


    return d_arcsec

#-----------------------------------------------------------
#function id_angular_groupings
def id_angular_groupings(angle_list, max_variance, angle_type, grouping_type, reverse):
    #called for determining tight hard groupings of HA (hour angle), probably used for determining if tracking
    #called for determining soft groupings in RA (Right ascension), probably used for determining if fields of view are contiguos, ie not during slew

    #angle_list is a list of strings that represent angles that are iterated through and used in delta_arcsec
    #angle_type is a string designated the type of angle ('HA', 'RA', 'DEC'), as they have slightly different conventions
    #max_variance is a float for the the abs(difference)<= max_variance that is allowable, in arcseconds
    #grouping_type is a string for the type of grouping, consecutively similar ('soft') and radially similar('hard') to value_ref (first or last value in group)
    #reverse is a boolean for whether it is iterated in reverse (only important if max_variance is very small and grouping type is 'hard') #*****POSSIBLY remove this capability?

    #calls delts_arcsec,
    #    passes along angle1_string and angle2_string (found in angle_list).
    #    passes along angle_type ('HA', 'RA', 'DEC')

    grouping_list = ['f']*len(angle_list) #initiates list of default 'f' for False
    grouping_n_c = -1 #starts at negative one because in the loop it always adds 1 first


    #applies reversed or not reversed

    if reverse == True:
        index_list = reversed(range(len(angle_list))) #list of length L ie [L-1, L-2, L-3,...2,1,0]
        c = +1 #c for relative location of comparison index, +1 in this case, referenced as angle_list[i+c]
    else:
        index_list = range(len(angle_list)) #list of length L ie [0,1,2,...L-3, L-2, L-1]
        c = -1 #c for relative location comparison index, -1 in this case, referenced as angle_list[i+c]

    i_start = index_list[0] #usually 0, L-1 if reverse==True

    #starts grouping sequence
    for i in index_list:
        #if first index, it will pass #kinda weird, what about just if i != i_start do the else thingy, get rid of pass
        if (i == i_start):
            pass
        #else, it will do comparison, assignment of i, and possibly retroactive assignment of i+c
        else:
            #grouping check
            if angle_list[i] == '' or angle_list[i + c] == '':
                continue
            #calculate d_angle *** can i make this sleeker?
            #----if hypothetically angle_list[i+c] was first instance of grouping
            if (grouping_list[i+c] == 'f'):
                d_angle = abs(delta_arcsec(angle_list[i],angle_list[i+c],angle_type))
                ref_value = angle_list[i+c]
            #----if possibly part of grouping
            #--------if grouping_type == 'hard'
            elif (grouping_type == 'hard'):
                d_angle = abs(delta_arcsec(angle_list[i],ref_value,angle_type))
            #--------if grouping_type == 'soft'
            elif (grouping_type == 'soft'):
                d_angle = abs(delta_arcsec(angle_list[i],angle_list[i+c],angle_type))
            else:#debugging purposes.
                print ('bad grouping type') #debugging purposes
            # d_angle has been calculated
            #finds if i is in group with i+c
            if (d_angle <= max_variance):
                #if i+c was first instance of the group
                if (grouping_list[i+c] == 'f'):

                    grouping_n_c += 1 #new group

                    #retroactively asigns grouping to i+c
                    grouping_list[i+c] = str(grouping_n_c)

                #asigns grouping to i
                grouping_list[i] = str(grouping_n_c)

            else:
                pass

    return grouping_list

#-----------------------------------------------------------
#function id_discrete_groupings
def id_discrete_groupings(data_list):
    #called for determining equal groupings of discrete data (difference = 0)
    #focus_list is a list of strings that represent focus positions that are iterated through

    grouping_list = ['f']*len(data_list) #initiates list of default 'f' for False
    grouping_n_c = -1 #starts at negative one because in the loop it always adds 1 first


    index_list = range(len(data_list)) #list of length L ie [0,1,2,...L-3, L-2, L-1]
    c = -1 #c for relative location comparison index, -1 in this case, referenced as data_list[i+c]

    i_start = index_list[0] #usually 0

    #starts grouping sequence
    for i in index_list:
        #if first index, it will pass #kinda weird, what about just if i != i_start do the else thingy, get rid of pass
        if (i == i_start):
            pass
        #else, it will do comparison, assignment of i, and possibly retroactive assignment of i+c
        else:
            """
            if (grouping_list[i+c] == 'f'):
                d_data = abs(data_list[i]-data_list[i+c])
                value_0 = focus_list[i+c]

            else:
                d_data = abs(data_list[i]-value_0)

            #pdb.set_trace()
            """
            #if (d_data == 0): #if i is in group with i+c
            if (data_list[i] == data_list [i+c]):

                #if i+1 is 1st instance of the group (and thus is not yet labeled as member of group)
                if (grouping_list[i+c] == 'f'):
                    grouping_n_c += 1 #new group
                    grouping_list[i+c] = str(grouping_n_c)



                grouping_list[i] = str(grouping_n_c)

            else:
                pass

    return grouping_list


#-----------------------------------------------------------
#function get_after_new_focus
def get_after_new_focus(focus_grouping, RA_grouping):
    #looks at all consecutive 'f' values for focus_grouping(meaning that the focus position is changing)
    #for each set of consecutive 'f' values, if the set is included in a loose RA_grouping (of non 'f's),
    #the RA sequence is a focusing set (to include/exclude the acquisitions in the focusing sequence)
    #if this is the first focusing set of the run, includes everything before this focusing sequence, just to be extra rigorous


    #initializes the after_new_focus list as by default false
    after_new_focus =[True]*len(focus_grouping)
    #print ('len(focus_grouping', len(focus_grouping))

    #gets indices of all instances of 'f' in focus_grouping, using a list comprehension (bad idea possibly?)
    focus_ind_not_grouped = [i for i, j in enumerate(focus_grouping) if j == 'f']
    #print ('focus_ind_not_grouped' , focus_ind_not_grouped);

    #makes list of lists of consecutive 'f's in focus_grouping
    focus_ind_consecutive= []
    for k, g in groupby(enumerate(focus_ind_not_grouped), lambda (i, x): i-x):
        focus_ind_consecutive.append(map(itemgetter(1), g))

    #print ('focus_ind_consecutive', focus_ind_consecutive);

    #makes a list of all the non 'f' values that occur in RA_grouping
    RA_values = list(Set(RA_grouping))
    #print ('RA_values', RA_values)
    while 'f' in RA_values:
        RA_values.remove('f')
    #print ('RA_values', RA_values)

    #makes list of lists of consecutive similar RA values, by iterating through each value in RA_values
    #using a list comprehension (bad idea possibly?)
    RA_ind_consecutive=[]
    for value in RA_values:
        RA_ind_grouped = [i for i, j in enumerate(RA_grouping) if (j == value)]

        #print ('RA_value: ' + value + 'RA_ind_grouped',RA_ind_grouped);
        RA_ind_consecutive.append(RA_ind_grouped)
    #print ('RA_ind_consecutive')


    #iterates through RA_ind_consecutive to each RA_ind_sublist
    #*****POSSIBLY very inefficient?
    for RA_ind_sublist in RA_ind_consecutive:

        #While in each RA_ind_sublist, iterates through each focus_ind_sublist in focus_ind consecutive and compares
        for focus_ind_sublist in focus_ind_consecutive:

            #comparing the set of focus_ind_sublist and RA_ind_sublist
            #forms intersection list
            intersection_subset = Set(focus_ind_sublist) & Set(RA_ind_sublist)
            intersection_sublist = list(intersection_subset)

            #If there is intersection
            if (len(intersection_sublist) > 0):
                if (focus_ind_sublist) == (focus_ind_consecutive[0]):
                    first = 0

                #if occurse after the first focusing sequence, first indice is set to the start of the contiguous RA sublist
                else:
                    first = intersection_sublist[0]


                last = intersection_sublist[len(intersection_sublist)-1]

                #designates images that are not after a focus sequence as false
                after_new_focus[first:last+1]=[False]*len(after_new_focus[first:last+1])
                #print ('len(after_new_focus) ',len(after_new_focus), ' first:last+1 ', first, last+1, ' first +1 - last ', first +1 - last)

            else:
                pass


    return after_new_focus


# #-----------------------------------------------------------

# #Make important groupings

# #----finds very tight HA groupings to determine if telescope is not moving, ie not tracking   #does 1 full iteration
# not_tracking_HA_groupings = []
# if len(HA) > 0:
#     not_tracking_HA_groupings = id_angular_groupings(HA,1.0,'HA','hard',False)

# #----finds very loose contiguous RA groupings to organize images of fields that are angularly similar
# #--------used for get_after_new_focus() #does 1 full iteration
# contiguous_RA_groupings = []
# if len(RA) > 0:
#     contiguous_RA_groupings = id_angular_groupings(RA,4.0*60.0,'RA','soft', False)

# #----finds groupings of focus with equal values, used for get_after_new_focus() #does 1 full iterations
# focus_groupings = []
# if len(focus) > 0:
#     focus_groupings = id_discrete_groupings(focus)

# #----figures out if images take place after the first focusing set and contiguous focusing sets.
# #--------iterations weird, but most of sorting is already done by finding the RA and focus groupings
# after_new_focus = get_after_new_focus (focus_groupings, contiguous_RA_groupings)

# #-----------------------------------------------------------


# #initiate default candidacies # *****POSSIBLY remove all type_cand references... not really necessary

# #----boolean list if candidate for being labeled as dark
# dark_cand = [False]*len(fn_list)

# #----boolean list if candidate for being labeled as flat (discontinued because PG flats may be used, and are weird)
# flat_cand = [False]*len(fn_list)

# #----boolean list if candidate for being labeled as photometry
# photomet_cand = [False]*len(fn_list)

# #----boolean list if candidate for being labeled as spectroscopy
# spec_cand = [False]*len(fn_list)

# #----boolean list if candidate for being labeled as polarimetry
# pol_cand = [False]*len(fn_list)

# #-----------------------------------------------------------


# #sets observation type (obt) to 'UNKNOWN' by default
# obt = ['UNKNOWN']*len(fn_list)

# #-----------------------------------------------------------






# #sorting candidacies
# ind = range(len(fn_list))
# for i in ind:

#     # *****POSSIBLY reconsider how if statements are organized

#     #if dark
#     if ((fore[i] == 'BrGamma__(2.17)') and (aft[i] == 'J__(1.25)')):
#         dark_cand[i] = True

#         obt[i] = 'dark'

#     #if flat (using not_tracking_HA_groupings, 'not_tracking' and != 'f' is sorta a double negative)
#     elif ((not_tracking_HA_groupings[i] != 'f') and (fore[i] in ['OPEN', 'PG', 'GRISM'])):
#           flat_cand[i] = True

#           obt[i] = 'flat'


#     #if tracking
#     elif (after_new_focus[i] == True):

#         #if photometry
#         if ((fore[i] in ['Diffuser', 'OPEN']) and (aft[i] in ['J__(1.25)', 'H__(1.64)', 'Ks__(2.15)'])):
#             photomet_cand[i] = True

#             obt[i] = 'photomet'

#         #if spectroscopy
#         elif ((fore[i] == 'GRISM') and (aft[i] in ['J__(1.25)', 'H__(1.64)', 'Ks__(2.15)'])):
#             spec_cand[i] = True

#             obt[i] = 'spec'

#         #if polarimetry
#         elif ((fore[i] == 'PG') and (aft[i] in ['J__(1.25)', 'H__(1.64)', 'Ks__(2.15)'])):
#             pol_cand[i] = True

#             obt[i] = 'pol'


#         else:

#             #usually nothing fits this case
#             #if something does fit this case, its probably acquisitions and skies and (useless?) sciences
#             #where observer forgot to change filter to typical positions
#             pass
#     else:

#         #should be only focus?
#         pass

#     print (i, fn_list[i],obt[i],fore[i],aft[i],exp[i],HA[i], RA[i],contiguous_RA_groupings[i],focus[i], focus_groupings[i],after_new_focus[i])

# DAT =  np.column_stack((np.asarray(ind), np.asarray(fn_list), np.asarray(obt), np.asarray(fore), np.asarray(aft), np.asarray(exp), np.asarray(HA), np.asarray(RA), np.asarray(contiguous_RA_groupings), np.asarray(focus), np.asarray(focus_groupings), np.asarray(after_new_focus)))


# save1_fn = 'sorter2_1_' + date + '.txt'
# np.savetxt(save1_fn, DAT, delimiter=" ", fmt="%s %s %s %s %s %s %s %s %s %s %s %s")


# print ('----------------------------------------------------------------')
# print ('')
# print ('Done sorting by observation type')

#=========================================================================

#stuff for matching science images with approprate flats




#------------------------
"""
obt_values_list = list(Set(obt))
print (obt_values_list)
while 'UNKNOWN' in obt_values_list:
    obt_values_list.remove('UNKNOWN')
print (obt_values_list)

#initiating lists of lists of indices of each value in initial list
obt_values_ind = []
fore_values_ind = []
aft_values_ind = []
exp_values_ind = []

contains_dark = False
contains_flat = False
contains_pol = False
contains_spec = False
contains_photomet = False

if ('dark' in obt_values_list):
    contains_dark = True
if ('flat' in obt_values_list):
    contains_flat = True
if ('pol' in obt_values_list):
    contains_pol = True
if ('spec' in obt_values_list):
    contains_spec = True
if ('photomet' in obt_values_list):
    contains_photomet = True


cont = True
if (True not in [contains_pol, contains_spec, contains_photomet]):
    print ("There are images to be calibrated.")
if (True not in[contains_pol, contains_spec, contains_photomet]):
    print ("There are no images to be calibrated.")
    cont = False
if (contains_dark == False):
    print ("There are no darks.")
    cont = False
if (contains_flat == False):
    print ("There are no flats.")
    cont = False
"""
#---------------------------------------------------


#sorting_array = np.column_stack((np.asarray(obt), np.asarray(fore), np.asarray(aft), np.asarray(exp)))


#----------------------------------------------
#function get_observation_set_indices()
def get_obs_set_indices(unique_sub_a, sorting_array):


    shape_a = np.shape(unique_sub_a)
    obs_set_indices = []
    for i in range(shape_a[0]):
        if (unique_sub_a[i,3] == 'all'): #obs,fore,aft,ignore exp
            sub_obs_set_indices = np.where((sorting_array[:,0] == unique_sub_a[i,0]) & (sorting_array[:,1] == unique_sub_a[i,1]) & (sorting_array[:,2] == unique_sub_a[i,2]))[0]

        else: #obs,fore,aft,exp
            sub_obs_set_indices = np.where((sorting_array[:,0] == unique_sub_a[i,0]) & (sorting_array[:,1] == unique_sub_a[i,1]) & (sorting_array[:,2] == unique_sub_a[i,2]) & (sorting_array[:,3] == unique_sub_a[i,3]))[0]


        obs_set_indices.append(list(sub_obs_set_indices))

    return obs_set_indices



#------------------------------------------------------

#------------------------------------------------------
#function choose_darks()
def get_where_is_dark(unique_science_row, unique_dark_a, dark_obs_set_fn_list_list):


    where_dark_obs_set_fn_list = list(np.where(unique_dark_a[:,3] == unique_science_row[3])[0])

    if len(where_dark_obs_set_fn_list) < 1:
        print ('no matching dark images, returning a blank list')

    return where_dark_obs_set_fn_list[0]

#------------------------------------------------------
#function map_to_dark()
def get_map_to_dark(path_fn_list, sorting_array, obs_input = 'dark', fore_input = 'BrGamma_(2.17)', aft_input = 'J__(1.25)', fore_pick = 'input', aft_pick = 'input', exp_input = 1, exp_pick = 'same'):
    # path_fn_list is the list of all the filenaes (including full path)
    # sorting_array is the obstype, fore, aft, exposure time array of all the images
    # obs_input is the default observation type which in this case make sense to map always to dark
    # fore_input is the default fore position which makes sense to default to BrGamma
    # aft_input is the default aft position which makes sense to default to J
    # fore_pick just means pay attention to the fore_input rather than something else
    # aft_pick just means pay attention to the aft_input rather than something else
    # exp_input is the preferred exposuretime to map to (usually pointless unless exp_pick says "input"
    # exp_pick says whether you want to use, same, max, all, etc...


    #unique array of all existing permutations of observation type (obs), fore, aft, and exposure time (exp)
    unique_a = np.vstack({tuple(row) for row in sorting_array})


    unique_science_a = unique_a[list(np.where((unique_a[:,0] == 'pol')|(unique_a[:,0] == 'spec')|(unique_a[:,0] == 'photomet'))[0]),:]


    if (exp_pick == 'same'):
        unique_dark_a = unique_a[list(np.where(unique_a[:,0] == 'dark')[0]),:]
    elif (exp_pick == 'same'):
        #not really sure here.
        unique_dark_a = unique_a[list(np.where(unique_a[:,0] == 'dark')[0]),:]





    foo = unique_science_a
    shape_unique_science_a = np.shape(unique_science_a)
    for i in range(shape_unique_science_a[0]):
        obs = obs_input

        if (fore_pick == 'same'):
            fore = unique_science_a[i,1]
        else:
            fore = fore_input

        if (aft_pick == 'same'):
            aft = unique_science_a[i,2]
        else:
            aft = aft_input

        if (exp_pick == 'same'):
            exp = unique_science_a[i,3]
        else:
            exp = exp_input


        foo[i,:] = np.array([obs,fore,aft,exp])



    map_to_dark = foo


    if (exp_pick == 'same'):
        unique_map_to_dark = np.vstack({tuple(row) for row in foo[:,0:4]})
    elif (exp_pick == 'same'):
        #not really sure here...
        unique_map_to_dark = np.vstack({tuple(row) for row in foo[:,0:4]})

    shape_unique_dark_a = np.shape(unique_dark_a)

    shape_unique_map_to_dark = np.shape(unique_map_to_dark)

    masterDark_name_list = ['']*len(path_fn_list)
    bpmap_name_list = ['']*len(path_fn_list)
    for i in range(shape_unique_map_to_dark[0]):
        if (exp_pick == 'same'):
            dark_where_list = list(np.where((sorting_array == unique_map_to_dark[i,:]).all(axis=1))[0])
            map_backwards = list(np.where((map_to_dark == unique_map_to_dark[i,:]).all(axis=1))[0])
        elif (exp_pick == 'same'):
            #not really sure here
            dark_where_list = list(np.where((sorting_array == unique_map_to_dark[i,:]).all(axis=1))[0])
            map_backwards = list(np.where((map_to_dark == unique_map_to_dark[i,:]).all(axis=1))[0])

        matching_science_where_list = []
        for where in map_backwards:
            unique_row_of_unique_science_a = unique_science_a[where,:]
            matching_science_where_list.append(list(np.where((sorting_array == unique_map_to_dark[i,:]).all(axis=1))[0]))

        dark_fn_list = [path_fn_list[j] for j in dark_where_list]
        if len(dark_fn_list) > 0:
            darkname, bp_name = calibration.masterDark(dark_fn_list, output_dir='/calib_files/')

            for where in matching_science_where_list:
                masterDark_name_list[where] = darkname
                bpmap_name_list[where] = bp_name


    return masterDark_name_list, bpmap_name_list






#------------------------------------------------------
#function get_map_to_flat()
def get_map_to_flat(path_fn_list, sorting_array, obs_input = 'flat', fore_input = 'OPEN', aft_input = 'J__(1.25)', exp_input = 1, fore_pick = 'same', aft_pick = 'same', exp_pick = 'all'):
    # path_fn_list is the list of all the filenaes (including full path)
    # sorting_array is the obstype, fore, aft, exposure time array of all the images
    # obs_input is the default observation type which in this case make sense to map always to dark
    # fore_input usually irrelevant
    # aft_input usually irrelevant
    # fore_pick just means map to the same values rather than a specific value
    # aft_pick just means map to the same values rather than a specific value
    # exp_input is the preferred exposuretime to map to (usually pointless unless exp_pick says "input"
    # exp_pick says whether you want to use, same, max, all, etc...




    #unique array of all existing permutations of observation type (obs), fore, aft, and exposure time (exp)
    unique_a = np.vstack({tuple(row) for row in sorting_array})


    #gets unique array of all the science images (ie pol, spec or photomet)
    unique_science_a = unique_a[list(np.where((unique_a[:,0] == 'pol')|(unique_a[:,0] == 'spec')|(unique_a[:,0] == 'photomet'))[0]),:]

    if (exp_pick == 'all'):
        foo = unique_a[list(np.where(unique_a[:,0] == 'flat')[0]),:]
        unique_flat_a = np.vstack({tuple(row) for row in foo[:,:]})
    elif (exp_pick == 'max'):
        #same as 'all' for now... not sure
        foo = unique_a[list(np.where(unique_a[:,0] == 'flat')[0]),:]
        unique_flat_a = np.vstack({tuple(row) for row in foo[:,0:3]})
    elif (exp_pick == 'same'):
        unique_flat_a = unique_a[list(np.where(unique_a[:,0] == 'flat')[0]),:]

    flat_exp_max = np.amax(unique_flat_a[:,3].astype(float))






    foo = unique_science_a
    shape_unique_science_a = np.shape(unique_science_a)
    for i in range(shape_unique_a[0]):
        obs = obs_input

        if (fore_pick == 'same'):
            fore = unique_science_a[i,1]
        else:
            fore = fore_input

        if (aft_pick == 'same'):
            aft = unique_science_a[i,2]
        else:
            aft = aft_input

        if (exp_pick == 'all'):
            exp = 'all'
        elif (exp_pick == 'max'):
            exp = flat_exp_max
        elif (exp_pick == 'same'):
            exp = unique_science_a[i,3]
        elif exptime:
            exp = exp_input
        foo[i,:] = np.array([obs,fore,aft,exp])



    map_to_flat = foo

    if (exp_pick == 'all'):
        unique_map_to_flat = np.vstack({tuple(row) for row in foo[:,0:3]})
    elif (exp_pick == 'max'):
        #same as 'all' for now... not sure
        unique_map_to_flat = np.vstack({tuple(row) for row in foo[:,0:3]})
    elif (exp_pick == 'same'):
        unique_map_to_flat = np.vstack({tuple(row) for row in foo[:,0:4]})

    shape_unique_flat_a = np.shape(unique_flat_a)

    shape_unique_map_to_flat = np.shape(unique_map_to_flat)

    masterFlat_name_list = ['']*len(path_fn_list)
    bpmap_name_list = ['']*len(path_fn_list)
    for i in range(shape_unique_map_to_flat[0]):
        if (exp_pick == 'all'):
            flat_where_list = list(np.where((sorting_array[:,0:3] == unique_map_to_flat[i,0:3]).all(axis=1))[0])
            map_backwards = list(np.where((map_to_flat[:,0:3] == unique_map_to_flat[i,0:3]).all(axis=1))[0])

        elif (exp_pick == 'max'):
            flat_where_list = list(np.where((sorring_array[:,0:3] == unique_map_to_flat[i,0:3]).all(axis=1))[0])
            map_backwards = list(np.where((map_to_flat[:,0:3] == unique_map_to_flat[i,0:3]).all(axis=1))[0])

        elif (exp_pick == 'same'):
            flat_where_list = list(np.where((sorting_array == unique_map_to_flat[i,:]).all(axis=1))[0])
            map_backwards = list(np.where((map_to_flat == unique_map_to_flat[i,:]).all(axis=1))[0])

        matching_science_where_list = []
        #map backwards to the science images
        for where in map_backwards:
            unique_row_of_unique_science_a = unique_science_a[where,:]
            matching_science_where_list.append(list(np.where((sorting_array == unique_map_to_flat[i,:]).all(axis=1))[0]))

        flat_fn_list = [path_fn_list[j] for j in flat_where_list]


        if len(flat_fn_list) > 0:

            flatname, bp_name = calibration.masterFlat(flat_fn_list,sub_dir_name = '/calib_files/')
            #map to specific file names
            for where in matching_science_where_list:
                masterFlat_name_list[where] = flatname
                bpmap_name_list[where] = bp_name


    return masterFlat_name_list, bpmap_name_list








#------------------------------------------------------
#function superman2()
def superman2(path_fn_list,sorting_array):
    print('Hi')

    master_dark_name_list, bpmap_name_list = get_map_to_dark(path_fn_list, sorting_array)
    master_flat_name_list, bpmap_name_list = get_map_to_flat(path_fn_list, sorting_array)
    print('Master Dark List: ' + master_dark_name_list + '\nMaster Flat List: ' + master_flat_name_list + '\nBP Map List: ' + bpmap_name_list)






#function superman()
def superman(path_fn_list,sorting_array):

    #part A, prepare BEFORE making of master darks and flats and such

    #unique array of all existing permutations of observation type (obs), fore, aft, and exposure time (exp)
    unique_a = np.vstack({tuple(row) for row in sorting_array})

    #mapped_a
    #finds the row where the unique_a array has 'dark', flat' and ('pol','spec','photomet')
    unique_dark_a = unique_a[list(np.where(unique_a[:,0] == 'dark')[0]),:]
    unique_flat_a = unique_a[list(np.where(unique_a[:,0] == 'flat')[0]),:]
    unique_science_a = unique_a[list(np.where((unique_a[:,0] == 'pol')|(unique_a[:,0] == 'spec')|(unique_a[:,0] == 'photomet'))[0]),:]

    #finds the maximum exposure time in the case that the criteria for flats is max exposure time
    flat_exp_max = np.amax(unique_flat_a[:,3].astype(float))

    #gets the list of lists of indices
    dark_obs_set_indices_list_list = get_obs_set_indices(unique_dark_a, sorting_array)
    flat_obs_set_indices_list_list = get_obs_set_indices(unique_flat_a, sorting_array)
    science_obs_set_indices_list_list = get_obs_set_indices(unique_science_a, sorting_array)

    #converting lists of lists of indices to lists of lists of filenames
    #initiates lists of lists of filenames
    dark_obs_set_fn_list_list = []
    flat_obs_set_fn_list_list = []
    science_obs_set_fn_list_list = []

    #does the conversions by iterating thought the list of lists, and then appending the sorted list comprehnsion of the filenames from the indices
    for i in range(len(dark_obs_set_indices_list_list)):
        dark_obs_set_fn_list_list.append(sorted([path_fn_list[j] for j in dark_obs_set_indices_list_list[i]]))

    for i in range(len(flat_obs_set_indices_list_list)):
        flat_obs_set_fn_list_list.append(sorted([path_fn_list[j] for j in flat_obs_set_indices_list_list[i]]))

    for i in range(len(science_obs_set_indices_list_list)):
        science_obs_set_fn_list_list.append(sorted([path_fn_list[j] for j in science_obs_set_indices_list_list[i]]))


    #part B: make master darks and master flats and such

    #real deal
    #iterates through each row in the unique_science array and figues out what the corresponding dark images should be
    for i in range(np.shape(unique_science_a)[0]):
        #gets index for row of matching dark
        where_is_dark = get_where_is_dark(unique_science_a[i,:], unique_dark_a, dark_obs_set_fn_list_list)

        #gets fn_list
        dark_obs_set_fn_list = dark_obs_set_fn_list_list[where_is_dark]

        #gets indices list
        dark_obs_set_indices_list = dark_obs_set_indices_list_list [where_is_dark]
        print (i, dark_obs_set_fn_list)
        if len(dark_obs_set_fn_list) > 0:
            darkname, bp_name = calibration.masterDark(dark_obs_set_fn_list,output_dir= '/calib_files/')

            print (i, darkname, bp_name)


#------------------------------------------------------------


#do superman...
#superman(path_fn_list, sorting_array)


#superman2(path_fn_list,sorting_array)
