import streamlit as st
import requests
import streamlit.components.v1 as components
from PIL import Image
from io import BytesIO
from st_files_connection import FilesConnection
import gcsManage as gm
import os
from math import nan
import urllib.parse
from urllib.parse import urlencode
import pandas as pd

conn = st.connection('gcs', type=FilesConnection)
all_tweets = conn.read("misinfo-harm/tweet_data_formatted_pt3.csv", input_format="csv", encoding="utf-8")

def disable():
    st.session_state.disabled = True

def enable():
    st.session_state.disabled = False

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def navigate_to_page():
    st.session_state.current_page = int(st.session_state.navigation)


def paginator(
    label, tweetSet, page, completed_tweets, min_index=0, max_index=20, on_sidebar=True
):
    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    n_pages = len(tweetSet)
    page_format_func = (
        lambda i: "Twitter " + str(i + 1) + (" ✅" if i in completed_tweets else "")
    )
    page_number = location.selectbox(
        label,
        range(n_pages),
        format_func=page_format_func,
        index=page,
        key="navigator",
        on_change=navigate_to_page,
    )

    return page_number


def find_the_remaining():
    id_list = list(range(st.session_state.annotation_number))
    remaining = list(set(id_list) - set(st.session_state.completed_tweet))
    if len(remaining) == 0:
        return int(st.session_state.annotation_number)
    else:
        return int(remaining[0])

def embed_tweet_page(tweet_url):
    if not st.session_state.formatted_link:
        tweet_id = tweet_url.split("/")[-1]
        tweet = all_tweets[all_tweets["tweet_real_id"] == int(tweet_id)]
        _name = urllib.parse.quote(tweet["user_name"].tolist()[0])
        _handle = tweet["user_username"].tolist()[0]
        _follower = tweet["user_followers_count"].tolist()[0]
        _following = int(tweet["user_following_count"].tolist()[0])
        _date = urllib.parse.quote(tweet["created_at"].tolist()[0])
        _profileImage = tweet["profile_img_file"].tolist()[0]
        _profileImageUrl = urllib.parse.quote(gm.generate_signed_url(file_path=f"{_profileImage}"), safe=':/')
        _verified = tweet["user_verified"].tolist()[0]
        user_description = tweet["user_description"].tolist()[0] if pd.notna(tweet["user_description"].iloc[0]) else ""
        _headline = urllib.parse.quote(user_description)
        # _commentcount = tweet["reply_count"].tolist()[0]
        _commentcount = 0
        _retweetcount = tweet["retweet_count"].tolist()[0]
        _favcount = tweet["like_count"].tolist()[0]
        text = tweet["text"].tolist()[0] if pd.notna(tweet["text"].iloc[0]) else ""
        _text = urllib.parse.quote(text)
        # _viewcount = tweet["impression_count"].tolist()[0]
        _viewcount = 0
        # _bookmark = tweet["bookmark_count"].tolist()[0]
        _bookmark = 0
        _imgurls = tweet["media_details"].tolist()[0]
        if str(_imgurls) != "nan" and _imgurls != "":
            try:
                my_list = _imgurls.split(";")
                tmp = ""
                for i in range(0, len(my_list)):
                    tmp += my_list[i]
                    if i != (len(my_list)-1):
                        tmp += ","
                _imgurls = tmp
            except:
                _imgurls = _imgurls
        else:
            _imgurls = ""
        formatted = f"https://linqiu0-0.github.io/fake-tweet-card/?name={_name}&date={_date}&handle={_handle}&profileImageUrl={_profileImageUrl}&follower={_follower}&following={_following}&verified={_verified}&headline={_headline}&commentCount={_commentcount}&retweetCount={_retweetcount}&favoriteCount={_favcount}&text={_text}&viewCount={_viewcount}&bookmark={_bookmark}&imageUrls={_imgurls}"
        st.session_state.formatted_link = formatted
    components.iframe(st.session_state.formatted_link, height=1500)
"https://linqiu0-0.github.io/fake-tweet-card/?name=Yakov%20%F0%9F%9A%B2%F0%9F%9A%83%F0%9F%9A%A0%F0%9F%8E%97&date=2020-04-20T16%3A20%3A00-0400&handle=transitive_bs&profileImageUrl=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F1554552556017295360%2FqMTXT-4A_normal.jpg&follower=322&following=534&verified=true&headline=Working%20to%20end%20career%20retaliation%20against%20%23survivors%20of%20sexual%20violence%20in%20Hollywood.%20Founded%20by%20%23SilenceBreaker%20%40sarahannmasse.%20%23HireSurvivorsHollywood&commentCount=300&retweetCount=2517&favoriteCount=16342&text=Happy%20%5CSunday%20to%20the%20%23HireSurvivorsHollywood%20Community!%20We%27ve%20decided%20to%20use%20Sundays%20to%20highlight%20%23survivors%20and%20%23SilenceBreakers%20and%20the%20wonderful%20work%20they%27re%20doing!%0AToday%20we%27re%20celebrating%20Amber%20Heard%20(%23AmberHeard)!%20https%3A%2F%2Ft.co%2FrCigkEijIY&viewCount=5000&bookmark=67897&imageUrls=https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FFiDqxUqWIAA_4RY%3Fformat%3Djpg%26name%3Dlarge,https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FFYUKXwFWAAEPeUV%3Fformat%3Djpg%26name%3Dsmall,https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FFYUKXwFWAAEPeUV%3Fformat%3Djpg%26name%3Dsmall,https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FFj8lwiZXwAA8iyO%3Fformat%3Djpg%26name%3Dmedium"

def get_survey_questions():
    return ["Does the message content include an explicit call to action? The message addresses the reader using pronouns such as 'you, we, us' or implies the reader's involvement. It might ask the reader to post, share, tell others about something, join an event, stay tuned, or some other follow up action.",
            "Does the piece of content explicitly or implicilty incorporate coordination efforts, such as dates/times, locations, or other arrangment for a follow-up? For example, using words such as soon, now, in the coming days.",
            "Does the message provide a way that people might be directly harmed? For example identifying information about an individual that is not widely or publicly known.",
            "Does the message directly address or reference children or use language aimed at a younger audience?", 
            "Does this message directly address or reference the elderly community, a subgroup of the elderly, or discus topics aimed at them? For example, people on government pensions, nursing home residents, etc.", 
            "Could this message introduce a degree of fear or feelings of uneasiness to the intended audience or general public?", 
            "Is this message content complicated to understand? For example, does it include technical terminology, specialized knowledge, or complex logic?", 
            "Do the people or entities who are spreading the piece of content have a broad reach (size of following on social media, “influencer,” presence on TV or other news media)?", 
            "Are the people or entities known to be repeat spreaders of questionable information? Hint: search the name of the author/poster and find whether they have been debunked before posting the current Tweet.",
            "Is there a lack of high-quality information that is refuting the message's claim? Do a quick internet search based on the Tweet content and see if there is any debunking information.",
            "Does the poster and/or organization/outlet have a noteworthy number of social media/community followers?",
            "Is the content published by an organization/outlet with transparent editorial control? Editorial control refers to the ability to review, standardize, or veto content. If the poster is not an organization or outlet select N/A.",
            "Does the message fit into a larger narrative that has been existing for some time?",
            "Does the message question or challenge the functioning of public institutions? Public institutions include schools, law enforcement, public transit, government agencies, etc.",
            "Does the message question other people in general within a community or society?",
            "Was this Tweet posted before 2024?"
            ]