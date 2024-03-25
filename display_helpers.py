import os
import zipfile
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

    #Set up a progress bar to track file processing
    current_file = st.empty()
    bar = st.progress(0)
    if len(files) == 0:
        st.stop()

    #Calculate the iteration index for progress bar updating
    indexIteration = (int) (100 / len(files))
    index = indexIteration

    #Initialize variables
    results = {}
    heatmaps = {}

    #Iterate through each file (if they have been inputted)
    if files is not None:
        for file in files: 

            #Display the current file name and update the progress
            current_file.text(f'Now analyzing {file.name}')
            bar.progress(index)
            index += indexIteration

            #Get the file data and add the output and heatmap to corresponding dicts
            resultsFilename, output, heatmap = analyze_file(file, calc, converter)
            results.update({resultsFilename, output})
            heatmaps.update({resultsFilename, heatmap})

    return results, heatmaps

def download_heatmaps(heatmaps):
    """Zip a collection of heatmaps and display a download button

    Args:
        heatmaps (list): A list of VFT heatmaps with reliability index data
    """    
    # Create a temporary directory to store the heatmap images
    temp_dir = "temp_heatmaps"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Save each heatmap as an image in the temporary directory
    for i, heatmap in enumerate(heatmaps):
        heatmap.write_image(f"{temp_dir}/heatmap_{i}.png")
    
    # Create a zip file containing the heatmap images
    with zipfile.ZipFile("heatmaps.zip", "w") as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    
    # Display a download button for the zip file
    with open("heatmaps.zip", "rb") as f:
        zip_data = f.read()
    st.download_button(label="Download Heatmaps", data=zip_data, file_name="heatmaps.zip", mime="application/zip")


def download_results(results):
    """Zip a collection of results files and display a download button

    Args:
        results (list): A list of file-like objects containing the
          results of a VFT
    """    
    # Create a temporary directory to store the results files
    temp_dir = "temp_results"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Save each result as a CSV file in the temporary directory
    for i, result in enumerate(results):
        with open(f"{temp_dir}/result_{i}.csv", "w") as f:
            f.write(result)
    
    # Create a zip file containing the results files
    with zipfile.ZipFile("results.zip", "w") as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    
    # Display a download button for the zip file
    with open("results.zip", "rb") as f:
        zip_data = f.read()
    st.download_button(label="Download Results", data=zip_data, file_name="results.zip", mime="application/zip")


def display_heatmaps(heatmaps):
    """Display a collection of heatmaps to the streamlit page

    Args:
        heatmaps (list): A list of VFT heatmaps with reliability index data
    """    
    # Calculate the number of columns based on browser width
    num_columns = min(4, max(2, int(st._get_metrics_reporter().layout['browser']['size']['width'] / 400)))
    
    # Calculate the number of rows
    num_rows = -(-len(heatmaps) // num_columns)  # Ceiling division
    
    # Display heatmaps in rows
    for i in range(num_rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            idx = i * num_columns + j
            if idx < len(heatmaps):
                cols[j].plotly_chart(heatmaps[idx])
            else:
                cols[j].empty()

