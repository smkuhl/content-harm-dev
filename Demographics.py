import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import random
import requests
import PIL
import time
import SurveyData as survey_data
import gcsManage as gm
from st_files_connection import FilesConnection
import os
import SurveyForm as survey_form

# This Library contains functions for Demographics Verification & Tweet Set Generation


def demographics_verification():

    st.subheader("Demographics Information")
    st.write(" ")

    col1, col2 = st.columns([1,1])
    with col1:
        age = st.number_input("What is your age?", value= None, min_value = 0, max_value = 120, step=1, key = "age")
        st.write(" ")
        st.write(" ")
        education = st.selectbox(
            "What is the highest degree or level of school you have completed? If currently enrolled, highest degree received.",
            (
                "Select an option...",
                "No schooling completed",
                "Nursery school to 8th grade",
                "Some high school, no diploma",
                "High school graduate, diploma or the equivalent (for example: GED)",
                "Some college credit, no degree",
                "Associate degree",
                "Bachelor’s degree",
                "Master’s degree",
                "Professional degree",
                "Doctorate degree",
            ),
            key="education",
        )
        st.write(" ")
        st.write(" ")

        political = st.selectbox(
            "In general, would you describe your political views as?",
            (
                "Select an option...",
                "Very conservative",
                "Conservative",
                "Moderate",
                "Liberal",
                "Very liberal",
            ),
            key="political_ideology",
        )

    def verify_valid_demo():
        if (
            st.session_state.political_ideology == "Select an option..."
            or st.session_state.education == "Select an option..."
            or (st.session_state.age == "" or None)
            or (st.session_state.age >= 120 or st.session_state.age <= 0)
        ):
            st.warning("Please check your inputs", icon="⚠️")
        elif(st.session_state.age < 18):
            st.warning("You need to be over 18 to participate the annotation", icon="⚠️")
        else:

            conn = st.connection('gcs', type=FilesConnection)
            existing_user_info = conn.read("tweet_annotation/users_all.csv", input_format="csv", ttl= 20)

            survey_data.get_tweet_set_random() # get a tweet_set based on the demographics information.
            new_user_data = [
                {
                    "username": st.session_state.UserIdentifier,
                    "start_id": st.session_state.StartID,
                    "age": st.session_state.age,
                    "education": st.session_state.education,
                    "political_ideology": st.session_state.political_ideology,
                }
            ]
            new_user_info = pd.DataFrame(new_user_data)
            df_to_store = pd.concat(
                [existing_user_info, new_user_info], ignore_index=True
            )
            df_to_store.to_csv("local_new_progress.csv",index= False)
            abs_path = os.path.abspath("local_new_progress.csv")
            gm.upload_csv(abs_path, 'users_all.csv')

            # User Unique Progress CSV
            template_data_user_progress = [
                {
                    "username": st.session_state.UserIdentifier,
                    "start_id": st.session_state.StartID,
                    "completed_tweet": str(st.session_state.completed_tweet),
                    "tweet_set":str(st.session_state.tweet_set),
                    "emergency_round": str({st.session_state.emergency_round:"-"})            
                }
            ]
            df_user_progress = pd.DataFrame(template_data_user_progress)
            user_progress_df_path = f"User{st.session_state.UserIdentifier}_progress.csv"
            df_user_progress.to_csv(user_progress_df_path, index = False)
            abs_path = os.path.abspath(user_progress_df_path)
            gm.upload_csv(abs_path, "User_Progress/"+user_progress_df_path)

            # User Annotation CSV
            template_data = [
                {
                    "username": "sample",
                    "tweetURL": "sample",
                    "Q1": "sample",
                    "Q2": "sample",
                    "Q3": "sample",
                    "Q4": "sample",
                }
            ]
            st.session_state.user_annotation_df = pd.DataFrame(template_data)
            user_df_path = f"User{st.session_state.UserIdentifier}_annotation.csv"
            st.session_state.user_annotation_df.to_csv(user_df_path, index = False)
            abs_path = os.path.abspath(user_df_path)
            gm.upload_csv(abs_path, "User_Annotation/"+user_df_path)

            st.session_state.page_status = "Instruction"
            st.session_state.counter += 100
            
    next = st.button("Continue", on_click = verify_valid_demo)



  