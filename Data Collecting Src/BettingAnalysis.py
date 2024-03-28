import json
import re
import os
from datetime import datetime

# Assuming external configuration for paths, percentages, and team names
from config import TEAM_DICT, DATA_DIRECTORY

class BettingAnalysis:
    def __init__(self, league):
        self.league = league
        self.data_directory = f"{DATA_DIRECTORY}/{league}/"
        self.general_stats = {'Cover': None, 'Over': None}
        self.home_stats = {'Cover': None, 'Over': None, 'MOV': None}
        self.away_stats = {'Cover': None, 'Over': None, 'MOV': None}

    def load_statistics(self):
        for stat in ['Cover', 'Over']:
            self.general_stats[stat] = self._calculate_general_stat(stat)
            self.home_stats[stat] = self._load_stat_file(f"{stat.lower()}/home/Sortedhome{stat}.jl")
            self.away_stats[stat] = self._load_stat_file(f"{stat.lower()}away/Sortedaway{stat}.jl")
        self.home_stats['MOV'] = self._load_stat_file(f"{stat.lower()}/home/SortedhomeCover.jl", is_mov=True)
        self.away_stats['MOV'] = self._load_stat_file(f"{stat.lower()}/away/SortedawayCover.jl", is_mov=True)

    def _calculate_general_stat(self, stat):
        # Paths to the different datasets
        current_season_path = f"{stat.lower()}/general/SortedCurrentSeason.jl"
        last_10_years_path = f"{self.data_directory}{stat.lower()}/general/Sorted10Year.jl"
        all_time_path = f"{self.data_directory}{stat.lower()}/general/SortedAllTime.jl"

        # Load the datasets
        current_season_data = self._load_stat_file(current_season_path)
        last_10_years_data = self._load_stat_file(last_10_years_path)
        all_time_data = self._load_stat_file(all_time_path)

        # Combine the datasets
        combined_data = {}
        for team in current_season_data:
            current = current_season_data.get(team, 0)
            last_10_years = last_10_years_data.get(team, 0)
            all_time = all_time_data.get(team, 0)

            # Example combination logic: 60% current, 30% last 10 years, 10% all time
            combined_score = 0.6 * current + 0.3 * last_10_years + 0.1 * all_time
            combined_data[team] = combined_score

        return combined_data

    def _load_stat_file(self, path, is_mov=False):
        full_path = os.path.join(self.data_directory, path)
        data = {}
        current_directory = os.getcwd()
        print(current_directory)
        with open(full_path, 'r') as file:
            for line in file:
                team, value = self._parse_line(line, is_mov)
                data[team] = value
        return data

    def _parse_line(self, line, is_mov):
        team_search = re.search(r'"Team":\s*"([^"]+)"', line)
        team = team_search.group(1) if team_search else "Unknown"
        if is_mov:
            value_search = re.search(r'([-]?\d+\.\d+)$', line)
        else:
            value_search = re.search(r"\b\d+\.\d+\b", line)
        value = float(value_search.group()) / 100 if value_search else 0.0
        return team, value

    def best_odds_general(self, stat):
        #Determine the team with the best odds for a given statistic (Cover or Over).
        if stat not in self.general_stats:
            print(f"Invalid stat: {stat}")
            return None

        best_chance = -1.0
        best_team = "None"
        for team, chance in self.general_stats[stat].items():
            if chance > best_chance:
                best_chance = chance
                best_team = team

        print(f"Generally, the most likely team to {stat.lower()} is: {best_team} with a chance of {best_chance}")
        return best_team, best_chance

    def game_analysis(self, home_team, away_team, home_spread, away_spread):
        #Analyze a game given the teams and spreads, making recommendations.
        print(f"Analyzing {away_team} at {home_team}:")

        # Assess the potential for Over/Under bets
        home_over_chance = self.home_stats['Over'].get(home_team, 0)
        away_over_chance = self.away_stats['Over'].get(away_team, 0)
        if home_over_chance > 0.5 and away_over_chance > 0.5:
            print("Recommendation: Consider betting on the Over for this game.")
        elif home_over_chance < 0.5 and away_over_chance < 0.5:
            print("Recommendation: Consider betting on the Under for this game.")

        # Assess Cover bets based on general cover chance and specific home/away stats
        home_cover_chance = self.home_stats['Cover'].get(home_team, 0)
        away_cover_chance = self.away_stats['Cover'].get(away_team, 0)
        if home_cover_chance > away_cover_chance:
            print(f"Recommendation: Bet on {home_team} to cover the spread of {home_spread}.")
        else:
            print(f"Recommendation: Bet on {away_team} to cover the spread of {away_spread}.")

        # Evaluate game based on MOV and spreads
        home_mov = self.home_stats['MOV'].get(home_team, 0)
        away_mov = self.away_stats['MOV'].get(away_team, 0)
        # Simplified MOV logic; in a real scenario, this might involve more nuanced analysis
        if home_mov + home_spread > away_mov + away_spread:
            print(f"Based on MOV: {home_team} has a better chance to beat the spread.")
        else:
            print(f"Based on MOV: {away_team} has a better chance to beat the spread.")

def main():
    # Example usage
    nba_analysis = BettingAnalysis('NBA')
    nba_analysis.load_statistics()

    cbb_analysis = BettingAnalysis('CBB')
    cbb_analysis.load_statistics()

    mlb_analysis = BettingAnalysis('MLB')
    mlb_analysis.load_statistics()

if __name__ == "__main__":
    main()
