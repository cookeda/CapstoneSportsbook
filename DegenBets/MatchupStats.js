// MatchupStats.js
import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import matchupsData from './Data/merged_data.json'; // Adjust the path as necessary

const MatchupStats = () => {
  const navigation = useNavigation();
  const [theme, setTheme] = useState('light');

  const toggleTheme = () => {
    setTheme(currentTheme => currentTheme === 'light' ? 'dark' : 'light');
  };
  <TouchableOpacity onPress={toggleTheme} style={styles.buttonStyle}>
    <Text style={{ color: theme === 'dark' ? '#FFF' : '#000', fontWeight: 'bold' }}>
        Toggle Theme
    </Text>
  </TouchableOpacity>

  const matchups = Object.entries(matchupsData);


  return (
    <View style={{ flex: 1, backgroundColor: theme === 'dark' ? '#333' : '#f0f0f0' }}>
        <TouchableOpacity onPress={toggleTheme} style={styles.buttonStyle}>
            <Text style={{ color: '#000' }}>Theme</Text>
        </TouchableOpacity>
        <ScrollView style={styles.container}>
            {matchups.map(([matchId, matchupDetails], index) => (
                <TouchableOpacity
                    key={index}
                    onPress={() => navigation.navigate('MatchupDetails',{
                        homeTeam: matchupDetails['Home Team'], 
                        awayTeam: matchupDetails['Away Team'],
                        over_score: matchupDetails['over_score'],
                        cover_rating: matchupDetails['cover_rating'],
                        team_to_cover: matchupDetails['team_to_cover'],
                    })}
                    style={[styles.matchupContainer, {backgroundColor: theme === 'dark' ? '#555' : '#ccc'}]}
                >
                    <Text style={[styles.teamText, {color: theme === 'dark' ? '#FFF' : '#000'}]}>Match ID: {matchId}</Text>
                    <Text style={[styles.containerTitle, {color: theme === 'dark' ? '#FFF' : '#000'}]}>{matchupDetails['Away Team']} @ {matchupDetails['Home Team']}</Text>
                    <Text style={{color: theme === 'dark' ? '#FFF' : '#000'}}>Home Spread: {matchupDetails['Home Spread']}</Text>
                    <Text style={{color: theme === 'dark' ? '#FFF' : '#000'}}>Away Spread: {matchupDetails['Away Spread']}</Text>
                    <Text style={{color: theme === 'dark' ? '#FFF' : '#000'}}>Total Points: {matchupDetails['Total Points']}</Text> 
                    <Text style={{color: theme === 'dark' ? '#FFF' : '#000'}}>Cover Rating: {matchupDetails['cover_rating']}</Text>
                    <Text style={{color: theme === 'dark' ? '#FFF' : '#000'}}>Team to Cover: {matchupDetails['team_to_cover']}</Text>
                    <Text style={{color: theme === 'dark' ? '#FFF' : '#000'}}>Total Rating: {matchupDetails['over_score']}</Text>
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
  containerTitle: {
      fontWeight: 'bold',
  },
  teamText: {},

  buttonStyle: {
    position: 'absolute', // Making the button float in a fixed position
    top: 10,              // 10 pixels from the top
    right: 10,            // 10 pixels from the right
    backgroundColor: '#E1E1E1',  // Neutral background
    padding: 10,          // Padding inside the button
    borderRadius: 20,     // Rounded corners
    shadowOpacity: 0.3,   // Adding some shadow
    shadowRadius: 3,
    shadowColor: '#000',
    shadowOffset: { height: 2, width: 0 },
    elevation: 3,          // Elevation for Android (similar to shadow)
    zIndex: 1000, 
}
});


export default MatchupStats;
