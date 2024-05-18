import streamlit as st
from weibull_calculator import WeibullCalculator
from unit_conversions import UnitConversions
from display_helpers import *

#Get the log files from user input
files = initial_setup()

#Initialize "static" classes
calc = WeibullCalculator()
converter = UnitConversions()

#Open and analyze the log files
results, heatmaps = open_files(files, calc, converter)

#TODO: button to allow user to decide if they want to view heatmaps

#If button: display heatmaps
display_heatmaps(heatmaps)
#else:

download_heatmaps(heatmaps)

download_results(results)