import imp
import matplotlib.pyplot as plt
import seaborn as sns
from pytz_deprecation_shim import build_tzinfo
import streamlit as st
import preprocessor as pre
import helper

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    #getting datafram and preprocessing it
    df = pre.preprocess(data)

    # fetch unique users and sort them
    user_list=df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    # create dropbox
    selected_user = st.sidebar.selectbox("Show Analysis WRT ",user_list)

    if st.sidebar.button("Show Analysis"):
        #Stats Area
        num_messages, words, media_msg, links = helper.fetch_stats(selected_user, df) # num of messages of selected user
        st.header('Top Statistics')

        col1, col2, col3, col4 = st.columns(4)
       
        with col1: #num of messages
            st.header('Total Messages')
            st.title(num_messages)

        with col2: #num of words
            st.header('Total Words')
            st.title(words)

        with col3: #num of Media messages
            st.header('Media Shared')
            st.title(media_msg)

        with col4: #num of links
            st.header('Links Shared')
            st.title(links)

        # Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        plt.xticks(rotation='vertical')
        plt.plot(timeline['time'],timeline['messages'])
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        plt.xticks(rotation='vertical')
        plt.plot(daily_timeline['only_date'],daily_timeline['messages'])
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header('Top Busy Days')
            busy_day=helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            plt.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header('Top Busy Months')
            busy_month=helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            plt.bar(busy_month.index,busy_month.values, color='green')
            st.pyplot(fig)

        # Overall Activity
        st.header("Overall Activity Map")
        overall_activity=helper.overall_activity(selected_user,df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(overall_activity,cmap='coolwarm')
        st.pyplot(fig)

        # finding the busiest users in the group(Group Level)
        if selected_user == 'Overall':
            st.title("Top Busy Users")
            col1, col2 = st.columns(2)
            fig, ax = plt.subplots()
            x, new_df = helper.top_busy_users(df)

            with col1: # barplot for top busy users
                plt.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2: 
                st.dataframe(new_df)

        # Create Wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user,df) 
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        
