import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import random
import SurveyUtils as su
from st_files_connection import FilesConnection


# This library handles the distribution & management of survey data.
group_size = 6
tweet_dataset_filepath = "misinfo-harm/tweet_data_formatted_pt3.csv"

def get_tweet_set_random():
    conn = st.connection('gcs', type=FilesConnection)
    df = conn.read(tweet_dataset_filepath,input_format="csv", encoding="utf-8")

    group_num = max(df['Group'].tolist())
    rounds = int(st.session_state.annotation_number / group_size)
    group_id = []
    tmp =  random.randint(1, group_num)
    while rounds > 0:
        group_id.append(tmp)
        if(tmp+1 > group_num):
            tmp = (tmp+1) % group_num
        else:
            tmp += 1
        rounds -= 1
    tweet_set = []


    for i in group_id:
        filtered = df[(df['Group'] == i)]['tweet_url'].tolist()
        tweet_set += filtered

        
    start_id = (group_id[0]-1)*group_size + 1
    st.session_state["current_page"] = 0
    st.session_state["tweet_set"] = tweet_set
    st.session_state["StartID"] = start_id
    st.session_state["completed_tweet"] = []


def cluster_demographics():
    demo_label = ""
    if st.session_state.age >= 0 and st.session_state.age < 35:
        demo_label += "y-"
    elif st.session_state.age >= 35 and st.session_state.age < 60:
        demo_label += "m-"
    else:
        demo_label += "o-"

    if st.session_state.education in {"No schooling completed","Nursery school to 8th grade","Some high school, no diploma","High school graduate, diploma or the equivalent (for example: GED)"}:
        demo_label += "l-"
    else:
        demo_label += "h-"

    if st.session_state.political_ideology in {"Very conservative","Conservative"}:
        demo_label += "c"
    elif st.session_state.political_ideology in {"Very liberal","Liberal"}:
        demo_label += "l"
    else:
        demo_label += "n-"

    return demo_label

