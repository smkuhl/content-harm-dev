import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import random
import requests
import PIL
import time
import os
import sys
import streamlit.components.v1 as components
import SurveyUtils as su
import SurveyText as survey_text
import SurveyState as survey_state
import SurveyForm as survey_form
import Demographics as demographics
import LoginVerification as login_verification


st.set_page_config(page_title="Tweet Annotation", layout="wide")
num_tweet = 20  # i.e st.session_state.annotation_number, easier for referencing
css_path = os.path.abspath("style/style.css")
su.local_css(css_path)
survey_state.state_initializer()
# state_initializer()

######## intro page
if "counter" not in st.session_state or st.session_state.counter < 100:
    st.session_state.counter = 0
    st.image('https://social.cs.washington.edu/img/logo_long.png', width=200)  # Adjust the width as needed

    survey_text.print_intro()
    login_verification.login_ver()  # login verification
   
######### demographics page
elif (
    st.session_state.counter >= 100
    and st.session_state.counter <= 200
    and st.session_state.page_status == "Demographics"
):
    demographics.demographics_verification()

elif(
    st.session_state.counter > 200
    and st.session_state.page_status == "Instruction"
):
    st.title("Annotation Instruction")
    survey_text.print_instruction()
    
    def start_annotation():
        st.session_state.page_status = "Annotation"
        st.session_state.counter += 100
            
    start = st.button(label = "Start", on_click = start_annotation, type = "primary")

######## annotation page
elif (
    st.session_state.counter >= 300
    and len(st.session_state.completed_tweet) < st.session_state.annotation_number
):
    survey_text.print_annotation_guide()
    survey_form.print_sidebar()
    survey_form.print_form()

######## end page
else:
    survey_text.print_ending()
