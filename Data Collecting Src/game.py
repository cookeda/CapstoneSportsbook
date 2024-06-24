import json
import re
import os
from datetime import date as dt, timedelta
from datetime import time as time
from datetime import datetime
import pandas as pd


class Statistics:
    def __init__(self, direct):
        self.direct = direct

    def generalAlg(self, stat, league):
        type2 = stat if stat == "Cover" else "OU"
        result_dict = {}
        paths = [f"{self.direct}{league}/{stat.lower()}/general/SortedCurrentSeason{type2}.jl",
                 f"{self.direct}{league}/{stat.lower()}/general/SortedAllTime{type2}.jl",
                 f"{self.direct}{league}/{stat.lower()}/general/Sorted10Year{type2}.jl"]
        files = [open(path, 'r') for path in paths]
        for sixty, all, ten in zip(*files):
            team = re.search(r'"Team":\s*"([^"]+)"', ten).group(1).strip()
            sixtyPercent = float(re.search(r"\b\d+\.\d+\b", sixty).group()) / 100
            thirtyPercent = float(re.search(r"\b\d+\.\d+\b", all).group()) / 100
            tenPercent = float(re.search(r"\b\d+\.\d+\b", ten).group()) / 100
            perChance = (.6 * sixtyPercent) + (.3 * thirtyPercent) + (.1 * tenPercent)
            result_dict[team] = perChance
        [file.close() for file in files]
        return result_dict

    def getDictPercent(self, league, stat, hora):
        #if league == "NBA":
        #    direct = "../data/" + league + "/" + stat.lower() + "/" + hora + "/Sorted" + hora + stat + ".jl"
        #elif league == "CBB":
        #    direct = "../data/" + league + "/" + stat.lower() + "/" + hora + "/Sorted" + hora + stat + ".jl"
        if league == "MLB":
            direct = "../data/" + league + "/" + stat.lower() + "/" + hora + "/Sorted" + hora + stat + ".jl"
        else:
            print("Invalid League")
        result_dict = {}
        with open(direct, 'r') as fr:
            for line in fr:
                team = re.search(r'"Team":\s*"([^"]+)"', line).group(1)
                percent = float(re.search(r"\b\d+\.\d+\b", line).group()) / 100
                result_dict[team] = percent
        return result_dict

    def getDictMOV(self, league, stat, hora):
        #if league == "NBA":
         #   direct = "../data/" + league + "/" + stat.lower() + "/" + hora + "/Sorted" + hora + stat + ".jl"
        #elif league == "CBB":
        #    direct = "../data/" + league + "/" + stat.lower() + "/" + hora + "/Sorted" + hora + stat + ".jl"
        if league == "MLB":
            direct = "../data/" + league + "/" + stat.lower() + "/" + hora + "/Sorted" + hora + stat + ".jl"
        else:
            print("Invalid League")
        result_dict = {}
        with open(direct, 'r') as fr:
            for line in fr:
                team = re.search(r'"Team":\s*"([^"]+)"', line).group(1)
                mov = float(re.search(r'([-]?\d+\.\d+)$', line).group(1))
                result_dict[team] = mov
        return result_dict

    def getListPPG(self, file):
        with open(file, 'r') as fr:
            return [line.strip() for line in fr]

    def combineOnRanking(self, dict1, dict2):
        return_dict = {team: (dict1[team] + dict2[team]) / 2 for team in dict1 if team in dict2}
        return dict(sorted(return_dict.items(), key=lambda item: item[1], reverse=False))

    def sortByRank(self, input_dict):
        sorted_dict = sorted(input_dict.items(), key=lambda item: item[1], reverse=True)
        return {team: rank for rank, (team, percent) in enumerate(sorted_dict, start=1)}


class Game:
    def __init__(self, home_team, away_team, home_spread, away_spread, total, home_spread_odds, away_spread_odds,
                 over_odds, under_odds, league, stats):
        self.home_team = home_team
        self.away_team = away_team
        self.home_spread = float(home_spread)
        self.away_spread = float(away_spread)
        self.total = float(total)
        self.home_spread_odds = home_spread_odds
        self.away_spread_odds = away_spread_odds
        self.over_odds = over_odds
        self.under_odds = under_odds
        self.league = league
        self.stats = stats

    @classmethod
    def gameInputFromLite(cls, file, league, stats):
        with open(file, 'r', encoding='utf-8') as j:
            games_data = json.load(j)
        return [cls(game_info["Home Team"],
                    game_info["Away Team"],
                    game_info["Home Spread"].replace("Pick)", "0").replace("-Pick)", "0"),
                    game_info["Away Spread"].replace("Pick", "0").replace("-Pick", "0"),
                    game_info["Total Points"],
                    game_info["Home Spread Odds"],
                    game_info["Away Spread Odds"],
                    game_info["Over Odds"],
                    game_info["Under Odds"],
                    league, stats) for matchup_id, game_info in games_data.items()]

    def print_details(self):
        print(f"League: {self.league}")
        print(f"{self.away_team} at {self.home_team}")
        print(f"Home Spread: {self.home_spread}, Away Spread: {self.away_spread}, Total: {self.total}\n")

    def analyze_game(self):
        # Get general stats
        over_stats_general = self.stats.generalAlg("Over", self.league)
        cover_stats_general = self.stats.generalAlg("Cover", self.league)
        over_stats_home = self.stats.getDictPercent(self.league, "Over", "home")
        over_stats_away = self.stats.getDictPercent(self.league, "Over", "away")
        cover_stats_home = self.stats.getDictPercent(self.league, "Cover", "home")
        cover_stats_away = self.stats.getDictPercent(self.league, "Cover", "away")

        # Get Ratings
        home_over = (over_stats_general.get(self.home_team, 0) + over_stats_home.get(self.home_team, 0)) / 2
        away_over = (over_stats_general.get(self.away_team, 0) + over_stats_away.get(self.away_team, 0)) / 2
        home_cover_perc = (cover_stats_general.get(self.home_team, 0) + cover_stats_home.get(self.home_team, 0)) / 2
        away_cover_perc = (cover_stats_general.get(self.away_team, 0) + cover_stats_away.get(self.away_team, 0)) / 2
        home_over_score = 1 + (home_over * 9)
        away_over_score = 1 + (away_over * 9)

        # Encoding for negative sign
        self.over_odds = self.over_odds.replace('−', '-')
        self.under_odds = self.under_odds.replace('−', '-')
        self.home_spread_odds = self.home_spread_odds.replace('−', '-')
        self.away_spread_odds = self.away_spread_odds.replace('−', '-')

        # Slightly Adjust Ratings Based On What Vegas Thinks
        if float(self.over_odds) <= -130:
            home_over_score += 3
        elif float(self.over_odds) >= 100:
            home_over_score -= 2
        if float(self.under_odds) <= -130:
            away_over_score += 3
        elif float(self.under_odds) >= 100:
            away_over_score -= 2

        # Game Total Rating Average Of Both Teams
        over_rating = (home_over_score + away_over_score) / 2

        # Margin Of Victory + Spread
        homeMOV = self.stats.getDictMOV(self.league, "Cover", "home")
        awayMOV = self.stats.getDictMOV(self.league, "Cover", "away")
        home_cover = homeMOV.get(self.home_team, 0) + self.home_spread
        away_cover = awayMOV.get(self.away_team, 0) + self.away_spread

        # Percent Chance to Cover
        spread = abs(self.home_spread)
        home_cover_score = home_cover / spread
        away_cover_score = away_cover / spread

        # Adjust Ratings
        if home_cover_perc >= away_cover_perc:
            home_cover_score += 3
        else:
            away_cover_score += 3

        if float(self.home_spread_odds) <= -130:
            home_cover_score += 3
        elif float(self.home_spread_odds) >= 100:
            home_cover_score -= 2

        if float(self.away_spread_odds) <= -130:
            away_cover_score += 3
        elif float(self.away_spread_odds) >= 100:
            away_cover_score -= 2

        # Determine Who To Bet Spread
        if away_cover_score > home_cover_score:
            favored_to_cover = self.away_team
        else:
            favored_to_cover = self.home_team
        game_cover_score = abs(home_cover_score - away_cover_score)

        game_rating = game_cover_score
        betting_advice = f"Bet on {favored_to_cover} to cover the spread."

        # Return Data and Confidence Ratings For Game
        return {
            "matchup": f"{self.away_team} @ {self.home_team}",
            "over_score": over_rating,
            "game_rating": game_rating,
            "betting_advice": betting_advice,
            "home_cover": self.home_spread,
            "away_cover": self.away_spread,
            "total": self.total
        }


def cleanfile(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        open(file, 'a').close()


def main():
    direct = "../data/"
    stats = Statistics(direct)

    # Load games from all leagues
    leagues = {
        #'NBA': Game.gameInputFromLite("../Scrapers/Data/DK/NBA_Lite.json", 'NBA', stats),
        #'CBB': Game.gameInputFromLite("../Scrapers/Data/DK/CBB_Lite.json", 'CBB', stats),
        'MLB': Game.gameInputFromLite("../Scrapers/Data/DK/MLB_Lite.json", 'MLB', stats)
        # 'NFL': Game.gameInputFromJSON("../Scrapers/Data/DK/NFL.json", 'NFL', stats),
        # 'NHL': Game.gameInputFromJSON("../Scrapers/Data/DK/NHL.json", 'NHL', stats),
        # 'NBA': Game.gameInputFromJSON("../Scrapers/Data/DK/NBA.json", 'NBA', stats)
    }

    # Process games for each league
    game_list = []
    cover_recommendations = []  # Assuming this is defined somewhere
    over_scores = []  # Assuming this is also defined somewhere

    d = dt.today().strftime('%Y-%m-%d')
    for league_name, league_games in leagues.items():
        for game in league_games:
            summary = game.analyze_game()
            print(
                f"{summary['matchup']} ({league_name}): Cover Rating - {summary['game_rating']:.1f}, Over Score - {summary['over_score']:.1f}")
            print(summary['betting_advice'])

            # Append cover recommendations and over scores for ranking
            cover_recommendations.append(
                (league_name, summary['matchup'], summary['game_rating'], summary['betting_advice']))
            over_scores.append((league_name, summary['matchup'], summary['over_score']))

            # Preparing the game dictionary
            game_dict = {
                'date': d,
                'league': league_name,
                'matchup': summary['matchup'],
                'cover_rating': summary['game_rating'],
                'betting_advice': summary['betting_advice'],
                'over_score': summary['over_score'],
                'home_spread': summary['home_cover'],
                'away_spread': summary['away_cover'],
                'total': summary['total']
            }

            # Splitting 'matchup' into 'home_team' and 'away_team'
            home_team, away_team = game_dict['matchup'].split(' @ ')
            game_dict['home_team'] = home_team
            game_dict['away_team'] = away_team
            del game_dict['matchup']  # Removing 'matchup' key as it's no longer needed

            # Modifying 'betting_advice' to just include the team's name
            if "Bet on " in game_dict['betting_advice']:
                team_name = game_dict['betting_advice'].split('Bet on ')[1].split(' to cover the spread')[0]
                game_dict['betting_advice'] = team_name

            # Append the modified dictionary to game_list
            game_list.append(game_dict)
    # Rank and print cover recommendations across all leagues
    print("\nRanked Cover Recommendations Across All Leagues:")
    cover_recommendations.sort(key=lambda x: x[2], reverse=True)  # Sort by cover rating
    for league, matchup, rating, advice in cover_recommendations:
        print(f"{matchup} ({league}): Cover Rating - {rating:.1f}, {advice}")

    # Rank and print over scores across all leagues
    print("\nRanked Games by Over Score Across All Leagues:")
    over_scores.sort(key=lambda x: x[2], reverse=True)  # Sort by over score
    for league, matchup, score in over_scores:
        print(f"{matchup} ({league}): Over Score - {score:.1f}")
    return game_list


def game_list_to_dataframe(game_list):
    predictions_df = pd.DataFrame(game_list)
    return predictions_df


def save_to_csv(df, filename):
    # Save DataFrame to a CSV, appending if it exists.
    try:
        df.to_csv(filename, mode='w', header=False, index=False)
    except FileNotFoundError:
        df.to_csv(filename, mode='w', header=True, index=False)

def load_from_csv(file_path, column_names):
    return pd.read_csv(file_path, header=None, names=column_names)


if __name__ == '__main__':
    game_list = main()
    df = game_list_to_dataframe(game_list)
    print(df)
    save_to_csv(df, "../OddsHistory/History/Predictions.csv")

    column_names = ['Date', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10']
    #dailypd = load_from_csv("../OddsHistory/History/DailyPredictions.csv", column_names)

    current_time = datetime.now().strftime('%H:%M')
    if "05:30" <= current_time < "06:30":
        save_to_csv(df, "../OddsHistory/History/DailyPredictions.csv]")
    else:
        print("Avoided Overriding DailyPredictions")