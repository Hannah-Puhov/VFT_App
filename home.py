import streamlit as st
from display_helpers import *
from input_analyzer import open_files

files = initial_setup()
open_files(files)
