import pandas as pd


# Loads CSV file into dataframe
def load_from_csv(file_path, column_names):
    return pd.read_csv(file_path, header=None, names=column_names)


# Calls helper methods to get league data
def get_league_data(league, results_df):
    get_cover_by_league(league, results_df)
    get_total_by_league(league, results_df)
    get_splits_by_league(league, results_df)


# Gets record of Spread Bets by league
def get_cover_by_league(league, results_df):
    filtered_df = results_df[results_df['league'] == league]
    cover_counts = filtered_df['cover_true'].value_counts()
    true_count = cover_counts.get(True, 0)
    false_count = cover_counts.get(False, 0)
    print("Overall Cover:")
    print(str(true_count) + "-" + str(false_count) + "\n")


# Gets record of totals Bets (Over/Under) by league
def get_total_by_league(league, results_df):
    filtered_df = results_df[results_df['league'] == league]
    over_counts = filtered_df['over_true'].value_counts()
    true_count = over_counts.get(True, 0)
    false_count = over_counts.get(False, 0)
    print("Overall Total:")
    print(str(true_count) + "-" + str(false_count) + "\n")


# Splits up record by confidence rating to show ranges and record
def get_splits_by_league(league, results_df):
    # For Cover
    rating = 0
    ceiling = 1
    while rating < 15:
        # Ensure filtering is based on the filtered_df, not results_df
        filtered_df = results_df[(results_df['league'] == league) & (results_df['cover_rating'] >= rating) & (results_df['cover_rating'] <= ceiling)]
        cover_counts = filtered_df['cover_true'].value_counts()
        true_count = cover_counts.get(True, 0)
        false_count = cover_counts.get(False, 0)
        if true_count != 0 or false_count != 0:
            numerator = true_count
            denominator = true_count + false_count
            percent = round(numerator / denominator, 3) * 100
            print("Cover Record For in range: " + str(rating) + " to " + str(ceiling) + ".")
            print(str(true_count) + "-" + str(false_count) + " " +
                  str(percent) + "% \n")
        rating += 1
        ceiling += 1

    # For Totals
    # For Over
    # 6 is the Split for totals
    rating = 6
    ceiling = 6.2
    while rating < 10:
        # Ensure filtering is based on the filtered_df, not results_df
        filtered_df = results_df[(results_df['league'] == league) & (results_df['over_rating'] > rating) & (results_df['cover_rating'] <= ceiling)]
        over_counts = filtered_df['over_true'].value_counts()
        true_count = over_counts.get(True, 0)
        false_count = over_counts.get(False, 0)
        if true_count != 0 or false_count != 0:
            numerator = true_count
            denominator = true_count + false_count
            percent = round(numerator / denominator, 3) * 100
            print("Over Record For in range: " + str(rating) + " to " + str(ceiling) + ".")
            print(str(true_count) + "-" + str(false_count) + " " +
                  str(percent) + "% \n")
        rating += .2
        ceiling += .2

    # For Under
    # 6 is the split for totals
    rating = 6
    floor = 5.8
    while rating >= 0:
        # Ensure filtering is based on the filtered_df, not results_df
        filtered_df = results_df[(results_df['league'] == league) & (results_df['over_rating'] <= rating) & (results_df['over_rating'] >= floor)]
        over_counts = filtered_df['over_true'].value_counts()
        true_count = over_counts.get(True, 0)
        false_count = over_counts.get(False, 0)
        if true_count != 0 or false_count != 0:
            numerator = true_count
            denominator = true_count + false_count
            percent = round(numerator / denominator, 3) * 100
            print("Under Record For in range " + str(floor) + " to " + str(rating))
            print(str(true_count) + "-" + str(false_count) + " " +
                  str(percent) + "% \n")
        rating -= .2
        floor -= .2

# Gets total DegenBets Record
def get_overall_record(results_df):
    cover_counts = results_df['cover_true'].value_counts()
    over_counts = results_df['over_true'].value_counts()
    overall_counts = cover_counts + over_counts

    true_count = overall_counts.get(True, 0)
    false_count = overall_counts.get(False, 0)
    print("DegenBets record since 4/15/2024: ")
    print(str(true_count) + "-" + str(false_count) + "\n")


def get_daily_data(results_df):
    daily_cover = results_df.groupby('date')['cover_true'].value_counts().unstack(fill_value=0)
    daily_over = results_df.groupby('date')['over_true'].value_counts().unstack(fill_value=0)
    daily_data = daily_cover.add(daily_over, fill_value=0)

    for date in daily_data.index:
        true_count = daily_data.loc[date, True]
        false_count = daily_data.loc[date, False]
        print(f"{date}: {int(true_count)} - {int(false_count)}")

# Calls load
# Gets League data and overall data
def main():
    comparison_columns = ['date', 'league', 'betting_advice', 'cover_true', 'cover_rating', 'over_true', 'over_rating']
    results_df = load_from_csv("../OddsHistory/History/CumulativeResults.csv", comparison_columns)

    #results_df = load_from_csv("../OddsHistory/History/Splits/3_days.csv", comparison_columns)

    #results_df = load_from_csv("../OddsHistory/History/Splits/7_days.csv", comparison_columns)

    #results_df = load_from_csv("../OddsHistory/History/Splits/30_days.csv", comparison_columns)


    #get_league_data("CBB", results_df)
    print("-------------------------\nMLB DATA")
    get_league_data("MLB", results_df)
    print("-------------------------\nNBA DATA")
    get_league_data("NBA", results_df)
    print("-------------------------\nOVERALL DATA")
    get_overall_record(results_df)
    get_daily_data(results_df)
    print("-------------------------")

# Runs Main
if __name__ == "__main__":
    main()