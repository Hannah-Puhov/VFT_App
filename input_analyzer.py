import streamlit as st
import pandas as pd
import time

def open_files(files):

    current_file = st.empty()
    bar = st.progress(0)
    indexIteration = (int) (100 / len(files))
    index = indexIteration

    if files is not None:
        for file in files: 
            current_file.text(f'Now analyzing {file.name}')
            bar.progress(index)
            index += indexIteration
            time.sleep(2)

    st.success("All done!")