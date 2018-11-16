import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import threading
import datetime


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
      
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=100):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets

        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}


                parsed_tweet['text'] = tweet.text

                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)


                if tweet.retweet_count > 0:

                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)




            return tweets


        except tweepy.TweepError as e:

            print("Error : " + str(e))


def main():

    f = open("data.txt", "a")

    api = TwitterClient()

    tweets = api.get_tweets(query='$SPX', count=100)


    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets

    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))

    print(
        "Neutral tweets percentage: {} %".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / int(len(tweets))))

    f.write( "Positive tweets: " + str(100 * len(ptweets) / len(tweets)) + "   Negative Tweets: " + str(100 * len(ntweets) / len(tweets)) + "   Neutral tweets: " + str((len(tweets) - len(ntweets) - len(ptweets)) / int(len(tweets))) + "\n")



    #trying to write to file


    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    exit()








def printit():
    threading.Timer(600.0, printit).start()
    d = main()


printit()



