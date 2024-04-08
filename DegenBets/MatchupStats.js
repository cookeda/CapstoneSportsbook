// MatchupStats.js
import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import matchupsData from './Data/master/matchups.json'; // Adjust the path as necessary

const MatchupStats = () => {
  const navigation = useNavigation();
  const [theme, setTheme] = useState('dark');

  const toggleTheme = () => {
    setTheme(currentTheme => currentTheme === 'light' ? 'dark' : 'light');
  };

  const matchups = Object.entries(matchupsData);

  return (
    <View style={{ flex: 1 }}>
      <ScrollView style={[styles.container, {backgroundColor: theme === 'dark' ? '#333' : '#f0f0f0'}]}>
        {matchups.map(([matchId, matchupDetails], index) => (
          <TouchableOpacity
            key={index}
            onPress={() => navigation.navigate('MatchupDetails', { matchId })}
            style={[styles.matchupContainer, {backgroundColor: theme === 'dark' ? '#555' : '#ccc'}]}
          >
            <Text style={[styles.matchIdText, {color: theme === 'dark' ? '#FFF' : '#000'}]}>Match ID: {matchId}</Text>
            <Text style={[styles.teamText, {color: theme === 'dark' ? '#FFF' : '#000'}]}>{matchupDetails['Home Team']} vs {matchupDetails['Away Team']}</Text>
            <Text style={{color: theme === 'dark' ? '#FFF' : '#000'}}>Home Spread: {matchupDetails['Home Spread']}</Text>
            <Text style={{color: theme === 'dark' ? '#FFF' : '#000'}}>Away Spread: {matchupDetails['Away Spread']}</Text>
            <Text style={{color: theme === 'dark' ? '#FFF' : '#000'}}>Total Points: {matchupDetails['Total Points']}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  matchupContainer: {
    padding: 20,
    marginVertical: 8,
    marginHorizontal: 16,
    borderRadius: 5,
  },
  matchIdText: {
    fontWeight: 'bold',
  },
  teamText: {},
});

export default MatchupStats;
