// MatchupDetails.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useRoute } from '@react-navigation/native';

const MatchupDetails = () => {
  const route = useRoute();
  const { matchId } = route.params; // Retrieve matchId passed via navigation

  // Assume matchupsData is accessible here or fetch the details based on matchId
  // For demonstration, I'll use a placeholder for matchup details
  const matchupDetails = {/* Fetch or locate the matchup details using matchId */};

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Matchup Details</Text>
      {/* Display matchup details here */}
      <Text>Match ID: {matchId}</Text>
      {/* More details can be displayed here */}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  // Add styles for other elements as needed
});

export default MatchupDetails;
