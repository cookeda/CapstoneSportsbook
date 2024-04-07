const themes = {
  light: {
    backgroundColor: '#f0f0f0',
    textColor: '#333',
    containerBackground: '#ffffff',
  },
  dark: {
    backgroundColor: '#333',
    textColor: '#f0f0f0',
    containerBackground: '#1a1a1a',
  },
};

import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Button, TouchableOpacity } from 'react-native';
import matchupsData from './Data/master/matchups.json'; 

const MatchupStats = () => {
  const [theme, setTheme] = useState('dark'); // Default theme

  // Function to toggle theme
  const toggleTheme = () => {
    setTheme((currentTheme) => (currentTheme === 'light' ? 'dark' : 'light'));
  };

  // Convert the matchupsData object into an array of its entries
  const matchups = Object.entries(matchupsData);
  

  // Dynamic styles based on the current theme
  const dynamicStyles = getDynamicStyles(theme);

  return (
    <View style={{ flex: 1 }}>
      <Button title="Toggle Theme" onPress={toggleTheme} />
      <ScrollView style={[styles.container, {backgroundColor: themes[theme].containerBackground}]}>
        {matchups.map(([matchId, matchupDetails], index) => (
          <TouchableOpacity
            key={index}
            style={[styles.matchupContainer, {backgroundColor: themes[theme].backgroundColor}]}
            onPress={() => console.log(`Matchup ${matchId} clicked`)} // TODO: Implement navigation
          >
            <Text style={[styles.matchIdText, {color: themes[theme].textColor}]}>Match ID: {matchId}</Text>
            <Text style={[styles.teamText, {color: themes[theme].textColor}]}>{matchupDetails['Home Team']} vs. {matchupDetails['Away Team']}</Text>
            <Text style={{color: themes[theme].textColor}}>Home Spread: {matchupDetails['Home Spread']}</Text>
            <Text style={{color: themes[theme].textColor}}>Away Spread: {matchupDetails['Away Spread']}</Text>
            <Text style={{color: themes[theme].textColor}}>Total Points: {matchupDetails['Total Points']}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
};

// Separated the function to get dynamic styles based on the theme
function getDynamicStyles(theme) {
  return StyleSheet.create({
    container: {
      flex: 1,
      marginTop: 20,
    },
    matchupContainer: {
      padding: 20,
      marginVertical: 8,
      marginHorizontal: 16,
      borderRadius: 5,
    },
    matchIdText: {
      fontSize: 14,
      fontWeight: 'bold',
      marginBottom: 5,
    },
    teamText: {
      fontSize: 16,
      fontWeight: 'bold',
      marginBottom: 10,
    },
  });
}

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
