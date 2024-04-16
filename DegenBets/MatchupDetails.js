import React from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';
import { useRoute } from '@react-navigation/native';
import oddsData from './Data/master/odds.json';  // Ensure correct path

const MatchupDetails = () => {
  const route = useRoute();
  const { matchId, homeTeam, awayTeam, over_score, cover_rating, team_to_cover, time} = route.params; // Retrieve matchId passed via navigation

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>{awayTeam} @ {homeTeam} </Text>
      <Text style={styles.subtitle}>Time: {time}</Text>
      <Text style={styles.subtitle2}>O/U: {over_score}, Cover: {team_to_cover} {cover_rating}</Text>
      <View style={styles.tableHeader}>
        <Text style={styles.headerItem}>Book Name</Text>
        <Text style={styles.headerItem}>Away Spread</Text>
        <Text style={styles.headerItem}>Away ML</Text>
        <Text style={styles.headerItem}>Home Spread</Text>
        <Text style={styles.headerItem}>Home ML</Text>
        <Text style={styles.headerItem}>Total</Text>
        <Text style={styles.headerItem}>Over Odds</Text>
        <Text style={styles.headerItem}>Under Odds</Text>
      </View>
      {oddsData.map((item, index) => (
        <View key={index} style={styles.tableRow}>
          <Text style={styles.rowItem}>{item['Book Name']}</Text>
          <Text style={styles.rowItem}>{item['Away Spread']}, {item['Away Spread Odds']}</Text>
          <Text style={styles.rowItem}>{item['Away ML']}</Text>
          <Text style={styles.rowItem}>{item['Home Spread']}, {item['Home Spread Odds']}</Text>
          <Text style={styles.rowItem}>{item['Home ML']}</Text>
          <Text style={styles.rowItem}>{item['Total']}</Text>
          <Text style={styles.rowItem}>{item['Over Total Odds']}</Text>
          <Text style={styles.rowItem}>{item['Under Total Odds']}</Text>
        </View>
      ))}
    </ScrollView>
  );
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    backgroundColor: '#f0f0f0', // Updated background color for subtle texture
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    marginBottom: 12,
    color: '#2a2a2a', // Refined text color for high contrast
    textAlign: 'center', // Centering title for better balance
  },
  subtitle:{
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
    color: '#2a2a2a', // Refined text color for high contrast
    textAlign: 'center', // Centering title for better balance
  },
  subtitle2:{
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 6,
    color: '#2a2a2a', // Refined text color for high contrast
    textAlign: 'center', // Centering title for better balance
  },
  tableHeader: {
    flexDirection: 'row',
    backgroundColor: '#e8e8e8', // A solid background color for header
    borderRadius: 6,
    paddingVertical: 6,
    paddingHorizontal: 2,
    shadowColor: '#000', // Adding shadow for depth
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  headerItem: {
    flex: 1,
    fontWeight: '600',
    textAlign: 'center',
    color: '#505050',
  },
  tableRow: {
    flexDirection: 'row',
    backgroundColor: '#ffffff', // Keeping row backgrounds white for cleanliness
    paddingVertical: 10,
    paddingHorizontal: 2,
    borderRadius: 6,
    shadowColor: '#000', // Shadow for row items
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 2,
    marginVertical: 4,
  },
  rowItem: {
    flex: 1,
    textAlign: 'center',
    color: '#404040', // Slightly darker text for readability
    fontSize: 16, // Increased font size for accessibility
  },
});

export default MatchupDetails;
