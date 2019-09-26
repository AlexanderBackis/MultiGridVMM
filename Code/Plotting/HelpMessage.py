from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# =============================================================================
# Help message
# =============================================================================

def gethelp():
    msg = QMessageBox()
    msg.setStyleSheet("QLabel{min-width: 650px; min-height: 60px; font-size: 13px;}")
    msg.setText("How to use this program:")
    msg.setInformativeText("1. Click the \"cluster\" button and select a data file to be analysed. \n Sample: only takes small subset of data set. \n Clustering time window: change time window to define coincident events.    \n\n2. Apply filters (optional). Some filters are for events, some for clusters, some for both.\n     For events: \n     - Chips: which VMM chips \n     - Charge: ADC channels \n     - VMM channel: which channels for VMM \n     For clusters: \n     - gADC: grid ADC channel \t - wADC: wire ADC channel \n     - gM: grid multiplicity \t\t - wM: wire multiplicity\n     For both: \n     - timestamp in ns \n     - gCH: grid channel \t\t - wCH: wire channel  \n\n3. Click on the buttons to get the specific plots.\n     \n Pulse Height Spectra (PHS) \n    Options: \n     - number of bins for PHS plots \n     - channel mapping: VMM or Multi-Grid channel mapping \n     - for raw data, clustered data, and both overlayed PHS \n    Plots\n     - 1D (counts vs collected charge), \n     - 2D (charge vs channel) \n        for wires and grids \n     - Individual: saves 1D PHS for each channel in ../Results folder; or select an individual wire or grid channel\nCoincidences: coincidence events in \n     - 2D (grid vs wire channel number)\n     - 3D (spatial) \nMiscellaneous: \n     - timestamp: timestamp vs event number \n     - rate: prints the rate of neutron events \n     - VMM channels: histogram with channels for each VMM chip")
    msg.setWindowTitle("Help")
    #msg.setStandardButtons(QMessageBox.Ok).setText("Now you know.")
    #msg.addButton(QPushButton('I see.'), QMessageBox.YesRole)
    msg.exec_()
