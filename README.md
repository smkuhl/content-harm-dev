# misinfo-survey

> A Streamlit App for annotating randomized Tweets.


- Deployed on Streamlit Community Cloud (allows for one free private App)
- Assigned randomized groups of Tweets to users.


### App Structure

Cover Page -> Demographics -> Instruction -> Annotation -> End Cover

`gcsManager.py`: Manage Google Cloud Storage Connection 

`LoginVerification.py`: Login fuction on the Cover Page

`SurveyData.py`: Handle data randomization

`Demographics.py`: Handle Demographic Page (record new user's demographic + register the user)

`SurveyForm.py`: Handle data annotation

`SurveyText.py`: All text component

`SurveyState.py`: Initialize session_state

### Run

1. Set up your Google Cloud Storage Bucket for your datasets and directory needed.

```
your_gcs_bucket
│   all-tweet.csv # Upload your data
│   users_all.csv # Register users
│
└───User_Annotation # User's annotation for each Tweet
│   │   User{user1}_annotation.csv
│   │   User{user2}_annotation.csv
│   │   ...
│   
└───User_Progress # User's progress (ID of annotated/remaining Tweets, Exceptions)
    │   User{user1}_progress.csv
    │   User{user2}_progress.csv
    │   ... 
```

- all-tweet.csv.
- users_all.csv: [user_id, randomized_tweet_group_start_id, age, education, politic_ideology]
- User{user1}_annotation.csv: [username, tweetURL, Q1, Q2, Q3, Q4]
- User{user1}_progress.csv: [username, start_id, completed_tweet, tweet_set, emergency_round]


2. Clone the repository, upload the codes to your Github.
3. Go to [Stremlit Cloud](https://share.streamlit.io/) and create a New App.
4. Select your repository and deploy.
5. Copy your Google Cloud Storage Credentials (JSON) as follows, and paste in the App's Settings > Secrets.

```
[gcp_service_account]
key="""{"type": "service_account”, … ,"universe_domain": "googleapis.com"}"""
```

6. Modify the following as needed:
-  Filepath to your datasets
-  Number of Tweets to annotate  per user (Default: 2*10Tweets)
-  Annotation Questions


### Note

1. To develop locally, you might need to set up related certificates. 
2. If you are developing & deploying real-timely on Streamlit Community Cloud and encountered some strange bugs, try Reboot the App (this will cause reinitialization of session_state).

Feel free to contact Gloria via Slack / bguoac@uw.edu if you encountered any issues. :>

### References
- Streamlit Components: https://docs.streamlit.io/
- Deploy the App: https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app
- Connect to Google Cloud Storage: https://docs.streamlit.io/develop/tutorials/databases/gcs