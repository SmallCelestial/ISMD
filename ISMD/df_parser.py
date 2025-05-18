from typing import Iterable

import pandas as pd
from model import SocialInteraction, Tweet, User

_EXPECTED_COLUMNS = ["who", "to_whom", "interaction_type"]


def parse_dataframe(df: pd.DataFrame) -> Iterable[SocialInteraction]:
    missing = [col for col in _EXPECTED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {missing}")

    for _, row in df.iterrows():
        yield _row_to_social_interaction(row)


def _row_to_social_interaction(row: pd.Series) -> SocialInteraction:
    return SocialInteraction(
        who_id=str(row["who"]),
        to_whom_id=str(row["to_whom"]),
        interaction_type=str(row["interaction_type"]),
        who_username=row.get("who_username"),
        to_whom_username=row.get("to_whom_username"),
        item=row.get("item"),
    )


def get_users(df: pd.DataFrame) -> dict[str, User]:
    return {username: User(username) for username in df.name.unique()}


def iterate_tweets(df: pd.DataFrame) -> Iterable[Tweet]:
    for _, row in df.iterrows():
        content = row.get("text")
        username = row.get("name")

        yield Tweet(content, username)
