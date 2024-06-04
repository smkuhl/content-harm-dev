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
        import streamlit.components.v1 as components

        formatted = "https://linqiu0-0.github.io/fake-tweet-card/?name=Yakov%20%F0%9F%9A%B2%F0%9F%9A%83%F0%9F%9A%A0%F0%9F%8E%97&date=2020-04-20T16%3A20%3A00-0400&handle=transitive_bs&profileImageUrl=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F1554552556017295360%2FqMTXT-4A_normal.jpg&follower=322&following=534&verified=true&headline=Working%20to%20end%20career%20retaliation%20against%20%23survivors%20of%20sexual%20violence%20in%20Hollywood.%20Founded%20by%20%23SilenceBreaker%20%40sarahannmasse.%20%23HireSurvivorsHollywood&commentCount=300&retweetCount=2517&favoriteCount=16342&text=Happy%20%5CSunday%20to%20the%20%23HireSurvivorsHollywood%20Community!%20We%27ve%20decided%20to%20use%20Sundays%20to%20highlight%20%23survivors%20and%20%23SilenceBreakers%20and%20the%20wonderful%20work%20they%27re%20doing!%0AToday%20we%27re%20celebrating%20Amber%20Heard%20(%23AmberHeard)!%20https%3A%2F%2Ft.co%2FrCigkEijIY&viewCount=5000&bookmark=67897&imageUrls=https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FFiDqxUqWIAA_4RY%3Fformat%3Djpg%26name%3Dlarge,https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FFYUKXwFWAAEPeUV%3Fformat%3Djpg%26name%3Dsmall,https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FFYUKXwFWAAEPeUV%3Fformat%3Djpg%26name%3Dsmall,https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FFj8lwiZXwAA8iyO%3Fformat%3Djpg%26name%3Dmedium"
        components.iframe(formatted, height=1500,width=800)

        # try:
        su.embed_tweet_page(st.session_state.tweet_set[st.session_state.current_page])
        # except Exception as e:
            # Display the exception message to the user
            # st.warning(f"An error occurred: {str(e), } Debug this! it shouldn't happen")


            
         
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
                st.session_state.counter += 1
                if st.session_state.counter == st.session_state.annotation_number - 1:
                    st.session_state.current_page = su.find_the_remaining()
                else:
                    st.session_state.current_page += 1

                st.session_state.formatted_link = None
                # st.components.v1.html("<script>window.scrollTo(0, 0);</script>")  # Scroll to top
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
                

            st.session_state.completed_tweet.append(st.session_state.current_page)

            # Save the updated DataFrame to storage

            # Update Annotation
            user_df_path = f"User{st.session_state.UserIdentifier}_annotation.csv"
            st.session_state.user_annotation_df.to_csv(user_df_path)
            abs_path = os.path.abspath(user_df_path)
            gm.upload_csv(abs_path, "User_Annotation/"+user_df_path)

            # Update User unique progress
            conn = st.connection('gcs', type=FilesConnection)
            user_progress_df_path = f"User{st.session_state.UserIdentifier}_progress.csv"
            df_progress = conn.read("misinfo-harm/User_Progress/"+user_progress_df_path, input_format="csv", ttl= 20)
            df_progress["completed_tweet"] = str(st.session_state.completed_tweet)
            df_progress.to_csv("local_new_user_progress.csv")
            abs_path = os.path.abspath("local_new_user_progress.csv")
            gm.upload_csv(abs_path , "User_Progress/"+user_progress_df_path)
            
                                
                
                
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


        