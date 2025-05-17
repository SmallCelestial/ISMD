import re
from datetime import datetime
from typing import List


class User:
    def __init__(self, name: str, tweets: List['Tweet'] = None):
        self.name = name
        self.tweets = tweets if tweets else []

    def add_tweet(self, tweet: 'Tweet'):
        if self.tweets is None:
            self.tweets = []
        self.tweets.append(tweet)

    def get_all_mentions(self):
        mentions = set()
        for tweet in self.tweets:
            mentions.update(tweet.mentioned_users_names)

        return mentions

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Tweet:
    def __init__(self, content: str, retweets_count: int = 0, tweet_created_at: datetime = None):
        self.content = content
        self.retweet_count = retweets_count
        self.tweet_created_at = tweet_created_at
        self.mentioned_users_names = self.__find_mentioned_users()

    def __find_mentioned_users(self):
        mentions = re.findall(r"@(\w+)", self.content)
        return mentions


