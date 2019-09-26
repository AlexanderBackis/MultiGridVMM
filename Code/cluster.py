import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import struct
import re
import zipfile
import shutil
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    import h5py


# =============================================================================
# IMPORT DATA
# =============================================================================


def import_data(file_path, window):
    h5_file = h5py.File(file_path, 'r')
    if window.sample_button.isChecked():
        data = pd.DataFrame(h5_file['srs_hits'].value[0:20])
    else:
        data = pd.DataFrame(h5_file['srs_hits'].value)
    return data

# =============================================================================
# CLUSTER DATA
# =============================================================================


def cluster_data(df_raw, window, file_nbr, file_nbrs):
    # Inititate parameters
    time_window = float(window.time_window.text())  # [TDC Channels]
    # Initate data vectors
    size = df_raw.shape[0]
    wMraw = np.zeros([size], dtype=int)
    gMraw = np.zeros([size], dtype=int)
    data_dict = {'wCh': np.zeros([size], dtype=int),
                 'gCh': np.zeros([size], dtype=int),
                 'wM': np.zeros([size], dtype=int),
                 'gM': np.zeros([size], dtype=int),
                 'wADC': np.zeros([size], dtype=int),
                 'gADC': np.zeros([size], dtype=int),
                 'Time': np.zeros([size], dtype=int)
                 }
    MG_channels = {'wCh': np.zeros([size], dtype=int),
                   'gCh': np.zeros([size], dtype=int)}
    # Get mappings
    VMM_ch_to_MG24_ch = get_VMM_to_MG24_mapping()
    chip_id_to_wire_or_grid = {2: ['gCh', 'gM', 'gADC', 'gMAX'],
                               3: ['wCh', 'wM', 'wADC', 'wMAX'],
                               4: ['wCh', 'wM', 'wADC', 'wMAX'],
                               5: ['wCh', 'wM', 'wADC', 'wMAX']}
    gw_ADC_max = {'wMAX': 0, 'gMAX': 0}
    # Get first values
    index = 0
    first_row = df_raw.iloc[0]
    start_time = (int(first_row['srs_timestamp'])
                  + int(first_row['chiptime']))
    #start_time = (int(first_row['srs_timestamp']))
    ADC = int(first_row['adc'])
    chip_id = int(first_row['chip_id'])
    Ch = int(first_row['channel'])

    # Start first cluster
    gw_ADC_max['wMAX'], gw_ADC_max['wMAX'] = 0, 0
    data_dict['wCh'][index], data_dict['gCh'][index] = -1, -1
    data_dict['Time'][index] = start_time
    # Modify first cluster
    mgCh = VMM_ch_to_MG24_ch[chip_id][Ch]
    xCh, xM, xADC, xMAX = chip_id_to_wire_or_grid[chip_id]
    data_dict[xADC][index] += ADC
    data_dict[xM][index] += 1
    if ADC > gw_ADC_max[xMAX]:
        gw_ADC_max[xMAX] = ADC
        data_dict[xCh][index] = mgCh
    MG_channels[xCh][0] = mgCh
    # Get numpy arrays from data frame
    Chs = df_raw['channel'].values[1:].astype(np.int64)
    ADCs = df_raw['adc'].values[1:].astype(np.int64)
    chip_ids = df_raw['chip_id'].values[1:].astype(np.int64)
    Times = (df_raw['srs_timestamp'].values[1:].astype(np.int64)
             + df_raw['chiptime'].values[1:].astype(np.int64))
    #Times = (df_raw['srs_timestamp'].values[1:].astype(np.int64))
    clusterStartIndex = 0
    # Iterate through data
    for i, (Ch, ADC, chip_id, Time) in enumerate(zip(Chs, ADCs, chip_ids, Times)):
        mgCh = VMM_ch_to_MG24_ch[chip_id][Ch]
        if mgCh is None:
            mgCh = -10
        MG_channels['wCh'][i+1], MG_channels['gCh'][i+1] = -1, -1
        if (Time - start_time) < time_window: # selecting max ADC channel within a time window
            # Modify cluster
            xCh, xM, xADC, xMAX = chip_id_to_wire_or_grid[chip_id]
            data_dict[xADC][index] += ADC
            data_dict[xM][index] += 1
            if ADC > gw_ADC_max[xMAX]:
                gw_ADC_max[xMAX] = ADC
                data_dict[xCh][index] = mgCh
        else:
            gMraw[clusterStartIndex:i+1] = data_dict['gM'][index]
            wMraw[clusterStartIndex:i+1] = data_dict['wM'][index]
            # Increase cluster index and reset temporary variables
            index += 1
            clusterStartIndex = i+1
            start_time = Time
            # Start new cluster
            gw_ADC_max['wMAX'], gw_ADC_max['gMAX'] = 0, 0
            data_dict['wCh'][index], data_dict['gCh'][index] = -1, -1
            data_dict['Time'][index] = start_time
            # Modify new cluster
            xCh, xM, xADC, xMAX = chip_id_to_wire_or_grid[chip_id]
            data_dict[xADC][index] += ADC
            data_dict[xM][index] += 1
            if ADC > gw_ADC_max[xMAX]:
                gw_ADC_max[xMAX] = ADC
                data_dict[xCh][index] = mgCh
        # Add MG channel to the raw events
        MG_channels[xCh][i+1] = mgCh

    #Remove empty elements and save in DataFrame for easier analysis
    for key in data_dict.keys():
        data_dict[key] = data_dict[key][0:index]
    df_clustered = pd.DataFrame(data_dict)
    # Append vector to raw dataframe with MG channels
    df_raw = df_raw.join(pd.DataFrame(MG_channels))
    df_raw = df_raw.join(pd.DataFrame({'gM': gMraw}))
    df_raw = df_raw.join(pd.DataFrame({'wM': wMraw}))
    return df_clustered, df_raw

# =============================================================================
# Helper Functions
# =============================================================================

def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line'''

    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(mypath)
    except OSError as exc:
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else:
            raise


def get_VMM_to_MG24_mapping():
    # Import mapping
    dir_name = os.path.dirname(__file__)
    #path_mapping = os.path.join(dir_name, '../Tables/Latest_Isabelle_MG_to_VMM_Mapping.xlsx')
    #path_mapping = os.path.join(dir_name, '../Tables/MG_to_VMM_Mapping_old.xlsx')
    #path_mapping = os.path.join(dir_name, '../Tables/MG_to_VMM_Mapping_16_flipped.xlsx')
    path_mapping = os.path.join(dir_name, '../Tables/new_THE_MG_to_VMM_Mapping.xlsx')
    mapping_matrix = pd.read_excel(path_mapping).values
    # Store in convenient format
    VMM_ch_to_MG24_ch = np.empty((6, 80), dtype='object')
    for row in mapping_matrix:
        VMM_ch_to_MG24_ch[row[1]][row[2]] = row[5]
    return VMM_ch_to_MG24_ch
