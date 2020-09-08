import praw
import pandas as pd
import time
from instabot import Bot
import urllib.request
import os
from datetime import datetime
import tweet_analysis


def start():


    print("Bot starting Beep Boop")

    current_hot = []

    post_history = []

    reddit = praw.Reddit(client_id='REDDIT-BOT-ID', 
                        client_secret='REDDIT-BOT-SECRET', 
                        user_agent='INSTAGRAM-BOT-NAME', 
                        username='REDDIT-USER-ACCOUNT', 
                        password='REDDIT-USER-PASSWORD')

    subreddit = list(reddit.subreddit('blackpeopletwitter').hot(limit=12))


    for submissions in subreddit[2:]:

        current_hot.append((submissions.url, submissions.title, submissions.shortlink))


    bot = Bot()

    bot.login(username = "INSTAGRAM-BOT-NAME",  
    password = "INSTAGRAM-BOT-PASSWORD")



    while True:

        print("trying to find new content beep boop")

        compare_List = []

        subreddit = list(reddit.subreddit('blackpeopletwitter').hot(limit=12))

        for submissions in subreddit[2:]:

            compare_List.append((submissions.url, submissions.title, submissions.shortlink))


        print([i for i in compare_List if i not in current_hot])


        if set(compare_List) != set(current_hot):

            print("New post detected")


            temp = ([i for i in compare_List if i not in current_hot])

            print(temp)

            current_hot = compare_List

            for tuples in temp:

                if tuples[0] not in post_history:
                    
                    urllib.request.urlretrieve(tuples[0], "temp.jpg")
                    print("Picture is being posted -- beep boop") 
                    tweet_string = tweet_analysis.tweet_text("temp.jpg")

                    try:
                        if tweet_string != 'imgur format':
                            bot.upload_photo("temp.jpg", caption = tuples[1] + "  #reddit #blackpeopletwitter " + tweet_string) 
                        else:
                            print("imgur format not uploadable yet")
                            continue

                    except RuntimeError:

                        print("error caught!")
                        continue

                    post_history.append(tuples[0])
                    print("sucess!")


        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Trying again in 10 Min, current Time =", current_time)
        print(post_history)

        time.sleep(600)



start()
