#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Time series analysis

    Require:
     - ITSA module
     - param_itsa.py

    To lauch use the following lines in terminal:
     - module load python/python3.9
     - python3 tsanalysis_itsa.py CODE
        *CODE correspond to the code of the station you want to analyse

    ----
    Developed at: ISTerre
    By: Lou MARILL
"""




#%%#################

## IMPORT MODULES ##
####################

# General modules
import matplotlib
# deactivate figure display, need to be at the program's begginig
matplotlib.use('Agg')
from sys import path
import numpy as np
import os
from os.path import exists, getsize, isdir
from os import mkdir
module_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
path.append(module_dir)
from glob import glob

import shutil
from pathlib import Path

from datetime import datetime
# Program parameters
# import param_itsa as pm

# # Add path
# if exists(path_module):
#     path.append(path_module)
# else:
#     raise ValueError(f"The 'path_module' variable is incorrectly set in param_itsa.py:\n \
#             The directory {path_module} does not exist!")

# ITSA module
from itsa.gts.Gts import Gts
from itsa.lib.astrotime import cal2decyear, decyear2mjd, mjd2decyear
from itsa.lib.index_dates import get_index_from_dates
from itsa.lib.read_cat import read_antenna
from itsa.lib.read_cat import read_station_info
from itsa.lib.select_ev import select_ev
from itsa.lib.save_Gts_byproduct import save_byp


def tsanalysis(
    time_series_file,
    path_workdir,
    provider = "usgs",
    metadata_file=None,
    position = (None, None),
    ref_frame="IGS14",
    save_frame="IGS14",
    software="GipsyX",
    ini_time=None,
    fin_time=None,
    skip_inversion=False,
    auto_skip_inversion=True,
    skip_outliers_filter=False,
    thresh=5,
    window_len=60,
    perc_ts=0,
    station_input_type=None,
    station_input_name=None,
    Mw_min=5.1,
    Mw_post=6.1,
    Mw_spe=8,
    dco=1.15,
    dpost=1.3,
    dsse=1,
    dsw=1.0,
    pre_post=False,
    jps_window_data=365,
    post_window_data=730,
    mod_post="log10",
    tau_jps=10,
    tau_post=30,
    tau_spe=1,
    acc=False,
    disp_window=True,
    byp_make=False,
    byp_names=["RESIDUALS", "PHY", "GEO"],
    byp_vel=[True, False, True],
    byp_seas=[True, False, True],
    byp_ant=False,
    byp_co=[True, False, True],
    byp_sw=[True, False, True],
    byp_sse=[True, False, True],
    byp_post=[True, False, True],
    disp_byp=[False, True, True],
    parallel=False,
    n_jobs=1
):
    """
    Analyze GNSS time series for one or multiple stations.

    This function processes GNSS time series data to detect seismic-related events
    (co-seismic, post-seismic, SSE, swarms) and applies various models (logarithmic or 
    exponential) to model post-seismic relaxation, filter outliers, and produce by-products
    (e.g., residuals, velocity and seasonal trends).

    Parameters
    ----------
    folder_ts : str
        Directory containing the GNSS time series files (typically one file per station).
    
    stations : str or list of str
        GNSS station code(s) to be processed. May be a single station (str) or a list of station codes.
    
    path_workdir : str
        Working directory for temporary data and results output.
    
    ref_frame : str, default "IGS14"
        The reference frame of the input GNSS positions (e.g., "ITRF2014", "IGS14").
    
    save_frame : str, default "EURA"
        The target tectonic plate or reference frame for the output, such as "EURA" (Eurasia), "NOAM" (North America), 
        "ANTA" (Antartica), "ARAB" (Arabia), "AUST" (Australia), "INDI" (India), "NAZC" (Nasca), "NUBI" (Nubia),
        "PCFC" (Pacific), "  PS" (Peruvian Sliver), "SOAM" (South America), "SOMA" (Somalia).

    software : str, default "GipsyX"
        Software used to obtain the GNSS positions from the time series (e.g., "GipsyX", "GAMIT").
    
    ini_time : list of int or None
        Start date of the analysis period [year, month, day]. If None, the first date in the time series is used.
    
    fin_time : list of int or None
        End date of the analysis period [year, month, day]. If None, the last date in the time series is used.
    
    skip_inversion : bool, default False
        If True, skip the inversion step and only output the PBO.pos file.
    
    auto_skip_inversion : bool, default True
        Automatically skip inversion if the time series contains fewer than 100 data points.
    
    skip_outliers_filter : bool, default False
        If True, bypass the outlier filtering step.
    
    thresh : float, default 5
        Threshold value multiplied by the median absolute deviation (MAD) of the window to detect outliers.
    
    window_len : int, default 60
        Length of the sliding window (in days) for filtering.
    
    perc_ts : int, default 0
        Minimum percentage of valid data required within the analysis period. Set to 0 to use all available stations.
    
    station_input_type : str or None
        Format type of station metadata ("gipsyx", "gamit", "all"). If None, defaults to "gipsyx".
    
    station_input_name : str or None
        Name of the input file or folder containing station metadata. If None, defaults to "staDB".
    
    Mw_min : float, default 5.1
        Minimum moment magnitude (Mw) for considering all seismic events.
    
    Mw_post : float, default 6.1
        Minimum Mw for the post-seismic effect.
    
    Mw_spe : float, default 8
        Minimum Mw for special post-seismic effects (when using a distinct model).
    
    dco : float, default 1.15
        Influence radius parameter for co-seismic events.
    
    dpost : float, default 1.3
        Influence radius parameter for post-seismic effects.
    
    dsse : float, default 1
        Influence radius parameter for slow slip events (SSE).
    
    dsw : float, default 1.0
        Influence radius parameter for swarm events.
    
    pre_post : bool or int, default False
        If True, include the last post-seismic event regardless of its timing. If an int, 
        include only if the event occurred within the specified number of days prior to the period.
    
    jps_window_data : int, default 365
        Time window length (in days) for modeling jump events in the time series.
    
    post_window_data : int, default 730
        Time window length (in days) for the post-seismic analysis.
    
    mod_post : str, default "log10"
        Model type for post-seismic effects: "log10" for logarithmic or "exp" for exponential.
    
    tau_jps : int, default 10
        Relaxation time (in days) for jump window events.
    
    tau_post : int, default 30
        Relaxation time (in days) for the post-seismic window.
    
    tau_spe : int, default 1
        Relaxation time for special post-seismic effects (if applicable).
    
    acc : bool, default False
        If True, compute an acceleration term.
    
    disp_window : bool, default True
        If True, display or save the sliding-window analysis figure.
    
    byp_make : bool, default False
        If True, generate additional by-products such as:
            - Residuals, 
            - Velocity/acceleration trends, 
            - Seasonal variations, 
            - Antenna change effects, 
            - Seismic jumps, etc.
    
    byp_names : list of str, default ["RESIDUALS", "PHY", "GEO"]
        Names of the folders where by-products will be saved.
    
    byp_vel : list of bool, default [True, False, True]
        Flags to control the correction of velocity and acceleration trends for each by-product.
    
    byp_seas : list of bool, default [True, False, True]
        Flags for correcting seasonal variations (annual and semi-annual) in each by-product.
    
    byp_ant : bool, default True
        Flag to correct antenna changes.
    
    byp_co : list of bool, default [True, False, True]
        Flags to handle co-seismic jumps for each by-product.
    
    byp_sw : list of bool, default [True, False, True]
        Flags to handle swarm events for each by-product.
    
    byp_sse : list of bool, default [True, False, False]
        Flags to handle slow slip events (SSE) for each by-product.
    
    byp_post : list of bool, default [True, False, True]
        Flags to handle post-seismic effects for each by-product.
    
    disp_byp : list of bool, default [False, True, True]
        Flags to display figures for each by-product.
    
    parallel : bool, default False
        If True, process multiple stations in parallel using joblib (or other parallelism module).
    
    n_jobs : int, default 1
        Number of parallel jobs to run if `parallel` is True.

    Returns
    -------
    None
        The function does not return a value directly. It writes result files to `path_workdir`
        for each station processed.

    Notes
    -----
    - This function is designed for advanced GNSS time series analysis including seismic event detection,
      outlier filtering, and by-product generation.
    - Stations are processed independently, and the function can be executed in parallel to reduce processing time.
    """
    

    if not Path(time_series_file).exists() or not Path(time_series_file).is_file():
        raise ValueError(f" the path_workdir you enter ({time_series_file}) is not valid or is not a file")
    
    #file_ts = glob(f"{folder_ts}/{stations.lower()}*")
    
    #if not file_ts:
    #    file_ts = glob(f"{folder_ts}/{stations.upper()}*")
    
    #if not Path(file_ts).exists() or not Path(file_ts).is_dir():
    #    raise ValueError(f" the time series file you enter ({file_ts}) is not valid or is not a file")
    
    try:
        with open(time_series_file, 'r') as f:
            first_line = f.readline().strip()
            if not first_line.startswith("YYYY MM DD"):
                raise ValueError(f" the time series file you enter ({time_series_file}) is not valid")
    except Exception as e:
        print(f"Error opening file {time_series_file}: {e}")
        raise ValueError(f" the time series file you enter ({time_series_file}) is not valid")
        
    stations = (os.path.basename(time_series_file)[0:4]).upper()

    if not Path(path_workdir).exists() or not Path(path_workdir).is_dir():
        raise ValueError(f" the path_workdir you enter ({path_workdir}) is not valid or is not a folder")
    
    folder_res =f"{path_workdir}/RESULTS/"
    if not Path(folder_res).exists():
        Path(folder_res).mkdir(parents=True, exist_ok=True)
    
    folder_input =f"{path_workdir}/INPUT_FILES/"
    if not Path(folder_input).exists():
        Path(folder_input).mkdir(parents=True, exist_ok=True)

    # folder_cats =f"{folder_input}/INPUT_CATS/"
    # if not Path(folder_cats).exists():
    #     Path(folder_cats).mkdir(parents=True, exist_ok=True)
    
    # sse_file = Path(f"{folder_cats}/sse_catalog.txt")
    # unknown_ev_file = Path(f"{folder_cats}/unknown_ev_catalog.txt")
    
    # sse_url = "https://cloud.univ-grenoble-alpes.fr/s/p5nEEESByoAjfir/download/sse_catalog.txt"
    # unknown_ev_url = "https://cloud.univ-grenoble-alpes.fr/s/5dG9azeLRNNraZ3/download/unknown_ev_catalog.txt"
    
    # # Download the initial file from cloud if not found locally
    # if not sse_file.exists():
    #     print("Local catalog not found. Downloading initial file for sse catalog...")
    #     try:
    #         response = requests.get(sse_url)
    #         response.raise_for_status()
    #         sse_file.write_bytes(response.content)
    #         print(f"Initial catalog downloaded and saved to {str(sse_file.parent)}.")
    #     except Exception as e:
    #         raise RuntimeError(f"Failed to download initial sse catalog from cloud: {e}")
            
    # # Download the initial file from cloud if not found locally
    # if not unknown_ev_file.exists():
    #     print("Local catalog not found. Downloading initial file for ...")
    #     try:
    #         response = requests.get(unknown_ev_url)
    #         response.raise_for_status()
    #         unknown_ev_file.write_bytes(response.content)
    #         print(f"Initial catalog downloaded and saved to {str(unknown_ev_file.parent)}.")
    #     except Exception as e:
    #         raise RuntimeError(f"Failed to download initial unknown event catalog from cloud: {e}")
            
    # folder_stn_metadata =f"{folder_input}/INPUT_STN_METADATA/"
    # if not Path(folder_stn_metadata).exists():
    #     Path(folder_stn_metadata).mkdir(parents=True, exist_ok=True)
        
    # folder_stadb =f"{folder_stn_metadata}/staDB/"
    # if not Path(folder_stadb).exists():
    #     Path(folder_stadb).mkdir(parents=True, exist_ok=True)
        
    # folder_logfiles =f"{folder_stn_metadata}/logfiles/"
    # if not Path(folder_logfiles).exists():
    #     Path(folder_logfiles).mkdir(parents=True, exist_ok=True)
        
    #INPUT_TS
    
    folder_ts =f"{folder_input}/INPUT_TS/"
    if not Path(folder_ts).exists():
        Path(folder_ts).mkdir(parents=True, exist_ok=True)
    
    if not Path(f"{folder_ts}/{stations}.pos").exists():
        Path(f"{folder_ts}/{stations}.pos").symlink_to(time_series_file, target_is_directory=False)
    
    def write_QC(data, sta, folder):
        """
        Write QC indicators to a file
        """
        Sn = ts.data[1:, 4]
        Se = ts.data[1:, 5]
        Su = ts.data[1:, 6]
        avg_Sn = np.nanmean(Sn) 
        avg_Se = np.nanmean(Se) 
        avg_Su = np.nanmean(Su)
        qc_dir = os.path.join(folder_out, "QC")
        qc_file = os.path.join(qc_dir, f"qc_{ts.code}.txt")
        if not isdir(qc_dir):
            mkdir(qc_dir)
        with open(qc_file, "w") as qc:
                qc.write("Station avg_Sn avg_Se avg_Su\n")
                qc.write(f"{ts.code} {avg_Sn} {avg_Se} {avg_Su}\n")
    
    
    #%%###################
    ## READ TIME SERIES ##
    ######################
    
    # Create Gts
    if len(stations) != 4:
        raise ValueError(f"The code station {stations} is not valid")
        
    ts = Gts(stations)

    # Print in STDOUT
    print('Station: %s' %ts.code)
    print()
    
    # Read Gts
    # POS_FILES folder
    if not exists(folder_ts):
        raise ValueError(f"The 'folder_ts' variable is not valid:\n \
                The directory {folder_ts} does not exist!")
    
    # Read
    try:
        ts.read_allpos(folder_ts, ref_frame=ref_frame, process=software)
    except:
        print('[WARNING] from [tsanalysis_itsa]:')
        print("\tNo file '%s*.pos' was found in '%s'!" % (ts.code, folder_ts))
    else:
    
        # Limit Gts to given time period
        if ini_time is None:
            ini_time = ts.time[0, 0]
        else:
            ini_time = cal2decyear(ini_time[2], ini_time[1], ini_time[0])
        if fin_time is None:
            fin_time = ts.time[-1, 0]
        else:
            fin_time = cal2decyear(fin_time[2], fin_time[1], fin_time[0])
        
        # Use continuous time vector and remove duplicate dates
        ts.continuous_time(ini_time=ini_time, fin_time=fin_time, in_place=True)
       
        # Choose to skip inversion or not based on user parameters and timeseries length
        if not skip_inversion:
            if auto_skip_inversion == True:
                # skip inversion if timeseries shorter than 100 points
                if len(np.unique(np.where(~np.isnan(ts.data))[0])) > 100:
                    skip_inversion = False
                else:
                    skip_inversion = True
            else:
                skip_inversion = False
    
        # Find and remove outliers
        if skip_inversion == False:
            if skip_outliers_filter == False:
                ts.find_outliers(thresh, window_len)
                ts.remove_outliers(in_place=True)
            else:
                print('[WARNING] skip_outliers_filter set to True, skipping outliers filtering!')
        else:
            print('[WARNING] skip_inversion set to True, skipping inversion!')
            
        # Enough data to analyse?
        idx_nonan = np.unique(np.where(~np.isnan(ts.data))[0])
        if len(idx_nonan) > ts.time.shape[0]*perc_ts/100:
        
            # Limit Gts to given time period
            
            #%%#########################
            ## FIND ASSOCIATED EVENTS ##
            ############################

            folder_cats =f"{folder_input}/INPUT_CATS/"
            if not Path(folder_cats).exists():
                Path(folder_cats).mkdir(parents=True, exist_ok=True)
            
            sse_url = "https://cloud.univ-grenoble-alpes.fr/s/p5nEEESByoAjfir/download/sse_catalog.txt"
            unknown_ev_url = "https://cloud.univ-grenoble-alpes.fr/s/5dG9azeLRNNraZ3/download/unknown_ev_catalog.txt"
        
            # Input station metadata
            path_input_stnMD = os.path.join(folder_input, 'INPUT_STN_METADATA')
            # if station_input_name is None:
            #     antenna_path = os.path.join(path_input_stnMD, 'staDB')
            # else:
            #     antenna_path = os.path.join(path_input_stnMD, station_input_name)
            antenna_path = os.path.join(path_input_stnMD, 'staDB')
            if not Path(antenna_path).exists():
                Path(antenna_path).mkdir(parents=True, exist_ok=True)

            logfiles_path = os.path.join(path_input_stnMD, 'logfiles')
            if not Path(logfiles_path).exists():
                Path(logfiles_path).mkdir(parents=True, exist_ok=True)
            
            expected_metadata_file = f"{antenna_path}/{stations}.sta_db"
            if metadata_file and Path(metadata_file).is_file():
                # Validate the log file format
                content     = open(metadata_file, 'r', errors="ignore")

                first_line  = content.readline()
                second_line = content.readline()

                expression = "Site Information Form (site log"

                # if metadata_file.split(".")[-1] == "log":
                if expression in first_line and expression in second_line :
                    convert_log_to_staDB(metadata_file, antenna_path)
                    if not expected_metadata_file:
                        raise ValueError("the metadata file ({expected_metadata_file}) does not exist")
                        
                elif first_line.startswith("KEYWORDS") and second_line.startswith(stations.upper()):
                    Path(expected_metadata_file).symlink_to(metadata_file, target_is_directory=False)
            else:
                if isinstance(position, tuple) and isinstance(position[0], float)  and isinstance(position[1], float):
                    # print(stations, position, logfiles_path)
                    logfile_download = download_logfile(stations, position, logfiles_path)
                    if logfile_download:
                        convert_log_to_staDB(logfile_download, antenna_path)
                        if not expected_metadata_file:
                            raise ValueError("the metadata file ({expected_metadata_file}) does not exist")
                    else:
                        raise ValueError("failled to download logfile")
                else:
                    raise ValueError(f"the position argument ({position}) is not defined or is invalid")
            
            path_input_cats = os.path.join(folder_input, 'INPUT_CATS')
            isc_cat_file = os.path.join(path_input_cats, 'isc_catalog.txt')
            
            eq_cat_file = os.path.join(path_input_cats, f"{provider}_earthquake_catalogue.txt")
            update_seismic_catalog(eq_cat_file, provider, datetime.today().strftime("%Y-%m-%d"))

            sse_cat_file = Path(os.path.join(path_input_cats, 'sse_catalog.txt'))
            # Download the initial file from cloud if not found locally
            if not Path(sse_cat_file).exists():
                print("Local catalog not found. Downloading initial file for sse catalog...")
                try:
                    response = requests.get(sse_url)
                    response.raise_for_status()
                    sse_cat_file.write_bytes(response.content)
                    print(f"Initial catalog downloaded and saved to {str(sse_cat_file.parent)}.")
                except Exception as e:
                    raise RuntimeError(f"Failed to download initial sse catalog from cloud: {e}")
            sse_cat_file = str(sse_cat_file)
                    
            sw_cat_file = os.path.join(path_input_cats, 'swarm_catalog.txt')
            unsta_cat_file = os.path.join(path_input_cats, 'unknown_sta_catalog.txt')
            
            unev_cat_file = os.path.join(path_input_cats, 'unknown_ev_catalog.txt')
            # Download the initial file from cloud if not found locally
            if not Path(unev_cat_file).exists():
                print("Local catalog not found. Downloading initial file for ...")


                # response = requests.get(unknown_ev_url)
                # response.raise_for_status()
                # Path(unev_cat_file).write_bytes(response.content)
                # print(f"Initial catalog downloaded and saved to {str(unev_cat_file.parent)}.")

                try:
                    response = requests.get(unknown_ev_url)
                    response.raise_for_status()
                    Path(unev_cat_file).write_bytes(response.content)
                    print(f"Initial catalog downloaded and saved to {str(Path(unev_cat_file).parent)}.")
                except Exception as e:
                    raise RuntimeError(f"Failed to download initial unknown event catalog from cloud: {e}")
            
            # Jps metadata
            ts.jps.mag_min = Mw_min
            ts.jps.mag_post = Mw_post
            ts.jps.mag_spe = Mw_spe
            ts.jps.dco = dco
            ts.jps.dpost = dpost
            ts.jps.dsse = dsse
            ts.jps.dsw = dsw
            
            # Antenna changes
            # Read
            # Issue 31: allow use of GAMIT station.info
            print(antenna_path, ts.code)
            if station_input_type == None:
                ant_dates = read_antenna(antenna_path, ts.code)
            elif station_input_type.lower() == "gipsyx":
                ant_dates = read_antenna(antenna_path, ts.code)
            elif station_input_type.lower() == "gamit":
                ant_dates = read_station_info(antenna_path, ts.code)
            elif station_input_type.lower() == "all":
                # TODO: Gérer les collisions et lire des deux sources
                ant_dates = read_antenna(antenna_path, ts.code)
            else:
                ant_dates = read_antenna(antenna_path, ts.code)
            # Populate |self.jps|
            if ant_dates.size > 0:
                ts.jps.add_ev(np.c_[ant_dates, decyear2mjd(ant_dates)], 'A')
        
            # Earthquake catalog
            # ISC catalog
            if exists(isc_cat_file) and getsize(isc_cat_file) > 0:
                (isc_cat, type_isc) = select_ev(ts.XYZ0, isc_cat_file, 'ISC',
                                              Mw_min, dco, Mw_post,
                                              dpost)
                if isc_cat.size > 0:
                    isc_cat = isc_cat.reshape(-1, 5)
                    ts.jps.add_ev(np.c_[isc_cat[:, 0], decyear2mjd(isc_cat[:, 0])],
                                  type_isc, isc_cat[:, 1:-1], isc_cat[:, -1])
            # Handmade catalog
            if exists(eq_cat_file) and getsize(eq_cat_file) > 0:
                (eq_cat, type_eq) = select_ev(ts.XYZ0, eq_cat_file, 'E',
                                              Mw_min, dco, Mw_post,
                                              dpost)
                if eq_cat.size > 0:
                    eq_cat = eq_cat.reshape(-1, 5)
                    ts.jps.add_ev(np.c_[eq_cat[:, 0], decyear2mjd(eq_cat[:, 0])],
                                  type_eq, eq_cat[:, 1:-1], eq_cat[:, -1])
        
            # Swarm catalog (optional)
            if exists(sw_cat_file) and getsize(sw_cat_file) > 0:
                (sw_cat, type_sw) = select_ev(ts.XYZ0, sw_cat_file, 'W',
                                              None, dsw)           
                if sw_cat.size > 0:
                    sw_cat = sw_cat.reshape(-1, 6)
                    ts.jps.add_ev(np.c_[sw_cat[:, 0], decyear2mjd(sw_cat[:, 0])],
                                  type_sw, sw_cat[:, 1:-2], sw_cat[:, -2],
                                  sw_cat[:, -1])
        
            # SSE catalog (optional)
            if exists(sse_cat_file) and getsize(sse_cat_file) > 0:
                (sse_cat, type_sse) = select_ev(ts.XYZ0, sse_cat_file, 'S',
                                                Mw_min, dsse)            
                if sse_cat.size > 0:
                    sse_cat = sse_cat.reshape(-1, 6)
                    ts.jps.add_ev(np.c_[sse_cat[:, 0], decyear2mjd(sse_cat[:, 0])],
                                  type_sse, sse_cat[:, 1:-2], sse_cat[:, -2],
                                  sse_cat[:, -1])
                    
            # Unknown from unknown_sta_catalog.txt (optional)
            if exists(unsta_cat_file) and getsize(unsta_cat_file) > 0:
                # Read
                unsta_cat = np.genfromtxt(unsta_cat_file,
                                          dtype=[('Station', 'U4'),
                                                 ('Year', 'f8')])
                # Find station dates
                unsta_dates = unsta_cat[
                    np.where(unsta_cat['Station'] == ts.code)]['Year']
                # Transform to modified Julian days
                if unsta_dates.size > 0:
                    unsta_mjd = np.array(decyear2mjd(unsta_dates), dtype=int)+.5
                    # Populate |self.jps|
                    ts.jps.add_ev(np.c_[mjd2decyear(unsta_mjd),unsta_mjd], 'U')
        
            # Unknown from unknown_ev_catalog.txt (optional, to avoid)
            if exists(unev_cat_file) and getsize(unev_cat_file) > 0:
                # Read
                (unev_cat, type_unev) = select_ev(ts.XYZ0, unev_cat_file, 'U')           
                # Populate |self.jps|
                if unev_cat.size > 0:
                    unev_cat = unev_cat.reshape(-1, 6)
                    ts.jps.add_ev(np.c_[unev_cat[:, 0],
                                        decyear2mjd(unev_cat[:, 0])],
                                  type_unev, unev_cat[:, 1:-2], None,
                                  unev_cat[:, -1])
        
            # Sort events and remove duplicated dates
            ts.jps.remove_duplicated_dates()
               
            # Set Gts to NaN during unknown, antenna and earthquake events
            find_UAEP = np.isin(ts.jps.type_ev,['U','A','E','P'])
            idx_jps_UAEP = get_index_from_dates(ts.time[:, 1],
                                                ts.jps.dates[find_UAEP, 1])
            if skip_outliers_filter == False:
                ts.outliers = idx_jps_UAEP[np.where(idx_jps_UAEP>=0)]
                ts.remove_outliers(in_place=True)
                
        # Still enough data to analyse?
        idx_nonan = np.unique(np.where(~np.isnan(ts.data))[0])
        if len(idx_nonan) <= ts.time.shape[0]*perc_ts/100:
            print('[WARNING] from [tsanalysis_itsa]:')
            print('\tGts %s has not enough data within [%.3f;%.3f] to be analysed!'
                  % (ts.code, ini_time, fin_time))
            print()
        else:
            
            # Keep only useful events
            # Whithin the time period
            jps_period = ts.jps.select_ev(
                (ts.jps.dates[:, 1]>ts.time[idx_nonan[0], 1])
                & (ts.jps.dates[:, 1]<ts.time[idx_nonan[-1], 1]))
            # Last post-seismic event before the no-NaN time period
            if pre_post:
                idx_jp_add = np.where(
                    (ts.jps.type_ev=='P') &
                    (ts.jps.dates[:, 1]<=ts.time[idx_nonan[0], 1]))[0]
                if idx_jp_add.size == 0:
                    pre_post = False
                else:
                    idx_jp_add = idx_jp_add[-1]
                    if isinstance(pre_post, int):
                        time_lim = ts.time[idx_nonan[0], 1]-pre_post
                    if (isinstance(pre_post, int)
                        and ts.jps.dates[idx_jp_add, 1] > time_lim):
                        pre_post = False
                    else:
                        pre_post = True
                        jps_period.add_ev(ts.jps.dates[idx_jp_add, :],
                                          ts.jps.type_ev[idx_jp_add],
                                          ts.jps.coords[idx_jp_add, :],
                                          ts.jps.mag[idx_jp_add])
                        jps_period.reorder()
            ts.jps = jps_period
            
            # Change reference frame
            if ref_frame != save_frame and save_frame != ts.ref_frame:
                if (save_frame[:3].upper() == 'IGS'
                    or save_frame[:4].upper() == 'ITRF'):
                    ts.itrf_convert(save_frame, in_place=True)
                else:
                    ts.fixed_plate(save_frame[:4], in_place=True)
            
            # Put |self.t0| to the first available data
            ts.change_ref(ts.time[idx_nonan[0], 1])


            
            #%%###########
            ## ANALYSIS ##
            ##############
            
            
            if skip_outliers_filter == False:
                # Green's function initialisation
                # Constant term
                c = np.ones(ts.time.shape[0])
                # Velocity [mm/year]
                tg = ts.time[:, 0]-ts.time[0, 0]
                # Sesonal and semi-seasonal terms
                an1, an2 = np.cos(2.*np.pi*tg), np.sin(2.*np.pi*tg)
                sm1, sm2 = np.cos(4.*np.pi*tg), np.sin(4.*np.pi*tg)
                # Seasonal Green's functions
                G_seas = np.c_[c, tg, an1, an2, sm1, sm2]
                
                # Initialisation
                # Index of no-NaN data
                idx_nonan = np.unique(np.where(~np.isnan(ts.data))[0])
                # Figure folder
                folder_fig = os.path.join(folder_res , stations, 'PLOTS')
                folder_window = os.path.join(folder_fig, 'WINDOW')
                
                # Jps not empty?
                if ts.jps.shape() > 0:
                    
                    # Jump inversion
                    ts_res_jps = ts.window_analysis(
                        jps_window_data, np.c_[c, tg], tau_jps, mod_post,
                        disp=disp_window, folder_disp=os.path.join(folder_window, f"JPS{os.sep}"))
               
                    # Post-seismic inversion
                    # Take only Jps with solution != 0
                    idx_jps_ok = np.where((ts.MOD[:, :3]!=0).any(axis=1))[0]
                    # Shift index if one post-seismic before time period
                    if pre_post:
                        idx_jps_ok = [0]+list(idx_jps_ok+1)
                        jps_ok = ts.jps.select_ev(idx_jps_ok)
                    else:
                        jps_ok = ts.jps.select_ev(idx_jps_ok)
                    # Consider only post-seismic events
                    ts_res_jps.jps = jps_ok.select_ev(jps_ok.type_ev=='P')
                    if ts_res_jps.jps.shape() > 0:
                        # Inversion
                        ts_res_post = ts_res_jps.window_analysis(
                            post_window_data, G_seas, tau_post, mod_post,
                            'post', tau_spe, pre_post, disp=disp_window,
                            folder_disp=os.path.join(folder_window, f"POST{os.sep}"))
                        # Populate |ts.G| and |ts.MOD| with post window results
                        ts.G = np.c_[ts.G, ts_res_jps.G];
                        ts.MOD = np.vstack((ts.MOD, ts_res_jps.MOD))
                    else:
                        ts_res_post = ts_res_jps.copy()
                
                else:
                    ts_res_post = ts.copy()
                    
                # Long-term phenomena inversion
                # Quadratic inversion
                if acc:
                    # Copy
                    ts_acc = ts.copy()
                    ts_res_post_acc = ts_res_post.copy()
                    # Inversion
                    ts_res_acc = ts_res_post_acc.longt_analysis(np.c_[tg**2, G_seas])
                    # Recover all Jps events
                    ts_res_acc.jps = ts.jps.copy()
                    # Populate |ts_acc.G| and |ts_acc.MOD| with long-term phenomena
                    # inversion results
                    ts_acc.G = np.c_[ts_acc.G, ts_res_post_acc.G];
                    ts_acc.MOD = np.vstack((ts_acc.MOD, ts_res_post_acc.MOD))
                # Linear inversion
                ts_res = ts_res_post.longt_analysis(G_seas)
                # Recover all Jps events
                ts_res.jps = ts.jps.copy()
                # Populate |ts.G| and |ts.MOD| with long-term phenomena inversion
                # results
                ts.G = np.c_[ts.G, ts_res_post.G];
                ts.MOD = np.vstack((ts.MOD, ts_res_post.MOD))
                  
            
                #%%####################################
                ## DISPLAY ANALYSIS AND RESULTS DATA ##
                #######################################
                
                # Long-term phenomena inversion
                if disp_window:
                    from itsa.jps.Jps import Jps
                    ts_res_post.jps = Jps(ts.code)
                    ts_res_post.plot('darkgreen',
                                     ('Station '+ts_res_post.code
                                      + ' -- Seasonal inversion'),
                                     path_fig=os.path.join(folder_window, f"SEASONAL{os.sep}"))
            
                # Raw data and model
                ts.plot(name_fig=ts.code+'_data', path_fig=os.path.join(folder_fig, f"ANALYSIS{os.sep}"))
                
                # Residuals
                ts_res.plot('green', name_fig=ts_res.code+'_res',
                            path_fig=os.path.join(folder_fig, f"ANALYSIS{os.sep}"), size_marker=1)
                
                # Quadratic inversion
                if acc:
                    # Long-term phenomena inversion
                    if disp_window:
                        ts_res_post_acc.jps = Jps(ts.code)
                        ts_res_post_acc.plot('darkgreen',
                                             ('Station '+ts_res_post_acc.code
                                              + ' -- Seasonal inversion'),
                                             path_fig=os.path.join(folder_window, f"SEASONAL_QUA{os.sep}"),
                                             acc=True)
                    # Raw data and model
                    ts_acc.plot(name_fig=ts_acc.code+'_data',
                                path_fig=os.path.join(folder_fig, f"ANALYSIS_QUA{os.sep}"), acc=True) 
                    # Residuals
                    ts_res_acc.plot('green', name_fig=ts_res_acc.code+'_res',
                                    path_fig=os.path.join(folder_fig, f"ANALYSIS_QUA{os.sep}"),
                                    size_marker=1, acc=True)
 
            #%%#################################
            ## SAVE ANALYSIS AND RESULTS DATA ##
            ####################################
            
            # Data folder
            folder_out = os.path.join(folder_res , stations, 'OUTPUT_FILES')
            folder_pos = os.path.join(folder_out, 'TS_DATA')
            
            # Save RAW time series
            ts.write_PBOpos(os.path.join(folder_pos, 'RAW'), replace=True)
            
            if skip_outliers_filter == False:
                # Save Jps catalog
                ts.jps.write(os.path.join(folder_out, 'JPS'), replace=True)
                
                # Save Green's function and model amplitudes
                names_longt = ['Cst', 'Vel', 'An1', 'An2', 'Sm1', 'Sm2']
                ts.make_GMOD_names(names_longt, tau_post, tau_spe, pre_post)
                ts.write_Gtxt(os.path.join(folder_out, 'G_MATRIX'), replace=True)
                ts.write_MODtxt(os.path.join(folder_out, 'MODEL_AMP'), replace=True)
                
                # Acceleration?
                if acc:
                    ts_acc.make_GMOD_names(['Acc']+names_longt, tau_post,
                                           tau_spe, pre_post)
                    ts_acc.write_Gtxt(os.path.join(folder_out, 'G_MATRIX_QUA'), replace=True)
                    ts_acc.write_MODtxt(os.path.join(folder_out, 'MODEL_AMP_QUA'), replace=True)
    
                # Save QC indicators
                write_QC(ts.data, ts.code, folder_out)
                
                
                #%%###############################
                ## SAVE AND DISPLAY BY-PRODUCTS ##
                ##################################
                
                if byp_make:
                    save_byp(ts, byp_vel, byp_seas, byp_ant, byp_co,
                             byp_sw, byp_sse, byp_post, byp_names,
                             disp_byp, folder_pos, folder_fig, replace=True)
                    
                    # Acceleration?
                    if acc:
                        # Convert all |byp_| parameters into np.ndarray with same
                        # shape
                        from itsa.lib.modif_vartype import adapt_shape
                        (byp_names, byp_vel, byp_seas, byp_ant,
                         byp_co, byp_sw, byp_sse, byp_post,
                         disp_byp) = adapt_shape([byp_names, byp_vel,
                                                     byp_seas, byp_ant,
                                                     byp_co, byp_sw, byp_sse,
                                                     byp_post, disp_byp])
                        # Select only by-product impacted by acceleration
                        # and change by-product folder names
                        if isinstance(byp_vel, np.ndarray):
                            # Select only by-product impacted by acceleration
                            spe_acc = (byp_vel | byp_seas).astype('bool')
                            # Change by-product folder names
                            byp_acc_names = np.char.add(
                                byp_names[spe_acc], np.repeat('_QUA', sum(spe_acc)))
                            # Save and display
                            save_byp(ts_acc, byp_vel[spe_acc], byp_seas[spe_acc],
                                     byp_ant[spe_acc], byp_co[spe_acc],
                                     byp_sw[spe_acc], byp_sse[spe_acc],
                                     byp_post[spe_acc], byp_acc_names,
                                     disp_byp[spe_acc], folder_pos, folder_fig,
                                     replace=True)
                        elif byp_vel | byp_seas:
                            byp_acc_names = byp_names+'_QUA'
                            # Save and display
                            save_byp(ts_acc, byp_vel, byp_seas, byp_ant,
                                     byp_co, byp_sw, byp_sse, byp_post,
                                     byp_acc_names, disp_byp, folder_pos,
                                     folder_fig, replace=True)


        ############################
        # Still enough data to analyse?
        # path_workdir = ""
        
        result_folder = f"{path_workdir}/RESULTS"
        if Path(result_folder).exists() and  Path(result_folder).is_dir():
            list_stations = os.listdir(result_folder)
            
            if list_stations:
                for station in list_stations:
                    station_folder = f"{result_folder}/{station}"
                    if Path(station_folder).exists() and Path(station_folder).is_dir():
                        list_folders = os.listdir(station_folder)
                        
                        if list_folders:
                            for folder in list_folders:
                                content_folder = f"{station_folder}/{folder}"
                                if Path(content_folder).exists() and Path(content_folder).is_dir():
                                    shutil.rmtree(content_folder)







import os
import math
import requests
import csv
from io import StringIO

CATALOG_COLUMNS = ["year", "month", "day", "lat", "lon", "depth", "mag", "dist", "ID"]

def parse_isc_catalog(start_date: str, end_date: str, min_mag: float = 5.5):
    
    """
    Fetch and parse ISC earthquake data between given dates.

    Parameters:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        min_mag (float): Minimum magnitude filter.

    Returns:
        list: Sorted list of unique earthquake records as tuples.
    """
    
    url = (
        "https://www.isc.ac.uk/cgi-bin/web-db-run"
        f"?request=COMPREHENSIVE&out_format=CATCSV"
        f"&start_year={start_date[:4]}&start_month={int(start_date[5:7])}&start_day={int(start_date[8:10])}"
        f"&end_year={end_date[:4]}&end_month={int(end_date[5:7])}&end_day={int(end_date[8:10])}"
        f"&min_mag={min_mag}&req_mag_type=MW&req_mag_agcy=Any&include_links=on"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError("Failed to fetch ISC data.")
    
    data = []
    for line in response.text.split("\n"):
        row = line.replace("<", ",").replace(">", ",").split(",")
        if line.startswith(",a href=/cgi-bin/web-db-run?event_id") and len(row) > 23:
            try:
                year = int(row[11][:4])
                month = int(row[11][5:7])
                day = int(row[11][8:10])
                lat = float(row[13].strip())
                lon = float(row[14].strip())
                depth = float(row[15].strip())
                mag = float(row[23])
                dist = math.pow(10, 0.5 * mag - 0.8)
                eq_id = row[2]
                data.append((year, month, day, lat, lon, depth, mag, dist, eq_id))
            except Exception:
                continue
    return sorted(set(data))

def parse_emsc_catalog(end_date: str, min_mag: float = 5.5):

    """
    Fetch and parse EMSC earthquake data up to a given date.
    
    Parameters:
        end_date (str): End date in YYYY-MM-DD format.
        min_mag (float): Minimum magnitude filter.
    
    Returns:
        list: Sorted list of unique earthquake records as tuples.
    """
    
    url = (
        f"https://www.seismicportal.eu/fdsnws/event/1/query?"
        f"limit=200000&end={end_date}&format=text&minmag={min_mag}"
    )
    try:
        lines = requests.get(url, verify=False).text.split("\n")
    except:
        raise ConnectionError("Failed to fetch EMSC data.")

    data = []
    for row in lines[1:]:
        fields = row.split("|")
        if len(fields) == 13:
            try:
                year = int(fields[1][:4])
                month = int(fields[1][5:7])
                day = int(fields[1][8:10])
                lat = float(fields[2])
                lon = float(fields[3])
                depth = float(fields[4])
                mag = float(fields[10])
                dist = math.pow(10, 0.5 * mag - 0.8)
                eq_id = fields[0]
                data.append((year, month, day, lat, lon, depth, mag, dist, eq_id))
            except Exception:
                continue
    return sorted(set(data))

def parse_usgs_catalog(start_date: str, min_mag: float = 5.5):

    """
    Fetch and parse USGS earthquake data from a given start date.

    Parameters:
        start_date (str): Start date in YYYY-MM-DD format.
        min_mag (float): Minimum magnitude filter.

    Returns:
        list: Sorted list of unique earthquake records as tuples.
    """
    
    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
        f"&starttime={start_date}&minmagnitude={min_mag}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError("Failed to fetch USGS data.")

    csv_data = csv.reader(StringIO(response.text))
    next(csv_data, None)  # skip header

    data = []
    for row in csv_data:
        try:
            dt = datetime.datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%S.%fZ")
            lat = float(row[1])
            lon = float(row[2])
            depth = float(row[3])
            mag = float(row[4])
            place = row[11][:10]
            dist = math.pow(10, 0.5 * mag - 0.8)
            data.append((dt.year, dt.month, dt.day, lat, lon, depth, mag, dist, place))
        except:
            continue
    return sorted(set(data))

def get_last_date_from_catalog(file_path: str):
    """
    Extract the most recent date found in a catalog file.

    Parameters:
        file_path (str): Path to the catalog file.

    Returns:
        datetime.datetime: Latest date found in the catalog.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if not lines:
                return None
            dates = sorted(set("".join(line.split()[:3]) for line in lines))
            return datetime.datetime.strptime(dates[-1], "%Y%m%d")
    except FileNotFoundError:
        return None

def write_catalog_to_file(catalog: list, file_path: str, mode: str = "w"):
    """
    Write a catalog to a local file.

    Parameters:
        catalog (list): List of earthquake records (tuples).
        file_path (str): Output file path.
        mode (str): File write mode ('w' for overwrite, 'a' for append).
    """
    with open(file_path, mode) as f:
        for i, row in enumerate(catalog):
            line = f"{row[0]:4d} {row[1]:02d} {row[2]:02d} {row[3]:9.4f} {row[4]:9.4f} {row[5]:7.3f} {row[6]:5.3f} {row[7]:8.3f} {row[8]:10s}"
            if i < len(catalog) - 1:
                line += "\n"
            f.write(line)


def update_seismic_catalog(
    catalog_path: str, provider: str, ref_date: str, min_magnitude: float = 5.5):

    """
    Update a local catalog file using a given provider and reference date.

    Parameters:
        catalog_path (str): Path to the local catalog file.
        provider (str): Catalog provider (isc, emsc, usgs).
        ref_date (str): Update catalog up to this date (YYYY-MM-DD).
        min_magnitude (float): Minimum magnitude filter.

    Raises:
        ValueError: If the provider is not supported.
        RuntimeError: If fetching the cloud file fails.
    """
    
    provider = provider.lower()
    cloud_catalogs = {
        "emsc": "https://cloud.univ-grenoble-alpes.fr/s/rRLSZ9oGiMnbXgs/download/emsc_earthquake_catalogue.txt",
        "isc": "https://cloud.univ-grenoble-alpes.fr/s/m8Myxg2Ti87ANdk/download/isc_earthquake_catalogue.txt",
        "usgs": "https://cloud.univ-grenoble-alpes.fr/s/N3Z67gxzwgHWJWk/download/usgs_earthquake_catalogue.txt",
    }

    # Validate the provider
    if provider not in cloud_catalogs:
        raise ValueError(f"Unsupported provider: {provider}. Choose from {list(cloud_catalogs.keys())}")

    catalog_file = Path(catalog_path)

    # Download the initial file from cloud if not found locally
    if not catalog_file.exists():
        print(f"Local catalog not found. Downloading initial file for '{provider.upper()}'...")
        try:
            response = requests.get(cloud_catalogs[provider])
            response.raise_for_status()
            catalog_file.write_bytes(response.content)
            print(f"Initial catalog downloaded and saved to '{catalog_path}'.")
        except Exception as e:
            raise RuntimeError(f"Failed to download initial catalog from cloud: {e}")

    # # Get the latest date from the local catalog
    # last_date = get_last_date_from_catalog(catalog_path)
    # start_date = last_date + datetime.timedelta(days=1) if last_date else None
    # ref_dt = datetime.datetime.strptime(ref_date, "%Y-%m-%d")

    # if not last_date or last_date < ref_dt:
    #     print(f"Updating catalog '{provider.upper()}' from {start_date.strftime('%Y-%m-%d') if start_date else '2020-01-01'} to {ref_date}...")

    #     if provider == "isc":
    #         new_data = parse_isc_catalog(start_date.strftime("%Y-%m-%d") if start_date else "2020-01-01", ref_date, min_magnitude)
    #     elif provider == "emsc":
    #         new_data = parse_emsc_catalog(ref_date, min_magnitude)
    #     elif provider == "usgs":
    #         new_data = parse_usgs_catalog(start_date.strftime("%Y-%m-%d") if start_date else "2020-01-01", min_magnitude)

    #     if new_data:
    #         write_catalog_to_file(new_data, catalog_path, mode="a")
    #         print(f"Catalog updated with {len(new_data)} new entries from {provider.upper()}.")
    #     else:
    #         print("No new data found for the given period.")
    # else:
    #     print(f"Catalog is already up to date (last entry: {last_date.date()}).")
    
    
    


def date_format(install_date):
    if install_date.strip() and install_date[-1] != 'Z':
        return "%Y-%m-%d"
    else:
        return "%Y-%m-%dT%H:%MZ"

def convert_log_to_staDB(log_file, output_directory):
    """
    Convert a station log file to staDB format by extracting receiver and antenna information.

    :param log_file: The station log file to process
    :param output_directory: The directory to save the staDB output file
    """

    # Lists to store receiver and antenna data
    receiver_data = []
    antenna_data = []

    # Open and read the log file
    with open(log_file, 'r', errors="ignore") as file:
        line = file.readline()
        while not line.strip():
            line = file.readline()

        station_marker = line.split()[0][0:4]  # Extract station marker (first 4 characters)
        #station_marker = line.split()[0]

        while line:
            line = file.readline()

            # Extract coordinates and installation date
            if "Site Identification" in line:
                while "Receiver Information" not in line:
                    if "Date Installed" in line:
                        install_date = line.split(" :")[-1].strip()
                    elif "X coordinate" in line:
                        x_coordinate = line.split()[-1]
                    elif "Y coordinate" in line:
                        y_coordinate = line.split()[-1]
                    elif "Z coordinate" in line:
                        z_coordinate = line.split()[-1]
                    line = file.readline()

                try:
                    # Format the installation date and create the coordinate entry
                    install_date = datetime.strptime(install_date,  date_format(install_date)).strftime("%Y-%m-%d %H:%M:%S")
                    coordinates_entry = f"{station_marker}  STATE  {install_date}  {x_coordinate}  {y_coordinate}  {z_coordinate}   0.0   0.0   0.0"
                except ValueError:
                    pass
                    #print(f"Invalid date format 1: {install_date}")

            # Extract antenna information
            if "Antenna Type" in line:
                while "Date Removed" not in line:
                    if "Antenna Type" in line:
                        antenna_type = ' '.join(line.split(" :")[-1].split())
                    elif "Up Ecc" in line:
                        up_eccentricity = line.split(" :")[-1].strip()
                    elif "North Ecc" in line:
                        north_eccentricity = line.split(" :")[-1].strip()
                    elif "East Ecc" in line:
                        east_eccentricity = line.split(" :")[-1].strip()
                    elif "Serial Number" in line:
                        antenna_serial_number = line.split(" :")[-1].strip()
                    elif "Date Installed" in line:
                        antenna_install_date = line.split(" :")[-1].strip()
                    line = file.readline()

                try:
                    # Format the antenna installation date and create the antenna entry
                    antenna_install_date = datetime.strptime(antenna_install_date,  date_format(antenna_install_date)).strftime("%Y-%m-%d %H:%M:%S")
                    antenna_data.append(f"{station_marker}  ANT    {antenna_install_date}  {antenna_type}   {east_eccentricity}   {north_eccentricity}   {up_eccentricity} #{antenna_serial_number}")
                except ValueError:
                    pass

            # Extract receiver information
            if "Receiver Type" in line:
                while "Date Removed" not in line:
                    if "Receiver Type" in line:
                        receiver_type = line.split(" :")[-1].strip()
                    elif "Firmware Version" in line:
                        firmware_version = line.split(" :")[-1].strip()
                    elif "Date Installed" in line:
                        receiver_install_date = line.split(" :")[-1].strip()
                    line = file.readline()

                try:
                    # Format the receiver installation date and create the receiver entry
                    receiver_install_date = datetime.strptime(receiver_install_date,  date_format(receiver_install_date)).strftime("%Y-%m-%d %H:%M:%S")
                    receiver_data.append(f"{station_marker}  RX     {receiver_install_date}  {receiver_type} #{firmware_version}")
                except ValueError:
                    pass
                    #print(f"Invalid date format 3: {receiver_install_date}")

    # Save the data in the staDB format
    output_file = f"{output_directory}/{station_marker.lower()}.sta_db"

    with open(output_file, 'w', errors="ignore") as output:
        output.write("KEYWORDS: ID STATE END ANT RX\n")
        output.write(f"{station_marker}  ID  UNKNOWN  {station_marker}\n")
        output.write(f"{coordinates_entry}\n")

        for antenna_entry in antenna_data:
            output.write(f"{antenna_entry}\n")

        for index, receiver_entry in enumerate(receiver_data, 1):
            if index == len(receiver_data):
                gotoLine = ""
            else:
                gotoLine = "\n"
            output.write(f"{receiver_entry}{gotoLine}")
            


def get_country_code(country: str) -> str:
    """
    Retrieve the country code based on the country name.
    
    Args:
        country (str):  Name of the country.
    
    Returns:
        str:  Corresponding country code.
    """
    
    country_mapping = {
        "France métropolitaine": "00FRA", 
        "Guadeloupe": "00GLP", 
        "Saint-Barthélemy": "00BLM", 
        "Îles Éparses de l'océan Indien": "00ATF", 
        "Île Royale": "GUF", 
        "Saint-Martin (France)": "00MAF", 
        "Martinique": "00MTQ", 
        "Mayotte": "00MYT", 
        "Nouvelle-Calédonie": "00NCL", 
        "La Réunion": "00REU",
        "Saint-Pierre-et-Miquelon": "00SPM", 
        "Wallis-et-Futuna": "00WLF",
        "Nederland": "00NLD", 
        "Oranjestad": "00BES", 
        "Հայաստան": "00ARM",
        "Antarctica": "00ATA",
        "Österreich": "00AUT",
        "Belgien": "00BEL",
        "България": "00BGR",
        "Херцеговина": "00BIH",
        "Беларусь": "00BLR",
        "Schweiz/Suisse/Svizzera/Svizra": "00CHE",
        "Chile": "00CHL",
        "Kıbrıs": "00CYP",
        "Česko": "00CZE",
        "Deutschland": "00DEU",
        "Danmark": "00DNK",
        "España": "00ESP",
        "Eesti": "00EST",
        "Finland": "00FIN",
        "France": "00FRA",
        "Føroyar": "00FRO",
        "Kingdom": "00GBR",
        "Ελλάς": "00GRC",
        "Nunaat": "00GRL",
        "Hrvatska": "00HRV",
        "Magyarország": "00HUN",
        "Ireland": "00IRL",
        "Ísland": "00ISL",
        "Territory": "00ISR",
        "Italia": "00ITA",
        "Lietuva": "00LTU",
        "Lëtzebuerg": "00LUX",
        "Latvija": "00LVA",
        "Moldova": "00MDA",
        "Македонија": "00MKD",
        "Malta": "00MLT",
        "Гора": "00MNE",
        "Nederland": "00NLD",
        "Norge": "00NOR",
        "Perú": "00PER",
        "Polska": "00POL",
        "Portugal": "00PRT",
        "România": "00ROU",
        "Россия": "00RUS",
        "Marino": "00SMR",
        "Србија": "00SRB",
        "Slovensko": "00SVK",
        "Slovenija": "00SVN",
        "Sverige": "00SWE",
        "Argentina": "00ARG",
        "Türkiye": "00TUR",
        "الأردن": "00JOR",    
        "المغرب": "00MAR",    
        "Україна": "00UKR"
    }
    return country_mapping.get(country, "")



def download_logfile(station_code: str, coordinates: tuple, output_directory: str) -> str:
    """
    Download the logfile associated with a GNSS station from the M3G website, if not already present locally.

    Args:
        station_code (str): Code of the station (4 or 9 characters).
        coordinates (tuple): Tuple of (latitude, longitude) of the station.
        output_directory (str): Directory where logfiles are stored.

    Returns:
        str | None: Path to the downloaded logfile, or None if not available.
    """
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata_catalog = output_dir / "metadata_catalog.txt"
    
    # url_metadata_catalog = (
    #     "https://gnss-metadata.eu/v1/sitelog/metadata-list"
    #     "?downloadFormat=log&validMetadata=1&network=&country=&stationId="
    # )

    url_metadata_catalog = "https://cloud.univ-grenoble-alpes.fr/s/2wt6PBbCiGt5F7E/download/metadata_catalog.txt"


    # Download metadata catalog if not present
    if not metadata_catalog.exists():
        try:
            response = requests.get(url_metadata_catalog, timeout=20)
            response.raise_for_status()
            metadata_catalog.write_bytes(response.content)
            print(f"[INFO] Metadata catalog downloaded to {metadata_catalog}")
        except Exception as e:
            raise RuntimeError(f"Failed to download metadata catalog: {e}")

    # Determine expected name
    if len(station_code) == 4:
        latitude, longitude = coordinates
        country = ll2cou(latitude, longitude)
        station_country_code = get_country_code(country)
    elif len(station_code) == 9:
        station_country_code = ""
    else:
        print(f"[ERROR] Invalid station code length: {station_code}")
        return None

    expected_name = f"{station_code}{station_country_code}".lower()
    
    # Check if logfile already exists
    existing_logs = glob(str(output_dir / f"{expected_name}*.log"))
    if existing_logs:
        return existing_logs[0]  # Return the first match

    # Look for the metadata entry in the catalog
    loginfos = None
    with metadata_catalog.open('r') as f:
        for line in f:
            if line.startswith(expected_name.upper()):
                loginfos = line.strip()
                break

    if not loginfos:
        print(f"[WARNING] No metadata entry found for station: {expected_name}")
        return None

    parts = loginfos.split()
    if len(parts) < 6:
        print(f"[WARNING] Unexpected format in metadata line for {expected_name}: {loginfos}")
        return None

    loginfos_name = parts[2]
    loginfos_url = parts[5]
    logfile_path = output_dir / loginfos_name

    # Download logfile
    try:
        response = requests.get(loginfos_url, timeout=20)
        response.raise_for_status()
        logfile_path.write_bytes(response.content)
        print(f"[INFO] Logfile downloaded to {logfile_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to download logfile from {loginfos_url}: {e}")

    return str(logfile_path)


import random
from geopy.geocoders import Nominatim

def ll2cou(latitude: float, longitude: float()) -> str:
    """
    get country name from station position (latitude, longitude)
    
    Parameters:
    ----------
        longitude : float or np.ndarray
            Longitude in degrees (if unit is 'dec_deg') or radians (if unit is 'rad').
        latitude : float or np.ndarray
            Latitude in degrees (if unit is 'dec_deg') or radians (if unit is 'rad').
    
    Returns:
    -------
    string
        country name.
    """
    
    # List of names used to bypass the restrictions of the online server, which limits the number of requests per user.
    names="""Martin	Bernard	Thomas	Petit	Robert	Richard	Durand	Dubois	Moreau	Laurent	Simon	Michel	Lefebvre	Leroy
            Roux	David	Bertrand	Morel	Fournier	Girard	BonnetDupont	Lambert	Fontaine	Rousseau	Vincent	Muller	
            Lefevre	Faure	Andre	Mercier	Blanc	Guerin	Boyer	Garnier	Chevalier	Francois	Legrand	Gauthier	Garcia	
            Perrin	Robin	Clement	Morin	Nicolas	Henry	Roussel	Mathieu	Gautier	Masson	Marchand	Duval	Denis	Dumont	
            Marie	Lemaire	Noel	Meyer	Dufour	Meunier	Brun	Blanchard	Giraud	Joly	Riviere	Lucas	Brunet	Gaillard	
            Barbier	Arnaud	Martinez	Gerard	Roche	Renard	Schmitt	Roy	Leroux	Colin	Vidal	Caron	Picard	Roger	Fabre	
            Aubert	Lemoine	Renaud	Dumas	Lacroix	Olivier	Philippe	Bourgeois	Pierre	Benoit	Rey	Leclerc	Payet	Rolland	
            Leclercq	Guillaume	Lecomte	Lopez	Jean	Dupuy	Guillot	Hubert	Berger	Carpentier	Sanchez	Dupuis	Moulin	
            Louis	Deschamps	Huet	Vasseur	Perez	Boucher	Fleury	Royer	Klein	Jacquet	Adam	Paris	Poirier	Marty	
            Aubry	Guyot	Carre	Charles	Renault	Charpentier	Menard	Maillard	Baron	BertinBailly	Herve	Schneider	
            Fernandez	Le	Collet	Leger	Bouvier	Julien	Prevost	Millet	Perrot	Daniel	Le	Cousin	Germain	Breton	Besson	
            Langlois	Remy	Le	Pelletier	Leveque	Perrier	Leblanc	Barre	Lebrun	Marchal	Weber	Mallet	Hamon	Boulanger	
            Jacob	Monnier	Michaud	Rodriguez	Guichard	Gillet	Etienne	Grondin	Poulain	Tessier	Chevallier	CollinChauvin	Da	
            Bouchet	Gay	Lemaitre	Benard	Marechal	Humbert	Reynaud	Antoine	Hoarau	Perret	Barthelemy	Cordier	Pichon	Lejeune	
            Gilbert	Lamy	Delaunay	Pasquier	CarlieLaporte"""

    # chose agent name
    agent=random.choice(names.split())
    
    # initialize Nominatim API
    geolocator = Nominatim(user_agent=agent)
    
    # location informations
    location = geolocator.reverse(str(latitude)+","+str(longitude))
    
    # country name
    country =  (str(location).split()[-1].strip()).replace(',','')
    
    if country == "France":
        return str(location).split(",")[-3].strip()
        # {{"France métropolitaine": "FRA"}, {"Guadeloupe": "GLP"}, 
        #   {"Saint-Barthélemy": "BLM"}, {"Îles Éparses de l'océan Indien": "ATF"}, 
        #   {"Île Royale": "GUF"}, {"Saint-Martin (France)": "MAF"}, {"Martinique": "MTQ"}, 
        #   {"Mayotte": "MYT"}, {"Nouvelle-Calédonie": "NCL"}, {"La Réunion": "REU"},
        #   {"Saint-Pierre-et-Miquelon": "SPM"}, {"Wallis-et-Futuna": "WLF"}}
    elif country == "Nederland":
        return str(location).split(",")[-3].strip()
        # {{"Nederland": "NLD"}, {"Oranjestad": "BES"}}
    else:
        return country