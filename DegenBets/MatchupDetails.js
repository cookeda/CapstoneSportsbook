import React from 'react';
import { View, Text } from 'react-native';

const MatchupDetails = ({ route }) => {
  const { matchId } = route.params;
  // Logic to fetch and display details for the matchup
  
  return (
    <View>
      <Text>Details for Matchup ID: {matchId}</Text>
    </View>
  );
};

export default MatchupDetails;
