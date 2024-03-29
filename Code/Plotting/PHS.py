import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from matplotlib.colors import LogNorm
from Plotting.HelperFunctions import filter_events, filter_coincident_events

# ============================================================================
# PHS (1D) - VMM
# ============================================================================


def PHS_1D_VMM_plot(window):
    """
    VMM mapping. Returns 1D cumulative PHS plots for raw data.
    """
    def PHS_1D_plot_bus(events, sub_title, number_bins):
        # Plot
        if VMM == 2:
            sub_title += ' (Grids)'
        else:
            sub_title += ' (Wires)'
        plt.title(sub_title)
        plt.xlabel('Collected charge [ADC channels]')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        #plt.yscale('log')
        plt.hist(events.adc, bins=number_bins,
                 range=[0, 1050], histtype='stepfilled',
                 facecolor='lightgrey', ec='black', zorder=5)
    # Declare parameters
    VMM_order_20 = [2, 3, 4, 5]
    VMM_order_16 = [2, 3, 4, 5]
    number_bins = int(window.phsBins.text())
    # Import data
    df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    #print(df_16)
    # Initial filter
    clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.98)
    fig.set_figheight(8)
    fig.set_figwidth(13)
    # Plot figure

    # for 20 layers
    for i, VMM in enumerate(VMM_order_20):
        events_VMM_20 = clusters_20[clusters_20.chip_id == VMM]
        plt.subplot(2, 4, i+1)
        sub_title = 'VMM: %s' % VMM + " -- 20 layers"
        PHS_1D_plot_bus(events_VMM_20, sub_title, number_bins)

    # for 16 layers
    for i, VMM in enumerate(VMM_order_16):
        events_VMM_16 = clusters_16[clusters_16.chip_id == VMM]
        plt.subplot(2, 4, i+5)
        sub_title = 'VMM: %s' % VMM + " -- 16 layers"
        PHS_1D_plot_bus(events_VMM_16, sub_title, number_bins)
    #plt.tight_layout()
    plt.subplots_adjust(left=0.07, right=0.95, top=0.87, bottom=0.08, wspace=0.35, hspace=0.37)
    return fig

# ============================================================================
# PHS (1D) - MG
# ============================================================================

def PHS_1D_MG_plot(window):
    """
    MG mapping. Returns 1D cumulative PHS plot for raw events.
    """
    def PHS_1D_plot_bus(clusters, typeCh, sub_title, number_bins):
        # Plot
        plt.title(sub_title)
        plt.xlabel('Collected charge [ADC channels]')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        #plt.yscale('log')
        plt.hist(clusters[clusters[typeCh] >= 0].adc, bins=number_bins,
                 range=[0, 1050], histtype='stepfilled', ec='black',
                 facecolor='lightgrey', zorder=5)
    # Declare parameters
    number_bins = int(window.phsBins.text())
    typeChs = ['gCh', 'wCh']
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}

    # Import data
    df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Initial filter
    clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)

    # Prepare figure
    fig = plt.figure()
    title = 'PHS (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.98)
    fig.set_figheight(6)
    fig.set_figwidth(9)
    # Plot figure

    # for 20 layers
    for i, typeCh in enumerate(typeChs):
        plt.subplot(2, 2, i+1)
        sub_title = "%s -- 20 layers" % grids_or_wires[typeCh]
        PHS_1D_plot_bus(clusters_20, typeCh, sub_title, number_bins)
    plt.tight_layout()
    # for 16 layers
    for i, typeCh in enumerate(typeChs):
        plt.subplot(2, 2, i+3)
        sub_title = "%s -- 16 layers" % grids_or_wires[typeCh]
        PHS_1D_plot_bus(clusters_16, typeCh, sub_title, number_bins)
    #plt.tight_layout()
    plt.subplots_adjust(left=0.07, right=0.95, top=0.88, bottom=0.08, wspace=0.25, hspace=0.35)

    return fig


# =============================================================================
# PHS (2D) - VMM
# =============================================================================


def PHS_2D_VMM_plot(window):
    """
    VMM mapping. Returns 2D PHS plot.
    """
    def PHS_2D_plot_bus(events, VMM, limit, bins, sub_title, vmin, vmax):
        if VMM == 2:
            sub_title += ' (Grids)'
        else:
            sub_title += ' (Wires)'
        plt.xlabel('Channel')
        plt.ylabel('Charge [ADC channels]')
        plt.title(sub_title)
        plt.hist2d(events.channel, events.adc, bins=[bins, 120],
                   range=[limit, [0, 1050]], norm=LogNorm(),
                   vmin=vmin, vmax=vmax, cmap='jet')
        plt.colorbar()


    number_bins = int(window.phsBins.text())
    # Import data
    df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Initial filter
    clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)
    # Declare parameters
    VMM_order_20 = [2, 3, 4, 5]
    VMM_order_16 = [2, 3, 4, 5]
    VMM_limits_20 = [[15.5, 48.5],
                    [17.5, 46.5],
                    [16.5, 46.5],
                    [16.5, 46.5]]
    VMM_limits_16 = [[15.5, 48.5],
                    [17.5, 46.5],
                    [16.5, 46.5],
                    [16.5, 46.5]]
    VMM_bins_20 = [33, 29, 30, 30]
    VMM_bins_16 = [33, 29, 30, 30]
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (2D) - VMM\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.99)
    vmin = 1
    vmax_20 = clusters_20.shape[0] // 1000 + 100
    vmax_16 = clusters_16.shape[0] // 1000 + 100
    fig.set_figheight(8)
    fig.set_figwidth(13)
    # Plot figure
    # for 20 layers
    for i, (VMM, limit, bins) in enumerate(zip(VMM_order_20, VMM_limits_20, VMM_bins_20)):
        events_VMM_20 = clusters_20[clusters_20.chip_id == VMM]
        plt.subplot(2, 4, i+1)
        sub_title = 'VMM: %s -- 20 layers' % VMM
        PHS_2D_plot_bus(events_VMM_20, VMM, limit, bins, sub_title, vmin, vmax_20)
    plt.tight_layout()
    # for 16 layers
    for i, (VMM, limit, bins) in enumerate(zip(VMM_order_16, VMM_limits_16, VMM_bins_16)):
        events_VMM_16 = clusters_16[clusters_16.chip_id == VMM]
        plt.subplot(2, 4, i+5)
        sub_title = 'VMM: %s -- 16 layers' % VMM
        PHS_2D_plot_bus(events_VMM_16, VMM, limit, bins, sub_title, vmin, vmax_16)
    #plt.tight_layout()
    plt.subplots_adjust(left=0.06, right=0.97, top=0.89, bottom=0.08, wspace=0.38, hspace=0.35)
    return fig

# =============================================================================
# PHS (2D) - MG
# =============================================================================

def PHS_2D_MG_plot(window):
    """
    MG mapping. Returns 2D PHS plot.
    """
    def PHS_2D_plot_bus(events, typeCh, limit, bins, sub_title, vmin, vmax):
        plt.xlabel('Channel')
        plt.ylabel('Charge [ADC channels]')
        plt.title(sub_title)
        plt.hist2d(events[typeCh], events.adc, bins=[bins, 120],
                   range=[limit, [0, 1050]], norm=LogNorm(),
                   vmin=vmin, vmax=vmax, cmap='jet')
        plt.colorbar()

    def get_wire_events(events, window):
        events_red = None
        if window.wCh_filter.isChecked():
            wCh_min = window.wCh_min.value()
            wCh_max = window.wCh_max.value()
            events_red = events[(events['wCh'] >= wCh_min)
                                & (events['wCh'] <= wCh_max)]
        else:
            events_red = events[(events['wCh'] >= 0)
                                & (events['wCh'] <= 79)]

        return events_red

    def get_grid_events(events, window):
        events_red = None
        if window.gCh_filter.isChecked():
            gCh_min = window.gCh_min.value()
            gCh_max = window.gCh_max.value()
            events_red = events[(events['gCh'] >= gCh_min)
                              & (events['gCh'] <= gCh_max)]
        else:
            events_red = events[(events['gCh'] >= 0)
                              & (events['gCh'] <= 12)]

        return events_red


    # Import data
    df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Declare parameters
    typeChs = ['gCh', 'wCh']
    limits_20 = [[-0.5, 11.5], [-0.5, 78.5]]
    bins_20 = [12, 79]
    limits_16 = [[-0.5, 11.5], [-0.5, 62.5]]
    bins_16 = [12, 63]
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}
    # Initial filter
    clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)

    # Prepare figure
    fig = plt.figure()
    title = 'PHS (2D) - MG\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.99)
    vmin = None# 1
    vmax_20 = None #clusters_20.shape[0] // 1000 + 100
    vmax_16 = None #clusters_16.shape[0] // 1000 + 100
    fig.set_figheight(6)
    fig.set_figwidth(9)
    # Plot figure
    # for 20 layers
    for i, (typeCh, limit, bins) in enumerate(zip(typeChs, limits_20, bins_20)):
        # Filter events based on wires or grids
        if typeCh == 'wCh':
            events_red_20 = get_wire_events(clusters_20, window)
        else:
            events_red_20 = get_grid_events(clusters_20, window)
        plt.subplot(2, 2, i+1)
        sub_title = 'PHS: %s -- 20 layers' % grids_or_wires[typeCh]
        PHS_2D_plot_bus(events_red_20, typeCh, limit, bins, sub_title, vmin, vmax_20)
    plt.tight_layout()
    # for 16 layers
    for i, (typeCh, limit, bins) in enumerate(zip(typeChs, limits_16, bins_16)):
        # Filter events based on wires or grids
        if typeCh == 'wCh':
            events_red_16 = get_wire_events(clusters_16, window)
        else:
            events_red_16 = get_grid_events(clusters_16, window)
        plt.subplot(2, 2, i+3)
        sub_title = 'PHS: %s -- 16 layers' % grids_or_wires[typeCh]
        PHS_2D_plot_bus(events_red_16, typeCh, limit, bins, sub_title, vmin, vmax_16)
    #plt.tight_layout()
    plt.subplots_adjust(left=0.09, right=0.98, top=0.89, bottom=0.1, wspace=0.25, hspace=0.35)
    return fig


# =============================================================================
# PHS (Individual Channels)
# =============================================================================

def PHS_Individual_plot(window):
    """
    MG mapping, makes 1D PHS plot for all individual channels.
    Can be done for raw events, clustered events, and both overlayed.
    Accepts filters on grid and wire multiplicity.
    """
    # Import data
    df_events_20   = window.Events_20_layers
    df_events_16   = window.Events_16_layers
    # Intial filter
    events_20   = filter_events(df_events_20, window)
    events_16   = filter_events(df_events_16, window)
    # Declare parameters
    events_vec  = [events_16, events_20]
    detectors  = ['16_layers', '20_layers']
    layers_vec = [16, 20]
    dir_name = os.path.dirname(__file__)
    folder_path = os.path.join(dir_name, '../../Results/PHS')
    number_bins = int(window.phsBins.text())

    if window.PHS_raw.isChecked():
        # Save all PHS
        for events, detector, layers in zip(events_vec, detectors, layers_vec):
            # Save wires PHS
            for wCh in np.arange(0, layers*4, 1):
                print('%s, Wires: %d/%d' % (detector, wCh, layers*4-1))
                # Get ADC values
                adcs = events[events.wCh == wCh]['adc']
                # Plot
                fig = plt.figure()
                plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightgrey', ec='black', zorder=5)
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.title('PHS wires - Channel %d\nData set: %s' % (wCh, window.data_sets))
                # Save
                output_path = '%s/%s/Wires_%s_raw/Channel_%d.pdf' % (folder_path, detector, layers, wCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()
            # Save grids PHS
            for gCh in np.arange(0, 12, 1):
                print('%s, Grids: %d/11' % (detector, gCh))
                # Get ADC values
                adcs = events[events.gCh == gCh]['adc']
                # Plot
                fig = plt.figure()
                plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightgrey', ec='black', zorder=5)
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.title('PHS grids - Channel %d\nData set: %s' % (gCh, window.data_sets))
                # Save
                output_path = '%s/%s/Grids_%s_raw/Channel_%d.pdf' % (folder_path, detector, layers, gCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()

    elif window.PHS_clustered.isChecked():
        # Save all PHS
        for events, detector, layers in zip(events_vec, detectors, layers_vec):
            # Save wires PHS
            for wCh in np.arange(0, layers*4, 1):
                print('%s, Wires: %d/%d' % (detector, wCh, layers*4-1))
                # Get ADC values
                if window.wM_filter.isChecked():
                    adcs = events[(events.wCh == wCh)
                                & (window.wM_min.value() <= events.wM)
                                & (events.wM <= window.wM_max.value())
                                & (events.gM >= window.gM_min.value())
                                & (events.gM <= window.gM_max.value())
                                & (events.chip_id != 2)].adc
                else:
                    adcs = events[(events.wCh == wCh)
                                & (events.chip_id != 2)].adc
                # Plot
                fig = plt.figure()
                plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightblue', ec='black', zorder=5)
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.title('PHS wires - Channel %d\nData set: %s' % (wCh, window.data_sets))
                # Save
                output_path = '%s/%s/Wires_%s_clustered/Channel_%d.pdf' % (folder_path, detector, layers, wCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()
            # Save grids PHS
            for gCh in np.arange(0, 12, 1):
                print('%s, Grids: %d/11' % (detector, gCh))
                # Get ADC values
                if window.gM_filter.isChecked():
                    adcs = events[(events.gCh == gCh)
                                & (window.gM_min.value() <= events.gM)
                                & (events.gM <= window.gM_max.value())
                                & (events.wM >= window.wM_min.value())
                                & (events.wM <= window.wM_max.value())
                                & (events.chip_id == 2)].adc
                else:
                    adcs = events[(events.gCh == gCh)
                                & (events.chip_id == 2)].adc

                # Plot
                fig = plt.figure()
                plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightblue', ec='black', zorder=5)
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.title('PHS grids - Channel %d\nData set: %s' % (gCh, window.data_sets))
                # Save
                output_path = '%s/%s/Grids_%s_clustered/Channel_%d.pdf' % (folder_path, detector, layers, gCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()

    elif window.PHS_overlay.isChecked():
        # Save all PHS
        for events, detector, layers in zip(events_vec, detectors, layers_vec):
            # Save wires PHS
            for wCh in np.arange(0, layers*4, 1):
                print('%s, Wires: %d/%d' % (detector, wCh, layers*4-1))
                # Get ADC values
                adcs_events = events[events.wCh == wCh]['adc']
                if window.wM_filter.isChecked():
                    adcs_clusters = events[(events.wCh == wCh)
                                         & (window.wM_min.value() <= events.wM)
                                         & (events.wM <= window.wM_max.value())
                                         & (events.gM >= window.gM_min.value())
                                         & (events.gM <= window.gM_max.value())
                                         & (events.chip_id != 2)].adc
                else:
                    adcs_clusters = events[(events.wCh == wCh)
                                         & (events.chip_id != 2)].adc
                # Plot
                fig = plt.figure()
                plt.hist(adcs_events, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightgrey', ec='black', zorder=5, label='raw')
                plt.hist(adcs_clusters, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightblue', ec='black', alpha=0.6, zorder=5, label='clustered')
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.legend()
                plt.title('PHS wires - Channel %d\nData set: %s' % (wCh, window.data_sets))
                # Save
                output_path = '%s/%s/Wires_%s_overlay/Channel_%d.pdf' % (folder_path, detector, layers, wCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()
            # Save grids PHS
            for gCh in np.arange(0, 12, 1):
                print('%s, Grids: %d/11' % (detector, gCh))
                # Get ADC values
                adcs_events = events[events.gCh == gCh]['adc']
                if window.gM_filter.isChecked():
                    adcs_clusters = events[(events.gCh == gCh)
                                         & (window.gM_min.value() <= events.gM)
                                         & (events.gM <= window.gM_max.value())
                                         & (events.wM >= window.wM_min.value())
                                         & (events.wM <= window.wM_max.value())
                                         & (events.chip_id == 2)].adc
                else:
                    adcs_clusters = events[(events.gCh == gCh)
                                         & (events.chip_id == 2)].adc
                # Plot
                fig = plt.figure()
                plt.hist(adcs_events, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightgrey', ec='black', zorder=5, label='raw')
                plt.hist(adcs_clusters, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightblue', ec='black', alpha=0.6, zorder=5, label='clustered')
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.legend()
                plt.title('PHS grids - Channel %d\nData set: %s' % (gCh, window.data_sets))
                # Save
                output_path = '%s/%s/Grids_%s_overlay/Channel_%d.pdf' % (folder_path, detector, layers, gCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()

def PHS_Individual_Channel_plot(window, channel):
    """
    MG mapping, makes 1D PHS plot for all individual channels, but only
    one at a time: Select wire/grid channel and which detector.
    Can be done for raw events, clustered events, and both overlayed.
    Accepts filters on grid and wire multiplicity.
    """
    # Import data
    df_events_20   = window.Events_20_layers
    df_events_16   = window.Events_16_layers
    # Intial filter
    events_20   = filter_events(df_events_20, window)
    events_16   = filter_events(df_events_16, window)

    if window.ind_ch_20.isChecked():
        events = events_20
        layers = '20 layers'
    else:
        events = events_16
        layers = '16 layers'

    number_bins = int(window.phsBins.text())
    # Plot
    fig = plt.figure()
    # Get ADC values
    if window.PHS_raw.isChecked():
        if window.ind_gCh.isChecked():
            adcs = events[events.gCh == channel]['adc']
            w_or_g = 'grid'
        elif window.ind_wCh.isChecked():
            adcs = events[events.wCh == channel]['adc']
            w_or_g = 'wire'
        plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                facecolor='lightgrey', ec='black', zorder=5)
    elif window.PHS_clustered.isChecked():
        if window.ind_gCh.isChecked():
            w_or_g = 'grid'
            if window.gM_filter.isChecked():
                adcs = events[(events.gCh == channel)
                            & (window.gM_min.value() <= events.gM)
                            & (events.gM <= window.gM_max.value())
                            & (events.wM >= window.wM_min.value())
                            & (events.wM <= window.wM_max.value())
                            & (events.chip_id == 2)].adc
            else:
                adcs = events[(events.gCh == channel)
                            & (events.chip_id == 2)].adc
        elif window.ind_wCh.isChecked():
            w_or_g = 'wire'
            if window.wM_filter.isChecked():
                adcs = events[(events.wCh == channel)
                            & (window.wM_min.value() <= events.wM)
                            & (events.wM <= window.wM_max.value())
                            & (events.gM >= window.gM_min.value())
                            & (events.gM <= window.gM_max.value())
                            & (events.chip_id != 2)].adc
            else:
                adcs = events[(events.wCh == channel)
                            & (events.chip_id != 2)].adc
        plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                facecolor='lightblue', ec='black', zorder=5)
    elif window.PHS_overlay.isChecked():
        if window.ind_gCh.isChecked():
            w_or_g = 'grid'
            adcs_events = events[events.gCh == channel]['adc']
            if window.gM_filter.isChecked():
                adcs_clusters = events[(events.gCh == channel)
                                     & (window.gM_min.value() <= events.gM)
                                     & (events.gM <= window.gM_max.value())
                                     & (events.wM >= window.wM_min.value())
                                     & (events.wM <= window.wM_max.value())
                                     & (events.chip_id == 2)].adc
            else:
                adcs_clusters = events[(events.gCh == channel)
                                     & (events.chip_id == 2)].adc

        elif window.ind_wCh.isChecked():
            w_or_g = 'wire'
            adcs_events = events[events.wCh == channel]['adc']
            if window.wM_filter.isChecked():
                adcs_clusters = events[(events.wCh == channel)
                                     & (window.wM_min.value() <= events.wM)
                                     & (events.wM <= window.wM_max.value())
                                     & (events.gM >= window.gM_min.value())
                                     & (events.gM <= window.gM_max.value())
                                     & (events.chip_id != 2)].adc
            else:
                adcs_clusters = events[(events.wCh == channel)
                                     & (events.chip_id != 2)].adc

        plt.hist(adcs_events, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                 facecolor='lightgrey', ec='black', zorder=5, label='raw')
        plt.hist(adcs_clusters, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                 facecolor='lightblue', ec='black', alpha=0.6, zorder=5, label='clustered')
        plt.legend()
    plt.grid(True, which='major', zorder=0)
    plt.grid(True, which='minor', linestyle='--', zorder=0)
    plt.xlabel('Collected charge [ADC channels]')
    plt.ylabel('Counts')
    plt.title('PHS %s channel %d -- %s\nData set: %s' % (w_or_g, channel, layers, window.data_sets))
    return fig

def PHS_cluster_plot(window):
    """
    MG mapping, makes 1D PHS plot for clustered (neutron)
    events
    """
    def PHS_cluster_plot_bus(clusters, typeCh, sub_title, number_bins):
        plt.title(sub_title)
        plt.xlabel('Collected charge [ADC channels]')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        if typeCh == 'gCh':
            if window.gM_filter.isChecked():
                adcs = clusters[(window.gM_min.value() <= clusters.gM)
                              & (clusters.gM <= window.gM_max.value())
                              & (clusters.wM >= window.wM_min.value())
                              & (clusters.wM <= window.wM_max.value())
                              & (clusters.chip_id == 2)].adc
            else:
                adcs = clusters[clusters.chip_id == 2].adc

        elif typeCh == 'wCh':
            if window.wM_filter.isChecked():
                adcs = clusters[(window.wM_min.value() <= clusters.wM)
                              & (clusters.wM <= window.wM_max.value())
                              & (clusters.gM >= window.gM_min.value())
                              & (clusters.gM <= window.gM_max.value())
                              & (clusters.chip_id != 2)].adc
            else:
                adcs = clusters[clusters.chip_id != 2].adc
        #plt.yscale('log')
        plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                 facecolor='lightblue', ec='black', zorder=5)

    # Import data
    df_16 = window.Events_16_layers
    df_20 = window.Events_20_layers
    # Initial filter
    clusters_16 = filter_events(df_16, window)
    clusters_20 = filter_events(df_20, window)
    number_bins = int(window.phsBins.text())
    # Prepare figure
    fig = plt.figure()
    title = 'PHS clustered (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.98)
    fig.set_figheight(6)
    fig.set_figwidth(8)

    typeChs = ['gCh', 'wCh']
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}
    # for 20 layers
    for i, typeCh in enumerate(typeChs):
        plt.subplot(2, 2, i+1)
        sub_title = "%s -- 20 layers" % (grids_or_wires[typeCh])
        PHS_cluster_plot_bus(clusters_20, typeCh, sub_title, number_bins)
    # for 16 layers
    for i, typeCh in enumerate(typeChs):
        plt.subplot(2, 2, i+3)
        sub_title = "%s -- 16 layers" % (grids_or_wires[typeCh])
        PHS_cluster_plot_bus(clusters_16, typeCh, sub_title, number_bins)
    plt.subplots_adjust(left=0.1, right=0.93, top=0.88, bottom=0.1, wspace=0.35, hspace=0.35)
    return fig

def PHS_1D_overlay_plot(window):
    """
    MG mapping, makes 1D PHS plot overlaying raw events and clustered
    events
    """
    def PHS_1D_overlay_plot_bus(events, typeCh, sub_title, number_bins):
        # Plot
        plt.title(sub_title)
        plt.xlabel('Collected charge [ADC channels]')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        #plt.yscale('log')
        if typeCh == 'gCh':
            if window.gM_filter.isChecked():
                adcs_clusters = events[(window.gM_min.value() <= events.gM)
                                     & (events.gM <= window.gM_max.value())
                                     & (events.wM >= window.wM_min.value())
                                     & (events.wM <= window.wM_max.value())
                                     & (events.chip_id == 2)].adc
            else:
                adcs_clusters = events[events.chip_id == 2].adc
        elif typeCh == 'wCh':
            if window.wM_filter.isChecked():
                adcs_clusters = events[(window.wM_min.value() <= events.wM)
                                     & (events.wM <= window.wM_max.value())
                                     & (events.gM >= window.gM_min.value())
                                     & (events.gM <= window.gM_max.value())
                                     & (events.chip_id != 2)].adc
            else:
                adcs_clusters = events[events.chip_id != 2].adc
        plt.hist(events[events[typeCh] >= 0].adc, bins=number_bins,
                 range=[0, 1050], histtype='stepfilled', ec='black',
                 facecolor='lightgrey', zorder=5, label='raw')
        plt.hist(adcs_clusters, bins=number_bins,
                 range=[0, 1050], histtype='stepfilled', ec='black',
                 facecolor='lightblue', alpha=0.6, zorder=5, label='clustered')
        plt.legend()

    # Import data
    raw_20 = window.Events_20_layers
    raw_16 = window.Events_16_layers
    # Apply filters
    events_16 = filter_events(raw_16, window)
    events_20 = filter_events(raw_20, window)

    number_bins = int(window.phsBins.text())
    typeChs = ['gCh', 'wCh']
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}
    # Prepare figure
    fig = plt.figure()
    title = 'PHS overlay (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.98)
    fig.set_figheight(6)
    fig.set_figwidth(8)
    # Plot figure
    # for 20 layers
    for i, typeCh in enumerate(typeChs):
        plt.subplot(2, 2, i+1)
        sub_title = "%s -- 20 layers" % (grids_or_wires[typeCh])
        PHS_1D_overlay_plot_bus(events_20, typeCh, sub_title, number_bins)
    # for 16 layers
    for i, typeCh in enumerate(typeChs):
        plt.subplot(2, 2, i+3)
        sub_title = "%s -- 16 layers" % (grids_or_wires[typeCh])
        PHS_1D_overlay_plot_bus(events_16, typeCh, sub_title, number_bins)

    plt.subplots_adjust(left=0.1, right=0.93, top=0.88, bottom=0.12, wspace=0.3, hspace=0.4)
    return fig
