import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import random
import SurveyUtils as su
from st_files_connection import FilesConnection
import datetime
import gcsManage as gm


# This library handles the distribution & management of survey data.
group_size = 6
tweet_dataset_filepath = "misinfo-harm/no_links_replies_data - Sheet1.csv"

def get_tweet_set_random():
    """
    Selects a random group of tweets for annotation based on their annotation status and count. The function prioritizes 
    tweet groups that have the minimum count of annotations to ensure balanced annotation across groups during each round 
    of annotation. 

    The function ensures that groups marked as 'Annotating' and not completed within 24 hours are considered 'Unannotated' 
    again. This is to handle cases where an annotation process may have been started but not finished. 

    Annotated_Count refers how many times this tweet group has been completed, not how many times it has been assigned to 
    annotate
    
    Returns:
        list: A list of tweet URLs from the selected group for annotation.
    """

    conn = st.connection('gcs', type=FilesConnection)
    tweet_info = conn.read(tweet_dataset_filepath,input_format="csv", encoding="utf-8")
    # annotation progress
    df = conn.read("misinfo-harm/group_annotation_progress.csv",input_format="csv", encoding="utf-8")
    

    time_threshold = datetime.timedelta(days=1).total_seconds()
    current_time = datetime.datetime.now()

    
    # Get the group with the minimum annotation count
    min_count = df['Annotated_Count'].min()
    candidate_groups = df[(df['Annotated_Count'] == min_count)]

    # Eligible group is either never assigned in the current round or the last annotation expires     
    eligible_groups = candidate_groups[
        (candidate_groups['Status'] == 'Unannotated') | 
        ((candidate_groups['Status'] == 'Annotating') & (int(current_time.timestamp()) - candidate_groups['Last_Annotated'] > time_threshold))
    ]

    # If no eligible groups found, handle groups based on their status and last annotated time
    if eligible_groups.empty:
        # Find groups that are currently being annotated and select the one with the oldest annotation start
        annotating_groups = df[df['Status'] == 'Annotating']
        if not annotating_groups.empty:
            # Sort these groups by 'Last_Annotated' to find the oldest
            oldest_group = annotating_groups.sort_values('Last_Annotated', ascending=True).iloc[0]['Group']
            selected_group = oldest_group
        else:
            # If no groups are in 'Annotating' state, assume all groups are fully annotated
            # Randomly select any group to restart annotation process
            df['Status'] = 'Unannotated'
            df['Last_Annotated'] = pd.NaT
            selected_group = random.choice(df['Group'].unique())
    else:
        selected_group = random.choice(eligible_groups['Group'].unique())

    # Update the DataFrame for the selected group
    df.loc[df['Group'] == selected_group, 'Status'] = 'Annotating'
    df.loc[df['Group'] == selected_group, 'Last_Annotated'] = current_time.timestamp()
    df.loc[df['Group'] == selected_group, 'Last_Annotated_time'] = current_time

    gm.upload_csv(df.to_csv(index=False), "group_annotation_progress.csv")

    
    # Filter tweets for annotation
    tweet_set = tweet_info[tweet_info['Group'] == selected_group]['tweet_url'].tolist()


    st.session_state["current_page"] = 0
    st.session_state["tweet_set"] = tweet_set
    st.session_state["GroupID"] = selected_group
    st.session_state["completed_tweet"] = []

def update_annotation_count():
    conn = st.connection('gcs', type=FilesConnection)
    # annotation progress
    df = conn.read("misinfo-harm/group_annotation_progress.csv",input_format="csv", encoding="utf-8")
    df.loc[df['Group'] == st.session_state["GroupID"], 'Annotated_Count'] += 1
    gm.upload_csv(df.to_csv(index=False), "group_annotation_progress.csv")

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

