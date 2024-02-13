import json
#60% Current + 30% 10 Year + 10% All Time
# For Atlanta = (.6 * .28) + (.3 * .485) + (.1 * .484)
#             = (.168)     + (.1455)     + (.0484)      = .3619
# 36.19% Chance at Covering

# For Denver OU = (.6 * .373)   + (.3 * .517) + (.1 * .515)
#               = (.2238)       + (.1551)     + (.0515)     = .4304 DOES NOT WORK FOR OU CURRENT
# TODO FIX ABOVE

def mathStuff(type):
    type2 = ""
    if type == "Cover":
        type2 = type

    if type == "Over":
        type2 = "OU"

    dict = {}
    with open("data/" + type.lower() + "/SortedCurrentSeason" + type2 + ".jl", 'r') as current:
        with open("data/" + type.lower() + "/SortedAllTime" + type2 + ".jl", 'r') as all:
            with open("data/" + type.lower() + "/Sorted10Year" + type2 + ".jl", 'r') as ten:
                for sixty in current:
                    for tenp in all:
                        for thirty in ten:
                            team = (((str(thirty).split(':')[1]).split(',')[0]).rstrip('\"'))
                            print(sixty[-8:-4])
                          #  print(thirty[-8:-4])
                          #  print(tenp[-8:-4])
                            perChance = (.6 * (float(sixty[-8:-4]) / 100)) + \
                                        (.3 * (float(thirty[-8:-4]) / 100)) + \
                                        (.1 * (float(tenp[-8:-4]) / 100))
                            dict[team] = perChance
                print(dict)
                return dict

def bestOdds(dict, type):
    bestOdds = -99
    bestTeam = "Nobody"
    for team in dict:
        percent = float(dict[team])
        if percent > bestOdds:
            bestOdds = percent
            bestTeam = team
    print("The best team to bet on any given night is " + bestTeam + " percent: " + str(bestOdds))

def main():
    dict1 = mathStuff("Cover")
    #   dict2 = mathStuff("Over")
    bestOdds(dict1, "Cover")
    #    bestOdds(dict2, "Over")

if __name__ == '__main__':
    main()