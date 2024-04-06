import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import matchupsData from './NBA_Lite.json';

const MatchupStats = () => {
  // Convert the matchupsData object into an array of its values
  const matchups = Object.values(matchupsData);

  return (
    <ScrollView style={styles.container}>
      {matchups.map((matchup, index) => (
        <View key={index} style={styles.matchupContainer}>
          <Text style={styles.teamText}>{matchup['Home Team']} vs. {matchup['Away Team']}</Text>
          <Text>Home Spread: {matchup['Home Spread']}</Text>
          <Text>Away Spread: {matchup['Away Spread']}</Text>
          <Text>Total Points: {matchup['Total Points']}</Text>
          <Text>MatchupID: {matchup['']}</Text>
        </View>
      ))}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 20,
  },
  matchupContainer: {
    backgroundColor: '#f0f0f0',
    padding: 20,
    marginVertical: 8,
    marginHorizontal: 16,
    borderRadius: 5,
  },
  teamText: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
});

export default MatchupStats;