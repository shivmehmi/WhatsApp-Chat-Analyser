from urlextract import URLExtract
extractor = URLExtract()
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter


# calculating stats
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1. fetch number of messages
    num_messages = df.shape[0]

    # 2. fetch num of words
    words = []
    for msg in df['messages']:
        words.extend(msg.split())

    # 3. fetch num of media messages
    media_msg = df[df['messages'] == '<Media omitted>\n'].shape[0]

    # 4. fetch num of links
    links = []

    for msg in df['messages']:
        links.extend(extractor.find_urls(msg))

    return num_messages, len(words), media_msg, len(links)

# finding the busiest users in the group(Group Level)
def top_busy_users(df):
    x=df['user'].value_counts()

    new_df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    
    return x, new_df

# Wordcloud
def create_wordcloud(selected_user,df):
    f= open('hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp=df.drop(df[df['messages'] == '<Media omitted>\n'].index)

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=300, min_font_size=10, background_color='white')
    temp['messages']=temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=' '))
    return df_wc

# Most common words
def most_common_words(selected_user, df):
    f= open('hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp=df.drop(df[df['messages'] == '<Media omitted>\n'].index)

    words = []
    for msg in temp['messages']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    from collections import Counter
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

#Timeline
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['month_num']=df['dates'].dt.month
    timeline=df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time

    return timeline

# Dialy Timeline
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline=df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

# Week Activity Map
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    week_activity=df['day_name'].value_counts()

    return week_activity

# Month Activity Map
def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    month_activity=df['month'].value_counts()

    return month_activity

# Overall Activity
def overall_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]    

    overall_activity = df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)

    return overall_activity
