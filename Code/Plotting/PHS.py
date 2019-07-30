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
        plt.yscale('log')
        plt.hist(events.adc, bins=number_bins,
                 range=[0, 1050], histtype='step',
                 color='black', zorder=5)
    # Declare parameters
    VMM_order_20 = [2, 3, 4, 5]
    VMM_order_16 = [2, 3, 4, 5]
    number_bins = int(window.phsBins.text())
    # Import data
    #df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Initial filter
    #clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=1.03)
    fig.set_figheight(8)
    fig.set_figwidth(10)
    # Plot figure
    """
    # for 20 layers
    for i, VMM in enumerate(VMM_order_20):
        events_VMM_20 = clusters_20[clusters_20.chip_id == VMM]
        plt.subplot(4, 2, i+1)
        sub_title = 'VMM: %s' % VMM + " -- 20 layers"
        PHS_1D_plot_bus(events_VMM_20, sub_title, number_bins)
    plt.tight_layout()
    """
    # for 16 layers
    for i, VMM in enumerate(VMM_order_16):
        events_VMM_16 = clusters_16[clusters_16.chip_id == VMM]
        #plt.subplot(4, 2, i+5)
        plt.subplot(2, 2, i+1)
        sub_title = 'VMM: %s' % VMM + " -- 16 layers"
        PHS_1D_plot_bus(events_VMM_16, sub_title, number_bins)
    plt.tight_layout()
    return fig


# ============================================================================
# PHS (1D) - MG
# ============================================================================


def PHS_1D_MG_plot(window):
    def PHS_1D_plot_bus(events, typeCh, sub_title, number_bins):
        # Plot
        plt.title(sub_title)
        plt.xlabel('Collected charge [ADC channels]')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        plt.yscale('log')
        plt.hist(events[events[typeCh] >= 0].adc, bins=number_bins,
                 range=[0, 1050], histtype='step',
                 color='black', zorder=5)

    # Declare parameters
    number_bins = int(window.phsBins.text())
    typeChs = ['wCh', 'gCh']
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}

    # Import data
    #df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Initial filter
    #clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)

    # Prepare figure
    fig = plt.figure()
    title = 'PHS (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=1.03)
    fig.set_figheight(4)
    fig.set_figwidth(10)
    # Plot figure
    """
    # for 20 layers
    for i, typeCh in enumerate(typeChs):
        plt.subplot(2, 2, i+1)
        sub_title = "%s -- 20 layers" % typeCh
        PHS_1D_plot_bus(clusters_20, typeCh, sub_title, number_bins)
    plt.tight_layout()
    """
    # for 16 layers
    for i, typeCh in enumerate(typeChs):
        plt.subplot(2, 2, i+3)
        sub_title = "%s -- 16 layers" % typeCh
        PHS_1D_plot_bus(clusters_16, typeCh, sub_title, number_bins)
    plt.tight_layout()

    return fig


# =============================================================================
# PHS (2D) - VMM
# =============================================================================


def PHS_2D_VMM_plot(window):
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
    #df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Initial filter
    #clusters_20 = filter_events(df_20, window)
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
    fig.suptitle(title, x=0.5, y=1.03)
    vmin = 1
    #vmax_20 = clusters_20.shape[0] // 1000 + 100
    vmax_16 = clusters_16.shape[0] // 1000 + 100
    fig.set_figheight(8)
    fig.set_figwidth(10)
    # Plot figure
    """
    # for 20 layers
    for i, (VMM, limit, bins) in enumerate(zip(VMM_order_20, VMM_limits_20, VMM_bins_20)):
        events_VMM_20 = clusters_20[clusters_20.chip_id == VMM]
        plt.subplot(4, 2, i+1)
        sub_title = 'VMM: %s -- 20 layers' % VMM
        PHS_2D_plot_bus(events_VMM_20, VMM, limit, bins, sub_title, vmin, vmax_20)
    plt.tight_layout()
    """
    # for 16 layers
    for i, (VMM, limit, bins) in enumerate(zip(VMM_order_16, VMM_limits_16, VMM_bins_16)):
        events_VMM_16 = clusters_16[clusters_16.chip_id == VMM]
        plt.subplot(4, 2, i+5)
        sub_title = 'VMM: %s -- 16 layers' % VMM
        PHS_2D_plot_bus(events_VMM_16, VMM, limit, bins, sub_title, vmin, vmax_16)
    plt.tight_layout()
    return fig

# =============================================================================
# PHS (2D) - MG
# =============================================================================


def PHS_2D_MG_plot(window):
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
    #df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Declare parameters
    typeChs = ['wCh', 'gCh']
    limits_20 = [[-0.5, 78.5], [-0.5, 11.5]]
    bins_20 = [79, 12]
    limits_16 = [[-0.5, 62.5], [-0.5, 11.5]]
    bins_16 = [63, 12]
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}
    # Initial filter
    #clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)

    # Prepare figure
    fig = plt.figure()
    title = 'PHS (2D) - MG\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=1.03)
    vmin = None# 1
    vmax_20 = None #clusters_20.shape[0] // 1000 + 100
    vmax_16 = None #clusters_16.shape[0] // 1000 + 100
    fig.set_figheight(4)
    fig.set_figwidth(10)
    # Plot figure
    """
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
    """
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
    plt.tight_layout()
    return fig


# =============================================================================
# PHS (Individual Channels)
# =============================================================================

def PHS_Individual_plot(window):
    # Import data
    #df_20 = window.Events
    df_16 = window.Events
    # Intial filter
    events_16 = filter_events(df_16, window)
    #events_20 = filter_events(df_20, window)
    # Declare parameters
    events_vec = [events_16, events_20]
    detectors = ['16_layers', '20_layers']
    layers_vec = [16, 20]
    dir_name = os.path.dirname(__file__)
    folder_path = os.path.join(dir_name, '../../Results/PHS/')
    number_bins = int(window.phsBins.text())
    # Save all PHS
    for events, detector, layers in zip(events_vec, detectors, layers_vec):
        # Save wires PHS
        for wCh in np.arange(0, layers*4, 1):
            print('%s, Wires: %d/%d' % (detector, wCh, layers*4-1))
            # Get ADC values
            adcs = events[events.wCh == wCh]['adc']
            # Plot
            fig = plt.figure()
            plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='step',
                     color='black', zorder=5)
            plt.grid(True, which='major', zorder=0)
            plt.grid(True, which='minor', linestyle='--', zorder=0)
            plt.xlabel('Collected charge [ADC channels]')
            plt.ylabel('Counts')
            plt.title('PHS wires - Channel %d\nData set: %s' % (wCh, window.data_sets))
            # Save
            output_path = '%s/%s/Wires/Channel_%d.pdf' % (folder_path, detector, wCh)
            fig.savefig(output_path, bbox_inches='tight')
            plt.close()
        # Save grids PHS
        for gCh in np.arange(0, 12, 1):
            print('%s, Grids: %d/11' % (detector, gCh))
            # Get ADC values
            adcs = events[events.gCh == gCh]['adc']
            # Plot
            fig = plt.figure()
            plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='step',
                     color='black', zorder=5)
            plt.grid(True, which='major', zorder=0)
            plt.grid(True, which='minor', linestyle='--', zorder=0)
            plt.xlabel('Collected charge [ADC channels]')
            plt.ylabel('Counts')
            plt.title('PHS grids - Channel %d\nData set: %s' % (gCh, window.data_sets))
            # Save
            output_path = '%s/%s/Grids/Channel_%d.pdf' % (folder_path, detector, gCh)
            fig.savefig(output_path, bbox_inches='tight')
            plt.close()
