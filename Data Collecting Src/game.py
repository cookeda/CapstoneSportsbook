import json
import re
import os
from datetime import date as dt

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
            sixtyPercent = float(re.search(r"\b\d+\.\d+\b", sixty).group())/100
            thirtyPercent = float(re.search(r"\b\d+\.\d+\b", all).group())/100
            tenPercent = float(re.search(r"\b\d+\.\d+\b", ten).group())/100
            perChance = (.6 * sixtyPercent) + (.3 * thirtyPercent) + (.1 * tenPercent)
            result_dict[team] = perChance
        [file.close() for file in files]
        return result_dict

    def getDictPercent(self, league, stat, hora):
        if league == "NBA":
            direct = "../data/" + league + "/" + stat.lower() + "/" + hora + "/Sorted" + hora + stat + ".jl"
        elif league == "CBB":
            direct = "../data/" + league + "/" + stat.lower() + "/" + hora + "/Sorted" + hora + stat + ".jl"
        elif league == "MLB":
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

    def getDictMOV(self, file):
        result_dict = {}
        with open(file, 'r') as fr:
            for line in fr:
                team = re.search(r'"Team":\s*"([^"]+)"', line).group(1)
                mov = float(re.search(r'([-]?\d+\.\d+)$', line).group(1))
                result_dict[team] = mov
        return result_dict

    def getListPPG(self, file):
        with open(file, 'r') as fr:
            return [line.strip() for line in fr]

    def combineOnRanking(self, dict1, dict2):
        return_dict = {team: (dict1[team] + dict2[team])/2 for team in dict1 if team in dict2}
        return dict(sorted(return_dict.items(), key=lambda item: item[1], reverse=False))

    def sortByRank(self, input_dict):
        sorted_dict = sorted(input_dict.items(), key=lambda item: item[1], reverse=True)
        return {team: rank for rank, (team, percent) in enumerate(sorted_dict, start=1)}


class Game:
    def __init__(self, home_team, away_team, home_spread, away_spread, total, league, stats):
        self.home_team = home_team
        self.away_team = away_team
        self.home_spread = float(home_spread)
        self.away_spread = float(away_spread)
        self.total = float(total)
        self.league = league
        self.stats = stats

    @classmethod
    def gameInputFromJSON(cls, file, league, stats):
        with open(file, 'r') as j:
            games_data = json.load(j)
        return [cls(game["Home Team Rank Name"],
                    game["Away Team Rank Name"],
                    game['DK Home Odds']['Spread'].replace("Pick)", "0").replace("-Pick)", "0"),
                    game['DK Away Odds']['Spread'].replace("Pick", "0").replace("-Pick", "0"),
                    game['Game']['Total'],
                    league, stats) for game in games_data]

    def print_details(self):
        print(f"League: {self.league}")
        print(f"{self.away_team} at {self.home_team}")
        print(f"Home Spread: {self.home_spread}, Away Spread: {self.away_spread}, Total: {self.total}\n")

    def analyze_game(self):
        # Example of using stats for analysis
        # Let's assume we're interested in the "Cover" stats for this analysis
        cover_stats_general = self.stats.generalAlg("Cover", self.league)
        over_stats_general = self.stats.generalAlg("Over", self.league)

        cover_stats_home = self.stats.getDictPercent(self.league, "Cover", "home")
        cover_stats_away = self.stats.getDictPercent(self.league, "Cover", "away")
        over_stats_home = self.stats.getDictPercent(self.league, "Over", "home")
        over_stats_away = self.stats.getDictPercent(self.league, "Over", "away")

        home_cover = (cover_stats_general.get(self.home_team, 0) + cover_stats_home.get(self.home_team, 0)) / 2
        away_cover = (cover_stats_general.get(self.away_team, 0) + cover_stats_away.get(self.away_team, 0)) / 2

        home_over = (over_stats_general.get(self.home_team, 0) + over_stats_home.get(self.home_team, 0)) / 2
        print(self.home_team, over_stats_home.get(self.home_team, 0))
        away_over = (over_stats_general.get(self.away_team, 0) + over_stats_away.get(self.away_team, 0)) / 2

        home_cover_score = 1 + (home_cover * 9)  # Assuming cover stats are [0,1]
        away_cover_score = 1 + (away_cover * 9)
        home_over_score = 1 + (home_over * 9)
        away_over_score = 1 + (away_over * 9)

        over_rating = (home_over_score + away_over_score) / 2

        cover_difference = abs(home_cover_score - away_cover_score)
        base_rating = (home_cover_score + away_cover_score) / 2
        difference_adjustment = (10 - cover_difference) / 10
        game_rating = base_rating * difference_adjustment
        game_rating = max(1, min(game_rating, 10))

        # Determine which team to bet on for the spread
        favored_to_cover = self.home_team if home_cover_score > away_cover_score else self.away_team
        betting_advice = f"Bet on {favored_to_cover} to cover the spread."

        return {
            "matchup": f"{self.away_team} @ {self.home_team}",
            "cover_scores": (home_cover_score, away_cover_score),
            "over_score": over_rating,
            "game_rating": max(1, game_rating),  # Ensure rating is at least 1
            "betting_advice": betting_advice
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
        'NBA': Game.gameInputFromJSON("../Scrapers/Data/DK/NBA.json", 'NBA', stats),
        'CBB': Game.gameInputFromJSON("../Scrapers/Data/DK/CBB.json", 'CBB', stats),
        'MLB': Game.gameInputFromJSON("../Scrapers/Data/DK/MLB.json", 'MLB', stats)
    }

    cover_recommendations = []
    over_scores = []

    # Process games for each league
    for league_name, league_games in leagues.items():
        for game in league_games:
            summary = game.analyze_game()
            print(f"{summary['matchup']} ({league_name}): Cover Rating - {summary['game_rating']:.1f}, Over Score - {summary['over_score']:.1f}")
            print(summary['betting_advice'])

            # Append cover recommendations and over scores for ranking
            cover_recommendations.append((league_name, summary['matchup'], summary['game_rating'], summary['betting_advice']))
            over_scores.append((league_name, summary['matchup'], summary['over_score']))

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


if __name__ == '__main__':
    main()