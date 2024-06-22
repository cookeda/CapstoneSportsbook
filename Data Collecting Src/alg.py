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
from collections import Counter

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

def getListPPG(file):
    result_list = []
    with open(file, 'r') as fr:
        for line in fr:
            result_list.append(line.strip())
    return result_list

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

def gameInput(homeTeam, homeSpread, awayTeam, awaySpread, total, league):
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
        ppg = ppgNBA


    elif league == 'CBB':
        numTeams = len(choCBB)
        coverHome = choCBB[homeTeam]
        coverAway = cacCBB[awayTeam]
        overHome = chcCBB[homeTeam]
        overAway = caoCBB[awayTeam]
        movHome = homeMOV2[homeTeam]
        movAway = awayMOV2[awayTeam]
        ppg = ppgCBB

    elif league == 'MLB':
        numTeams = len(choMLB)
        coverHome = choMLB[homeTeam]
        coverAway = cacMLB[awayTeam]
        overHome = chcMLB[homeTeam]
        overAway = caoMLB[awayTeam]
        movHome = homeMOV3[homeTeam]
        movAway = awayMOV3[awayTeam]
        ppg = ppgMLB

    oumidTier = numTeams * .35 # Top 30% Change to 30
    oulowTier = numTeams * .75  # Starting point for Bottom 30% Change to 70

    covermidTier = numTeams * .7
    coverlowTier = numTeams * .85

    print("For " + awayTeam + " At " + homeTeam + ":")
    try:
        with open(direct + 'results.txt', 'a') as fp:
            fp.write("For " + awayTeam + " At " + homeTeam + ":" + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

    print("*      TOTALS:      *")
    try:
        with open(direct + 'results.txt', 'a') as fp:
            fp.write("*      TOTALS:      *\n")
    except Exception as e:
        print(f"Error writing to file: {e}")
    overunder(league, homeTeam, overHome, awayTeam, overAway, oulowTier, oumidTier)
    basedOnPGG(league, homeTeam, awayTeam, ppg, total)
    print("*      COVER:      *")
    try:
        with open(direct + 'results.txt', 'a') as fp:
            fp.write("*      COVER:      *\n")
    except Exception as e:
        print(f"Error writing to file: {e}")
    coverNormal(league, homeTeam, coverHome, awayTeam, coverAway, coverlowTier, covermidTier)
    basedOnSpreadMov(league, homeTeam, awayTeam, movHome, movAway, homeSpread, awaySpread, coverHome, coverAway)


def gameInputFromJSON(file, league):
    with open(file, 'r') as j:
        games = json.load(j)
    for game in games:
        homeTeam = game["Home Team Rank Name"]
        awayTeam = game["Away Team Rank Name"]
        homeSpread = game['DK Home Odds']['Spread']
        awaySpread = game['DK Away Odds']['Spread']
        total = game['Game']['Total']
        if homeSpread == "Pick)" or homeSpread == "-Pick)":
            homeSpread = "0"

        if awaySpread == "Pick" or awaySpread == "-Pick":
            awaySpread = "0"
        gameInput(homeTeam, homeSpread, awayTeam, awaySpread, total, league)

def gameInputFromLite(file, league):
    with open(file, 'r') as j:
        games = json.load(j)
    
    # Processing each game using its Matchup ID as the key
    for matchup_id, game_info in games.items():
        homeTeam = game_info["Home Team"]
        awayTeam = game_info["Away Team"]
        homeSpread = game_info["Home Spread"]
        awaySpread = game_info["Away Spread"]
        total = game_info["Total Points"]

        # Adjusting for 
        gameInput(homeTeam, homeSpread, awayTeam, awaySpread, total, league)


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
    global ppgNBA       # PPG stats
    global ppgCBB
    global ppgMLB
    global parlay       # Parlay List
    global teamDict     # Team Dictionary in form City: Team Name
    global direct
    # Connor
    direct = "../data/"
    # Devin
    #direct = "data/"

    cleanfile(direct + "results.txt")
    parlay = []
    d = dt.today()
    generalCover = generalAlg("Cover", "NBA")
    generalOver = generalAlg("Over", "NBA")
    generalCover2 = generalAlg("Cover", "CBB")
    generalOver2 = generalAlg("Over", "CBB")
    generalCover3 = generalAlg("Cover", "MLB")
    generalOver3 = generalAlg("Over", "MLB")

    # For Home
    #homeCover = getDictPercent(direct + "NBA/cover/home/SortedhomeCover.jl")
    #homeCover2 = getDictPercent(direct + "CBB/cover/home/SortedhomeCover.jl")
    homeCover3 = getDictPercent(direct + "MLB/cover/home/SortedhomeCover.jl")

    #homeOver = getDictPercent(direct + "NBA/over/home/SortedhomeOver.jl")
    #homeOver2 = getDictPercent(direct + "CBB/over/home/SortedhomeOver.jl")
    homeOver3 = getDictPercent(direct + "MLB/over/home/SortedhomeOver.jl")

    #homeMOV = getDictMOV("../data/NBA/cover/home/SortedhomeCover.jl")
    #homeMOV2 = getDictMOV("../data/CBB/cover/home/SortedhomeCover.jl")
    homeMOV3 = getDictMOV("../data/MLB/cover/home/SortedhomeCover.jl")

    # For Away
    #awayCover = getDictPercent(direct + "NBA/cover/away/SortedawayCover.jl")
    #awayCover2 = getDictPercent(direct + "CBB/cover/away/SortedawayCover.jl")
    awayCover3 = getDictPercent(direct + "MLB/cover/away/SortedawayCover.jl")

    #awayOver = getDictPercent(direct + "NBA/over/away/SortedawayOver.jl")
    #awayOver2 = getDictPercent(direct + "CBB/over/away/SortedawayOver.jl")
    awayOver3 = getDictPercent(direct + "MLB/over/away/SortedawayOver.jl")

    #awayMOV = getDictMOV("../data/NBA/cover/away/SortedawayCover.jl")
    #awayMOV2 = getDictMOV("../data/CBB/cover/away/SortedawayCover.jl")
    awayMOV3 = getDictMOV("../data/MLB/cover/away/SortedawayCover.jl")

    #ppgNBA = getListPPG("../data/NBA/over/general/SortedPointAverages.jl")
    #ppgCBB = getListPPG("../data/CBB/over/general/SortedPointAverages.jl")
    ppgMLB = getListPPG("../data/MLB/over/general/SortedPointAverages.jl")

    # Variables stand for Combine Home/Away Over/Cover (ex: Combine Home Over = cho)
    #choNBA = combineOnRanking(sortByRank(generalOver), sortByRank(homeOver))
    #choCBB = combineOnRanking(sortByRank(generalOver2), sortByRank(homeOver2))
    choMLB = combineOnRanking(sortByRank(generalOver3), sortByRank(homeOver3))

    #chcNBA = combineOnRanking(sortByRank(generalCover), sortByRank(homeCover))
    #chcCBB = combineOnRanking(sortByRank(generalCover2), sortByRank(homeCover2))
    chcMLB = combineOnRanking(sortByRank(generalCover3), sortByRank(homeCover3))

    #caoNBA = combineOnRanking(sortByRank(generalOver), sortByRank(awayOver))
    #caoCBB = combineOnRanking(sortByRank(generalOver2), sortByRank(awayOver2))
    caoMLB = combineOnRanking(sortByRank(generalOver3), sortByRank(awayOver3))

    #cacNBA = combineOnRanking(sortByRank(generalCover), sortByRank(awayCover))
    #cacCBB = combineOnRanking(sortByRank(generalCover2), sortByRank(awayCover2))
    cacMLB = combineOnRanking(sortByRank(generalCover3), sortByRank(awayCover3))


    # Run Manually
    #gameInput(home, away, league)

    #gameInputFromJSON("../Scrapers/Data/DK/NBA.json", 'NBA')
    #gameInputFromJSON("../Scrapers/Data/DK/CBB.json", 'CBB')
    #gameInputFromJSON("../Scrapers/Data/DK/MLB.json", 'MLB')

    #gameInputFromLite("../Scrapers/Data/DK/MLB_Lite.json", 'MLB')
    #gameInputFromLite("../Scrapers/Data/DK/CBB_Lite.json", 'CBB')
    #gameInputFromLite("../Scrapers/Data/DK/NBA_Lite.json", 'NBA')

    duplicateCount = Counter(parlay)
    lockList = []
    processed_items = set()

    # Iterate through the list backwards to avoid index issues when removing items
    for item in parlay[:]:  # Make a shallow copy of the list for safe iteration
        if duplicateCount[item] > 1 and item not in processed_items:
            # Keep only one instance in 'parlay' and move the rest to 'lockList'
            while parlay.count(item) > 1:
                parlay.remove(item)
                lockList.append(item)
            processed_items.add(item)  # Mark as processed

    print("-----------------------------")
    print("Total Bet Count: " + str(len(parlay)))
    print("Silver Bets")
    print(parlay)

    print("Gold Bets")
    print("Gold Count: " + str(len(lockList)))
    print(lockList)
    try:
        with open(direct + 'results.txt', 'a') as fp:
            fp.write("Total Bet Count: " + str(len(parlay)) + "\n")
            fp.write("-----------------------------\nSilver Bets:\n" + json.dumps(parlay))
            fp.write("-----------------------------\nGold Bets:\n" + json.dumps(lockList))
    except Exception as e:
        print(f"Error writing to file: {e}")
    print("Date: ", d)


def coverNormal(league, homeTeam, coverHome, awayTeam, coverAway, lowTier, midTier):
    # Cover | Returns false when sucessful to tell gameInput to go to MOV/Spread data
    if coverHome <= midTier and coverAway > lowTier:
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
        return False
    elif coverHome > lowTier and coverAway <= midTier:
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
        return False
    else:
        print("Don't Bet On Spread")
        return True


def overunder(league, homeTeam, overHome, awayTeam, overAway, lowTier, midTier):
    # Over
    if overHome <= midTier and overAway <= midTier:
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Take the over!" + '\n' + "Home Rank :" + str(overHome) + '\n' + "Away Rank: " + str(
                    overAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        print("Take the over!")
        print("Home Rank :" + str(overHome))
        print("Away Rank: " + str(overAway))
        parlay.append(league + ": " + awayTeam + " At " + homeTeam + ": Over")
        return False

    elif overHome > lowTier and overAway > lowTier:
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Take the under!" + '\n' + "Home Rank :" + str(overHome) + '\n' + "Away Rank: " + str(
                    overAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        print("Take the under!")
        print("Home Rank :" + str(overHome))
        print("Away Rank: " + str(overAway))
        parlay.append(league + ": " + awayTeam + " At " + homeTeam + ": Under")
        return False

    else:
        print("Don't bet on O/U")
        print("Home Rank :" + str(overHome))
        print("Away Rank: " + str(overAway))
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Don't bet on O/U" + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        return True


def basedOnSpreadMov(league, homeTeam, awayTeam, movHome, movAway, homeSpread, awaySpread, coverHome, coverAway):
    # Home Bet
    print("HOME: " + "MOV: " + str(movHome) + " Spread: " + str(homeSpread))
    print("AWAY: " + "MOV: " + str(movAway) + " Spread: " + str(awaySpread))
    if ((float(movHome) + float(homeSpread)) > 0) and (coverHome < coverAway):
        print("Bet on " + homeTeam + " to Cover!")
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Bet on " + homeTeam + " to Cover! \n")
                fp.write("HOME: " + "MOV: " + str(movHome) + " Spread: " + str(homeSpread) + "\n" + "AWAY: " +
                         "MOV: " + str(movAway) + " Spread: " + str(awaySpread) + "\n")
        except Exception as e:
            print(f"Error writing to file: {e}")
        parlay.append(league + ": " + homeTeam + ": Cover")
        return True
    # Away Bet
    if ((float(movAway) + float(awaySpread)) > 0) and (coverAway < coverHome):
        print("Bet on " + awayTeam + " to Cover!")
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Bet on " + awayTeam + " to Cover!")
        except Exception as e:
            print(f"Error writing to file: {e}")
        parlay.append(league + ": " + awayTeam + ": Cover")
        return True
    return False

def basedOnPGG(league, homeTeam, awayTeam, ppg, total):
    for team in ppg:
        tdict = json.loads(team)
        if tdict["Team"] == homeTeam:
            homeTotalAVG = float(tdict["PPG"]) * .25
            homeL3 = float(tdict["Last 3"]) * .25
            homeAVG = float(tdict["Home"]) * .5
            myAverageHome = homeTotalAVG + homeL3 + homeAVG

        if tdict["Team"] == awayTeam:
            awayTotalAVG = float(tdict["PPG"]) * .25
            awayL3 = float(tdict["Last 3"]) * .25
            awayAVG = float(tdict["Away"]) * .5
            myAverageAway = awayTotalAVG + awayL3 + awayAVG

    if ((myAverageHome + myAverageAway) - 10) > float(total):
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Take the over!\n" + "Book Total: " + str(total) + " Our Projected Total: " +
                         str(myAverageHome + myAverageAway) + '\n' + "Home Average: " +
                         str(myAverageHome) + '\n' + "Away Average: " + str(myAverageAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        print("Take the over!")
        print("Book Total: " + str(total) + " Our Projected Total: " + str(myAverageHome + myAverageAway))
        print("Home Average: " + str(myAverageHome))
        print("Away Average: " + str(myAverageAway))
        parlay.append(league + ": " + awayTeam + " At " + homeTeam + ": Over")

    elif((myAverageHome + myAverageAway + 10) <= float(total)):
        try:
            with open(direct + 'results.txt', 'a') as fp:
                fp.write("Take the under!" + "Book Total: " + str(total) + " Our Projected Total: " +
                         str(myAverageHome + myAverageAway) + '\n' + "Home Average: " +
                         str(myAverageHome) + '\n' + "Away Average: " + str(myAverageAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        print("Take the under!")
        print("Book Total: " + str(total) + " Our Projected Total: " + str(myAverageHome + myAverageAway))
        print("Home Average: " + str(myAverageHome))
        print("Away Average: " + str(myAverageAway))
        parlay.append(league + ": " + awayTeam + " At " + homeTeam + ": Under")
    else:
        print("Don't Take OU")


if __name__ == '__main__':
    main()