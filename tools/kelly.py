#Multiplier, odds, %, br
# def kelly (float multiplier, string odds, float xHit, float bankroll) > float ():

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

def expected_value(odds, wager):
    implied_prob = implied_prob(odds)
    

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
#Vig Calculator



print(implied_prob('-120'))
print(implied_prob('+160'))
print(implied_prob('-1010'))
