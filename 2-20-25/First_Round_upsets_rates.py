# -*- coding: utf-8 -*- 
"""
Created on Thu Feb 20 12:55:12

@author: adam
"""

import pandas as pd

# Define the target rating column for upsets
RATING_COLUMN = "RPPF"

# Define first-round matchups (Round of 64, excluding play-in games)
first_round_matchups = {
    1: 16, 2: 15, 3: 14, 4: 13, 5: 12, 6: 11, 7: 10, 8: 9
}

def analyze_rppf_upsets_first_round(file_path):
    df = pd.read_csv(file_path)

    # Identify numerical columns (excluding Year, Seed, and Wins)
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    numeric_columns = [col for col in numeric_columns if col not in ["Year", "Seed", "Wins"]]

    total_games = 0
    rppf_upsets = 0
    column_success_counts = {col: 0 for col in numeric_columns}  # Track how often a column was higher in the upset team

    for year in df["Year"].unique():
        year_data = df[df["Year"] == year]

        for region in ["E", "M", "S", "W"]:
            region_teams = year_data[year_data["Region"] == region]

            # **First Round (Round of 64)**
            for high_seed, low_seed in first_round_matchups.items():
                high_team = region_teams[region_teams["Seed"] == high_seed]
                low_team = region_teams[region_teams["Seed"] == low_seed]

                if not high_team.empty and not low_team.empty:
                    winner = high_team if high_team["Wins"].values[0] > low_team["Wins"].values[0] else low_team
                    loser = low_team if winner.equals(high_team) else high_team

                    total_games += 1  # Count all first-round games

                    # **Check if this was an RPPF-based upset**
                    if winner[RATING_COLUMN].values[0] < loser[RATING_COLUMN].values[0]:
                        rppf_upsets += 1
                        for col in numeric_columns:
                            if winner[col].values[0] > loser[col].values[0]:  
                                column_success_counts[col] += 1

    # **Calculate success rates for each column in RPPF-based upsets**
    success_rates = {col: (column_success_counts[col] / rppf_upsets) * 100 if rppf_upsets > 0 else 0 for col in numeric_columns}

    # **Print the total number of first-round games analyzed**
    print(f"\nTotal First-Round Games Analyzed: {total_games}")

    # **Print results in console**
    print("\nRPPF-Based Upset Success Rates by Column (First Round Only):")
    for col, rate in success_rates.items():
        print(f"{col}: {rate:.2f}%")

    # **Print the proportion of RPPF-based upsets**
    rppf_upset_rate = (rppf_upsets / total_games) * 100 if total_games > 0 else 0
    print(f"\nPercentage of First-Round Games that were RPPF Upsets: {rppf_upset_rate:.2f}%")

    # **Save results to CSV**
    output_df = pd.DataFrame(list(success_rates.items()), columns=["Rating Column", "RPPF Upset Success Rate (%)"])
    output_df.to_csv("rppf_upset_success_rates_first_round.csv", index=False)

    print("\nRPPF upset success rates (first round) have been saved to 'rppf_upset_success_rates_first_round.csv'")

# Example usage
analyze_rppf_upsets_first_round("RPPF_RW4_Tournament_Data.csv")
