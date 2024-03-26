# Algorithm for determining likelihood
# Should be updated to reflect per bet and compare if a bet is good or bad
# Should take into consideration home advantage, etc. down the line
# Pretty sure the math is right currently

# Determines general percentage on the basis of
# 60% Current, 30% Over The Last 10 Years, 10% All Time

import json
import re
import os
import time
from datetime import date as dt

teamDict = {
    'Hawks': 'Atlanta',
    'Celtics': 'Boston',
    'Nets': 'Brooklyn',
    'Hornets': 'Charlotte',
    'Bulls': 'Chicago',
    'Cavaliers': 'Cleveland',
    'Mavericks': 'Dallas',
    'Nuggets': 'Denver',
    'Pistons': 'Detroit',
    'Warriors': 'Golden State',
    'Rockets': 'Houston',
    'Pacers': 'Indiana',
    'Clippers': 'LA Clippers',
    'Lakers': 'LA Lakers',
    'Grizzlies': 'Memphis',
    'Heat': 'Miami',
    'Bucks': 'Milwaukee',
    'Timberwolves': 'Minnesota',
    'Pelicans': 'New Orleans',
    'Knicks': 'New York',
    'Thunder': 'Okla City',
    'Magic': 'Orlando',
    '76ers': 'Philadelphia',
    'Suns': 'Phoenix',
    'Trailblazers': 'Portland',
    'Kings': 'Sacramento',
    'Spurs': 'San Antonio',
    'Raptors': 'Toronto',
    'Jazz': 'Utah',
    'Wizards': 'Washington'
}

def generalAlg(stat, league):
    type2 = ""
    if stat == "Cover":
        type2 = stat

    if stat == "Over":
        type2 = "OU"

    result_dict = {}
    with open(direct + league + "/" + stat.lower() + "/general/SortedCurrentSeason" + type2 + ".jl", 'r') as current:
        with open(direct + league + "/" + stat.lower() + "/general/SortedAllTime" + type2 + ".jl", 'r') as all:
            with open(direct + league + "/" + stat.lower() + "/general/Sorted10Year" + type2 + ".jl", 'r') as ten:
                for sixty, tenp, thirty in zip(current, all, ten):
                    team_search = re.search(r'"Team":\s*"([^"]+)"', thirty)
                    team = team_search.group(1).strip()
                    match = re.search(r"\b\d+\.\d+\b", sixty)
                    sixtyPercent = float(match.group())/100
                    match = re.search(r"\b\d+\.\d+\b", thirty)
                    thirtyPercent   = float(match.group())/100
                    match = re.search(r"\b\d+\.\d+\b", tenp)
                    tenPercent      = float(match.group())/100
                    perChance = (.6 * sixtyPercent) + \
                                (.3 * thirtyPercent) + \
                                (.1 * tenPercent)

                    result_dict[team] = perChance
                return result_dict

# Generates best team for a general stat (Cover or OU)
def bestOddsGeneral(result_dict, stat):
    bestChance = -99
    bestTeam = "Nobody"
    for team in result_dict:
        percent = float(result_dict[team])
        if percent > bestChance:
            bestChance = percent
            bestTeam = team
    if stat == "Cover":
        print("Generally, the most likely team to cover is: " + bestTeam + " Chance: " + str(bestChance))

    if stat == "Over":
        print("Generally, the most likely team to go over is: " + bestTeam + " Chance: " + str(bestChance))

# Gets python dictionary from a file
def getDictPercent(file):
    result_dict = {}
    with open(file, 'r') as fr:
        for line in fr:
            team_search = re.search(r'"Team":\s*"([^"]+)"', line)
            team = team_search.group(1) if team_search else "Unknown"

            percent_search = re.search(r"\b\d+\.\d+\b", line)
            percent = float(percent_search.group()) / 100 if percent_search else 0.0

            result_dict[team] = percent
    return result_dict

def getDictMOV(file):
    result_dict = {}
    with open(file, 'r') as fr:
        for line in fr:
            # First, extract the team name from the JSON-like structure
            team_search = re.search(r'"Team":\s*"([^"]+)"', line)
            team = team_search.group(1) if team_search else "Unknown"

            # Now, extract the MOV value from the end of the line
            mov_search = re.search(r'([-]?\d+\.\d+)$', line)
            mov = float(mov_search.group(1)) if mov_search else 0.0

            result_dict[team] = mov
    return result_dict

def combineOnRanking(dict1, dict2):
    return_dict = {}
    for team1 in dict1:
        if team1 in dict2:
            both = (dict1[team1] + dict2[team1])/2
            return_dict[team1] = both
    #print(return_dict)
    sorted_dict = sorted(return_dict.items(), key=lambda item: item[1], reverse=False)
    #print(sorted_dict)
    return dict(sorted_dict)

def sortByRank(input_dict):
    sorted_dict = sorted(input_dict.items(), key=lambda item: item[1], reverse=True)
    ranked_dict = {team: rank for rank, (team, percent) in enumerate(sorted_dict, start=1)}
    return ranked_dict

def gameInput(homeTeam, homeSpread, awayTeam, awaySpread, league):
    entered = 0
    print("-----------------------------")
    try:
        with open(direct + 'results.txt', 'a') as fp:
            fp.write("-----------------------------" + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Rankings for team
    if league == 'NBA':
        numTeams = len(choNBA)
        coverHome = choNBA[homeTeam]
        coverAway = cacNBA[awayTeam]
        overHome = chcNBA[homeTeam]
        overAway = caoNBA[awayTeam]
        movHome = homeMOV[homeTeam]
        movAway = awayMOV[awayTeam]

    elif league == 'CBB':
        numTeams = len(choCBB)
        coverHome = choCBB[homeTeam]
        coverAway = cacCBB[awayTeam]
        overHome = chcCBB[homeTeam]
        overAway = caoCBB[awayTeam]
        movHome = homeMOV2[homeTeam]
        movAway = awayMOV2[awayTeam]

    topTier = numTeams * 0.10  # Top 10% Change to 20
    midTier = numTeams * 0.322  # Top 30% Change to 30
    lowTier = numTeams * 0.70  # Starting point for Bottom 30% Change to 70
    ass = numTeams * 0.833  # Bottom 10% Change to 80

    print("For " + awayTeam + " At " + homeTeam + ":")
    try:
        with open(direct + 'results.txt', 'a') as fp:
            fp.write("For " + awayTeam + " At " + homeTeam + ":" + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Over
    if overHome <= midTier and overAway <= midTier:
        if overHome <= topTier and overAway <= topTier:
            try:
                with open(direct + 'results.txt', 'a') as fp:
                    fp.write("Lock ALERT!" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
            print("LOCK ALERT!")
            lockparlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Over")
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Take the over!" + '\n' + "Home Rank :" + str(overHome) + '\n' +"Away Rank: " + str(overAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        print("Take the over!")
        print("Home Rank :" + str(overHome))
        print("Away Rank: " + str(overAway))
        parlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Over")

    elif overHome > lowTier and overAway > lowTier:
        if overHome > ass and overAway > ass:
            try:
                with open(direct + 'results.txt', 'a') as fp:
                    fp.write("Lock ALERT!" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
            print("LOCK ALERT!")
            lockparlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Under")
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Take the under!" + '\n' + "Home Rank :" + str(overHome) + '\n' +"Away Rank: " + str(overAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        print("Take the under!")
        print("Home Rank :" + str(overHome))
        print("Away Rank: " +str(overAway))
        parlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Under")

    else:
        print("Don't bet on O/U")
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Don't bet on O/U" + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")

    # Cover
    print("HOME: " + "MOV: " + str(movHome) + " Spread: " + str(homeSpread))
    print("AWAY: " + "MOV: " + str(movAway) + " Spread: " + str(awaySpread))
    if coverHome <= midTier and coverAway > lowTier:
        if coverHome <= topTier and coverAway > ass:
            print("LOCK ALERT!")
            try:
                with open(direct + 'results.txt', 'a') as fp:
                    fp.write("LOCK ALERT!" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
            lockparlay.append(league + ": " + homeTeam + ": Cover")
        print("Bet on " + homeTeam + " to Cover!")
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Bet on " + homeTeam + " to Cover!" + '\n' + "Home Rank :" + str(coverHome) + '\n' +"Away Rank: " + str(coverAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        print("Home Rank :" + str(coverHome))
        print("Away Rank: " + str(coverAway))
        parlay.append(league + ": " + homeTeam + ": Cover")
    elif coverHome > lowTier and coverAway <= midTier:
        if coverHome > ass and coverAway <= topTier:
            print("LOCK ALERT!")
            try:
                with open(direct + 'results.txt', 'a') as fp:
                    fp.write("LOCK ALERT!" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
            lockparlay.append(league + ": " + awayTeam + ": Cover")
        print("Bet on " + awayTeam + " to Cover!")
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Bet on " + awayTeam + " to Cover!" + '\n' + "Home Rank :" + str(coverHome) + '\n' +"Away Rank: " + str(coverAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        print("Home Rank :" + str(coverHome))
        print("Away Rank: " + str(coverAway))
        parlay.append(league + ": " + awayTeam + ": Cover")
    basedOnSpreadMov(league, homeTeam, awayTeam, movHome, movAway, homeSpread, awaySpread, coverHome, coverAway)
def basedOnSpreadMov(league, homeTeam, awayTeam, movHome, movAway, homeSpread, awaySpread, coverHome, coverAway):
    # Home Bet
    if ((float(movHome) + float(homeSpread)) > 0) and (coverHome < coverAway):
        print("Bet on " + homeTeam + " to Cover!")
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Bet on " + homeTeam + " to Cover!" + '\n' + "Home Rank :" + str(
                    coverHome) + '\n' + "Away Rank: " + str(coverAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        print("Home Rank :" + str(coverHome))
        print("Away Rank: " + str(coverAway))
        parlay.append(league + ": " + homeTeam + ": Cover")
    # Away Bet
    if ((float(movAway) + float(awaySpread)) > 0) and (coverAway < coverHome):
        print("Bet on " + awayTeam + " to Cover!")
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Bet on " + awayTeam + " to Cover!" + '\n' + "Home Rank :" + str(
                    coverHome) + '\n' + "Away Rank: " + str(coverAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        print("Home Rank :" + str(coverHome))
        print("Away Rank: " + str(coverAway))
        parlay.append(league + ": " + awayTeam + ": Cover")

def gameInputFromJSON(file, league):
    with open(file, 'r') as j:
        games = json.load(j)
    for game in games:
        homeTeam = game["Home Team Rank Name"]
        awayTeam = game["Away Team Rank Name"]
        homeSpread = game['DK Home Odds']['Spread']
        awaySpread = game['DK Away Odds']['Spread']
        if homeSpread == "Pick)" or homeSpread == "-Pick)":
            homeSpread = "0"

        if awaySpread == "Pick" or awaySpread == "-Pick":
            awaySpread = "0"
        gameInput(homeTeam, homeSpread, awayTeam, awaySpread, league)

def cleanfile(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        open(file, 'a')

def main():
    global generalOver  # General Over Dict
    global generalOver2
    global generalOver3
    global generalCover # General Cover Dict
    global generalCover2
    global generalCover3
    global homeOver     # Home Over Dict
    global homeOver2
    global homeOver3
    global homeCover    # Home Cover Dict
    global homeCover2
    global homeCover3
    global homeMOV     # Home Margin of Victory
    global homeMOV2
    global homeMOV3
    global awayOver     # Away Over Dict
    global awayOver2
    global awayOver3
    global awayCover    # Away Cover Dict
    global awayCover2
    global awayCover3
    global awayMOV     # Away Margin of Victory
    global awayMOV2
    global awayMOV3
    global choNBA          # Combined Home Over
    global choCBB
    global choMLB
    global chcNBA          # Combined Home Cover
    global chcCBB
    global chcMLB
    global caoNBA          # Combined Away Over
    global caoCBB
    global caoMLB
    global cacNBA          # Combined Away Cover
    global cacCBB
    global cacMLB

    global parlay       # Parlay List
    global lockparlay
    global teamDict     # Team Dictionary in form City: Team Name
    global direct
    # Connor
    direct = "../data/"
    # Devin
    #direct = "data/"

    cleanfile(direct + "results.txt")
    parlay = []
    lockparlay = []
    d = dt.today()
    generalCover = generalAlg("Cover", "NBA")
    generalOver = generalAlg("Over", "NBA")
    generalCover2 = generalAlg("Cover", "CBB")
    generalOver2 = generalAlg("Over", "CBB")
    generalCover3 = generalAlg("Cover", "MLB")
    generalOver3 = generalAlg("Over", "MLB")

    # For Home
    homeCover = getDictPercent(direct + "NBA/cover/home/SortedhomeCover.jl")
    homeCover2 = getDictPercent(direct + "CBB/cover/home/SortedhomeCover.jl")
    #homeCover3 = getDict(direct + "MLB/cover/home/SortedhomeCover.jl")

    homeOver = getDictPercent(direct + "NBA/over/home/SortedhomeOver.jl")
    homeOver2 = getDictPercent(direct + "CBB/over/home/SortedhomeOver.jl")
    #homeOver3 = getDict(direct + "MLB/over/home/SortedHomeOver.jl")

    homeMOV = getDictMOV("../data/NBA/cover/home/SortedhomeCover.jl")
    homeMOV2 = getDictMOV("../data/CBB/cover/home/SortedhomeCover.jl")
    #homeMOV3 = getDictMOV("../data/MLB/cover/home/SortedhomeCover.jl")

    # For Away
    awayCover = getDictPercent(direct + "NBA/cover/away/SortedawayCover.jl")
    awayCover2 = getDictPercent(direct + "CBB/cover/away/SortedawayCover.jl")
    #awayCover3 = getDict(direct + "MLB/cover/away/SortedawayCover.jl")

    awayOver = getDictPercent(direct + "NBA/over/away/SortedawayOver.jl")
    awayOver2 = getDictPercent(direct + "CBB/over/away/SortedawayOver.jl")
    #awayOver3 = getDict(direct + "MLB/over/away/SortedawayOver.jl")

    awayMOV = getDictMOV("../data/NBA/cover/away/SortedawayCover.jl")
    awayMOV2 = getDictMOV("../data/CBB/cover/away/SortedawayCover.jl")
    #awayMOV3 = getDictMOV("../data/MLB/cover/away/SortedawayCover.jl")

    # Variables stand for Combine Home/Away Over/Cover (ex: Combine Home Over = cho)
    choNBA = combineOnRanking(sortByRank(generalOver), sortByRank(homeOver))
    choCBB = combineOnRanking(sortByRank(generalOver2), sortByRank(homeOver2))
    #choMLB = combineOnRanking(sortByRank(generalOver3), sortByRank(homeOver3))

    chcNBA = combineOnRanking(sortByRank(generalCover), sortByRank(homeCover))
    chcCBB = combineOnRanking(sortByRank(generalCover2), sortByRank(homeCover2))
    #chcMLB = combineOnRanking(sortByRank(generalCover3), sortByRank(homeCover3))

    caoNBA = combineOnRanking(sortByRank(generalOver), sortByRank(awayOver))
    caoCBB = combineOnRanking(sortByRank(generalOver2), sortByRank(awayOver2))
    #caoMLB = combineOnRanking(sortByRank(generalOver3), sortByRank(homeOver3))

    cacNBA = combineOnRanking(sortByRank(generalCover), sortByRank(awayCover))
    cacCBB = combineOnRanking(sortByRank(generalCover2), sortByRank(awayCover2))
    #cacMLB = combineOnRanking(sortByRank(generalCover3), sortByRank(awayCover3))

    # Run Manually
    #gameInput(home, away, league)

    gameInputFromJSON("../Scrapers/Data/DK/NBA.json", 'NBA')
    gameInputFromJSON("../Scrapers/Data/DK/CBB.json", 'CBB')
    # TODO: MLB NOT SUPPORTED
    #gameInputFromJSON("../Scrapers/Data/DK/MLB.json", 'MLB')
    print("Recommended Bets: ")
    print(parlay)
    try:
        with open(direct + 'results.txt', 'a') as fp:
            fp.write("-----------------------------\nRecommended Bets:\n" + json.dumps(parlay))
    except Exception as e:
        print(f"Error writing to file: {e}")

    print("Locks: ")
    print(lockparlay)
    print("Date: ", d)
    try:
        with open(direct + 'results.txt', 'a') as fp:
            fp.write("\nLocks: " + '\n' + json.dumps(lockparlay) + '\n')
            fp.write("Date: " + str(d))
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == '__main__':
    main()

# Idea for new Algorithm:
# Pass 3 (or more) parameters through that you want to use to determine the algorithm
# For Example
# alg(Team, Location, Type, Stat)         alg(Magic, Home, Cover, 2.5)
# Calculates how well the Magic do at home against the spread
# Compares that value to the value of 2.5, returns how likely it is to hit