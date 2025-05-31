from typing import Iterable

import pandas as pd

import src.app.utils.df_parser as df_parser
from src.app.model import Interaction, Tweet, User, UserNetwork


def iterate_interactions(tweets: Iterable[Tweet]) -> Iterable[Interaction]:
    for tweet in tweets:
        for username in tweet.find_mentioned_users():
            yield Interaction(User(tweet.username), User(username))


def create_user_network(df: pd.DataFrame) -> UserNetwork:
    if is_dataframe_with_content(df):
        return _create_user_network_by_content(df)

    return _create_user_network_by_cols(df)


def _create_user_network_by_content(df: pd.DataFrame) -> UserNetwork:
    users = df_parser.get_users(df).values()
    tweets = df_parser.iterate_tweets(df)
    interactions = iterate_interactions(tweets)

    return UserNetwork(list(users), list(interactions))


def _create_user_network_by_cols(df: pd.DataFrame) -> UserNetwork:
    social_interactions = df_parser.parse_dataframe(df)

    users = set()
    interactions = set()

    for social_interaction in social_interactions:
        user_from = User(
            name=social_interaction.who_username or social_interaction.who_id
        )
        user_to = User(
            name=social_interaction.to_whom_username or social_interaction.to_whom_id
        )

        users.add(user_from)
        users.add(user_to)

        interaction = Interaction(user1=user_from, user2=user_to)
        interactions.add(interaction)

    return UserNetwork(list(users), list(interactions))


def is_dataframe_with_content(df: pd.DataFrame) -> bool:
    cols = df.columns
    return ("text" in cols or "content" in cols) and "name" in cols
