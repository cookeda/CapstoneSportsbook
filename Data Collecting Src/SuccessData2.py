import pandas as pd
from datetime import datetime, timedelta

def load_from_csv(file_path, column_names):
    df = pd.read_csv(file_path, header=None, names=column_names)
    df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' column is datetime type
    return df

def filter_by_period(results_df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    return results_df[(results_df['date'] >= start_date) & (results_df['date'] <= end_date)]

def save_period_data(results_df, file_name):
    if not results_df.empty:
        results_df.to_csv(file_name, index=False)
        # Generate summary without datetime_is_numeric
        summary = results_df.describe(include='all')  # Removed datetime_is_numeric=True
        summary_file_name = file_name.replace(".csv", "_summary.txt")
        with open(summary_file_name, 'w') as f:
            summary.to_string(f)
        print(f"Data and summary saved to {file_name} and {summary_file_name}")
    else:
        print(f"No data available for {file_name}")
        
def get_time_period_data(results_df):
    today = pd.to_datetime(datetime.now().date())
    three_days_ago = today - timedelta(days=3)
    seven_days_ago = today - timedelta(days=7)
    thirty_days_ago = today - timedelta(days=30)
    
    last_3_days_data = filter_by_period(results_df, three_days_ago, today)
    last_7_days_data = filter_by_period(results_df, seven_days_ago, today)
    last_30_days_data = filter_by_period(results_df, thirty_days_ago, today)
    
    save_period_data(last_3_days_data, "../OddsHistory/History/Splits/3_days.csv")
    save_period_data(last_7_days_data, "../OddsHistory/History/Splits/7_days.csv")
    save_period_data(last_30_days_data, "../OddsHistory/History/Splits/30_days.csv")


def get_splits_by_league(league, results_df):
    # For Cover
    rating = 0
    ceiling = 3
    while rating < 15:
        # Ensure filtering is based on the filtered_df, not results_df
        filtered_df = results_df[(results_df['league'] == league) & (results_df['cover_rating'] >= rating) & (results_df['cover_rating'] <= ceiling)]
        cover_counts = filtered_df['cover_true'].value_counts()
        true_count = cover_counts.get(True, 0)
        false_count = cover_counts.get(False, 0)
        if true_count != 0 or false_count != 0:
            print("Cover Record For in range: " + str(rating) + " to " + str(ceiling) + ".")
            print(str(true_count) + "-" + str(false_count) + "\n")
        rating += 3
        ceiling += 3

    # For Totals
    # For Over
    # 6 is the Split for totals
    rating = 6
    ceiling = 6.5
    while rating < 10:
        # Ensure filtering is based on the filtered_df, not results_df
        filtered_df = results_df[(results_df['league'] == league) & (results_df['over_rating'] > rating) & (results_df['cover_rating'] <= ceiling)]
        over_counts = filtered_df['over_true'].value_counts()
        true_count = over_counts.get(True, 0)
        false_count = over_counts.get(False, 0)
        if true_count != 0 or false_count != 0:
            print("Over Record For in range: " + str(rating) + " to " + str(ceiling) + ".")
            print(str(true_count) + "-" + str(false_count) + "\n")
        rating += .5
        ceiling += .5

    # For Under
    # 6 is the split for totals
    rating = 6
    floor = 5.5
    while rating >= 0:
        # Ensure filtering is based on the filtered_df, not results_df
        filtered_df = results_df[(results_df['league'] == league) & (results_df['over_rating'] <= rating) & (results_df['over_rating'] >= floor)]
        over_counts = filtered_df['over_true'].value_counts()
        true_count = over_counts.get(True, 0)
        false_count = over_counts.get(False, 0)
        if true_count != 0 or false_count != 0:
            print("Under Record For in range " + str(floor) + " to " + str(rating))
            print(str(true_count) + "-" + str(false_count) + "\n")
        rating -= .5
        floor -= .5


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

def get_overall_record(results_df):
    cover_counts = results_df['cover_true'].value_counts()
    over_counts = results_df['over_true'].value_counts()
    overall_counts = cover_counts + over_counts

    true_count = overall_counts.get(True, 0)
    false_count = overall_counts.get(False, 0)
    print("DegenBets record since 4/15/2024: ")
    print(str(true_count) + "-" + str(false_count) + "\n")



# Gets record of totals Bets (Over/Under) by league
def get_total_by_league(league, results_df):
    filtered_df = results_df[results_df['league'] == league]
    over_counts = filtered_df['over_true'].value_counts()
    true_count = over_counts.get(True, 0)
    false_count = over_counts.get(False, 0)
    print("Overall Total:")
    print(str(true_count) + "-" + str(false_count) + "\n")


def main():
    comparison_columns = ['date', 'league', 'betting_advice', 'cover_true', 'cover_rating', 'over_true', 'over_rating']
    results_df = load_from_csv("../OddsHistory/History/CumulativeResults.csv", comparison_columns)

    #results_df = load_from_csv("../OddsHistory/History/Splits/e_.csv", comparison_columns)


    # Process league data and overall data
    print("-------------------------\nMLB DATA")
    get_league_data("MLB", results_df)
    print("-------------------------\nNBA DATA")
    get_league_data("NBA", results_df)
    print("-------------------------\nOVERALL DATA")
    get_overall_record(results_df)
    
    # New time period data fetching and saving
    get_time_period_data(results_df)
    print("-------------------------")

# Include all other necessary functions like get_league_data, get_cover_by_league, etc., here

if __name__ == "__main__":
    main()
