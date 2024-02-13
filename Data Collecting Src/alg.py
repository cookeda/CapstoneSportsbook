# Algorithm for determining likelihood
# Should be updated to reflect per bet and compare if a bet is good or bad
# Should take into consideration home advantage, etc. down the line
# Pretty sure the math is right currently
def alg(stat):
    type2 = ""
    if stat == "Cover":
        type2 = stat

    if stat == "Over":
        type2 = "OU"

    result_dict = {}
    with open("../data/" + stat.lower() + "/SortedCurrentSeason" + type2 + ".jl", 'r') as current:
        with open("../data/" + stat.lower() + "/SortedAllTime" + type2 + ".jl", 'r') as all:
            with open("../data/" + stat.lower() + "/Sorted10Year" + type2 + ".jl", 'r') as ten:
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


def bestOdds(result_dict, stat):
    bestChance = -99
    bestTeam = "Nobody"
    for team in result_dict:
        percent = float(result_dict[team])
        if percent > bestChance:
            bestChance = percent
            bestTeam = team
    if stat == "Cover":
        print("The Most Likely Team to Cover is: " + bestTeam)

    if stat == "Over":
        print("The Most Likely Team to go Over is: " + bestTeam)


def main():
    dict1 = alg("Cover")
    dict2 = alg("Over")
    bestOdds(dict1, "Cover")
    bestOdds(dict2, "Over")


if __name__ == '__main__':
    main()