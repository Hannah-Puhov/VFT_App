import pandas as pd
import streamlit as st

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
