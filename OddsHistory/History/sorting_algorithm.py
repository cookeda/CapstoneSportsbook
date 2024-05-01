import pandas as pd
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

main_intervals = [(0, 3), (3, 6), (6, 9), (9, 12), (12, 15)]
over_ranges = [(6, 6.5), (6.5, 7), (7, 7.5), (7.5, 8), (8, 8.5), (8.5, 9)]
under_ranges = [(5.5, 6), (5, 5.5), (4.5, 5), (4, 4.5), (3.5, 4), (3, 3.5)]

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

print("Recommended Cover Bet Rating Windows for Today by League:")
print(cover_stats.sort_values(by=['League', 'CoverScoreAvg'], ascending=False).groupby('League').head(10))
print("\nRecommended Total Bet Rating Windows for Today by League:")
print(total_stats.sort_values(by=['League', 'TotalScoreAvg'], ascending=False).groupby('League').head(10))
