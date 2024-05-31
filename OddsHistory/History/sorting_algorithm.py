import pandas as pd
import json
import numpy as np
from datetime import datetime

def map_to_subinterval(rating, bins):
    for lower, upper in bins:
        step = (upper - lower) / 1  # Define 4 sub-intervals within each main interval
        for i in range(1):
            sub_lower = lower + i * step
            sub_upper = sub_lower + step
            if sub_lower <= rating < sub_upper:
                return f"{sub_lower:.1f}-{sub_upper:.1f}"
    return "Out of defined range"

def map_total_to_window(total_rating, over_ranges, under_ranges):
    for range_type, ranges in [('Over', over_ranges), ('Under', under_ranges)]:
        for lower, upper in ranges:
            if lower <= total_rating <= upper:
                return f"{range_type} {lower}-{upper}"
    return "Out of defined range"

# Load your CSV file without headers
data = pd.read_csv('CumulativeResults.csv', header=None)
data.columns = ['Date', 'League', 'Team', 'CoverResult', 'CoverRating', 'TotalResult', 'TotalRating']

data['Date'] = pd.to_datetime(data['Date'])
data['CoverResult'] = data['CoverResult'].astype(int)
data['TotalResult'] = data['TotalResult'].astype(int)

main_intervals = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16)]
over_ranges = [(6.0, 6.19), (6.2, 6.39), (6.4, 6.59), (6.6, 6.79), (6.8, 6.99), (7, 7.19), (7.2, 7.39), (7.4, 7.59), (7.6, 7.79), (7.8, 7.99), (8.0, 8.19), (8.2, 8.39), (8.4, 8.59), (8.6, 8.79), (8.8, 8.99), (9, 9.19), (9.2, 9.5), (9.5, 10), (10, 10.5)]
under_ranges = [(5.8, 5.99), (5.6, 5.79), (5.4, 5.59), (5.2, 5.39), (5.0, 5.19), (4.8, 4.99), (4.6, 4.79), (4.4, 4.59), (4.2, 4.39), (4.0, 4.19), (3.8, 3.99), (3.6, 3.79), (3.4, 3.59), (3.2, 3.39), (3.0, 3.19), (2.8, 2.99), (2.5, 2.79), (2, 2.49), (1.5, 1.99), (1, 1.49), (0.5, 0.99), (0, 0.49)]

data['CoverRatingWindow'] = data['CoverRating'].apply(lambda x: map_to_subinterval(x, main_intervals))
data['TotalRatingWindow'] = data['TotalRating'].apply(lambda x: map_total_to_window(x, over_ranges, under_ranges))

lambda_ = 0.1  # Decay rate
current_date = datetime.now()
data['DaysAgo'] = (current_date - data['Date']).dt.days
data['DecayFactor'] = np.exp(-lambda_ * data['DaysAgo'])

data['CoverScore'] = data['CoverRating'] * data['CoverResult'] * data['DecayFactor']
data['TotalScore'] = data['TotalRating'] * data['TotalResult'] * data['DecayFactor']

# Additional computations for bet count and expected hit rate
data['BetCount'] = 1
cover_stats = data.groupby(['League', 'CoverRatingWindow']).agg(
    CoverScoreAvg=('CoverScore', 'mean'),
    BetCount=('BetCount', 'sum'),
    xHitRate=('CoverResult', 'mean')
).reset_index()
total_stats = data.groupby(['League', 'TotalRatingWindow']).agg(
    TotalScoreAvg=('TotalScore', 'mean'),
    BetCount=('BetCount', 'sum'),
    xHitRate=('TotalResult', 'mean')
).reset_index()

cover_stats_sorted = cover_stats.sort_values(by=['League', 'CoverRatingWindow'], ascending=[True, True])
total_stats_sorted = total_stats.sort_values(by=['League', 'TotalRatingWindow'], ascending=[True, True])

print("Recommended Cover Bet Rating Windows for Today by League:")
print(cover_stats_sorted)
print("\nRecommended Total Bet Rating Windows for Today by League:")
print(total_stats_sorted)

# Save sorted dataframes to CSV
cover_stats_sorted.to_csv('cover_stats_sorted.csv', index=False)
total_stats_sorted.to_csv('total_stats_sorted.csv', index=False)
