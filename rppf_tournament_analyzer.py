# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 12:55:12

@author: adamj using chatgpt and a little intuition. For andre to look at and turn into a butterfly
"""

import pandas as pd

# Define the target rating column here
RATING_COLUMN = "RPPF"  # Change this to any column you want to analyze, RANKS will be in reverse order to barthag.

# Manually enter overall top 4 seeds by year to determine Final Four matchups
top_4_seeds = {
    2024: ["E", "S", "M", "W"],  # Top 4 overall seeds in clockwise 1-4 order.
    2023: ["S", "M", "W", "E"],
    2022: ["W", "S", "M", "E"],
    2021: ["W", "S", "M", "E"],
    2019: ["E", "S", "M", "W"],
    2018: ["S", "E", "M", "W"],
    2017: ["E", "M", "S", "W"],
    2016: ["S", "E", "M", "W"],
    2015: ["M", "E", "S", "W"],
    2014: ["S", "W", "M", "E"],
    2013: ["M", "S", "E", "W"],
    2012: ["S", "E", "M", "W"]
}

# Define first-round matchups (excluding play-in games)
first_round_matchups = {
    1: 16, 2: 15, 3: 14, 4: 13, 5: 12, 6: 11, 7: 10, 8: 9
}

def calculate_matchup_success_rate(file_path):
    df = pd.read_csv(file_path)
    
    correct_predictions = 0
    total_games_overall = 0

    for year in df["Year"].unique():
        year_data = df[df["Year"] == year]
        total_games = 0  
        advancing_teams = {}  

        for region in ["E", "M", "S", "W"]:
            region_teams = year_data[year_data["Region"] == region]
            advancing_teams[region] = {}

            # **Round of 64**
            advancing_teams[region][1] = []
            for high_seed, low_seed in first_round_matchups.items():
                high_team = region_teams[region_teams["Seed"] == high_seed]
                low_team = region_teams[region_teams["Seed"] == low_seed]

                if not high_team.empty and not low_team.empty:
                    winner = high_team if high_team["Wins"].values[0] > low_team["Wins"].values[0] else low_team
                    advancing_teams[region][1].append(winner)
                    total_games += 1

                    # **Correctly compare rating values**
                    higher_rating_team = high_team if high_team[RATING_COLUMN].values[0] > low_team[RATING_COLUMN].values[0] else low_team
                    if (winner["Team"].values[0] == higher_rating_team["Team"].values[0]):
                        correct_predictions += 1

            # **Rounds 2-4 (Advancing to Elite 8)**
            for round_num in range(2, 5):  
                advancing_teams[region][round_num] = []
                round_winners = advancing_teams[region][round_num - 1]

                for i in range(0, len(round_winners), 2):  
                    team1, team2 = round_winners[i], round_winners[i + 1]
                    winner = team1 if team1["Wins"].values[0] > team2["Wins"].values[0] else team2
                    advancing_teams[region][round_num].append(winner)
                    total_games += 1

                    # *Compare rating values**
                    higher_rating_team = team1 if team1[RATING_COLUMN].values[0] > team2[RATING_COLUMN].values[0] else team2
                    if winner["Team"].values[0] == higher_rating_team["Team"].values[0]:
                        correct_predictions += 1

        # **Final Four (cross-region matchups)**
        final_four_teams = []
        if year in top_4_seeds:
            for region in top_4_seeds[year]:
                final_four_teams.append(advancing_teams[region][4][0])

            if len(final_four_teams) == 4:
                matchups = [(0, 3), (1, 2)]
                advancing_teams["FinalFour"] = []

                for idx1, idx2 in matchups:
                    team1, team2 = final_four_teams[idx1], final_four_teams[idx2]
                    winner = team1 if team1["Wins"].values[0] > team2["Wins"].values[0] else team2
                    advancing_teams["FinalFour"].append(winner)
                    total_games += 1

                    # **Compare rating values**
                    higher_rating_team = team1 if team1[RATING_COLUMN].values[0] > team2[RATING_COLUMN].values[0] else team2
                    if winner["Team"].values[0] == higher_rating_team["Team"].values[0]:
                        correct_predictions += 1

        # **Championship Game**
        if len(advancing_teams["FinalFour"]) == 2:
            team1, team2 = advancing_teams["FinalFour"]
            winner = team1 if team1["Wins"].values[0] > team2["Wins"].values[0] else team2
            total_games += 1

            # **Compare rating values**
            higher_rating_team = team1 if team1[RATING_COLUMN].values[0] > team2[RATING_COLUMN].values[0] else team2
            if winner["Team"].values[0] == higher_rating_team["Team"].values[0]:
                correct_predictions += 1

        # **Final Check: Did We Count All 63 Games?**
        total_games_overall += total_games
        print(f"Year {year}: Total games analyzed = {total_games}")

        if total_games != 63:
            print(f"⚠ WARNING: {year} does not have exactly 63 games! Check data.")

    success_rate = (correct_predictions / total_games_overall) * 100 if total_games_overall > 0 else 0
    print(f"\nOverall Success Rate for {RATING_COLUMN}: {success_rate:.2f}%")

# Example usage
calculate_matchup_success_rate("RPPF_RW4_Tournament_Data.csv")
