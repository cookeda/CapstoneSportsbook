# Algorithm for determining likelihood
# Should be updated to reflect per bet and compare if a bet is good or bad
# Should take into consideration home advantage, etc. down the line
# Pretty sure the math is right currently

# Determines general percentage on the basis of
# 60% Current, 30% Over The Last 10 Years, 10% All Time

import json

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
    'Trail Blazers': 'Portland',
    'Kings': 'Sacramento',
    'Spurs': 'San Antonio',
    'Raptors': 'Toronto',
    'Jazz': 'Utah',
    'Wizards': 'Washington'
}

def generalAlg(stat):
    type2 = ""
    if stat == "Cover":
        type2 = stat

    if stat == "Over":
        type2 = "OU"

    result_dict = {}
    with open("../data/" + stat.lower() + "/general/SortedCurrentSeason" + type2 + ".jl", 'r') as current:
        with open("../data/" + stat.lower() + "/general/SortedAllTime" + type2 + ".jl", 'r') as all:
            with open("../data/" + stat.lower() + "/general/Sorted10Year" + type2 + ".jl", 'r') as ten:
                for sixty, tenp, thirty in zip(current, all, ten):
                    team = (((str(thirty).split(':')[1]).split(',')[0]).rstrip('\"'))
                    sixtyPercent    = float(sixty[-13:-9])/100
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

# Generates best team for a specified stat (Away, Home)
def bestOdds(result_dict, stat, spec):
    bestChance = -99
    bestTeam = "Nobody"
    i = 1
    for team in result_dict:
        percent = float(result_dict[team])
        if percent > bestChance:
            bestChance = percent
            bestTeam = team
    #print("Best team at " + spec + " for the stat: " + stat + " is " + bestTeam + " at " + str(bestChance))

# Gets python dictionary from a file
def getDict(file):
    result_dict = {}
    with open(file, 'r') as fr:
        for line in fr:
            team = (((str(line).split(':')[1]).split(',')[0]).rstrip('\"'))
            percent = float(line[-13:-9])/100
            result_dict[team] = percent
        return result_dict

# Combines different dictionaries to create a new one
# Uses bestOdds to get best team on this combination
def combine(dict1, dict2, dec1, dec2, stat, spec):
    if((dec1 + dec2) == 1):
        final_dict = {}
        for team1, team2 in zip(dict1, dict2):
            fifty1 = dict1[team1]
            fifty2 = dict2[team2]
            perchance = (dec1 * fifty1) + (dec2 * fifty2)
            final_dict[team1] = perchance

        bestOdds(final_dict, stat, spec)
        #print(final_dict)

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

def gameInput(homeTeam, awayTeam):
    print("-----------------------------")
    homeTeam = (' "' + homeTeam)
    awayTeam = (' "' + awayTeam)


    # Rankings for team
    coverHome = cho[homeTeam]
    coverAway = cac[awayTeam]
    overHome = chc[homeTeam]
    overAway = cao[awayTeam]

    print("For " + awayTeam + " At " + homeTeam + ":")

    # Over
    if overHome <= 10 and overAway <= 10:
        if overHome <= 5 and overAway <= 5:
            print("LOCK ALERT!")
        print("Take the over!")
        parlay.append(awayTeam + " At " + homeTeam + ": Over")
    elif overHome > 20 and overAway > 20:
        if overHome > 25 and overAway > 25:
            print("LOCK ALERT!")
        print("Take the under!")
        parlay.append(awayTeam + " At " + homeTeam + ": Under")
    else:
        print("Don't bet on O/U")

    # Cover
    if coverHome <= 10 and coverAway > 20:
        if coverHome <= 5 and coverAway > 25:
            print("LOCK ALERT!")
        print("Bet on " + homeTeam + " to Cover!")
        parlay.append(homeTeam + ": Cover")
    elif coverHome > 20 and coverAway <= 10:
        if coverHome <= 5 and coverAway > 25:
            print("LOCK ALERT!")
        print("Bet on " + awayTeam + " to Cover!")
        parlay.append(awayTeam + ": Cover")
    else:
        print("Don't bet on Cover")

def gameInputFromJSON(file):
    with open(file, 'r') as j:
        games = json.load(j)
    for game in games:
        homeTeam = teamDict[game["Home Team"].title()]
        awayTeam = teamDict[game["Away Team"].title()]
        gameInput(homeTeam, awayTeam)

def main():
    global generalOver  # General Over Dict
    global generalCover # General Cover Dict
    global homeOver     # Home Over Dict
    global homeCover    # Home Cover Dict
    global awayOver     # Away Over Dict
    global awayCover    # Away Cover Dict
    global cho          # Combined Home Over
    global chc          # Combined Home Cover
    global cao          # Combined Away Over
    global cac          # Combined Away Cover
    global parlay       # Parlay List
    global teamDict     # Team Dictionary in form City: Team Name

    parlay = []
    #print("General (LEAST ACCURATE): ")
    generalCover = generalAlg("Cover")
    generalOver = generalAlg("Over")
    #bestOddsGeneral(generalCover, "Cover")
    #bestOddsGeneral(generalOver, "Over")

    # For Home
    #print("CURRENT HOME ODDS: ")
    homeCover = getDict("../data/cover/home/SortedhomeCover.jl")
    #bestOdds(homeCover, "Cover", "Home")
    homeOver = getDict("../data/over/home/SortedhomeOver.jl")
    #bestOdds(homeOver, "Over", "Home")

    # For Away
    #print("CURRENT AWAY ODDS: ")
    awayCover = getDict("../data/cover/away/SortedawayCover.jl")
    #bestOdds(awayCover, "Cover", "Away")
    awayOver = getDict("../data/over/away/SortedawayOver.jl")
    #bestOdds(awayOver, "Over", "Away")

    # testing new stuff
    #print("COMBINED (MOST ACCURATE): ")
    combine(generalCover, homeCover, .3, .7, "Cover", "Home")
    combine(generalOver, homeOver, .3, .7, "Over", "Home")
    combine(generalCover, awayCover, .3, .7, "Cover", "Away")
    combine(generalOver, awayOver, .3, .7, "Over", "Away")
    # Variables stand for Combine Home/Away Over/Cover (ex: Combine Home Over = cho)
    #print("Scores for home over: ")
    cho = combineOnRanking(sortByRank(generalOver), sortByRank(homeOver))
    #print("Scores for home cover: ")
    chc = combineOnRanking(sortByRank(generalCover), sortByRank(homeCover))
    #print("Scores for away over: ")
    cao = combineOnRanking(sortByRank(generalOver), sortByRank(awayOver))
    #print("Scores for away cover: ")
    cac = combineOnRanking(sortByRank(generalCover), sortByRank(awayCover))

    # test
    #gameInput('Milwaukee', "Charlotte")
    #gameInput('Washington', 'Golden State')
    #gameInput('Cleveland', 'Dallas')
    #gameInput('Orlando', 'Brooklyn')
    #gameInput('New York', 'New Orleans')
    #gameInput('Boston', 'Philadelphia')
    #gameInput('Atlanta', 'Utah')
    #gameInput('Minnesota', 'San Antonio')
    #gameInput('Chicago', 'Detroit')
    #gameInput('Okla City', 'Houston')
    #gameInput('Portland', 'Miami')

    gameInputFromJSON("../dk.json")

    print("Your Parlay: ")
    print(parlay)

    # TARGET ALG?
    # .5 Advanced Stats + .3 Spec Stats + .2 General Stats
if __name__ == '__main__':
    main()

# Idea for new Algorithm:
# Pass 3 (or more) parameters through that you want to use to determine the algorithm
# For Example
# alg(Team, Location, Type, Stat)         alg(Magic, Home, Cover, 2.5)
# Calculates how well the Magic do at home against the spread
# Compares that value to the value of 2.5, returns how likely it is to hit