import streamlit as st
import pandas as pd
import time
import SurveyData as survey_data
import SurveyUtils as su
import json
import ast
from st_files_connection import FilesConnection
import os
import gcsManage as gm



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
                st.session_state.GroupID = int(
                existing_user_info[
                    existing_user_info["username"] == st.session_state.UserIdentifier
                ]["group_id"].iloc[0]
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
                user_df_path = f"User_{st.session_state.UserIdentifier}_annotation.csv"
                conn = st.connection('gcs', type=FilesConnection)
                st.session_state.user_annotation_df = conn.read("misinfo-harm/User_Annotation/"+ user_df_path, input_format="csv", ttl= 20)
                          
                
                tmp_page = su.find_the_remaining()
                st.session_state.current_page = int(tmp_page)
            else: # new user
                conn = st.connection('gcs', type=FilesConnection)
                existing_user_info = conn.read("misinfo-harm/users_all.csv", input_format="csv", ttl= 20)

                survey_data.get_tweet_set_random() 
                new_user_data = [
                    {
                        "username": st.session_state.UserIdentifier,
                        "group_id": st.session_state.GroupID,
                    }
                ]
                new_user_info = pd.DataFrame(new_user_data)
                df_to_store = pd.concat(
                    [existing_user_info, new_user_info], ignore_index=True
                )
                local_new_progress = df_to_store.to_csv(index= False)
                gm.upload_csv(local_new_progress, 'users_all.csv')

                # User Unique Progress CSV
                template_data_user_progress = [
                    {
                        "username": st.session_state.UserIdentifier,
                        "group_id": st.session_state.GroupID,
                        "completed_tweet": str(st.session_state.completed_tweet),
                        "tweet_set":str(st.session_state.tweet_set),
                        "emergency_round": str({st.session_state.emergency_round:"-"})            
                    }
                ]
                df_user_progress = pd.DataFrame(template_data_user_progress)
                user_progress_df_path = f"User{st.session_state.UserIdentifier}_progress.csv"
                df_user_progress_csv = df_user_progress.to_csv(index = False)
                gm.upload_csv(df_user_progress_csv, "User_Progress/"+user_progress_df_path)

                # User Annotation CSV
                questions = su.get_survey_questions()
                template_data = [
                    {
                        "username": "sample",
                        "tweetURL": "sample",
                    }
                ]
                for i in range(len(questions)):
                    template_data[0][f"Q{i+1}"] = "sample"
                st.session_state.user_annotation_df = pd.DataFrame(template_data)
                user_df_path = f"User_{st.session_state.UserIdentifier}_annotation.csv"
                user_annotation_df_csv = st.session_state.user_annotation_df.to_csv(index = False)
                gm.upload_csv(user_annotation_df_csv, "User_Annotation/" + user_df_path)

                
            st.session_state.page_status = "Instruction"
            st.session_state.warning_visibility = False
            st.session_state.counter += 201
        else:
            st.session_state.warning_visibility = True

    next = st.button("Continue", on_click=verify_next, type="primary")
    
    if st.session_state.warning_visibility:
        warning = st.warning("Please check your identifier or indicate your consent.", icon="⚠️")
