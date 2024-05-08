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

conn = st.connection('gcs', type=FilesConnection)
all_tweets = conn.read("tweet_annotation/all-tweet-0425.csv", input_format="csv")

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

    tweet = all_tweets[all_tweets["tweet_url"] == tweet_url]
    _name = urllib.parse.quote(tweet["user_name"].tolist()[0])
    _handle = tweet["user_username"].tolist()[0]
    _follower = tweet["user_followers_count"].tolist()[0]
    _following = int(tweet["user_following_count"].tolist()[0])
    _date = urllib.parse.quote(tweet["created_at"].tolist()[0])
    _profileImage = tweet["profile_img_file"].tolist()[0]
    _profileImageUrl = urllib.parse.quote(gm.generate_signed_url(file_path=f"profile_images_new/{_profileImage}"), safe=':/')
    _verified = tweet["user_verfied"].tolist()[0]
    _headline = urllib.parse.quote(tweet["user_description"].tolist()[0])
    _commentcount = tweet["reply_count"].tolist()[0]
    _retweetcount = tweet["retweet_count"].tolist()[0]
    _favcount = tweet["like_count"].tolist()[0]
    _text = urllib.parse.quote(tweet["text"].tolist()[0])
    _viewcount = tweet["impression_count"].tolist()[0]
    _bookmark = tweet["bookmark_count"].tolist()[0]
    _imgurls = tweet["media_details"].tolist()[0]
    if str(_imgurls) != "nan" and _imgurls != "":
        try:
            my_list = _imgurls.split(",")
            tmp = ""
            for i in range(0, len(my_list)):
                tmp += (my_list[i].split("photo:"))[1]
                if i != (len(my_list)-1):
                    tmp += ","
            _imgurls = tmp
        except:
            _imgurls = _imgurls
    else:
        _imgurls = ""
    formatted = f"https://linqiu0-0.github.io/fake-tweet-card/?name={_name}&date={_date}&handle={_handle}&profileImageUrl={_profileImageUrl}&follower={_follower}&following={_following}&verified={_verified}&headline={_headline}&commentCount={_commentcount}&retweetCount={_retweetcount}&favoriteCount={_favcount}&text={_text}&viewCount={_viewcount}&bookmark={_bookmark}&imageUrls={_imgurls}"
    components.iframe(formatted, height=1500)