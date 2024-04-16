import pandas as pd
def main():
    comparison_columns = ['date', 'league', 'betting_advice', 'cover_true', 'cover_rating', 'over_true', 'over_rating']
    results_df = load_from_csv("../OddsHistory/History/CumulativeResults.csv", comparison_columns)

    get_leauge_data("NBA")
    get_leauge_data("MLB")
    get_leauge_data("CBB")
def load_from_csv(file_path, column_names):
    return pd.read_csv(file_path, header=None, names=column_names)

def get_leauge_data(leauge):
    return 0

if __name__ == "__main__":
    main()