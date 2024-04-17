import pandas as pd
def main():
    comparison_columns = ['date', 'league', 'betting_advice', 'cover_true', 'cover_rating', 'over_true', 'over_rating']
    results_df = load_from_csv("../OddsHistory/History/CumulativeResults.csv", comparison_columns)

    #get_league_data("CBB", results_df)
    get_league_data("MLB", results_df)
    get_league_data("NBA", results_df)

def load_from_csv(file_path, column_names):
    return pd.read_csv(file_path, header=None, names=column_names)

def get_league_data(league, results_df):
    get_cover(league, results_df)
    get_total(league, results_df)

def get_cover(league, results_df):
    filtered_df = results_df[results_df['league'] == league]
    cover_counts = filtered_df['cover_true'].value_counts()
    print("Spread for " + league + ":")
    print(cover_counts)
def get_total(league, results_df):
    filtered_df = results_df[results_df['league'] == league]
    over_counts = filtered_df['over_true'].value_counts()
    print("Totals for " + league + ":")
    print(over_counts)

if __name__ == "__main__":
    main()