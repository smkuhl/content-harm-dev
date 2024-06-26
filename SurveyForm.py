import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import random
import requests
import PIL
import time
import os
import SurveyUtils as su
import SurveyText as survey_text
import SurveyData as survey_data
from st_files_connection import FilesConnection
import gcsManage as gm


def print_sidebar():
    with st.sidebar:
        st.progress(
            int(
                (len(st.session_state.completed_tweet)+1)
                / (st.session_state.annotation_number)
                * 100
            )
        )
        latest_iteration = st.empty()
        latest_iteration.text(
            "You are on Tweet "
            f"{len(st.session_state.completed_tweet) + 1}"
            + "/" 
            + f"{st.session_state.annotation_number}"
        )

        col1, col2 = st.columns(2)
        # try:
        su.embed_tweet_page(st.session_state.tweet_set[st.session_state.current_page])
        # except Exception as e:
        #     # Display the exception message to the user
        #     st.warning(f"An error occurred: {str(e), } Debug this! it shouldn't happen")


            
         
def load_survey(questions):
    start_idx = [0, 3, 7, 9, 12]
    headers = ["Actionability", "Exploitativeness", "Likelihood of Spread", "Believability", "Social Fragmentation"]
    for i, question in enumerate(questions):
        # display the header if it's the first question in that section
        if i in start_idx:
                idx = start_idx.index(i)
                st.subheader(f"{headers[idx]}")

        # bold first part of the question
        parts = question.split('?', 1)
        if len(parts) > 1:
            bold_part = f"**{parts[0]}?**"
            rest_part = parts[1].strip()
            question_formatted = f"{bold_part}\n\n{rest_part}"
        else:
            question_formatted = f"**{question}**"

        # handle custom answers besides just yes, no, na
        if i == 11: # index of not an organization question
            response=st.radio(label=f"Q{i+1}: {question_formatted}", options=["Yes", "No", "Not an Organization", "Not Applicable"], horizontal=True, index=None, key=f"{st.session_state.current_page+1}_{i}")
        elif i == 9: # index of lack of high quality information
            response=st.radio(label=f"Q{i+1}: {question_formatted}", options=["Yes, there is a lack of high quality information", "Yes, there is information but it is low quality", "No, there is high quality information"], horizontal=True, index=None, key=f"{st.session_state.current_page+1}_{i}")
        else:
            response=st.radio(label=f"Q{i+1}: {question_formatted}", options=["Yes", "No", "Not Applicable"], horizontal=True, index=None, key=f"{st.session_state.current_page+1}_{i}")
        st.session_state.responses[i] = response
        if response == "Not Applicable":
            text_response = st.text_input("Please add your reasoning for selecting not applicable", value='', key=f"{st.session_state.current_page+1}_{i}_text")
            st.session_state.explanations[i] = text_response

    

def print_form():
    '''
    if (st.session_state.current_page+1)%2 == 0:
        twitter_account = f"<div> You are viewing <span class='highlight darkslateblue'>Tweet {st.session_state.current_page+1}</span><br/>"
    else:
        twitter_account = f"<div> You are viewing <span class='highlight my_red'>Tweet {st.session_state.current_page+1}</span><br/>"
    st.markdown(twitter_account, unsafe_allow_html=True)
    '''
    
    questions = su.get_survey_questions()
    st.session_state.responses = [None] * len(questions)
    st.session_state.explanations = {}

    with st.container(border=True):
        load_survey(questions)

        
        def check_unanswered(responses, explanations):
            unanswered_questions = [f"Q{qid + 1}" for qid, resp in enumerate(responses) if resp is None or resp == ""]
            unanswered_explanations = [f"Q{eid + 1}-reason" for eid, expl in explanations.items() if expl is None or expl == ""]
            return unanswered_questions + unanswered_explanations

        def display_warning(unanswered_items):
            if unanswered_items:
                warning_message = f"Please answer all questions and provide necessary reasons. \n Missing Questions: {', '.join(unanswered_items)}"
                st.warning(warning_message, icon="⚠️")
                return False
            return True

        def handle_submission(responses, explanations):
            unanswered_items = check_unanswered(responses, explanations)
            if display_warning(unanswered_items):
                submit_verify(responses, explanations)
                st.session_state.current_page += 1
                st.session_state.formatted_link = None
                # if last annotation
                if len(st.session_state.completed_tweet) == st.session_state.annotation_number - 1:
                    survey_data.update_annotation_count()

                st.rerun()

        def submit_verify(responses, explanations):
            new_data = {
                    "username": st.session_state.UserIdentifier,
                    "tweetURL": st.session_state.tweet_set[
                        st.session_state.current_page
                    ],
            }
            
            for i, response in enumerate(responses):
                new_data[f"Q{i+1}"] = response
                if i in explanations:
                    new_data[f"Q{i+1}-reason"] = explanations[i]
                else:
                    new_data[f"Q{i+1}-reason"] = ""
                
            new_record = pd.DataFrame([new_data])

            # 2. Check if a record for this UserIdentifier and TweetURL already exists
            existing_record_mask = (
                st.session_state.user_annotation_df["username"]
                == st.session_state.UserIdentifier
            ) & (
                st.session_state.user_annotation_df["tweetURL"]
                == st.session_state.tweet_set[st.session_state.current_page]
            )

            # 3. If yes, overwrite; Else, concatenate the new record
            if existing_record_mask.sum() > 0:
                # If a record exists, update it
                if st.session_state.current_page in st.session_state.completed_tweet:
                    st.session_state.completed_tweet.remove(st.session_state.current_page)
                    st.session_state.user_annotation_df.loc[
                        existing_record_mask, ["Q1", "Q1-reason", "Q2", "Q2-reason", "Q3", "Q3-reason", "Q4", "Q4-reason", "Q5", "Q5-reason", "Q6", "Q6-reason", "Q7", "Q7-reason", \
                            "Q8", "Q8-reason", "Q9", "Q9-reason", "Q10", "Q10-reason", "Q11", "Q11-reason", "Q12", "Q12-reason", "Q13", "Q13-reason", "Q14", "Q14-reason", "Q15", "Q15-reason", "Q16", "Q16-reason",]
                    ] = (
                        responses
                    )
                    st.success(
                        "Your response has been updated! ",
                        icon="✅",
                    )
            else:
                # Otherwise, concatenate the new record
                st.session_state.user_annotation_df = pd.concat(
                    [st.session_state.user_annotation_df, new_record],
                    ignore_index=True,
                )
                st.success(
                    "Your response has been saved!",
                    icon="✅",
                )
                js = '''
                    <script>
                        var body = window.parent.document.querySelector(".main");
                        console.log(body);
                        body.scrollTop = 0;
                    </script>
                    '''
                st.components.v1.html(js)  
                st.write("\n")
                

            st.session_state.completed_tweet.append(st.session_state.current_page)

            # Save the updated DataFrame to storage

            # Update Annotation
            user_annotation_df_csv = st.session_state.user_annotation_df.to_csv(index=False)
            gm.upload_csv(user_annotation_df_csv, f"User_Annotation/User{st.session_state.UserIdentifier}_annotation.csv")

            # Update User unique progress
            conn = st.connection('gcs', type=FilesConnection)
            user_progress_df_path = f"User{st.session_state.UserIdentifier}_progress.csv"
            df_progress = conn.read("misinfo-harm/User_Progress/"+user_progress_df_path, input_format="csv", ttl= 20)
            df_progress["completed_tweet"] = str(st.session_state.completed_tweet)
            df_progress_csv =  df_progress.to_csv( index=False)
            gm.upload_csv(df_progress_csv , "User_Progress/"+user_progress_df_path)
            
                                
                
                
        button_label = "Finish & Continue" if len(st.session_state.completed_tweet) == st.session_state.annotation_number - 1 else "Save & Continue"
        submitted = st.button(button_label, type="primary")
        
        if submitted:
            handle_submission(st.session_state.responses, st.session_state.explanations)
            st.write("\n")
            
           
def print_helper():
    st.caption("Labeling")
    st.write("Tweets may and may not contain images. Below are some examples of labeling Tweets with images:")
    col1, colx, col2, coly, col3 = st.columns([3,1,3,1,3])
    with col1: 
        st.caption("Example 1: ")
        survey_text.print_example(1)
    with col2:
        st.caption("Example 2: ")
        survey_text.print_example(2)
    st.caption("Note:")
    st.write("""
                1. Loading the Tweet and images may take several seconds. \n
                2. When encountering loading problems, try refresh the page or clean the cache and then login again. \n
                3. When navigating using the Paginator, it may occasionally jump back to Tweet 1. We are working on fixing it ASAP.
                """)


        