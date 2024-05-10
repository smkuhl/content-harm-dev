import streamlit as st
import pandas as pd
import time
import SurveyData as survey_data
import SurveyUtils as su
import json
import ast
from st_files_connection import FilesConnection

num_tweet = 20


def login_ver():

    with st.container(border = True):
        col1, col2, col3 = st.columns(3)

        with col1:
            identifier = st.text_input("Your unique Prolific ID: ", value="")
            identifier_check = st.text_input("Please enter again:", value="")

        consent_agree = st.checkbox(
            "I have read and understood the above terms and conditions and voluntarily consent to participate in this survey",
            value=False,
            key=None,
            help=None,
            on_change=None,
            args=None,
            kwargs=None,
            disabled=False,
            label_visibility="visible",
        )

    def verify_next():
        if consent_agree and (identifier and identifier == identifier_check):
            st.session_state.UserIdentifier = identifier

            conn = st.connection('gcs', type=FilesConnection)
            existing_user_info = conn.read("misinfo-harm/users_all.csv", input_format="csv", ttl= 20)

            if st.session_state.UserIdentifier in set(existing_user_info["username"]):
                # proceed to annotation
                st.session_state.StartID = int(
                    existing_user_info[
                        existing_user_info["username"]
                        == st.session_state.UserIdentifier
                    ]["start_id"]
                )

                # read completed Tweets from User unique Progress

                conn = st.connection('gcs', type=FilesConnection)
                user_progress_df_path = f"User{st.session_state.UserIdentifier}_progress.csv"
                user_progress_df = conn.read("misinfo-harm/User_Progress/"+user_progress_df_path, input_format = "csv", ttl= 20)
                tmp_completed_tweet = user_progress_df["completed_tweet"].iloc[0]
                if tmp_completed_tweet == "[]":
                    st.session_state.completed_tweet = []
                else:
                    st.session_state.completed_tweet = ast.literal_eval(tmp_completed_tweet)

                st.session_state.emergency_round = len(ast.literal_eval(user_progress_df["emergency_round"].iloc[0]))-1
                st.session_state.tweet_set = ast.literal_eval(user_progress_df["tweet_set"].iloc[0])

                # Load User Annotation
                user_df_path = f"User{st.session_state.UserIdentifier}_annotation.csv"
                conn = st.connection('gcs', type=FilesConnection)
                st.session_state.user_annotation_df = conn.read("misinfo-harm/User_Annotation/"+ user_df_path, input_format="csv", ttl= 20)
                          
                st.session_state.page_status = "Instruction"
                st.session_state.warning_visibility = False
                tmp_page = su.find_the_remaining()
                st.session_state.current_page = int(tmp_page)
                st.session_state.counter += 201
            else:
                st.session_state.page_status = "Demographics"
                st.session_state.warning_visibility = False
                st.session_state.counter += 101
        else:
            st.session_state.warning_visibility = True

    next = st.button("Continue", on_click=verify_next, type="primary")
    
    if st.session_state.warning_visibility:
        warning = st.warning("Please check your identifier or indicate your consent.", icon="⚠️")
