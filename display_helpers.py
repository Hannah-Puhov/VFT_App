import pandas as pd
import streamlit as st
from input_analyzer import analyze_file

def initial_setup():
    """
    Perform the initial setup for the VFT results/heatmap generator

    Returns:
        list: A list containing the uploaded files
    """
    st.markdown("""
        <h1 style="text-align: center;">
            VFT Heatmap and Results Generator
        </h1>
        
        <p style="text-align: center;">
            Generate results files and heatmaps from uploaded
            VFT log files
        </p> 
        """, unsafe_allow_html=True)
    
    st.markdown("""
            ### Input VFT log files below:
            
            Refresh to add additional files
            """)
    
    files = st.file_uploader("Test log files", accept_multiple_files=True, type='csv', label_visibility='hidden')

    return files

def open_files(files, calc, converter):
    """Open inputted files and call file analyzer, then return
        results file text and heatmaps

    Args:
        files (list): List of UploadedFile objects from the st file input
        calc (WeibullCalculator): Global Weibull calculator object 
        converter (UnitConversions): Global unit conversions object

    Returns:
        map, map: A map of results file names and the corresponding list of lines,
                    A map of results file names and the corresponding heatmaps
    """    
    current_file = st.empty()
    bar = st.progress(0)
    if len(files) == 0:
        st.stop()

    indexIteration = (int) (100 / len(files))
    index = indexIteration

    results = {}
    heatmaps = {}
    if files is not None:
        for file in files: 
            current_file.text(f'Now analyzing {file.name}')
            bar.progress(index)
            index += indexIteration
            resultsFilename, output, heatmap = analyze_file(file, calc, converter)
            results.update({resultsFilename, output})
            heatmaps.update({resultsFilename, heatmap})

    return results, heatmaps

def download_heatmaps(heatmaps):
    """Zip a collection of heatmaps and display a download button

    Args:
        heatmaps (list): A list of VFT heatmaps with reliability index data
    """    
    pass

def download_results(results):
    """Zip a collection of results files and display a download button

    Args:
        results (list): A list of file-like objects containing the
          results of a VFT
    """    
    pass

def display_heatmaps(heatmaps):
    """Display a collection of heatmaps to the streamlit page

    Args:
        heatmaps (list): A list of VFT heatmaps with reliability index data
    """    
    pass

