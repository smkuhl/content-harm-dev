import streamlit as st

definition = "<div><ul><li>is <span class='lemonchiffon'>politically polarized</span><br/><li>is <span class='lemonchiffon'>influenced by bandwagon cues</span><br/><li> often <span class='lemonchiffon'>relies on emotions</span> instead of <span class= 'lemonchiffon'>rational thinking</span><li>tends to believe information that <span class='lemonchiffon'>aligns with their prior beliefs</span>."


def print_intro():
    st.title("Welcome to Tweet Annotation!")
    st.write(" ")
    st.write(
        """
        :technologist: We are a group of researchers from the Social Futures Lab at the University of Washington. 
        
        We cordially invite you to participate this annotation of content harmfulness.
        


        
        :warning: **Content Warning**
        
        This study may contain tweets with, but not limited to, violence, abusive language, or death, which may be disturbing. TODO: (You may skip questions or submit the survey at any time.) (because technically you can't skip tweets) You must be above 18 to participate in the annotation. We advise discretion while proceeding.
        



        :lock: **We Value Your Privacy**
        
        Your privacy is our top priority. All information provided will be used exclusively for research purposes, kept confidential, and anonymized.

        You have the right to withdraw your participation and request data deletion at any time. We assure you that your privacy will be strictly protected. 



        

        :memo: **What Will You Do**
         
        You will read 10 Tweets. 

        For each Tweet, you will annotate their potential harms from five different perspectives: actionability, exploitativeness, likelihood of spread, believability, and social fragmentation.

        You may the use internet to search any topics, people, organizations, etc. However we encourage you to not spend to much time on questions you do not know the answer to. Please refrain from looking up the tweet directly or using any AI agent such as ChatGPT, Bard, or Bing Chat. 
      
        """
    )


    st.write("\n")
    st.write(" ")
    st.write(
        """
        
        This annotation survey will take around 30 minutes. After submitting the survey, click on the link provided to be redirected. This will provide proof of completion.
        
        We would like to express our gratitude for your time and contribution to our research. If you have any questions, please feel free to contact us at smkuhl@cs.washington.edu.
        
        \n
        \n
        \n

        ⬇️ Please enter your unique Prolific ID to begin your annotation task or restore your progress.
        """
    )

def print_annotation_guide():
    st.write('#')
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
        Please follow this link to confirm your completion for Prolific: [INSERT PROLIFIC LINK HERE]
        Should you have any inquiries, please contact us at smkuhl@cs.washington.edu or lq9@cs.washington.edu.
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