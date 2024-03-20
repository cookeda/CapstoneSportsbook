# Algorithm for determining likelihood
# Should be updated to reflect per bet and compare if a bet is good or bad
# Should take into consideration home advantage, etc. down the line
# Pretty sure the math is right currently

# Determines general percentage on the basis of
# 60% Current, 30% Over The Last 10 Years, 10% All Time

import json
import re
import os

#global topTier
#global midTier
#global lowTier
#global ass


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
    with open("../data/" + league + "/" + stat.lower() + "/general/SortedCurrentSeason" + type2 + ".jl", 'r') as current:
        with open("../data/" + league + "/" + stat.lower() + "/general/SortedAllTime" + type2 + ".jl", 'r') as all:
            with open("../data/" + league + "/" + stat.lower() + "/general/Sorted10Year" + type2 + ".jl", 'r') as ten:
                for sixty, tenp, thirty in zip(current, all, ten):
                    team_search = re.search(r'"Team":\s*"([^"]+)"', thirty)
                    team = team_search.group(1).strip()
                    match = re.search(r"\b\d+\.\d+\b", sixty)
                    sixtyPercent = float(match.group())/100
                    thirtyPercent   = float(thirty[-13:-9])/100
                    tenPercent      = float(tenp[-13:-9])/100
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
def getDict(file):
    result_dict = {}
    with open(file, 'r') as fr:
        for line in fr:
            team_search = re.search(r'"Team":\s*"([^"]+)"', line)
            team = team_search.group(1) if team_search else "Unknown"

            percent_search = re.search(r"\b\d+\.\d+\b", line)
            percent = float(percent_search.group()) / 100 if percent_search else 0.0

            result_dict[team] = percent
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

def gameInput(homeTeam, awayTeam, league):
    try:
        with open('../data/ACCURACYresults.txt', 'a') as fp:
            fp.write("-----------------------------" + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")
    if awayTeam == "New" or homeTeam == "New":
        return
    if awayTeam == "Oklahoma":
        awayTeam = "Okla City"
    if homeTeam == "Oklahoma":
        homeTeam = "Okla City"

    numTeams = len(choNBA)
    coverHome = choNBA[homeTeam]
    coverAway = cacNBA[awayTeam]
    overHome = chcNBA[homeTeam]
    overAway = caoNBA[awayTeam]

    topTier = numTeams * 0.177  # Top 10% Change to 20
    midTier = numTeams * 0.322  # Top 30% Change to 30
    lowTier = numTeams * 0.688  # Starting point for Bottom 30% Change to 70
    ass = numTeams * 0.833  # Bottom 10% Change to 80
    try:
        with open('../data/ACCURACYresults.txt', 'a') as fp:
            fp.write("For " + awayTeam + " At " + homeTeam + ":" + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Over
    if overHome <= midTier and overAway <= midTier:
        if overHome <= topTier and overAway <= topTier:
            try:
                with open('../data/ACCURACYresults.txt', 'a') as fp:
                    fp.write("Lock ALERT!" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
            lockparlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Over")
            return "lockO"
        try:
            with open('../data/ACCURACYresults.txt', 'a') as fp:
                fp.write("Take the over!" + '\n' + "Home Rank :" + str(overHome) + '\n' +"Away Rank: " + str(overAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        parlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Over")
        return "RecO"

    elif overHome > lowTier and overAway > lowTier:
        if overHome > ass and overAway > ass:
            try:
                with open('../data/ACCURACYresults.txt', 'a') as fp:
                    fp.write("Lock ALERT!" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
            lockparlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Under")
            return "lockU"
        try:
            with open('../data/ACCURACYresults.txt', 'a') as fp:
                fp.write("Take the under!" + '\n' + "Home Rank :" + str(overHome) + '\n' +"Away Rank: " + str(overAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        parlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Under")
        return "recU"

    else:
        try:
            with open('../data/ACCURACYresults.txt', 'a') as fp:
                fp.write("Don't bet on O/U" + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")

    # Cover
    if coverHome <= midTier and coverAway > lowTier:
        if coverHome <= topTier and coverAway > ass:
            try:
                with open('../data/ACCURACYresults.txt', 'a') as fp:
                    fp.write("LOCK ALERT!" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
            lockparlay.append(league + ": " + homeTeam + ": Cover")
            return "lockHC"
        try:
            with open('../data/ACCURACYresults.txt', 'a') as fp:
                fp.write("Bet on " + homeTeam + " to Cover!" + '\n' + "Home Rank :" + str(overHome) + '\n' +"Away Rank: " + str(overAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        parlay.append(league + ": " + homeTeam + ": Cover")
        return "recHC"
    elif coverHome > lowTier and coverAway <= midTier:
        if coverHome > ass and coverAway <= topTier:
            try:
                with open('../data/ACCURACYresults.txt', 'a') as fp:
                    fp.write("LOCK ALERT!" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
            lockparlay.append(league + ": " + awayTeam + ": Cover")
            return "lockAC"
        try:
            with open('../data/ACCURACYresults.txt', 'a') as fp:
                fp.write("Bet on " + awayTeam + " to Cover!" + '\n' + "Home Rank :" + str(overHome) + '\n' +"Away Rank: " + str(overAway) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        parlay.append(league + ": " + awayTeam + ": Cover")
        return "recAC"
    else:
        try:
            with open('../data/ACCURACYresults.txt', 'a') as fp:
                fp.write("We do not recommend, but you do you" + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
        if coverHome > coverAway:
            try:
                with open('../data/ACCURACYresults.txt', 'a') as fp:
                    fp.write("Bet on " + homeTeam + " to Cover!" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
        elif coverAway > coverHome:
            try:
                with open('../data/ACCURACYresults.txt', 'a') as fp:
                    fp.write("Bet on " + awayTeam + " to Cover!" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
        else:
            try:
                with open('../data/ACCURACYresults.txt', 'a') as fp:
                    fp.write("EVEN ODDS DON'T BET" + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
        return 0


def gameInputFromJSON(file, league):
    recNumerator = 0
    recDenomiator = 0
    lockNumerator = 0
    lockDenominator = 0
    missCounter = 0
    with open(file, 'r') as j:
        games = json.load(j)
    for game in games:
        homeTeam = game["Home Team"]
        homeSpread = game['Home Spread']
        homeScore = game['Home Score']
        awayTeam = game["Away Team"]
        awaySpread = game['Away Spread']
        awayScore = game['Away Score']
        ouResult = game["OU Result"]

        typeOfBet = gameInput(homeTeam, awayTeam, league)
        itHit = didItHit(homeSpread, homeScore, awaySpread, awayScore, ouResult, typeOfBet)

        if typeOfBet == "recHC" or "recAC" or "recO" or "recU":
            if itHit is True:
                recNumerator += 1
                recDenomiator += 1
            else:
                recDenomiator += 1
        elif typeOfBet == "lockHC" or "lockAC" or "lockO" or "lockU":
            if itHit is True:
                lockNumerator += 1
                lockDenominator += 1
            else:
                lockDenominator += 1
        elif typeOfBet == 0:
            missCounter += 1

        else:
            print("ERROR: GAME INPUT RETURNED SOMETHING UNEXPECTED: " + str(typeOfBet))

    print("Recommended Bets %: " + str(recNumerator/recDenomiator))
    with open('../data/ACCURACYresults.txt', 'a') as fp:
        fp.write("Recommended Bets %: " + str(recNumerator/recDenomiator) + '\n')
    print("Lock Bets %: " + str(lockNumerator / lockDenominator))
    with open('../data/ACCURACYresults.txt', 'a') as fp:
        fp.write("Lock Bets %: " + str(lockNumerator / lockDenominator) + '\n')
    print("Amount of games passed on: " + str(missCounter))
    with open('../data/ACCURACYresults.txt', 'a') as fp:
        fp.write("Amount of games passed on: " + str(missCounter) + '\n')


def didItHit(homeSpread, homeScore, awaySpread, awayScore, ouResult, typeOfBet):
    if (typeOfBet == "lockO" or "recO") and (ouResult == "O"):
        return True

    elif (typeOfBet == "lockU" or "recU") and (ouResult == "U"):
        return True

    elif (typeOfBet == "lockHC" or "recHC") and ((homeScore + homeSpread) > awayScore):
        return True

    elif (typeOfBet == "lockAC" or "recAC") and ((awayScore + awaySpread) > homeScore):
        return True

    else:
        return False


def cleanfile(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        open(file, 'a')

def main():
    global generalOver  # General Over Dict
    global generalCover # General Cover Dict
    global homeOver     # Home Over Dict
    global homeCover    # Home Cover Dict
    global awayOver     # Away Over Dict
    global awayCover    # Away Cover Dict
    global choNBA          # Combined Home Over
    global chcNBA          # Combined Home Cover
    global caoNBA          # Combined Away Over
    global cacNBA          # Combined Away Cover

    global parlay       # Parlay List
    global lockparlay
    global teamDict     # Team Dictionary in form City: Team Name

    parlay = []
    lockparlay = []
    generalCover = generalAlg("Cover", "NBA")
    generalOver = generalAlg("Over", "NBA")

    # For Home
    homeCover = getDict("../data/NBA/cover/home/SortedhomeCover.jl")
    homeOver = getDict("../data/NBA/over/home/SortedhomeOver.jl")

    # For Away
    awayCover = getDict("../data/NBA/cover/away/SortedawayCover.jl")
    awayOver = getDict("../data/NBA/over/away/SortedawayOver.jl")

    # Variables stand for Combine Home/Away Over/Cover (ex: Combine Home Over = cho)
    choNBA = combineOnRanking(sortByRank(generalOver), sortByRank(homeOver))
    chcNBA = combineOnRanking(sortByRank(generalCover), sortByRank(homeCover))
    caoNBA = combineOnRanking(sortByRank(generalOver), sortByRank(awayOver))
    cacNBA = combineOnRanking(sortByRank(generalCover), sortByRank(awayCover))

    # Run Manually
    #gameInput(home, away, league)

    gameInputFromJSON("../OddsHistory/nba.json", 'NBA')
    try:
        with open('../data/ACCURACYresults.txt', 'a') as fp:
            fp.write("-----------------------------\nRecommended Bets:\n" + json.dumps(parlay))
    except Exception as e:
        print(f"Error writing to file: {e}")

    try:
        with open('../data/ACCURACYresults.txt', 'a') as fp:
            fp.write("\nLocks: " + '\n' + json.dumps(lockparlay) + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == '__main__':
    main()