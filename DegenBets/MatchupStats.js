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
                <Text style={styles.oddsLabel}>ML Away</Text>
                <Text style={styles.oddsValue}>-999</Text>
              </View>
              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>Total  O {details['Total Points']}</Text>
                <Text style={styles.oddsValue}>{details['Over Odds']}</Text>
              </View>

              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>Spread Home</Text>
                <Text style={styles.oddsValue}>{details['Away Spread']}</Text>
              </View>
              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>Spread Away</Text>
                <Text style={styles.oddsValue}>{details['Home Spread']}</Text>
              </View>

              <View style={styles.oddsBox}>
              <Text style={styles.oddsLabel}>Total U {details['Total Points']}</Text>
                <Text style={styles.oddsValue}>{details['Under Odds']}</Text>
              </View>

              <View style={styles.oddsBox}>
                <Text style={styles.oddsLabel}>ML Home</Text>
                <Text style={styles.oddsValue}>-9999</Text>
              </View>
              <Text style={styles.leagueText}>MLB</Text> 
              <Text style={styles.timeText}>{details['Time']}</Text>
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
    padding:10,
  },
  timeText: {
    fontSize: 12,
    color: '#666',
    textAlign: 'right',
    padding: 13,
  },
});

export default MatchupStats;
