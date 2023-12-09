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
from st_aggrid import AgGrid
plt.style.use('grayscale')

# Load libraries for R interaction
import os
os.environ['R_HOME'] = "D:\Programas\R-4.3.1"
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
##############################################################################
# GLOBAL PARAMETERS
MODEL_PATH = r'models'
MODEL_NAME = '/model_glm.rds'
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
# old 
#def preprocess_input(age , female , height , weight, bmi , smoker , alcohol , nutrition,
#                     prior , leukocytosis , steroids , cci , asa, renal , albumin , hemoglobin , 
#                    hand , emergent , laparoscopic , ileostoma , type_ , indication , perforation,
#                     livermets):
def preprocess_input(asa, height, weight, bmi, smoker, alcohol,
                     leukocytosis, cci, renal,
                     albumin, hemoglobin, emergent, laparoscopic, type_):
    # Dictionary to save the information
    information = {}
    
    # Female
    #if female == 'Male':
    #    information['female'] = [0]
    #else:
    #    information['female'] = [1]
    # Age
    #information['age'] = [int(age)]
    # Height
    information['height'] = [int(height)]
    # Weight
    information['weight'] = [int(weight)]
    # BMI
    information['bmi'] = [float(bmi)]
    # Smoker
    if smoker == 'Yes':
        information['smoker'] = [1]
    else:
        information['smoker'] = [0]
    # Alcohol
    if alcohol == 'Yes':
        information['alcohol'] = [1]
    else:
        information['alcohol'] = [0]
    # Nutrition Score
    #information['nutrition'] = [float(nutrition)]
    # Prior abdominal surgery
    #if prior == 'Yes':
    #    information['prior'] = [1]
    #else:
    #    information['prior'] = [0]
    # Leokocytosis
    if leukocytosis == 'Yes':
        information['leukocytosis'] = [1]
    else:
        information['leukocytosis'] = [0]
    # Steroids Usage
    #if steroids == 'Yes':
    #    information['steroids'] = [1]
    #else:
    #    information['steroids'] = [0]
    # CCI
    information['cci'] = [float(cci)]
    # ASA Score
    if asa == 'I':
        information['asa'] = [1]
    if asa == 'II':
        information['asa'] = [2]
    if asa == 'III':
        information['asa'] = [3]
    if asa == 'IV':
        information['asa'] = [4]
    # Renal Function
    if renal == 'G1':
        information['renal'] = [1]
    if renal == 'G2':
        information['renal'] = [2]
    if renal == 'G3':
        information['renal'] = [3]
    if renal == 'G4':
        information['renal'] = [4]
    if renal == 'G5':
        information['renal'] = [5]
    # Albumin
    information['albumin'] = [float(albumin)]
    # Hemoglobin
    information['hemoglobin'] = [float(hemoglobin)]
    # Technique Hand sewn
    #if hand == 'Yes':
    #    information['hand'] = [1]
    #if hand == 'No':
    #    information['hand'] = [0]
    #if hand == 'Unkown':
    #    information['hand'] = [2]
    # Emergency surgery
    if emergent == 'Yes':
        information['emergent'] = [1]
    else:
        information['emergent'] = [0]
    # Laparoscopic
    if laparoscopic == 'Open':
        information['laparoscopic'] = [1]
    if laparoscopic == 'Laparoscopic':
        information['laparoscopic'] = [2]
    if laparoscopic == 'Robotic':
        information['laparoscopic'] = [3]
    # Ileostoma
    #if ileostoma == 'Yes':
    #    information['ileostoma'] = [1]
    #else:
    #    information['ileostoma'] = [0]
    # Surgical Type Approach
    if type_ == 'Extended Left Hemicolectomy':
        information['type'] = [2]
    if type_ == 'Extended Right Hemicolectomy':
        information['type'] = [4]
    if type_ == 'Ileocecal Resection':
        information['type'] = [5]
    if type_ == 'Transverse colectomy':
        information['type'] = [6]
    if type_ == 'Rectosigmoid resertion / Sigmoidectomy':
        information['type'] = [7]
    if type_ == 'Hartmann´s reversal or reversal of colostomy':
        information['type'] = [9]
    # Indication
    #if indication == 'Tumor':
    #    information['indication'] = [1]
    #if indication == 'IBD':
    #    information['indication'] = [2]
    #if indication == 'Diverticulitis disease +':
    #    information['indication'] = [3]
    #if indication == 'Diverticulitis disease':
    #    information['indication'] = [4]
    #if indication == 'Other':
    #    information['indication'] = [5]
    #if indication == 'Ischemia':
    #    information['indication'] = [6]
    # Perforation
    #if perforation == 'Yes':
    #    information['perforation'] = [1]
    #else:
    #    information['perforation'] = [0]
    # Livermets
    #if livermets == 'Yes':
    #    information['livermets'] = [1]
    #else:
    #    information['livermets'] = [0]
    
    # Convert to a dataframe
    information = pd.DataFrame(data = information)
    
    return information

##############################################################################
# Page configuration
st.set_page_config(page_title = "Anastomotic Leakage Prediction App",
                   page_icon=":chart_with_upwards_trend:")

st.set_option('deprecation.showPyplotGlobalUse', False)
# Initialize app
model =  initialize_app()

# Option Menu configuration
selected = option_menu(
    menu_title = 'Main Menu',
    options = ['Home'],
    icons = ['house' ],
    menu_icon = 'cast',
    default_index = 0,
    orientation = 'horizontal')

######################
# Home page layout
######################
if selected == 'Home':
    st.title('Anastomotic Leakage Prediction App')
    st.subheader("To predict A.I. value, you need to follow the steps below:")
    st.markdown("""
    1. Enter clinical parameters of patient on the left side bar.
    2. Press the "Predict" button and wait for the result.
    """)
    
    # Sidebar layout
    st.sidebar.title("Patiens Info")
    st.sidebar.subheader("Please choose parameters")
    
    # Patients info input
    #female = st.sidebar.selectbox('Gender', ('Male' , 'Female'))
    #age = st.sidebar.slider("Age:", min_value = 18, max_value = 100,step = 1)
    height = st.sidebar.slider("Height:", min_value = 140 , max_value = 220, step = 1)
    weight = st.sidebar.slider("Weight:", min_value = 40 , max_value = 160, step = 1)
    bmi = st.sidebar.slider("BMI:" , min_value = 20.0, max_value = 60.0, step = 0.1)
    smoker = st.sidebar.selectbox('Smoker:', ('Yes' , 'No'))
    alcohol = st.sidebar.selectbox('Alcohol:', ('Yes' , 'No'))
    #nutrition = st.sidebar.slider("Nutrition Score:", min_value = 1 , max_value = 10, step = 1)
    #prior = st.sidebar.selectbox('Prior Abdominal Surgery:', ('Yes' , 'No'))
    leukocytosis = st.sidebar.selectbox('Leukocytosis:', ('Yes' , 'No'))
    #steroids = st.sidebar.selectbox('Steroids Usage:', ('Yes' , 'No'))
    cci = st.sidebar.slider("CCI:", min_value = 0 , max_value = 20, step = 1)
    asa = st.sidebar.selectbox('ASA Score', ('I', 'II', 'III', 'IV'))
    renal = st.sidebar.selectbox('Renal Function', ('G1', 'G2', 'G3', 'G4' , 'G5'))
    laparoscopic = st.sidebar.selectbox('Laparoscopic', ('Open', 'Laparoscopic', 'Robotic'))
    albumin = st.sidebar.slider("Albumin:" , min_value = 0.0, max_value = 10.0, step = 0.1)
    hemoglobin = st.sidebar.slider("Hemoglobin:" , min_value = 0.0, max_value = 20.0, step = 0.1)
    #hand = st.sidebar.selectbox('Technique (Hand-Sewn):', ('Yes' , 'No' , 'Unknown'))
    emergent = st.sidebar.selectbox('Emergency Surgery:', ('Yes' , 'No'))
    #ileostoma = st.sidebar.selectbox('Ileostoma:', ('Yes' , 'No'))
    type_ = st.sidebar.selectbox('Surgical Approach:', ('Extended Left Hemicolectomy', # 2
                                                        'Extended Right Hemicolectomy', # 4
                                                        'Ileocecal Resection', # 5
                                                        'Transverse colectomy', # 6
                                                        'Rectosigmoid resertion / Sigmoidectomy', # 7
                                                        'Hartmann´s reversal or reversal of colostomy')) # 9
    #indication = st.sidebar.selectbox('Indication:', ('Tumor',
    #                                                  'IBD',
    #                                                  'Divertivulitis disease',
    #                                                  'Other',
    #                                                  'Ischemia'))
    #perforation = st.sidebar.selectbox('Perforation:', ('Yes' , 'No'))
    #livermets = st.sidebar.selectbox('Livermets:', ('Yes' , 'No'))
    
    # Parser user information
    #user_input = preprocess_input(age, female, height, weight, bmi, smoker, alcohol,
    #                              nutrition, prior, leukocytosis, steroids, cci, asa, renal,
    #                              albumin, hemoglobin, hand, emergent, laparoscopic, ileostoma, type_,
    #                              indication, perforation, livermets)
    user_input = preprocess_input(asa, height, weight, bmi, smoker, alcohol,
                                  leukocytosis, cci, renal,
                                  albumin, hemoglobin, emergent, laparoscopic, type_)
    # Prediction
    predict_button = st.button('Predict')
    if predict_button:
        st.markdown("---")
        # Check that bmi pre is equal or greater than 35
        number_of_warnings = 0
        if user_input['bmi'].values[0] < 20:
            st.warning('The value of BMI 6 pre is lower than 35, check the input', icon="⚠️")
            number_of_warnings += 1
        if number_of_warnings == 0:
            # Predict label
            # Convert pandas dataframe into R object
            with localconverter(ro.default_converter + pandas2ri.converter):
                user_input_r = ro.conversion.py2rpy(user_input)
            # Perform prediction with the loaded model
            prediction_r = ro.r['predict'](model, user_input_r)
            # Convert prediction into python object
            with localconverter(ro.default_converter + pandas2ri.converter):
                prediction_python = ro.conversion.rpy2py(prediction_r)
            # Text to show
            if prediction_python[0] == 'ainYES':
                text_to_show_aux = 'Anastomotic Leakage'
            else:
                text_to_show_aux = 'No Anastomotic Leakage'
            text_to_show = '**' + 'The Label predicted is --> ' + text_to_show_aux + '**'
            # Predict probabilities
            # Assign user input in R
            ro.r.assign('user_input' , user_input_r)
            # Command in R to make prediction
            comand_predict = f"predict(loaded_model, newdata = user_input, type='prob')"
            probs_r = ro.r(comand_predict)
            # convert to pandas
            with localconverter(ro.default_converter + pandas2ri.converter):
                probs_python = ro.conversion.rpy2py(probs_r)
            probs_python.index = ['Probability']
            probs_python.columns = ['No \nAnastomotic Leakage' , 'Anastomotic Leakage']
            st.markdown("<p style='text-align: center;'><strong>Probabilities</strong></p>", unsafe_allow_html=True)
            st.dataframe(probs_python.reset_index(drop = True).astype('object'),
                         column_config = {'index' : 'Metric'},
                         hide_index = True)
            left_column , center_column, right_column = st.columns(3)
            st.markdown(text_to_show)
    # Sponsor Images
    st.markdown("---")
    st.markdown("<p style='text-align: center;'><strong>Sponsored By:</strong></p>", unsafe_allow_html=True)
    images = [r"images/clarunis.PNG",
              r"images/DBE Schwarz.JPG",
              r"images/gzo.png",
              r"images/KSBL.PNG",
              r"images/medtronic.png"]
    column_1 , column_2 , column_3 = st.columns(3 , gap = 'large')
    with column_1:
        st.image(images[3] , width = 100)
    with column_2:
        st.image(images[1] , width = 100)
    with column_3:
        st.image(images[4] , width = 150)
    column_3 , column_4 , column_5 = st.columns(3 , gap = 'medium')
    with column_3:
        st.image(images[0] , width = 150)
    with column_4:
        st.markdown('#')
    with column_5:
        st.image(images[2] , width = 150)
