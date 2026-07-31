"""
Pulls NBA player stats via nba_api and merges with a salary dataset to compute
performance-per-dollar value metrics.
 
IMPORTANT: nba_api does NOT include contract/salary data. You need to download
a salary CSV separately, e.g. from Kaggle (search "NBA player salaries") or
Spotrac. Set SALARY_CSV_PATH below to point at that file.
 
Expected salary CSV columns (rename yours to match, or edit the merge below):
    player_name, season, salary
 
pip install nba_api pandas numpy
"""

import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguedashplayerstats
import time

SEASON = "2024-25"
SALARY_CSV_PATH = "NBA Player Salaries_2024-25_1.csv" # columns: Player, Team, Salary (Salary is formatted like "$55,761,216 ")

def pull_player_stats(season=SEASON):
    """Pulls per-game and advanced stats for all players in a season."""
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star="Regular Season",
        per_mode_detailed="PerGame"
    )
    df = stats.get_data_frames()[0]

    # Keep the columns most relevant to a value analysis
    keep_cols = [
        "PLAYER_NAME", "TEAM_ABBREVIATION", "AGE", "GP", "MIN",
        "PTS", "REB", "AST", "STL", "BLK", "TOV",
        "FG_PCT", "FG3_PCT", "FT_PCT", "PLUS_MINUS"
    ]
    df = df[keep_cols].rename(columns={
        "PLAYER_NAME": "player_name",
        "TEAM_ABBREVIATION": "team",
        "AGE": "age",
        "GP": "games_played",
        "MIN": "minutes_per_game",
        "PTS": "points_per_game",
        "REB": "rebounds_per_game",
        "AST": "assists_per_game",
        "STL": "steals_per_game",
        "BLK": "blocks_per_game",
        "TOV": "turnovers_per_game",
        "FG_PCT": "fg_pct",
        "FG3_PCT": "three_pt_pct",
        "FT_PCT": "ft_pct",
        "PLUS_MINUS": "plus_minus"
    })
    return df

def compute_production_score(df):
    """
    Simple composite production score to rank players on overall output.
    Weights are a judgment call -- document this choice in your write-up,
    it's exactly the kind of decision that shows analytical thinking.
    """
    df["production_score"] = (
        df["points_per_game"] * 1.0 +
        df["rebounds_per_game"] * 1.2 +
        df["assists_per_game"] * 1.5 +
        df["steals_per_game"] * 2.0 +
        df["blocks_per_game"] * 2.0 -
        df["turnovers_per_game"] * 1.0
    )
    return df

def merge_with_salary(stats_df, salary_csv_path=SALARY_CSV_PATH):
    salary_df = pd.read_csv(salary_csv_path)

    # Salary column looks like '$55,761,216 ' (currency-formatted text) -- convert to a real number
    salary_df["salary"] = (
        salary_df["Salary"]
        .astype(str)
        .str.replace(r"[$,]", "", regex=True)
        .str.strip()
        .astype(float)
    )
    salary_df = salary_df.rename(columns={"Player": "player_name"})

    # Normalize name formatting to improve join match rate
    stats_df["player_name_clean"] = stats_df["player_name"].str.strip().str.lower()
    salary_df["player_name_clean"] = salary_df["player_name"].str.strip().str.lower()

    merged = stats_df.merge(
        salary_df[["player_name_clean", "salary"]],
        on="player_name_clean",
        how="inner"  # drops players you couldn't match -- check match rate!
    )
    merged = merged.drop(columns=["player_name_clean"])
    return merged

def compute_value_metrics(df):
    df["salary_millions"] = df["salary"] / 1_000_000
    df["production_per_million"] = (df["production_score"] / df["salary_millions"]).round(2)
    df["points_per_million"] = (df["points_per_game"] / df["salary_millions"]).round(2)
    return df.sort_values("production_per_million", ascending=False)

if __name__ == "__main__":
    print(f"Pulling {SEASON} player stats from stats.nba.com...")
    stats = pull_player_stats()
    time.sleep(1)  # be polite to the API

    stats = compute_production_score(stats)

    print(f"Pulled stats for {len(stats)} players.")
    print(f"Now merging with salary data from {SALARY_CSV_PATH}...")
    print("(Make sure you've downloaded a salary CSV and set SALARY_CSV_PATH above)")

    try:
        merged = merge_with_salary(stats)
        merged = compute_value_metrics(merged)

        match_rate = len(merged) / len(stats) * 100
        print(f"Matched {len(merged)}/{len(stats)} players ({match_rate:.1f}%)")

        merged.to_csv("nba_player_value.csv", index=False)
        print("Saved to nba_player_value.csv")
        print("\nTop 10 most efficient players (production per $1M salary):")
        print(merged[["player_name", "team", "production_score",
                       "salary_millions", "production_per_million"]].head(10))
    except FileNotFoundError:
        print(f"\n[!] Couldn't find {SALARY_CSV_PATH}. Download an NBA salary CSV "
              f"(e.g. from Kaggle) and update SALARY_CSV_PATH before running this step.")
        stats.to_csv("nba_player_stats_only.csv", index=False)
        print("Saved stats-only file to nba_player_stats_only.csv in the meantime.")
