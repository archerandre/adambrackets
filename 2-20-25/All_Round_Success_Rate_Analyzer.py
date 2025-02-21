# -*- coding: utf-8 -*- 
"""
Created on Thu Feb 20 12:55:12

@author: success rates by adamj using chatgpt and a little intuition. For andre to look at and turn into a butterfly
"""

import pandas as pd

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
    
    # Automatically detect numerical columns (excluding Year, Seed, and Wins if present)
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    numeric_columns = [col for col in numeric_columns if col not in ["Year", "Seed", "Wins"]]

    results = {}

    for rating_col in numeric_columns:
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

                        # **Compare rating values**
                        higher_rating_team = high_team if high_team[rating_col].values[0] > low_team[rating_col].values[0] else low_team
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

                        # **Compare rating values**
                        higher_rating_team = team1 if team1[rating_col].values[0] > team2[rating_col].values[0] else team2
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
                        higher_rating_team = team1 if team1[rating_col].values[0] > team2[rating_col].values[0] else team2
                        if winner["Team"].values[0] == higher_rating_team["Team"].values[0]:
                            correct_predictions += 1

            # **Championship Game**
            if len(advancing_teams["FinalFour"]) == 2:
                team1, team2 = advancing_teams["FinalFour"]
                winner = team1 if team1["Wins"].values[0] > team2["Wins"].values[0] else team2
                total_games += 1

                # **Compare rating values**
                higher_rating_team = team1 if team1[rating_col].values[0] > team2[rating_col].values[0] else team2
                if winner["Team"].values[0] == higher_rating_team["Team"].values[0]:
                    correct_predictions += 1

            total_games_overall += total_games

        # Calculate success rate for this rating column
        success_rate = (correct_predictions / total_games_overall) * 100 if total_games_overall > 0 else 0
        results[rating_col] = success_rate

    # Convert results dictionary to a DataFrame and export to CSV
    output_df = pd.DataFrame(list(results.items()), columns=["Rating Column", "Success Rate (%)"])
    output_df.to_csv("ALL_success_rates_RW4.csv", index=False)

    print("Success rates have been saved to 'ALL_success_rates_RW4.csv'")

# Example usage
calculate_matchup_success_rate("RPPF_RW4_Tournament_Data.csv")
