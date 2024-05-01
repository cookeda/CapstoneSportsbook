import React from 'react';import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import matchupsData from './Data/merged_data.json';
// import oddsData from './Data/Cleaned/AggregateOdds.json'; // New import for odds data

const MatchupStats = () => {
  const navigation = useNavigation();
  const matchups = Object.entries(matchupsData);

  const isTeamToCoverAwayTeam = (teamToCover, awayTeam) => {
    //console.log(`Checking if ${teamToCover} is the away team: ${awayTeam}`);
    return teamToCover === awayTeam;
  };
  
  // console.log(matchups);
  
  return (
    <View style={styles.container}>
    <Text style={styles.star_rate}>NBA Star Hitrates: Cover (3: 50%, 2: 61%, 1: 42%) NBA Total (-3:61%, -2:50%, -1:43%, 0: Nah)</Text>
    <Text style={styles.star_rate}>MLB Star Hitrates: Cover (3: 53%, 2: 50%, 1: 50.7%) MLB Total (-3:52%, -2:50%, -1:43%,  0: Nah) </Text>

      <ScrollView style={styles.scrollContainer}>
        {matchups.map(([matchId, details], index) => {
          // Calculate result for each matchup within the map function
          const result = isTeamToCoverAwayTeam(details['team_to_cover'], details['Away Team']);
          const league = details["League"];
          // console.log(`Match ID: ${matchId}, Result: ${result}`); // Debugging output
          return (
            <TouchableOpacity
              key={matchId}
              onPress={() => navigation.navigate('MatchupDetails',{
                        homeTeam: details['Home Team'], 
                        homeAbv: details['Home Abv'],
                        awayTeam: details['Away Team'],
                        awayAbv: details['Away Abv'],
                        over_score: details['total_rating'],
                        cover_grade: details['cover_grade'],
                        team_to_cover: details['team_to_cover'],
                        time: details['Time'],
                        matchId
                    })}              
              style={styles.matchupContainer}
            >
              <View style={styles.matchupHeader}>
                <Text style={styles.teamName}>{details['Away Team']} {result ? ' (Covering)' : ''}</Text>
                <Text style={styles.vsText}>@</Text>
                <Text style={styles.teamName}>{result ? '': ' (Covering)'} {details['Home Team']}</Text>
              </View>
            <View style={styles.oddsContainer}>
              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>{details['Away Abv']} Win</Text>
                <Text style={styles.oddsValue}>{details['Away ML']}</Text>
                <Text style={styles.oddsLabel}>{details['Away ML Book']}</Text>
              </View>
              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>Total  O{details['Total Points']}</Text>
                <Text style={styles.oddsValue}>{details['Over Odds']}</Text>
                <Text style={styles.oddsLabel}>{details['Over Odds Book']}</Text>

              </View>
              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>{details['Home Abv']} Win</Text>
                <Text style={styles.oddsValue}>{details['Home ML']}</Text>
                <Text style={styles.oddsLabel}>{details['Home ML Book']}</Text>

              </View>

              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>{details['Away Abv']} {details['Away Spread']}</Text>
                <Text style={styles.oddsValue}>{details['Away Spread Odds']}</Text>
                <Text style={styles.oddsLabel}>{details['Away Spread Odds Book']}</Text>

              </View>

              <View style={styles.oddsBox}>
              <Text style={styles.oddsLabel}>Total  U{details['Total Points']}</Text>
                <Text style={styles.oddsValue}>{details['Under Odds']}</Text>
                <Text style={styles.oddsLabel}>{details['Under Odds Book']}</Text>

              </View>

              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>{details['Home Abv']} {details['Home Spread']}</Text>
                <Text style={styles.oddsValue}>{details['Home Spread Odds']}</Text>
                <Text style={styles.oddsLabel}>{details['Home Spread Odds Book']}</Text>

              </View>

              <Text style={styles.leagueText}>{league}</Text> 
              <Text style={styles.timeText}>{details['Time']}</Text>

              
              <View style={styles.ratingsContainer}>
                {/* <Text style={styles.ratingsText}>Team to Cover: {details['team_to_cover']}, </Text> */}
                <Text style={styles.oddsValue}> STARS </Text>
                <Text style={styles.ratingsText}>Cover: {details['cover_grade']}, </Text>
                <Text style={styles.ratingsText}>Total: {details['total_rating']}</Text>
              </View>


            </View>
              
          </TouchableOpacity>
        );
        })}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f0f0f0',
  },
  scrollContainer: {
    flex: 1,
  },
  matchupContainer: {
    backgroundColor: '#fff',
    marginVertical: 4,
    marginHorizontal: 16,
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#e1e1e1',
  },
  matchupHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  teamName: {
    fontWeight: 'bold',
    fontSize: 16,
  },
  vsText: {
    fontSize: 16,
  },
  star_rate: {
    fontSize: 18,
    //fontWeight: 'bold',
    textAlign: 'center',
    alignItems: 'center',
    padding:10,
  },
  oddsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    paddingBottom: 0,
  },
  oddsBox: {
    minWidth: '30%',
    padding: 6,
    margin: 2,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#e1e1e1',
    borderRadius: 4,
  },
  oddsLabel: {
    fontSize: 12,
    color: '#666',
  },
  oddsValue: {
    fontWeight: 'bold',
    fontSize: 14,
  },
  leagueText: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'left',
    alignItems: 'center',

    padding:10,
  },
  timeText: {
    fontSize: 12,
    color: '#666',
    textAlign: 'right',
    padding: 13,
  },
  ratingsContainer:{
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 8,
  },
  ratingsText: {
    fontSize: 14,
  }
});

export default MatchupStats;
