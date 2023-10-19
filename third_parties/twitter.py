import os
from datetime import datetime, timezone
import logging
import json
import pathlib

import tweepy

logger = logging.getLogger("twitter")

use_twitter = os.getenv("USE_TWITTER", "False")

twitter_client = (
    tweepy.Client(
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
    )
    if use_twitter == "True"
    else None
)

twitter_file = pathlib.Path(__file__).parent / "edens_tweets.json"


def scrape_user_tweets(username: str, num_tweets=5) -> list[dict]:
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url"
    """
    return (
        _scrape_user_tweets_from_api(username, num_tweets)
        if use_twitter == "True"
        else _scrape_user_tweets_from_file(twitter_file)
    )


def _scrape_user_tweets_from_file(filepath: pathlib.Path) -> list[dict]:
    with filepath.open("r") as f:
        return json.load(f)


def _scrape_user_tweets_from_api(username: str, num_tweets=5) -> list[dict]:
    # if you want to use Twitter lookup API, need "basic" or "pro" subscription. ("free" doesn't support)
    user_id = twitter_client.get_user(username=username).data.id
    tweets = twitter_client.get_users_tweets(
        id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
    )

    tweet_list = []

    for tweet in tweets.data:
        tweet_dict = {
            "time_posted": str(datetime.now(timezone.utc) - tweet.created_at),
            "text": tweet.text,
            "url": f"https://twitter.com/{username}/status/{tweet.id}",
        }
        tweet_list.append(tweet_dict)

    return tweet_list
