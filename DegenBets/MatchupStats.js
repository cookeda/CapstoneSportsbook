import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import matchupsData from './Data/merged_data.json';

const MatchupStats = () => {
  const navigation = useNavigation();
  const matchups = Object.entries(matchupsData);

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scrollContainer}>
        {matchups.map(([matchId, details], index) => (
          <TouchableOpacity
            key={matchId}
            onPress={() => navigation.navigate('MatchupDetails', details)}
            style={styles.matchupContainer}
          >
            <View style={styles.matchupHeader}>
              <Text style={styles.teamName}>{details['Away Team']}</Text>
              <Text style={styles.vsText}>@</Text>
              <Text style={styles.teamName}>{details['Home Team']}</Text>
            </View>
            <View style={styles.oddsContainer}>
              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>{details['Away Abv']} Win</Text>
                <Text style={styles.oddsValue}>{details['Away ML']}</Text>
              </View>
              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>Total  O{details['Total Points']}</Text>
                <Text style={styles.oddsValue}>{details['Over Odds']}</Text>
              </View>
              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>{details['Home Abv']} Win</Text>
                <Text style={styles.oddsValue}>{details['Home ML']}</Text>
              </View>

              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>{details['Away Abv']} {details['Away Spread']}</Text>
                <Text style={styles.oddsValue}>{details['Away Spread Odds']}</Text>
              </View>

              <View style={styles.oddsBox}>
              <Text style={styles.oddsLabel}>Total U{details['Total Points']}</Text>
                <Text style={styles.oddsValue}>{details['Under Odds']}</Text>
              </View>

              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>{details['Home Abv']} {details['Home Spread']}</Text>
                <Text style={styles.oddsValue}>{details['Home Spread Odds']}</Text>
              </View>

              <Text style={styles.leagueText}>{details['League']}</Text> 
              <Text style={styles.timeText}>{details['Time']}</Text>

              
              <View style={styles.ratingsContainer}>
                <Text style={styles.ratingsText}>{details['team_to_cover']}, </Text>
                <Text style={styles.ratingsText}>Cover: {details['cover_rating']}, </Text>
                <Text style={styles.ratingsText}>Total: {details['over_score']}</Text>
              </View>


            </View>
              
          </TouchableOpacity>
        ))}
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
