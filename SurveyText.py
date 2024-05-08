import streamlit as st

definition = "<div><ul><li>is <span class='lemonchiffon'>politically polarized</span><br/><li>is <span class='lemonchiffon'>influenced by bandwagon cues</span><br/><li> often <span class='lemonchiffon'>relies on emotions</span> instead of <span class= 'lemonchiffon'>rational thinking</span><li>tends to believe information that <span class='lemonchiffon'>aligns with their prior beliefs</span>."


def print_intro():
    st.title("Welcome to Tweet Annotation!")
    st.write(" ")
    st.write(
        """
        :technologist: We are a group of researchers from the Social Futures Lab at the University of Washington. 
        
        We cordially invite you to participate this annotation of tweet believability.
        


        
        :warning: **Content Warning**
        
        Please be aware that subsequent tweets could contain potentially unsettling or sensitive content. You must be above 18 to participate in the annotation. We advise discretion while proceeding.
        



        :lock: **We Value Your Privacy**
        
        Your privacy is our top priority. All information provided will be used exclusively for research purposes, kept confidential, and anonymized.

        You have the right to withdraw your participation and request data deletion at any time. We assure you that your privacy will be strictly protected. 



        

        :memo: **What Will You Do**
         
        You will read 20 Tweets. 

        For each Tweet, please evaluate how believable it is to you, to your friends and peers, and to the general public.

        We value users' opinion about the Tweet, therefore we suggest annotating the Tweet without searching on the Internet.
      
        """
    )


    st.write("\n")
    st.write(" ")
    st.write(
        """
        
        This annotation survey will take around 40 minutes.
        
        We would like to express our gratitude for your time and contribution to our research. If you have any questions, please feel free to contact us at bguoac@uw.edu.
        
        \n
        \n
        \n

        ⬇️ Please enter your unique Prolific ID to begin your annotation task or restore your progress.
        """
    )

def print_annotation_guide():
    st.title("Tweet Annotation")
    st.write
    st.write(
        """
        You are going view a series of Tweets. \n
        For each Tweet shown on the left, please answer the following questions.
        """
    )


def print_ending():
    
    st.write(
        """
        All your annotations have been recorded.
        Thank you very much!
    """
    )
    st.balloons()

    st.write(
        """
        Should you have any inquiries, please contact us at bguoac@uw.edu.
        We would like to thank you again for the participation! :)
        """
    )
    

def print_example(id):

    if id == 1:
        st.markdown("""
            User @user_bbb attached a screenshot of user @user_aaa's Tweet on "Moon landing wasn't real" and express agreement with its content.
            You need to evaluate the belivability of **@user_bbb's Tweet**, i.e **content about agreement of @user_aaa's Tweet content**.
        """)


        st.image("./img/Tweet_A.png")

    elif id == 2:
        st.markdown("""
            User @user_bbb attached a screenshot of user @user_aaa's Tweet about election and believe its content is somewhat false.
            You need to evaluate the believability of **@user_bbb's Tweet**, i.e **content about claiming @user_aaa's Tweet content is false**.
        """)
        st.image("./img/Tweet_B.png")

    elif id == 3:
        st.write("""
        **Reply to a tweet**
                 
        * Primary Tweet: Tweet C
        * What to consider: Regard TWeet A and B as part of context, Tweet C information(e.g. text, image, tags, embedded url(without opening it), comment counts, like counts) + User C's metadata.
                 
        """)
        st.image("./img/Tweet_C.png")



def print_instruction():

    st.write(" ")
    st.write(" ")

    st.subheader("What is Tweet Annotation for?")
    st.write("""
             Tweet Annotation is... 
        """)

    st.write(" ")
    st.write(" ")
    
    st.subheader("What You Need to Do?")
    st.write(
        """ You will read 20 tweets. 
            For each tweet, you may use all information available to evaluate **how believable it is to you**, **to your friends and peers**, and **to the overall society**.
      """
    )

    st.write(" ")
    st.write(" ")
    
    st.write(""" ⚠️ **Content Warning**
             

        Please be aware that subsequent tweets could contain potentially unsettling or sensitive content. You must be above 18 to participate in the annotation. We advise discretion while proceeding.
    """)

    st.write(" ")
    st.write(" ")

    st.subheader("Labeling Example")
    st.write("Tweets may and may not contain images. Below are some examples of labeling Tweets with images:")


    st.caption("Note:")
    st.write("""
                1. Loading the Tweet and images may take several seconds. \n
                2. When encountering loading problems, try refresh the page or clean the cache and then login again. \n
                """)