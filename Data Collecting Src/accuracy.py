# Algorithm for determining likelihood
# Should be updated to reflect per bet and compare if a bet is good or bad
# Should take into consideration home advantage, etc. down the line
# Pretty sure the math is right currently

# Determines general percentage on the basis of
# 60% Current, 30% Over The Last 10 Years, 10% All Time

import json
import re
import os


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
                    sixtyPercent = float(match.group()) / 100
                    match = re.search(r"\b\d+\.\d+\b", thirty)
                    thirtyPercent = float(match.group()) / 100
                    match = re.search(r"\b\d+\.\d+\b", tenp)
                    tenPercent = float(match.group()) / 100
                    # Changes Accuracy
                    perChance = (.7 * sixtyPercent) + \
                                (.2 * thirtyPercent) + \
                                (.1 * tenPercent)

                    result_dict[team] = perChance
                return result_dict

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
            # Changes Accuracy
            first = dict1[team1] * .7
            second = dict2[team1] * .3
            both = first + second
            #both = (dict1[team1] + dict2[team1])/2
            return_dict[team1] = both
    #print(return_dict)
    sorted_dict = sorted(return_dict.items(), key=lambda item: item[1], reverse=False)
    #print(sorted_dict)
    return dict(sorted_dict)

def sortByRank(input_dict):
    sorted_dict = sorted(input_dict.items(), key=lambda item: item[1], reverse=True)
    ranked_dict = {team: rank for rank, (team, percent) in enumerate(sorted_dict, start=1)}
    return ranked_dict

def gameInput(homeTeam, homeSpread, awayTeam, awaySpread, league, low, mid):
    # only used for special total
    with open("../OddsHistory/nba.json", 'r') as j:
        games = json.load(j)
    for game in games:
        homeScore = game['Home Score']
        awayScore = game['Away Score']

    try:
        with open('../data/ACCURACYresults.txt', 'a') as fp:
            fp.write("-----------------------------" + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")
    if awayTeam == "New" or homeTeam == "New" or awayTeam == "Los" or homeTeam == "Los":
        return "N", "N"
    if awayTeam == "Oklahoma":
        awayTeam = "Okla City"
    elif homeTeam == "Oklahoma":
        homeTeam = "Okla City"
    if awayTeam == "San":
        awayTeam = "San Antonio"
    elif homeTeam == "San":
        homeTeam = "San Antonio"
    if awayTeam == "Golden":
        awayTeam = "Golden State"
    elif homeTeam == "Golden":
        homeTeam = "Golden State"

    numTeams = len(choNBA)
    coverHome = choNBA[homeTeam]
    coverAway = cacNBA[awayTeam]
    overHome = chcNBA[homeTeam]
    overAway = caoNBA[awayTeam]
    movHome = homeMOV[homeTeam]
    movAway = awayMOV[awayTeam]
    ppg = ppgNBA

    # Changes Accuracy
    midTier = numTeams * mid  # Top 32.2% | GPT SAID .3
    lowTier = numTeams * low  # Bottom 70% | GPT SAID .7

    #ncres = normalCover(league, homeTeam, coverHome, awayTeam, coverAway, lowTier, midTier)
    ncres = ".55"
    #movres = basedOnSpreadMov(league, homeTeam, awayTeam, movHome, movAway, homeSpread, awaySpread, coverHome, coverAway)
    movres = ".54"
    if (ncres == "recHC") or (movres == "recHC"):
        coverResult = "recHC"
    elif (ncres == "recAC") or (movres == "recAC"):
        coverResult = "recAC"
    else:
        coverResult = "N"

    #nores = normalOver(league, homeTeam, overHome, awayTeam, overAway, lowTier, midTier)
    nores = "58.2"
    total = homeScore + awayScore
    #ppgres = basedOnPGG(league, homeTeam, awayTeam, ppg, total)
    ppgres = "50.8"
    if (nores == "recO") or (ppgres == "recO"):
        overResult = "recO"
    elif (nores == "recU") or (ppgres == "recU"):
        overResult = "recU"
    else:
        overResult = "N"
    return coverResult, overResult
def normalCover(league, homeTeam, coverHome, awayTeam, coverAway, lowTier, midTier):
    if (coverHome <= midTier and coverAway > lowTier):
        parlay.append(league + ": " + homeTeam + ": Cover")
        return "recHC"

    elif coverHome > lowTier and coverAway <= midTier:
        parlay.append(league + ": " + awayTeam + ": Cover")
        return "recAC"
    return "N"

def normalOver(league, homeTeam, overHome, awayTeam, overAway, lowTier, midTier):
    if overHome <= midTier and overAway <= midTier:
        parlay.append(league + ": " + awayTeam + " At " + homeTeam + ": Over")
        return "recO"

    elif overHome > lowTier and overAway > lowTier:
        parlay.append(league + ": " + awayTeam + " At " + homeTeam + ": Under")
        return "recU"
    return "N"

def basedOnSpreadMov(league, homeTeam, awayTeam, movHome, movAway, homeSpread, awaySpread, coverHome, coverAway):
    # Home Bet
    if ((float(movHome) + float(homeSpread)) > 0) and (coverHome < coverAway):
        parlay.append(league + ": " + homeTeam + ": Cover")
        return "recHC"

    # Away Bet
    if ((float(movAway) + float(awaySpread)) > 0) and (coverAway < coverHome):
        parlay.append(league + ": " + awayTeam + ": Cover")
        return "recAC"
    return "N"


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

    if (myAverageHome + myAverageAway - 20) > float(total):
        parlay.append(league + ": " + awayTeam + " At " + homeTeam + ": Over")
        return "recO"

    elif (myAverageHome + myAverageAway + 10) < float(total):
        return "recU"
    else:
        return "N"
def gameInputFromJSON(file, league, low, mid):
    recNumerator = 0
    recDenomiator = 0
    missCounter = 0
    recCounter = 0
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

        if homeSpread == "Pick)" or homeSpread == "-Pick)":
            homeSpread = "0"

        if awaySpread == "Pick)" or awaySpread == "-Pick)":
            awaySpread = "0"

        typeOfBet = gameInput(homeTeam, homeSpread, awayTeam, awaySpread, league, low, mid)
        coverResult, overResult = typeOfBet

        itHit = didItHit(homeSpread, homeScore, awaySpread, awayScore, ouResult, coverResult)
        if coverResult == "recHC" or coverResult == "recAC":
            if itHit is True:
                recNumerator += 1
                recDenomiator += 1
                recCounter += 1
            else:
                recDenomiator += 1
        elif coverResult == "N":
            missCounter += 1

        #else:
            #print("ERROR: GAME INPUT RETURNED SOMETHING UNEXPECTED: " + str(coverResult))

        itHit = didItHit(homeSpread, homeScore, awaySpread, awayScore, ouResult, overResult)
        if overResult == "recO" or overResult == "recU":
            if itHit is True:
                recNumerator += 1
                recDenomiator += 1
                recCounter += 1
            else:
                recDenomiator += 1
        elif overResult == "N":
            missCounter += 1
        #else:
            #print("ERROR: GAME INPUT RETURNED SOMETHING UNEXPECTED: " + str(overResult))

    if recDenomiator != 0:
        print("Recommended Bets %: " + str(recNumerator/recDenomiator) + " (" + str(recCounter) + " Games)")
        with open('../data/ACCURACYresults.txt', 'a') as fp:
            fp.write("Recommended Bets %: " + str(recNumerator/recDenomiator) + '\n')
            return recNumerator/recDenomiator
    print("Amount of games passed on: " + str(missCounter) + " Games")
    with open('../data/ACCURACYresults.txt', 'a') as fp:
        fp.write("Amount of games passed on: " + str(missCounter) + " Games" + '\n')


def didItHit(homeSpread, homeScore, awaySpread, awayScore, ouResult, typeOfBet):
    if (typeOfBet == "recO") and (ouResult == "O"):
        return True

    elif (typeOfBet == "recU") and (ouResult == "U"):
        return True

    elif (typeOfBet == "recHC") and ((homeScore + homeSpread) > awayScore):
        return True

    elif (typeOfBet == "recAC") and ((awayScore + awaySpread) > homeScore):
        return True

    else:
        return False

def cleanfile(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        open(file, 'a')

def main():
    global generalOver      # General Over Dict
    global generalCover     # General Cover Dict
    global homeOver         # Home Over Dict
    global homeCover        # Home Cover Dict
    global homeMOV          # Home Margin of Victory
    global awayOver         # Away Over Dict
    global awayCover        # Away Cover Dict
    global awayMOV          # Away Margin of Victory
    global ppgNBA           # PPG NBA STATS
    global choNBA          # Combined Home Over
    global chcNBA          # Combined Home Cover
    global caoNBA          # Combined Away Over
    global cacNBA          # Combined Away Cover

    global parlay       # Parlay List
    global teamDict     # Team Dictionary in form City: Team Name

    parlay = []
    generalCover = generalAlg("Cover", "NBA")
    generalOver = generalAlg("Over", "NBA")
    ppgNBA = getListPPG("../data/NBA/over/general/SortedPointAverages.jl")

    # For Home
    homeCover = getDictPercent("../data/NBA/cover/home/SortedhomeCover.jl")
    homeMOV = getDictMOV("../data/NBA/cover/home/SortedhomeCover.jl")
    homeOver = getDictPercent("../data/NBA/over/home/SortedhomeOver.jl")

    # For Away
    awayCover = getDictPercent("../data/NBA/cover/away/SortedawayCover.jl")
    awayMOV = getDictMOV("../data/NBA/cover/away/SortedawayCover.jl")
    awayOver = getDictPercent("../data/NBA/over/away/SortedawayOver.jl")

    # Variables stand for Combine Home/Away Over/Cover (ex: Combine Home Over = cho)
    choNBA = combineOnRanking(sortByRank(generalOver), sortByRank(homeOver))
    chcNBA = combineOnRanking(sortByRank(generalCover), sortByRank(homeCover))
    caoNBA = combineOnRanking(sortByRank(generalOver), sortByRank(awayOver))
    cacNBA = combineOnRanking(sortByRank(generalCover), sortByRank(awayCover))

    # Run Manually
    #gameInput(home, away, league)

    bestLow = 0  # .75
    bestMid = 0  # .35
    best = 0
    low = .9
    while low > 0:
        mid = .9
        while mid > .25:
            acc = gameInputFromJSON("../OddsHistory/nba.json", 'NBA', low, mid)
            print("Percent " + str(acc) + " Mid: " + str(mid) + " Low: " + str(low))
            if acc > best:
                best = acc
                bestMid = mid
                bestLow = low
            mid -= 0.05
        low -= 0.05
    print("Percent " + str(best) + " Mid: " + str(bestMid) + " Low: " + str(bestLow))
    try:
        with open('../data/ACCURACYresults.txt', 'a') as fp:
            fp.write("-----------------------------\nRecommended Bets:\n" + json.dumps(parlay))
    except Exception as e:
        print(f"Error writing to file: {e}")


if __name__ == '__main__':
    main()