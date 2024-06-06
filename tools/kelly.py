#Multiplier, odds, %, br
# def kelly (float multiplier, string odds, float xHit, float bankroll) > float ():

#Odds converter
#Raw Kelly
#Unit Sizing
#Calculators:
#Arbitrage
#EV
#Bonus Bet 
#Half Point
#Hold
    #Implied Probability: implied_prob
#Kelly
#No-Vig Fair Odds
#Odds Converter
#Parlay
#Point Spread
#Poisson
#Round Robin
    #Vig Calculator: vig

def implied_prob(odds):
    #returns boolean indicating favorite (true) or underdog (false)
    favorite = (odds[0] == '-')
    odds = float(odds[1:])
    if favorite:
        prob = (odds / (odds + 100))
    else:
        prob = (100 / (odds + 100))
    prob = round(prob * 100, 2)

    return prob 

def kelly(multiplier, line_odds, xHitRate):
    #returns kelly multiplier
    lose_prob = 100 - xHitRate
    bet_gain = implied_prob(line_odds)
    print(bet_gain)
    kelly = xHitRate - (lose_prob / bet_gain)
    kelly = round(kelly, 2)
    return kelly

print(kelly(1, '-110', 60))


def vig(line1_odds, line2_odds):
    #used for checking all outcomes of a game   NOTE: for other sports might need more line options
    #returns vig of line 1 and line 2 (this is the edge the sportsbook gains)
    #ideally the lower vig is the better market, but i still take any +5% edge
    line1_imp = implied_prob(str(line1_odds))
    line2_imp = implied_prob(str(line2_odds))
    vig = (100 - (line1_imp + line2_imp)) * -1
    return round(vig, 2)


# print("implied prob test ")
# print(implied_prob('-120'))
# print(implied_prob('+160'))
# print(implied_prob('-1010'))
print(vig('-120', '+125'))
