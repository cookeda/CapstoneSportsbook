import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import matchupsData from './Data/master/matchups.json'; // Adjust the path as necessary

const MatchupStats = () => {
  // Convert the matchupsData object into an array of its entries
  const matchups = Object.entries(matchupsData);

  return (
    <ScrollView style={styles.container}>
      {matchups.map(([matchId, matchupDetails], index) => (
        <View key={index} style={styles.matchupContainer}>
          <Text style={styles.matchIdText}>Match ID: {matchId}</Text>
          <Text style={styles.teamText}>{matchupDetails['Home Team']} vs. {matchupDetails['Away Team']}</Text>
          <Text style={{fontWeight: "bold"}}> Home Spread: {matchupDetails['Home Spread']}</Text>
          <Text>Away Spread: {matchupDetails['Away Spread']}</Text>
          <Text>Total Points: {matchupDetails['Total Points']}</Text>
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
  matchIdText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  teamText: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
});

export default MatchupStats;