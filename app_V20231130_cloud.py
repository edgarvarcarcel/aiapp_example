# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:52:34 2023

This file is used to generate app for Anastomotic leaage prediction
"""

# Load libraries
import streamlit as st
import scipy.stats as sta
import pandas as pd
import pickle as pkl
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import numpy as np
plt.style.use('grayscale')

# Load libraries for R interaction
import os
#os.environ['R_HOME'] = "D:\Programas\R-4.3.1"
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
##############################################################################
# GLOBAL PARAMETERS
MODEL_PATH = r'models'
MODEL_NAME = '/model_lasso.rds'
DATA_PATH = r'data'
DATA_FILE_NAME = '\DATA_COMPLETE_New.xlsx'
COMMAND_LOAD_R_MODEL = 'loaded_model <- readRDS("' + MODEL_PATH + MODEL_NAME + '")'



##############################################################################
# Initializite app by loading model
@st.cache_data() # We use this decorator so this initialization doesn't run every time the user change into the page
def initialize_app():
    # Load the model in R
    ro.r('library(caret)')
    ro.r(COMMAND_LOAD_R_MODEL)
    print('R Model loaded')
    # Assign model in Python
    loaded_model = ro.r('loaded_model')
    
    return loaded_model
###############################################################################
# Preprocess input function
def preprocess_input(age , female , height , weight, bmi , smoker , alcohol , nutrition,
                     prior , leukkocytosis , steroids , cci , asa, renal , albumin , hemoglobin , 
                     hand , emergent , laparoscopic , ileosotma , type_ , indication , perforation,
                     livermets):
    
    
    
    
    return None

##############################################################################
# Page configuration
st.set_page_config(
    page_title="Anastomotic Leakage Prediction App"
)
st.set_option('deprecation.showPyplotGlobalUse', False)
# Initialize app
model =  initialize_app()

# Option Menu configuration
selected = option_menu(
    menu_title = 'Main Menu',
    options = ['Home' , 'Case 1' , 'Case 2'],
    icons = ['house' , 'book' , 'evenlope'],
    menu_icon = 'cast',
    default_index = 0,
    orientation = 'horizontal')

######################
# Home page layout
######################
if selected == 'Home':
    st.title('BMI Prediction App')
    st.markdown("""
    This app contains 3 sections which you can access from the horizontal menu above.\n
    The sections are:\n
    Home: The main page of the app.\n
    Case 1: On this section you can predict the BMI future values of the patient when you don't have information for future BMI\n
    Case 2: On this section you can predict future BMI values based on the real BMI values you already have.
    """)