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
        st.session_state.current_page = su.paginator(
            "Select a Tweet",
            st.session_state.tweet_set,
            st.session_state.current_page,
            st.session_state.completed_tweet,
        )

        st.progress(
            int(
                (len(st.session_state.completed_tweet)+1)
                / (st.session_state.annotation_number)
                * 100
            )
        )
        latest_iteration = st.empty()
        latest_iteration.text(
            f"{len(st.session_state.completed_tweet)}"
            + "/" 
            + f"{st.session_state.annotation_number}"
            + " Tweet annotations completed."
        )

        col1, col2 = st.columns(2)


        if (st.session_state.current_page+1)%2 == 0:
            twitter_title = f"<div><span class='highlight darkslateblue'>Tweet {st.session_state.current_page+1}</span><br/>"
        else:
            twitter_title = f"<div><span class='highlight my_red'>Tweet {st.session_state.current_page+1}</span><br/>"
  
        # st.subheader(f"Tweet {st.session_state.current_page+1}")
        st.markdown(twitter_title, unsafe_allow_html=True)
        try:
            su.embed_tweet_page(st.session_state.tweet_set[st.session_state.current_page])
        except:
            emergency_tweet = survey_data.get_a_tweet()
            su.embed_tweet_page(st.session_state.tweet_set[st.session_state.current_page])

            st.session_state.emergency_round += 1
            st.session_state.tweet_set[st.session_state.current_page] = emergency_tweet # update current tweet_set

            conn = st.connection('gcs', type=FilesConnection)
            user_progress_df_path = f"User{st.session_state.UserIdentifier}_progress.csv"
            df = conn.read("tweet_annotation/User_Progress/"+ user_progress_df_path, input_format="csv", ttl= 20)
            df['tweet_set'] = str(st.session_state.tweet_set) # TODO
            df['emergency_round'] = str({st.session_state.emergency_round:st.session_state.current_page}) # TODO
            df.to_csv("local_new_user_progress.csv")
            abs_path = os.path.abspath("local_new_user_progress.csv")
            gm.upload_csv(abs_path , "User_Progress/"+user_progress_df_path)


def print_form():
    with st.form("my_form"):
        if (st.session_state.current_page+1)%2 == 0:
            twitter_account = f"<div> You are viewing <span class='highlight darkslateblue'>Tweet {st.session_state.current_page+1}</span><br/>"
        else:
            twitter_account = f"<div> You are viewing <span class='highlight my_red'>Tweet {st.session_state.current_page+1}</span><br/>"
        st.markdown(twitter_account, unsafe_allow_html=True)

        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            
            Q1 = st.selectbox(
                "Q1. How **believable** does the Tweet appear to you?",
                [
                    "",
                    "Not believable at all",
                    "Somewhat not believable",
                    "Neutral",
                    "Somewhat believable",
                    "Very believable",
                    "Not applicable (Please briefly explain the reason in Q4)",
                ],
                placeholder="",
                key="Q1",
            )

            st.write("\n")
            st.write("\n")

            Q2 = st.selectbox(
                "Q2. How likely do you think **your friends** or **peers** will find the above Tweet believable?",
                [
                    "",
                    "Not believable at all",
                    "Somewhat not believable",
                    "Neutral",
                    "Somewhat believable",
                    "Very believable",
                    "Not applicable (Please briefly explain the reason in Q4)",
                ],
                placeholder="",
                key="Q2",
            )

            st.write("\n")
            st.write("\n")

            Q3 = st.selectbox(
                "Q3. If this Tweet were widely spread, its message would likely be believed by:",
                ["", "Many", "Few", "Not applicable (Please briefly explain the reason in Q4)"],
                key="Q3",
                placeholder="",
            )

            st.write("\n")
            st.write("\n")

        Q4 = st.text_area("Q4. Additional comments (*Required if you opt \"Not Applicable\" in any one of Q1-Q3)", key="Q4")

        def submit_verify():
            # Store current data to the database
            # 1. Create a new df for this annotation
            # 2. Check if a record for this UserIdentifier and TweetURL already exists
            # 3. If yes, overwrite; Else, append to the end
            
            # 1. Create a new df for this annotation
            new_data = [
                {
                    "username": st.session_state.UserIdentifier,
                    "tweetURL": st.session_state.tweet_set[
                        st.session_state.current_page
                    ],
                    "Q1": st.session_state.Q1,
                    "Q2": st.session_state.Q2,
                    "Q3": st.session_state.Q3,
                    "Q4": st.session_state.Q4,
                }
            ]
            new_record = pd.DataFrame(new_data)

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
                        existing_record_mask, ["Q1", "Q2", "Q3", "Q4"]
                    ] = (
                        st.session_state.Q1,
                        st.session_state.Q2,
                        st.session_state.Q3,
                        st.session_state.Q4,
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
            df_progress = conn.read("tweet_annotation/User_Progress/"+user_progress_df_path, input_format="csv", ttl= 20)
            df_progress["completed_tweet"] = str(st.session_state.completed_tweet)
            df_progress.to_csv("local_new_user_progress.csv")
            abs_path = os.path.abspath("local_new_user_progress.csv")
            gm.upload_csv(abs_path , "User_Progress/"+user_progress_df_path)

        def submitted_and_next():
            if (
                st.session_state.Q1 == ""
                or st.session_state.Q2 == ""
                or st.session_state.Q3 == ""
            ):
                st.warning("Please answer all questions", icon="⚠️")
            elif(
                (st.session_state.Q1 == "Not applicable (Please briefly explain the reason in Q4)"
                or st.session_state.Q2 == "Not applicable (Please briefly explain the reason in Q4)"
                or st.session_state.Q3 == "Not applicable (Please briefly explain the reason in Q4)")
                and st.session_state.Q4 == ""
            ): 
                st.warning("Please briefly comment the reason(s) for opting \"Not applicable\" in Q1-Q3.",  icon="⚠️")
            else:
                submit_verify()
                if st.session_state.current_page != st.session_state.annotation_number-1:
                    st.session_state.current_page += 1
                else:
                    st.session_state.current_page = su.find_the_remaining()
                st.session_state.counter += 1
                st.session_state.Q1 = ""
                st.session_state.Q2 = ""
                st.session_state.Q3 = ""
                st.session_state.Q4 = ""

        def submitted_final():
            if (
                st.session_state.Q1 == ""
                or st.session_state.Q2 == ""
                or st.session_state.Q3 == ""
            ):
                st.warning("Please answer all questions", icon="⚠️")
            else:
                submit_verify()
                st.session_state.counter += 1
            
        if(len(st.session_state.completed_tweet) == st.session_state.annotation_number-1): 
            submitted = st.form_submit_button(
                "Finish & Continue", on_click=submitted_final, type="primary" # submit the final one
            )
        else:
            submitted = st.form_submit_button(
                "Save & Continue", on_click=submitted_and_next, type="primary" # submit an annotation
            )
            

    st.write("\n")

    def proceed_next():
        # Update progress data
        st.session_state.completed_tweet.append(st.session_state.current_page)
        finished_count = len(st.session_state.completed_tweet) + 1

        conn = st.connection('gcs', type=FilesConnection)
        user_progress_df_path = f"User{st.session_state.UserIdentifier}_progress.csv"
        df_progress = conn.read("tweet_annotation/User_Progress/"+user_progress_df_path, input_format="csv", ttl= 20)
        df_progress.loc[["start_id", "finished_count"]] = (st.session_state.StartID, finished_count)
        df_progress.to_csv("local_new_user_progress.csv")
        abs_path = os.path.abspath("local_new_user_progress.csv")
        gm.upload_csv(abs_path , "User_Progress/"+user_progress_df_path)

        st.session_state.counter += 1



    def proceed_previous():
        if st.session_state.current_page > 0:
            st.session_state.current_page -= 1
        st.session_state.Q1 = ""
        st.session_state.Q2 = ""
        st.session_state.Q3 = ""
        st.session_state.Q4 = ""

    col1, col2 = st.columns(2)
    if st.session_state.current_page != 0:
        prev_tweet = col1.button("Previous", on_click=proceed_previous)
           
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


        