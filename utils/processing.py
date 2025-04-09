import pandas as pd

from .constants import (
    FALSE_QUESTIONS,
    GROUP1_QUESTIONS,
    GROUP2_QUESTIONS,
    QUESTIONS,
    COLUMN_NAME_MAP,
    TRUE_QUESTIONS,
)


def process_qualtrics(df: pd.DataFrame, min_duration=None) -> pd.DataFrame:
    """
    Process the input from Qualtrics to make it suitable for analysis.
    Args:
        df (pd.DataFrame): The input DataFrame from Qualtrics.
        min_duration (int, optional): Minimum duration (seconds) for survey completion.
            Defaults to None, which means no minimum duration.
    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    df = df.rename(
        columns=COLUMN_NAME_MAP
    )  # rename the columns, mistakes in the survey
    df = df.rename(columns={col: col.lower() for col in df.columns})
    df = df[df.finished == "True"]  # remove unfinished responses
    df = df[df.status == "IP Address"]  # remove preview responses and header rows
    df = df[df.cue_group.notna()]  # remove rows with no cue group
    df.cue_group = df.cue_group.astype("category")  # convert cue group to category
    df.duration = df.duration.astype("int")  # convert duration to int
    if min_duration:
        df = df[df.duration >= min_duration]
    for col in df.columns:
        if col in QUESTIONS:
            # Participants answer question "Are they telling the truth?"
            df[col] = df[col].replace({"Non": False, "Oui": True})
            df[col] = df[col].astype("category")

    return df


def _get_score(row: pd.Series) -> float:
    """
    Calculate the score for a single row.
    Args:
        row (pd.Series): A single row of the DataFrame.
    Returns:
        float: The score for the row.
    """
    score = 0
    total = row.notna().sum()
    assert total != 0, "Row has no valid responses"
    for col in row.index:
        if row[col] == True and col in TRUE_QUESTIONS:
            score += 1
        if row[col] == False and col in FALSE_QUESTIONS:
            score += 1
    return score / total


def calculate_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate score for each participant in each group.
    Args:
        df (pd.DataFrame): The input DataFrame from Qualtrics.
    Returns:
        pd.DataFrame: The DataFrame with scores for each group.
            With two additional columns for both groups.
    """
    group1 = df[GROUP1_QUESTIONS]
    group2 = df[GROUP2_QUESTIONS]

    df["group1_score"] = group1.apply(_get_score, axis=1)
    df["group2_score"] = group2.apply(_get_score, axis=1)
    df["score_diff"] = df["group2_score"] - df["group1_score"]

    return df
