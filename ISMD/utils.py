from typing import Iterable

import pandas as pd

from ISMD.model import User, Tweet, Interaction, UserNetwork


def get_users(df: pd.DataFrame) -> dict[str, User]:
    return {username: User(username) for username in df.name.unique()}

def iterate_tweets(df: pd.DataFrame) -> Iterable[Tweet]:
    for _, row in df.iterrows():
        content = row.get('text')
        username = row.get('name')

        yield Tweet(content, username)

def iterate_interactions(tweets: Iterable[Tweet]) -> Iterable[Interaction]:
    for tweet in tweets:
        for username in tweet.find_mentioned_users():
            yield Interaction(User(tweet.username), User(username))

def create_user_network(df: pd.DataFrame) -> UserNetwork:
    users = get_users(df).values()
    tweets = iterate_tweets(df)
    interactions = iterate_interactions(tweets)

    return UserNetwork(list(users), list(interactions))
