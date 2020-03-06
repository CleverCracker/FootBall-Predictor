import pandas as pd
import numpy as np
import os
import csv
from datetime import datetime
# from scrapers import *

DATA_PATH = 'data/'

df1 = pd.read_csv(os.path.join(DATA_PATH, 'season-0708.csv'))
df2 = pd.read_csv(os.path.join(DATA_PATH, 'season-0809.csv'))
df3 = pd.read_csv(os.path.join(DATA_PATH, 'season-0910.csv'))
df4 = pd.read_csv(os.path.join(DATA_PATH, 'season-1011.csv'))
df5 = pd.read_csv(os.path.join(DATA_PATH, 'season-1112.csv'))
df6 = pd.read_csv(os.path.join(DATA_PATH, 'season-1213.csv'))
df7 = pd.read_csv(os.path.join(DATA_PATH, 'season-1314.csv'))
df8 = pd.read_csv(os.path.join(DATA_PATH, 'season-1415.csv'))
df9 = pd.read_csv(os.path.join(DATA_PATH, 'season-1516.csv'))
df10 = pd.read_csv(os.path.join(DATA_PATH, 'season-1617.csv'))
df11 = pd.read_csv(os.path.join(DATA_PATH, 'season-1718.csv'))
df12 = pd.read_csv(os.path.join(DATA_PATH, 'season-1819.csv'))
df13 = pd.read_csv(os.path.join(DATA_PATH, 'season-1920.csv'))

all_dfs = (df1, df2, df3, df4, df5, df6, df7,
           df8, df9, df10, df11, df12, df13)
for df in all_dfs:
    df.dropna(subset=['Date'], axis=0, how='all', inplace=True)

all_dfs
# col_needed = ["HomeTeam", "AwayTeam", "Date",
#               "FTHG", "FTAG", "FTR",
#               "HTHG", "HTAG", "HTR",
#               "HS", "AS", "HST", "AST",
#               "HF", "AF", "HC", "AC",
#               "HY", "AY", "HR", "AR",
#               "B365H", "B365D", "B365A",  # bet365
#               "BWH", "BWD", "BWA",  # bet and win
#               "WHH", "WHD", "WHA",  # William Hill
#               "VCH", "VCD", "VCA"]  # BetVictor
# col_needed


def parse_date(date):
    """
    Converts date from string to datetime object.
    """
    return datetime.strptime(date, '%d/%m/%y').date()


def parse_date_other(date):
    """
    Converts date when strptime layout is different
    """
    return datetime.strptime(date, '%d/%m/%Y').date()


df1.Date = df1.Date.apply(parse_date)
df2.Date = df2.Date.apply(parse_date)
df3.Date = df3.Date.apply(parse_date)
df4.Date = df4.Date.apply(parse_date)
df5.Date = df5.Date.apply(parse_date)
df6.Date = df6.Date.apply(parse_date)
df7.Date = df7.Date.apply(parse_date)
df8.Date = df8.Date.apply(parse_date)
df9.Date = df9.Date.apply(parse_date)
df10.Date = df10.Date.apply(parse_date)
df11.Date = df11.Date.apply(parse_date)
df12.Date = df12.Date.apply(parse_date_other)
df13.Date = df13.Date.apply(parse_date_other)


# Get only the columns we need to get stats
cols = ['Date', 'HomeTeam', 'AwayTeam', 'HS', 'AS',
        'FTHG', 'FTAG', 'FTR', 'B365H', 'B365D', 'B365A']

playing_stats1 = df1[cols]
playing_stats2 = df2[cols]
playing_stats3 = df3[cols]
playing_stats4 = df4[cols]
playing_stats5 = df5[cols]
playing_stats6 = df6[cols]
playing_stats7 = df7[cols]
playing_stats8 = df8[cols]
playing_stats9 = df9[cols]
playing_stats10 = df10[cols]
playing_stats11 = df11[cols]
playing_stats12 = df12[cols]
playing_stats13 = df13[cols]


def get_matchweek(playing_stat):
    """
    Adds matchweek feature to dataset
    """
    j = 1
    MatchWeek = []
    for i in range(len(playing_stat)):
        MatchWeek.append(j)
        if ((i + 1) % 10) == 0:
            j += 1
    playing_stat['MW'] = MatchWeek
    return playing_stat


playing_stats1 = get_matchweek(playing_stats1)
playing_stats2 = get_matchweek(playing_stats2)
playing_stats3 = get_matchweek(playing_stats3)
playing_stats4 = get_matchweek(playing_stats4)
playing_stats5 = get_matchweek(playing_stats5)
playing_stats6 = get_matchweek(playing_stats6)
playing_stats7 = get_matchweek(playing_stats7)
playing_stats8 = get_matchweek(playing_stats8)
playing_stats9 = get_matchweek(playing_stats9)
playing_stats10 = get_matchweek(playing_stats10)
playing_stats11 = get_matchweek(playing_stats11)
playing_stats12 = get_matchweek(playing_stats12)
playing_stats13 = get_matchweek(playing_stats13)

# Gets the goals scored agg arranged by teams and matchweek


def get_goals_scored(playing_stat):
    # Get the number of matchweeks in the season
    mw = max(playing_stat['MW'])

    # Create a dictionary with team names as keys
    teams = {}
    for i in playing_stat.groupby('HomeTeam').mean().T.columns:
        teams[i] = []

    # build dict where value is a list of goals scored per match
    for i in range(len(playing_stat)):
        HTGS = playing_stat.iloc[i]['FTHG']
        ATGS = playing_stat.iloc[i]['FTAG']
        teams[playing_stat.iloc[i].HomeTeam].append(HTGS)
        teams[playing_stat.iloc[i].AwayTeam].append(ATGS)

    # Create a dataframe for goals scored where rows are teams and cols are matchweek.
    GoalsScored = pd.DataFrame(data=teams, index=[i for i in range(mw)]).T
    GoalsScored[0] = 0
    # Aggregate to get uptil that point
    for i in range(2, mw):
        GoalsScored[i] = GoalsScored[i] + GoalsScored[i-1]
    return GoalsScored

# Gets the goals conceded agg arranged by teams and matchweek


def get_goals_conceded(playing_stat):
    # Get the number of matchweeks in the season
    mw = max(playing_stat['MW'])

    # Create a dictionary with team names as keys
    teams = {}
    for i in playing_stat.groupby('HomeTeam').mean().T.columns:
        teams[i] = []

    # build dict where value is a list of goals conceded per match
    for i in range(len(playing_stat)):
        ATGC = playing_stat.iloc[i]['FTHG']
        HTGC = playing_stat.iloc[i]['FTAG']
        teams[playing_stat.iloc[i].HomeTeam].append(HTGC)
        teams[playing_stat.iloc[i].AwayTeam].append(ATGC)

    # Create a dataframe for goals conceded where rows are teams and cols are matchweek.
    GoalsConceded = pd.DataFrame(data=teams, index=[i for i in range(mw)]).T
    GoalsConceded[0] = 0
    # Aggregate to get uptil that point
    for i in range(1, mw):
        GoalsConceded[i] = GoalsConceded[i] + GoalsConceded[i-1]
    return GoalsConceded


def get_goal_stats(playing_stat):
    GC = get_goals_conceded(playing_stat)
    GS = get_goals_scored(playing_stat)

    j = 0
    HTGS = []
    ATGS = []
    HTGC = []
    ATGC = []

    for i in range(len(playing_stat)):
        ht = playing_stat.iloc[i].HomeTeam
        at = playing_stat.iloc[i].AwayTeam
        HTGS.append(GS.loc[ht][j])
        ATGS.append(GS.loc[at][j])
        HTGC.append(GC.loc[ht][j])
        ATGC.append(GC.loc[at][j])

        if ((i + 1) % 10) == 0:
            j += 1

    playing_stat['HTGS'] = HTGS
    playing_stat['ATGS'] = ATGS
    playing_stat['HTGC'] = HTGC
    playing_stat['ATGC'] = ATGC

    return playing_stat


# Apply to each dataset
playing_stats1 = get_goal_stats(playing_stats1)
playing_stats2 = get_goal_stats(playing_stats2)
playing_stats3 = get_goal_stats(playing_stats3)
playing_stats4 = get_goal_stats(playing_stats4)
playing_stats5 = get_goal_stats(playing_stats5)
playing_stats6 = get_goal_stats(playing_stats6)
playing_stats7 = get_goal_stats(playing_stats7)
playing_stats8 = get_goal_stats(playing_stats8)
playing_stats9 = get_goal_stats(playing_stats9)
playing_stats10 = get_goal_stats(playing_stats10)
playing_stats11 = get_goal_stats(playing_stats11)
playing_stats12 = get_goal_stats(playing_stats12)
# playing_stats13 = get_goal_stats(playing_stats13)
df13
df12
df1