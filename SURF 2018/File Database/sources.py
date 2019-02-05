import wirc_drp.wirc_object as wo
import wirc_drp.utils.image_utils as IU
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import astropy.io.ascii as asci
import os
import importlib
import glob

def process_sources(calib_objs, date='', sources=False):
    '''
    Find the sources in the given calibrated images. Then, find cutouts, extract spectra,
    plot Q and U, and save various images to appropriate files.

    Params:
    calib_objs: Either a list of wirc_data objects or a blank list to be populated
    date: The date (YYYYMMDD), if needed to populate calib_objs
    sources: A boolean representing whether or not the pipeline is only processing sources

    Return:
    The list of calibrated objects, now modified with source information, if any
    '''
    # If the sources command line argument is active
    if sources:
        # If there are no calib_objs, then the user only gave a date
        if len(calib_objs) == 0:
            calib_objs = list(glob.glob('Calibrated Files/' + date + '/Auto_Reduced/*'))
        else:
            # Else, the user entered files with the -f argument
            for i in range(len(calib_objs)):
                calib_objs[i] = 'Calibrated Files/' + date + '/Auto_Reduced/' + calib_objs[i].split('/')[-1]
        # Load wirc objects for the necessary files (passed or from directory)
        calib_names = calib_objs
        calib_objs = []
        for name in calib_names:
            try:
                object = wo.wirc_data(wirc_object_filename=name)
                object.sky_fn = object.header['SKY_FN']
                object.raw_filename = object.header['RAW_FN']
                calib_objs.append(object)
            except KeyError:
                pass

    print('STARTING SOURCE PROCESSING')
    # Initialize the paths for the reduced data output
    plots_root = 'Reduced Data/Plots/' + date + '/'
    traces_root = 'Reduced Data/Trace Spectra/' + date + '/'
    cutouts_root = 'Reduced Data/Cutouts/' + date + '/'
    ex_cutouts_root = 'Reduced Data/Extracted Cutouts/' + date + '/'
    for root_path in [plots_root, traces_root, cutouts_root, ex_cutouts_root]:
        if not os.path.exists(root_path):
            os.makedirs(root_path)
    for obj in calib_objs:
        # Differentiate the process for sky files(skip),
        # science images with no sky file(perform no subtraction), and ones with
        # sky files (perform a subtraction)
        try:
            test = obj.header['SKY_FN']
            if test == 'None':
                data = obj.full_image
                sky_fn = None
            else:
                sky_data = fits.open(obj.sky_fn)
                sky = sky_data[0].data
                sky_data.close()
                data = obj.full_image - sky
                sky_fn = obj.sky_fn
        except KeyError:
            continue
        # Find sources in the image
        obj.find_sources(data, sky=sky_fn, threshold_sigma=5, plot=False, im_package='scipy', mode='pol', verbose=False)
        # print(obj.source_list)
        # Process each source for the given object
        for i, source in enumerate(obj.source_list):
            # Create specific file_paths for the data which will be gathered
            plots_path = plots_root + obj.raw_filename.split('/')[1][:-5] + '_Q_U_Plot{}.png'.format(i)
            trace_path = traces_root + obj.raw_filename.split('/')[1][:-5] + '_Spectra{}.png'.format(i)
            cutouts_path = cutouts_root + obj.raw_filename.split('/')[1][:-5] + '_Cutouts{}.png'.format(i)
            ex_cutouts_path = ex_cutouts_root + obj.raw_filename.split('/')[1][:-5] + '_ExCutouts{}.png'.format(i)
            # Get cutouts
            source.get_cutouts(obj.full_image, obj.DQ_image, obj.filter_name, replace_bad_pixels=True, method='interpolate', verbose=True)
            # Use the plot_cutouts() function to save cutout plots to disk
            source.plot_cutouts(output_name=cutouts_path, show=False)
            # Extract spectra
            source.extract_spectra(plot=False)
            # Use the plot_trace_spectra() function to save trace spectra plots to disk
            source.plot_trace_spectra(output_name=trace_path, show=False)
            # Use the plot_extracted_cutouts() function to save extracted cutout plots to disk
            source.plot_extracted_cutouts(output_name=ex_cutouts_path, show=False)
            # Calibrate and generate the Stokes Q and U plot for this source
            source.rough_lambda_calibration(method=2)
            source.compute_polarization(cutmin=20, cutmax=150)
            source.plot_Q_and_U(output_name=plots_path, show=False)
        #save_cutouts(obj, date)
        obj.save_wirc_object(obj.header['CAL_FN'])
    print('FINISHED PROCESSING SOURCES')
    return calib_objs
