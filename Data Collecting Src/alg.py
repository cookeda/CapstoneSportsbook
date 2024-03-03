# Algorithm for determining likelihood
# Should be updated to reflect per bet and compare if a bet is good or bad
# Should take into consideration home advantage, etc. down the line
# Pretty sure the math is right currently

# Determines general percentage on the basis of
# 60% Current, 30% Over The Last 10 Years, 10% All Time

import json
import re

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
            team_search = re.search(r'"Team":\s*"([^"]+)"', line)
            team = team_search.group(1) if team_search else "Unknown"

            percent_search = re.search(r"\b\d+\.\d+\b", line)
            percent = float(percent_search.group()) / 100 if percent_search else 0.0

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

def gameInput(homeTeam, awayTeam, league):
    print("-----------------------------")

    # Rankings for team
    if league == 'NBA':
        numTeams = len(choNBA)
        coverHome = choNBA[homeTeam]
        coverAway = cacNBA[awayTeam]
        overHome = chcNBA[homeTeam]
        overAway = caoNBA[awayTeam]

    elif league == 'CBB':
        numTeams = len(choCBB)
        coverHome = choCBB[homeTeam]
        coverAway = cacCBB[awayTeam]
        overHome = chcCBB[homeTeam]
        overAway = caoCBB[awayTeam]

    topTier = numTeams * 0.15  # Top 10% Change to 20
    midTier = numTeams * 0.25  # Top 30% Change to 30
    lowTier = numTeams * 0.75  # Starting point for Bottom 30% Change to 70
    ass = numTeams * 0.85  # Bottom 10% Change to 80
    print(topTier, midTier, lowTier, ass)

    print("For " + awayTeam + " At " + homeTeam + ":")

    # Over
    if overHome <= midTier and overAway <= midTier:
        if overHome <= topTier and overAway <= topTier:
            print("LOCK ALERT!")
            lockparlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Over")
        print("Take the over!")
        print("Home Rank :" + str(overHome))
        print("Away Rank: " + str(overAway))
        parlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Over")
    elif overHome > lowTier and overAway > lowTier:
        if overHome > ass and overAway > ass:
            print("LOCK ALERT!")
            lockparlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Under")
        print("Take the under!")
        print("Home Rank :" + str(overHome))
        print("Away Rank: " +str(overAway))
        parlay.append(league + ": " +awayTeam + " At " + homeTeam + ": Under")
    else:
        print("Don't bet on O/U")

    # Cover
    if coverHome <= midTier and coverAway > lowTier:
        if coverHome <= topTier and coverAway > ass:
            print("LOCK ALERT!")
            lockparlay.append(league + ": " +homeTeam + ": Cover")
        print("Bet on " + homeTeam + " to Cover!")
        print("Home Rank :" + str(coverHome))
        print("Away Rank: " + str(coverAway))
        parlay.append(league + ": " +homeTeam + ": Cover")
    elif coverHome > lowTier and coverAway <= midTier:
        if coverHome > ass and coverAway <= topTier:
            print("LOCK ALERT!")
            lockparlay.append(league + ": " +awayTeam + ": Cover")
        print("Bet on " + awayTeam + " to Cover!")
        print("Home Rank :" + str(coverHome))
        print("Away Rank: " + str(coverAway))
        parlay.append(league + ": " + awayTeam + ": Cover")
    else:
        print("Don't bet on Cover")

def gameInputFromJSON(file):
    with open(file, 'r') as j:
        games = json.load(j)
    for game in games:
        if game["Home Team"] == '76ERS':
            homeTeam = teamDict['76ers']
        elif game["Away Team"] == '76ERS':
            awayTeam = teamDict['76ers']
        else:
            homeTeam = teamDict[game["Home Team"].title()]
            awayTeam = teamDict[game["Away Team"].title()]
        gameInput(homeTeam, awayTeam)

def main():
    global generalOver  # General Over Dict
    global generalOver2
    global generalCover # General Cover Dict
    global generalCover2
    global homeOver     # Home Over Dict
    global homeOver2
    global homeCover    # Home Cover Dict
    global homeCover2
    global awayOver     # Away Over Dict
    global awayOver2
    global awayCover    # Away Cover Dict
    global awayCover2
    global choNBA          # Combined Home Over
    global choCBB
    global chcNBA          # Combined Home Cover
    global chcCBB
    global caoNBA          # Combined Away Over
    global caoCBB
    global cacNBA          # Combined Away Cover
    global cacCBB
    global parlay       # Parlay List
    global lockparlay
    global teamDict     # Team Dictionary in form City: Team Name

    parlay = []
    lockparlay = []
    #print("General (LEAST ACCURATE): ")
    generalCover = generalAlg("Cover", "NBA")
    print(generalCover)
    generalOver = generalAlg("Over", "NBA")
    generalCover2 = generalAlg("Cover", "CBB")
    generalOver2 = generalAlg("Over", "CBB")
    #bestOddsGeneral(generalCover, "Cover")
    #bestOddsGeneral(generalOver, "Over")

    # For Home
    #print("CURRENT HOME ODDS: ")
    homeCover = getDict("../data/NBA/cover/home/SortedhomeCover.jl")
    homeCover2 = getDict("../data/CBB/cover/home/SortedhomeCover.jl")
    #bestOdds(homeCover, "Cover", "Home")
    homeOver = getDict("../data/NBA/over/home/SortedhomeOver.jl")
    homeOver2 = getDict("../data/CBB/over/home/SortedhomeOver.jl")
    #bestOdds(homeOver, "Over", "Home")

    # For Away
    #print("CURRENT AWAY ODDS: ")
    awayCover = getDict("../data/NBA/cover/away/SortedawayCover.jl")
    awayCover2 = getDict("../data/CBB/cover/away/SortedawayCover.jl")
    #bestOdds(awayCover, "Cover", "Away")
    awayOver = getDict("../data/NBA/over/away/SortedawayOver.jl")
    awayOver2 = getDict("../data/CBB/over/away/SortedawayOver.jl")
    #bestOdds(awayOver, "Over", "Away")

    # testing new stuff
    #print("COMBINED (MOST ACCURATE): ")
    #combine(generalCover, homeCover, .3, .7, "Cover", "Home")
    #combine(generalOver, homeOver, .3, .7, "Over", "Home")
    #combine(generalCover, awayCover, .3, .7, "Cover", "Away")
    #combine(generalOver, awayOver, .3, .7, "Over", "Away")
    # Variables stand for Combine Home/Away Over/Cover (ex: Combine Home Over = cho)
    #print("Scores for home over: ")
    choNBA = combineOnRanking(sortByRank(generalOver), sortByRank(homeOver))
    choCBB = combineOnRanking(sortByRank(generalOver2), sortByRank(homeOver2))
    #print("Scores for home cover: ")
    chcNBA = combineOnRanking(sortByRank(generalCover), sortByRank(homeCover))
    chcCBB = combineOnRanking(sortByRank(generalCover2), sortByRank(homeCover2))
    #print("Scores for away over: ")
    caoNBA = combineOnRanking(sortByRank(generalOver), sortByRank(awayOver))
    caoCBB = combineOnRanking(sortByRank(generalOver2), sortByRank(awayOver2))
    #print("Scores for away cover: ")
    cacNBA = combineOnRanking(sortByRank(generalCover), sortByRank(awayCover))
    cacCBB = combineOnRanking(sortByRank(generalCover2), sortByRank(awayCover2))

    # Run Manually NBA
    #print(choNBA)
    gameInput('Brooklyn', 'Atlanta', 'NBA')
    gameInput('Miami', 'Utah', 'NBA')
    gameInput('Memphis', 'Portland', 'NBA')
    gameInput('LA Lakers', 'Denver', 'NBA')
    gameInput('Phoenix', 'Houston', 'NBA')

    # Run Manually CBB
    gameInput('Fordham', 'St Josephs', 'CBB')
    gameInput('Kansas', 'Baylor', 'CBB')
    gameInput('Illinois', 'Wisconsin', 'CBB')
    gameInput('Tulsa', 'Temple', 'CBB')
    gameInput('Monmouth', 'Elon', 'CBB')
    gameInput('Stonehill', 'Central Conn', 'CBB')
    gameInput('Miami (OH)', 'E Michigan', 'CBB')
    gameInput('Wofford', 'VMI', 'CBB')
    gameInput('Arkansas', 'Kentucky', 'CBB')
    gameInput('Oregon', 'Arizona', 'CBB')
    gameInput('Oklahoma St', 'Texas', 'CBB')
    gameInput('NC-Asheville', 'Radford', 'CBB')
    gameInput('Gard-Webb', 'Winthrop', 'CBB')
    gameInput('Charl South', 'Presbyterian', 'CBB')
    gameInput('Towson', 'NC-Wilmgton', 'CBB')
    gameInput('Hofstra', 'Col Charlestn', 'CBB')
    gameInput('Hampton', 'Wm & Mary', 'CBB')
    gameInput('Navy', 'American', 'CBB')
    gameInput('Geo Wshgtn', 'La Salle', 'CBB')
    gameInput('Duquesne', 'Geo Mason', 'CBB')
    gameInput('Merrimack', 'Sacred Hrt', 'CBB')
    gameInput('W Michigan', 'Ball St', 'CBB')
    gameInput('Toledo', 'Buffalo', 'CBB')
    gameInput('Mercer', 'Furman', 'CBB')
    gameInput('W Carolina', 'Chattanooga', 'CBB')
    gameInput('N Hampshire', 'Binghamton', 'CBB')
    gameInput('South Dakota', 'North Dakota', 'CBB')
    gameInput('S Dakota St', 'N Dakota St', 'CBB')
    gameInput('Marquette', 'Creighton', 'CBB')
    gameInput('U Mass', 'Davidson', 'CBB')
    gameInput('UTSA', 'S Methodist', 'CBB')
    gameInput('Citadel', 'Samford', 'CBB')
    gameInput('Mass Lowell', 'Vermont', 'CBB')
    gameInput('Penn St', 'Minnesota', 'CBB')
    gameInput('LSU', 'Vanderbilt', 'CBB')
    gameInput('Central Mich', 'Kent St', 'CBB')
    gameInput('Lindenwood', 'Morehead St', 'CBB')
    gameInput('Beth-Cook', 'Southern', 'CBB')
    gameInput('Iowa St', 'UCF', 'CBB')
    gameInput('NC State', 'N Carolina', 'CBB')
    gameInput('Miss State', 'Auburn', 'CBB')
    gameInput('S Florida', 'Charlotte', 'CBB')
    gameInput('USC', 'Washington', 'CBB')
    gameInput('Howard', 'Maryland ES', 'CBB')
    gameInput('Wyoming', 'Colorado St', 'CBB')
    gameInput('Northeastrn', 'Drexel', 'CBB')
    gameInput('NC A&T', 'Campbell', 'CBB')
    gameInput('Delaware', 'Stony Brook', 'CBB')
    gameInput('Saint Louis', 'Rhode Island', 'CBB')
    gameInput('Norfolk St', 'Delaware St', 'CBB')
    gameInput('NC Central', 'Coppin St', 'CBB')
    gameInput('Le Moyne', 'St Fran (PA)', 'CBB')
    gameInput('NC-Grnsboro', 'E Tenn St', 'CBB')
    gameInput('TN Tech', 'TN State', 'CBB')
    gameInput('NJIT', 'Bryant', 'CBB')
    gameInput('Maine', 'Albany', 'CBB')
    gameInput('Lamar', 'NW State', 'CBB')
    gameInput('TX-Arlington', 'Utah Valley', 'CBB')
    gameInput('N Arizona', 'Weber St', 'CBB')
    gameInput('S Car State', 'Morgan St', 'CBB')
    gameInput('High Point', 'Longwood', 'CBB')
    gameInput('F Dickinson', 'Wagner', 'CBB')
    gameInput('TN State', 'TN Martin', 'CBB')
    gameInput('SIU Edward', 'W Illinois', 'CBB')
    gameInput('SE Louisiana', 'TX A&M-CC', 'CBB')
    gameInput('TX A&M-Com', 'Hsn Christian', 'CBB')
    gameInput('Alabama St', 'Alab A&M', 'CBB')
    gameInput('Florida A&M', 'Grambling St', 'CBB')
    gameInput('Army', 'Loyola-MD', 'CBB')
    gameInput('Nicholls', 'McNeese St', 'CBB')
    gameInput('N Mex State', 'Jksnville St', 'CBB')
    gameInput('Portland St', 'Sac State', 'CBB')
    gameInput('Montana', 'Idaho', 'CBB')
    gameInput('Montana St', 'E Washingtn', 'CBB')
    gameInput('Wake Forest', 'VA Tech', 'CBB')
    gameInput('Iowa', 'Northwestern', 'CBB')
    gameInput('Virginia', 'Duke', 'CBB')
    gameInput('IUPUI', 'Cleveland St', 'CBB')
    gameInput('Pittsburgh', 'Boston Col', 'CBB')
    gameInput('Texas Tech', 'W Virginia', 'CBB')
    gameInput('Texas A&M', 'Georgia', 'CBB')
    gameInput('VCU', 'Richmond', 'CBB')
    gameInput('N Illinois', 'Akron', 'CBB')
    gameInput('WI-Grn Bay', 'WI-Milwkee', 'CBB')
    gameInput('Detroit', 'Oakland', 'CBB')
    gameInput('Jackson St', 'TX Southern', 'CBB')
    gameInput('New Orleans', 'Incar Word', 'CBB')
    gameInput('Dartmouth', 'Brown', 'CBB')
    gameInput('W Kentucky', 'Florida Intl', 'CBB')
    gameInput('Miss Val St', 'Ark Pine Bl', 'CBB')
    gameInput('Alcorn St', 'Prairie View', 'CBB')
    gameInput('UCLA', 'Wash State', 'CBB')
    gameInput('Kansas St', 'Cincinnati', 'CBB')
    gameInput('Rice', 'Wichita St', 'CBB')
    gameInput('Lafayette', 'Bucknell', 'CBB')
    gameInput('San Francisco', 'Santa Clara', 'CBB')
    gameInput('Columbia', 'U Penn', 'CBB')
    #gameInput('Rob Morris', 'Purdue Fort Wayne', 'CBB')
    gameInput('N Kentucky', 'Wright St', 'CBB')
    gameInput('Cornell', 'Princeton', 'CBB')
    gameInput('Harvard', 'Yale', 'CBB')
    gameInput('TX El Paso', 'Liberty', 'CBB')
    gameInput('Xavier', 'Georgetown', 'CBB')
    gameInput('Clemson', 'Notre Dame', 'CBB')
    gameInput('Houston', 'Oklahoma', 'CBB')
    gameInput('Michigan St', 'Purdue', 'CBB')
    gameInput('Tennessee', 'Alabama', 'CBB')
    gameInput('Syracuse', 'Louisville', 'CBB')
    gameInput('New Mexico', 'Boise St', 'CBB')
    gameInput('Loyola Mymt', 'Portland', 'CBB')
    gameInput('Denver', 'St. Thomas', 'CBB')
    #gameInput('UT Rio Grande Valley', 'Cal Baptist', 'CBB')
    gameInput('Middle Tenn', 'Sam Hous St', 'CBB')
    gameInput('San Diego', 'Cal St Nrdge', 'CBB')
    gameInput('Hawaii', 'UC Riverside', 'CBB')
    gameInput('N Colorado', 'Idaho St', 'CBB')
    gameInput('Mississippi', 'Missouri', 'CBB')
    gameInput('SE Missouri', 'S Indiana', 'CBB')
    gameInput('Tarleton St', 'S Utah', 'CBB')
    gameInput('California', 'Utah', 'CBB')
    gameInput('TX Christian', 'BYU', 'CBB')
    gameInput('Abl Christian', 'Utah Tech', 'CBB')
    gameInput('UCSB', 'CS Fullerton', 'CBB')
    gameInput('Gonzaga', 'St Marys', 'CBB')
    gameInput('San Jose St', 'UNLV', 'CBB')
    gameInput('Pacific', 'San Diego', 'CBB')
    gameInput('Ste F Austin', 'Grd Canyon', 'CBB')
    gameInput('CS Bakersfld', 'Cal Poly', 'CBB')
    gameInput('Lg Beach St', 'UC Irvine', 'CBB')

    #gameInputFromJSON("../dk.json")

    # 7/7 So Far
    print("Risky Parlay: ")
    print(parlay)

    print("Lock Parlay: ")
    print(lockparlay)

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