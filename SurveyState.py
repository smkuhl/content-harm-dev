import streamlit as st

#TODO: update the num tweet
num_tweet = 9
import pandas as pd

def state_initializer():
    if "annotation_number" not in st.session_state:
        st.session_state["annotation_number"] = num_tweet
    if "StartID" not in st.session_state:
        st.session_state["StartID"] = "0"
    if "TweetID" not in st.session_state:
        st.session_state["TweetID"] = "na"
    if "Q1" not in st.session_state:
        st.session_state["Q1"] = "na"
    if "Q2" not in st.session_state:
        st.session_state["Q2"] = "na"
    if "Q3" not in st.session_state:
        st.session_state["Q3"] = "na"
    if "Q4" not in st.session_state:
        st.session_state["Q4"] = ""
    if "Closing" not in st.session_state:
        st.session_state["Closing"] = False
    if "UserIdentifier" not in st.session_state:
        st.session_state["UserIdentifier"] = ""
    if "disabled" not in st.session_state:
        st.session_state.disabled = False
    if "user_annotation_df" not in st.session_state:
        st.session_state.user_annotation_df = pd.DataFrame([{"":""}])
    if "page_status" not in st.session_state:
        st.session_state["page_status"] = "Introduction"
    if "tweet_set" not in st.session_state:
        st.session_state["tweet_set"] = ""
    if "completed_tweet" not in st.session_state:
        st.session_state["completed_tweet"] = []
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 0
    if "navigation" not in st.session_state:
        st.session_state["navigation"] = 0
    if "emergency_round" not in st.session_state:
        st.session_state["emergency_round"] = 0
    if "formatted_link" not in st.session_state:
        st.session_state["formatted_link"] = ''
    
    # Store Demographics
    if "age" not in st.session_state:
        st.session_state["age"] = ""
    if 'education_level' not in st.session_state:
        st.session_state["education_level"] = ""
    if 'political_ideology' not in st.session_state:
        st.session_state["political_ideology"] = ""
    if 'warning_visibility' not in st.session_state:
        st.session_state["warning_visibility"] = False