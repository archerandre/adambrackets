# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:56:08 2025

@author: adamj
"""

import pandas as pd

def compare_to_champions(updated_file, champion_file):
    # Load datasets
    updated_df = pd.read_csv(updated_file)
    champion_stats_df = pd.read_csv(champion_file, index_col=0)
    
    # Identify numerical columns from champion stats
    numeric_columns = champion_stats_df.index.tolist()
    
    # Ensure updated_df has the same numerical columns
    updated_df = updated_df[numeric_columns + ["Team"]]
    
    # Filtering teams that fit within champion min-max range
    filtered_teams = updated_df.copy()
    for col in numeric_columns:
        min_val = champion_stats_df.loc[col, "Min Value"]
        max_val = champion_stats_df.loc[col, "Max Value"]
        filtered_teams = filtered_teams[(filtered_teams[col] >= min_val) & (filtered_teams[col] <= max_val)]
    
    # Display and save results
    if not filtered_teams.empty:
        print("Teams fitting within champion stat ranges:")
        print(filtered_teams)
        filtered_teams.to_csv("Teams_Within_Champion_Ranges_2025.csv", index=False)
        print("Filtered teams saved to 'Teams_Within_Champion_Ranges_*YEAR*.csv'")
    else:
        print("No teams fit within the champion stat ranges.")

# Example usage
updated_file = "RPPF_UPDATED_RW4_Analyze_2025.csv"  # Update with actual path
champion_file = "Champion_Stats.csv"   # Ensure this file exists
compare_to_champions(updated_file, champion_file)
