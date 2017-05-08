#!/usr/bin/env python3
"""Fweet Tlipper
Takes 200 tweets from a feed and searches for two terms.
If it finds either or both terms, they are swapped.
Resultant tweets are presented for your choice for retweeting.

Original code by /u/alfieish:
https://www.reddit.com/r/learnpython/comments/69txc2/
looking_for_critique_of_a_code_i_wrote_to_flip/
"""

import getopt
import os
import re
import sys
import tweepy       # https://github.com/tweepy/tweepy

def main(argv):
    """Main function"""

    help_text = """Fweet Tlipper v0.1

Usage:
  python fweet_tlipper.py [options]

Options:

  -h, --help                help
  -t, --test                test"""

    try:
        opts, args = getopt.getopt(argv, "ht", ["help", "test"])
    except getopt.GetoptError:
        print(args)
        print(help_text)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg)
            print(help)
            sys.exit()
        elif opt in ("-t", "--test"):
            test()
            sys.exit()
    target = input("Name of Twitter account to flip: @")
    term_1 = input("First term to swap (e.g. Trump): ")
    term_2 = input("Second term to swap (e.g. Clinton): ")
    tweets = get_tweets(target)
    tweet = swap_tweets(tweets, term_1, term_2)
    tweet = "RT @{} {}".format(target, tweet[:141-(len(target)+5)])
    retweet = input('{}\nPost above tweet? '.format(tweet))[0].lower()
    if retweet == 'y':
        post_tweet(tweet)

def authorize_account():
    """Authorizes Twitter account API.
    Pull Twitter credentials from environment variables (e.g. in virtualenv)

    Returns tweepy API.
    """

    # Twitter API credentials
    consumer_key = get_env_variable("CONSUMER_KEY")
    consumer_secret = get_env_variable("CONSUMER_SECRET")
    access_key = get_env_variable("ACCESS_KEY")
    access_secret = get_env_variable("ACCESS_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    return tweepy.API(auth)

def post_tweet(tweet):
    """Posts tweet to twitter account."""

    twitter_account = authorize_account()
    try:
        twitter_account.update_status(tweet)
        print("Tweet posted.")
    except tweepy.TweepError:
        print("Error: Tweet failed.")

def get_tweets(screen_name):
    """Retrieves MAXIMUM_ALLOWED_TWEETS from screen_name.

    screen_name     Str of twitter screen name

    Returns list of tweets.
    """
    MAXIMUM_ALLOWED_TWEETS = 200

    twitter_account = authorize_account()

    tweets = twitter_account.user_timeline(
        screen_name=screen_name,
        count=MAXIMUM_ALLOWED_TWEETS
        )
    tweets = [tweet.text for tweet in tweets]
    return tweets

def swap_tweets(tweets, term_1, term_2):
    """Searches tweets for term_1 and term_2. Performs swaps and presents a
    list of swapped tweets for user's choice.

    tweets      List of source tweets
    term_1      Str of first word to swap
    term_2      Str of second word to swap

    Returns str of selected tweet.
    """
    # only match full word in search terms
    target_words = re.compile(r'\b({}|{})\b'.format(term_1, term_2))
    regex_1 = re.compile(r'\b{}\b'.format(term_1))
    regex_2 = re.compile(r'\b{}\b'.format(term_2))
    regex_tmp = re.compile(r'\b55placeholder55\b')
    target_tweets = [tweet for tweet in tweets if target_words.search(tweet)]
    # TODO possible to swap in 1 step? take into account any occurence of
    # term_1 must be swapped to term_2 and vice versa
    target_tweets = [
        regex_1.sub('55placeholder55', tweet) for tweet in target_tweets
        ]
    target_tweets = [
        regex_2.sub(term_1, tweet) for tweet in target_tweets
        ]
    target_tweets = [
        regex_tmp.sub(term_2, tweet) for tweet in target_tweets
        ]
    for index, tweet in enumerate(target_tweets):
        print('{}: {}'.format(index, tweet))
    selected_tweet = input(
        "Enter no. of tweet to retweet: "
        )
    try:
        return target_tweets[int(selected_tweet)]
    except (ValueError, IndexError):
        sys.exit("Invalid tweet selected.")

def get_env_variable(var_name):
    """Get the environment variable or return exception.

    var_name        Str of environment variable

    Returns value of environment variable.
    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise KeyError(error_msg)

def test():
    """Runs doctest on functions."""

    import doctest
    print(doctest.testmod())

if __name__ == '__main__':
    main(sys.argv[1:])
