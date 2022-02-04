import csv
import os

import tweepy
from dotenv import load_dotenv
from datetime import datetime, timedelta

from twit import *

load_dotenv()


def tweepy_client():
    bearer_token = os.environ.get("BEARER_TOKEN")
    client = tweepy.Client(bearer_token)
    return client


def fetch_tweets():
    today = datetime.now()
    n_days_ago = today - timedelta(days=7)

    keyword = "covid"
    tweet_fields = [
        "attachments",
        "created_at",
        "entities",
        "lang",
        "possibly_sensitive",
        "text",
        "withheld"
    ]
    user_fields = [
        "created_at",
        "description",
        "entities,id",
        "location",
        "name",
        "pinned_tweet_id",
        "profile_image_url",
        "protected,public_metrics",
        "url",
        "username",
        "verified",
        "withheld",
    ]
    expansions = [
        "attachments.poll_ids",
        "attachments.media_keys",
        "author_id",
        "geo.place_id",
        "in_reply_to_user_id",
        "referenced_tweets.id",
        "entities.mentions.username",
        "referenced_tweets.id.author_id",
    ]

    pages = tweepy.Paginator(
        tweepy_client().search_recent_tweets,
        keyword,
        max_results=100,
        tweet_fields=tweet_fields,
        user_fields=user_fields,
        expansions=expansions,
        start_time=n_days_ago
    ).flatten(limit=200000)

    a_file = open("tweets.csv", "w")
    keys = ["id", "text", 'tweet_hashtags', 'tweet_annotations', 'tweet_entities', 'tweet_created_at', 'tweet_lang', 'tweet_domains', 'tweet_urls', 'tweet_mentions']
    dict_writer = csv.DictWriter(a_file, keys)
    dict_writer.writeheader()

    for tweet in pages:
        if tweet.lang == 'en':

            if tweet.entities:
                (tweet_mentions, tweet_hashtags, tweet_annotations, tweet_urls) = hydrate_entities(tweet.entities)
                tweet_entities, tweet_domains = hydrate_context_annotations(tweet.data)
            else:
                tweet_mentions = None
                tweet_hashtags = None
                tweet_annotations = None
                tweet_urls = None
                tweet_entities = None
                tweet_domains = None

            tweet_dict = {
                "id": tweet.id,
                "text": tweet.text,
                "tweet_created_at": tweet.created_at,
                "tweet_lang": tweet.lang,
                "tweet_mentions": tweet_mentions,
                "tweet_hashtags": tweet_hashtags,
                "tweet_annotations": tweet_annotations,
                "tweet_urls": tweet_urls,
                "tweet_entities": tweet_entities,
                "tweet_domains": tweet_domains
            }

            dict_writer.writerow(tweet_dict)

    a_file.close()


if __name__ == '__main__':
    fetch_tweets()
