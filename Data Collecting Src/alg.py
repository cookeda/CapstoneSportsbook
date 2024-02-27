# Algorithm for determining likelihood
# Should be updated to reflect per bet and compare if a bet is good or bad
# Should take into consideration home advantage, etc. down the line
# Pretty sure the math is right currently

# Determines general percentage on the basis of
# 60% Current, 30% Over The Last 10 Years, 10% All Time



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
                    sixtyPercent    = float(sixty[-8:-4])/100
                    thirtyPercent   = float(thirty[-8:-4])/100
                    tenPercent      = float(tenp[-8:-4])/100
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
    print("Best team at " + spec + " for the stat: " + stat + " is " + bestTeam + " at " + str(bestChance))

# Gets python dictionary from a file
def getDict(file):
    result_dict = {}
    with open(file, 'r') as fr:
        for line in fr:
            team = (((str(line).split(':')[1]).split(',')[0]).rstrip('\"'))
            percent = float(line[-8:-4])/100
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
    print(sorted_dict)
    return dict(sorted_dict)

def sortByRank(input_dict):
    sorted_dict = sorted(input_dict.items(), key=lambda item: item[1], reverse=True)
    ranked_dict = {team: rank for rank, (team, percent) in enumerate(sorted_dict, start=1)}
    return ranked_dict

def gameInput(homeTeam, awayTeam):
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
        print("Take the over!")
    elif overHome > 20 and overAway > 20:
        print("Take the under!")
    else:
        print("Don't bet on O/U")

    # Cover
    if coverHome <= 10 and coverAway> 20:
        print("Bet on" + homeTeam + "to Cover!")
    if coverHome > 20 and coverAway <= 10:
        print("Bet on" + awayTeam + "to Cover!")
    else:
        print("Don't bet on Cover")


def main():
    # Very basic prediction calculating on account for
    # current season, last 10 years, and all time
    global generalOver
    global generalCover
    global homeOver
    global homeCover
    global awayOver
    global awayCover
    global cho
    global chc
    global cao
    global cac

    print("General (LEAST ACCURATE): ")
    generalCover = generalAlg("Cover")
    generalOver = generalAlg("Over")
    bestOddsGeneral(generalCover, "Cover")
    bestOddsGeneral(generalOver, "Over")

    # For Home
    print("CURRENT HOME ODDS: ")
    homeCover = getDict("../data/cover/home/SortedhomeCover.jl")
    bestOdds(homeCover, "Cover", "Home")
    homeOver = getDict("../data/over/home/SortedhomeOver.jl")
    bestOdds(homeOver, "Over", "Home")

    # For Away
    print("CURRENT AWAY ODDS: ")
    awayCover = getDict("../data/cover/away/SortedawayCover.jl")
    bestOdds(awayCover, "Cover", "Away")
    awayOver = getDict("../data/over/away/SortedawayOver.jl")
    bestOdds(awayOver, "Over", "Away")

    # testing new stuff
    print("COMBINED (MOST ACCURATE): ")
    combine(generalCover, homeCover, .3, .7, "Cover", "Home")
    combine(generalOver, homeOver, .3, .7, "Over", "Home")
    combine(generalCover, awayCover, .3, .7, "Cover", "Away")
    combine(generalOver, awayOver, .3, .7, "Over", "Away")
    # TODO: THIS DOES NOT SEEM TO BE WORKING
    print("Scores for home over: ")
    cho = combineOnRanking(sortByRank(generalOver), sortByRank(homeOver))
    print("Scores for home cover: ")
    chc = combineOnRanking(sortByRank(generalCover), sortByRank(homeCover))
    print("Scores for away over: ")
    cao = combineOnRanking(sortByRank(generalOver), sortByRank(awayOver))
    print("Scores for away cover: ")
    cac = combineOnRanking(sortByRank(generalCover), sortByRank(awayCover))

    # test
    gameInput('Indiana', "Toronto")
    gameInput('New York', 'Detroit')
    gameInput('Memphis', 'Brooklyn')
    gameInput('Sacramento', 'Miami')
    # Maybe add a "Here is your parlay" output
    
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