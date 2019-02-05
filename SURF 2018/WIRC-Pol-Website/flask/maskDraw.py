# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 18:03:08 2016

@author: kaew
draw and plot wircpol frame along with spectra positions given the sources locations
This can be overlaid on the FITS of a source.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits as f
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.visualization import LogStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from astropy import wcs
#from astropy.io.votable import parse_single_table
from astropy.utils.data import download_file
from scipy.ndimage import rotate
import requests
import fnmatch
from astropy.vo.client import conesearch
from astropy.vo.client.exceptions import VOSError

#plt.figure(figsize = (5,5))
###WIRCPOL specs
pxscale = 0.2487          #arcsec/pix
twomass_scale = 1.000008  #arcsec/pix
#length of spectra ~100 px
fov = 8.489 #wircpol FOV in arcmin
# spec_len = 1.5*60/twomass_scale #length of the spectra, check this ##OLD 
# spec_dist = 3.001*60/twomass_scale #distsance from the source to the center of the spectra in arcmin ##OLD
spec_len = 58 * pxscale / twomass_scale    #Kaew says it should be 58 WIRC pixels long. 
spec_dist = 455 * pxscale / twomass_scale  #Kaew says it should be centered at about 455 WIRC pixels away. 

def specs(source):
    """return the edges of the spectra given the location of the source.
    Use pixel coordinates here."""
    x = source[0]
    y = source[1]
    spec1 = ((x - spec_dist -  spec_len/2 , x - spec_dist + spec_len/2), \
        (y + spec_dist + spec_len/2, y + spec_dist - spec_len/2))
    spec2 = ((x + spec_dist -  spec_len/2 , x + spec_dist + spec_len/2), \
        (y + spec_dist - spec_len/2, y + spec_dist + spec_len/2))
    spec3 = ((x - spec_dist -  spec_len/2 , x - spec_dist + spec_len/2), \
        (y - spec_dist - spec_len/2, y - spec_dist + spec_len/2))
    spec4 =((x + spec_dist -  spec_len/2 , x + spec_dist + spec_len/2), \
        (y - spec_dist + spec_len/2, y - spec_dist - spec_len/2))
    return (spec1,spec2,spec3,spec4)

def maskDraw(sources, mags, color , with_spec = True, alpha = 0.2):
    """Draw circles at where sources in the frame are along with the spectra it 
    will produce, if with_spec = True. If not, only draw circle. the input format is a list
    of pair (x,y). Use pixel location."""
    #plt.figure(figsize = (10,10))
    mags = np.array(mags)
    for j,i in enumerate(sources):
        mark = plt.Circle(i,radius = 7, color = color, fill = False)
        plt.gca().add_patch(mark)
        if with_spec:
            spec = specs(i)
        
        if color != 'r':
            plt.text(i[0]+5, i[1]+7, "{:0.2f}".format(mags[j]), color=color, fontsize=4)
        for j in spec:
            s = plt.Line2D(j[0], j[1], lw = 3, alpha = alpha, color = color) 
            plt.gca().add_line(s)
        #print(spec[0])
        
#maskDraw([(0,0), (-0.1,0.5), (0.2,0.3)])
#maskDraw([(0,0),(-0.1,0.3),(0.2,-0.1)])
#plt.xlim([-2,2])
#plt.ylim([-2,2])
#plt.show()
        
def drawFrame(ra, dec, target, sources, mags, band, outname = 'frame.pdf', target_name=None):
    """drawFrame takes the pointing ra,dec, call fetch2mass to get the FITS image 
    of the area, plot the FoVs of WIRCPOL. Then from the list of sources+target, 
    plot the resulting spectra."""
    
    #######Fetch and show a 2MASS image from the given position#############
    image_fits = fetch2mass(ra,dec,band)
    file = f.open(image_fits)
    w = wcs.WCS(image_fits)
    image = file[0].data
    vmin = np.min(image[~np.isnan(image)])
    vmax = np.max(image[~np.isnan(image)])
    #do this later so it doesn't affect stretching
    image = np.nan_to_num(image)
    #position angle
    pa = 0
    image = rotate(image, pa)
    #normalization
    norm = ImageNormalize(vmin = 1.0*vmin, vmax = 0.4*vmax, stretch = LogStretch())
    #show image, inverted, grayscale, nomalized
    fig = plt.figure(figsize = (6,6))
    #projection = w is to use WCS as axes
    fig.add_subplot(111, projection = w)
    im= plt.imshow(image ,origin = 'lower', norm = norm, cmap = 'gray_r')
    

    ########Now, mark the FOV of the WIRC camera
    center_pix = w.all_world2pix(np.array([[ra,dec]]),0)[0]
    x = center_pix[0]
    y = center_pix[1]
    side = fov*60/2/twomass_scale #each half height of the FOV.
    wirc_side = fov*60/2/twomass_scale
    detector = plt.Polygon(np.array([ [x-side, y+side], [x+side, y+side],\
                            [x+side, y-side], [x-side, y-side]]), \
                            fill = False, color = 'k')
    plt.gca().add_patch(detector)
    # im.set_extent([x-side, x+side, y-side, y+side])
    

    ########Mark the opening of the mask in the middle of the detector
    side = side/2 #this is the mask side
    mask = plt.Polygon(np.array([ [x-side, y+side], [x+side, y+side],\
                            [x+side, y-side], [x-side, y-side]]), \
                            fill = False, color = 'k')
    plt.gca().add_patch(mask)  
    ########Mark the sources near this target, filter sources to only those in the mask
    if(sources != []):
        sources_pix = w.all_world2pix(sources,0)
        sources_pix_enclosed = []
        mags_enclosed = []
        for j,i in enumerate(sources_pix):
            # if mask.contains_point(i):
            sources_pix_enclosed = sources_pix_enclosed +[i]
            mags_enclosed.append(mags[j])
        #sources_pix = sources_pix[mask.contains_point(sources_pix)]  
        maskDraw(np.array(sources_pix_enclosed), np.array(mags_enclosed), color = 'b') 
    
    #######Mark all targets and show the spectral lines.
    #for i in target: #should be order pairs of ra/dec in decimal degree
    target_pix = w.all_world2pix(target,0)   
    #print(target_pix)
    maskDraw(target_pix, ['Target'], color = 'r', alpha =0.8)

   ######## Add the mask obscurations
    # Horizontal Width = 61 pixels. 
    spider_width=61/4. #The width of the spiders is 61 pixels on the WIRC camera, but the image is in 2MASS coordinates which has a pixel scale of about 1arsecond/pixel. So divid by four. 
    # print target_pix
    im_shape = np.shape(image) 
    # plt.plot([target_pix[0][0]+spider_width/2.,x+side+spider_width/2.], [target_pix[0][1],y+side])
    plt.plot([target_pix[0][0]+spider_width/2.,x+side], [target_pix[0][1],y+side-spider_width/2.], color='k')
    plt.plot([target_pix[0][0]+spider_width/2.,x+side], [target_pix[0][1],y-side+spider_width/2.], color='k')
    plt.plot([target_pix[0][0]-spider_width/2.,x-side], [target_pix[0][1],y+side-spider_width/2.], color='k')
    plt.plot([target_pix[0][0]-spider_width/2.,x-side], [target_pix[0][1],y-side+spider_width/2.], color='k')
    plt.plot([target_pix[0][0],x-side+spider_width/2.], [target_pix[0][1]+spider_width/2.,y+side], color='k')
    plt.plot([target_pix[0][0],x+side-spider_width/2.], [target_pix[0][1]+spider_width/2.,y+side], color='k')
    plt.plot([target_pix[0][0],x-side+spider_width/2.], [target_pix[0][1]-spider_width/2.,y-side], color='k')
    plt.plot([target_pix[0][0],x+side-spider_width/2.], [target_pix[0][1]-spider_width/2.,y-side], color='k')
    
    # im.set_extent([x-wirc_side, x+wirc_side, y-wirc_side, y+wirc_side])
    # im.set_extent([x-side, x+side, y-side, y+side])
    # plt.xlim([-100,600])
    plt.xlim([x-wirc_side, x+wirc_side])
    plt.ylim([y-wirc_side, y+wirc_side])
    # plt.ylim([-100,600])

    # if target_name != None:
    plt.title(target_name)

    try:
        plt.savefig(outname, format = 'png') #for now!
    except:
        pass
    # plt.savefig(outname+.png)


#drawFrame(127.277667, +14.939583, np.array([[127.277667, +14.939583],[127.30625,14.939602]]), [], 'J')
    
#This function retreive FITS for a source at the given ra/dec
#To be written

def fetch2mass(ra, dec, band):
    """fetch a 2MASS image around the given ra, dec in decimal degrees
    and a string for the desired band ('J', 'H', or 'K') """
    base = "http://irsa.ipac.caltech.edu/ibe/sia/twomass/allsky/allsky?"
    pos = "POS=%f,%f"%(ra,dec)
    size = "&size="+str(9.5/60) #size of the search, square a bit bigger than WIRC fov of 8'
    intersect = "&INTERSECT=CENTER"    
    xml = (requests.get(base+pos+size+intersect)).text
    #This is very ad-hoc. Use a proper xml parsing in a revision!
    xml = xml.split('<TD>')
    for i in range(len(xml)):
        if fnmatch.fnmatch(xml[i], '2MASS All-Sky Data Release*'+band+'*'):
            link = (xml[i+1].split("</TD>")[0])
    link = link+'?center=%f,%fdeg&size=9.5arcmin&gzip=false'%(ra,dec)
    #print(fits)
    fits = download_file(link)
    return fits
    
#This function queries the 2MASS point source catalog for neighboring sources
#around the given location within the FOV. Note that the target might also be 
#included in the search result. 

def query2mass(ra, dec, fov2mass = fov/4*u.arcmin):
    """
    Inputs: RA and dec in degree decimal
    Output:     A table containing neighboring sources and the associated data 
                from the 2MASS PSC including the coordinates and the mags
    Sample usage: 
            result = query2mass(120,30) 
    Key columns: result['ra'], ['dec'], ['j_m'], ['h_m'],['k_m'], ['j_msigcom'], etc. 
    Check for None return
    This should be updated to work on Python 3.5"""
    # tmass_psc = 'Two Micron All Sky Survey (2MASS) 1' #Old Name
    # tmass_psc = '2MASS All-Sky Catalog of Point Sources (Cutri+ 2003)'
    tmass_psc = 'http://vizier.u-strasbg.fr/viz-bin/votable/-A?-out.all&-source=II/246/out&' #The catalog we're using
    c = SkyCoord(ra = ra*u.degree, dec = dec*u.degree) #make a SkyCoord object
    # res = conesearch.conesearch(c, fov*u.arcmin, catalog_db = tmass_psc, verbose = True)
    try: #conesearch doesn't work sometimes. Use this to handle exceptions
        res = conesearch.conesearch(c, fov2mass, catalog_db = tmass_psc, verbose = True)
        return res.array.data
    except VOSError:
        return None
    


#print(query2mass(120,30))

#Now, put them all together. findingChart takes in only RA/Dec and the band, and
#create a pdf of the finding chart with all fovs and masks on top with all 
#neighboring sources brighter than maglim.
def findingChart(ra,dec, band, maglim, target_name = None, output_prefix = '', fov2mass = fov/4*u.arcmin):
    """
    Inputs: RA and dec in degree decimal
            Band ('J', 'H', or 'K')
            maglim is the magnitude of the dimmest neighboring source to include in the chart.
                This is usually related to the brightness of the target.
    Output: A PDF of the finding chart
    """
    #First create a source list. Try querying max 10 times
    res = None
    i = 0
    while res == None and i < 10:
        print('Querying 2MASS')
        res = query2mass(ra,dec, fov2mass = fov2mass) 
        i = i+1
    #loop through the results and create the source array
    sources = []
    mags = []
    # print(type(res))
    # print(res.dtype.names)
    for k in res:
        # print(type(k[band+'mag']))
        # if (k[band+'mag'] < float(maglim)) and (k[band+'cmsig'] > float(0.0)):
        if (k[band+'mag'] < float(maglim)):
            #Mag cut and make sure it's not a limit in the 2mass catalog
            sources = sources +  [[k['RAJ2000'], k['DEJ2000']]]
            mags.append(k[band+'mag'])
    sources = np.array(sources)
    print(sources)
    mags = np.array(mags)

    
    #Now we have an array of sources. The array of target is, for now, just
    target = np.array([[ra,dec]])
    
    drawFrame(ra,dec, target, sources, mags, band, output_prefix+'finding_chart_'+str(ra)+'_'+str(dec)+band+'.png', target_name=target_name)
    

#######################################################
### Main ###
if __name__ == "__main__":
    findingChart(247.327305  , 3.5932, 'J',  14.0, target_name = "Test Target Name", output_prefix='test')
#findingChart(267.599375 ,  42.377028, 'J', 17.0)
#findingChart(324.86154  , 2.339638, 'J', 16.0)
            
    plt.show()    


    