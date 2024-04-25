import React from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';
import { useRoute } from '@react-navigation/native';
import aggData from './Data/Cleaned/AggregateOdds.json';  // Ensure correct path
import MatchupStats from './MatchupStats';


const MatchupDetails = () => {
  const route = useRoute();
  const { details, matchId, homeTeam, awayTeam, homeAbv, awayAbv, over_score, cover_rating, team_to_cover, time, result, league } = route.params; // Retrieve matchId passed via navigation
  // home_team = MatchupStats.getHomeTeam(home_team)
  // const findOddsByMatchId = (id) => {
  //   return aggData.filter(item => item.MatchupID === id);
  // };
//  const currentMatchOdds = findOddsByMatchId(matchId);
  const aggData1 = {
    "5a31e1ff_2848484e_NBA": {
      "Info Table": {
          "Away Team": "Cleveland Cavaliers",
          "Away Team Rank Name": "Cleveland",
          "Away Abv": "CLE",
          "Away ID": "5a31e1ff",
          "Home Team": "Orlando Magic",
          "Home Team Rank Name": "Orlando",
          "Home Abv": "ORL",
          "Home ID": "2848484e",
          "Start Time": "7:30 PM",
          "League": "NBA"
      },
      "Bet Tables": [
          {
              "Book Name": "Bovada",
              "Away Spread": "+2.5",
              "Away Spread Odds": "-110",
              "Away ML": "+115",
              "Home Spread": "-2.5",
              "Home Spread Odds": "-110",
              "Home ML": "-135",
              "Total": "201.5",
              "Over Total Odds": "-105",
              "Under Total Odds": "-115"
          },
          {
              "Book Name": "DK",
              "Away Spread": "+2",
              "Away Spread Odds": "−110",
              "Away ML": "+110",
              "Home Spread": "-2",
              "Home Spread Odds": "−110",
              "Home ML": "−130",
              "Total": "200",
              "Over Total Odds": "−110",
              "Under Total Odds": "−110"
          }
      ]
  },
  }

  // function filterDataByKey(data, keyFilter) {
  //   return Object.entries(data).reduce((acc, [key, value]) => {
  //     if (keyFilter(key, value)) {
  //       acc[key] = value;
  //     }
  //     return acc;
  //   }, {});
  // }
  // const filteredData = filterDataByKey(aggData, (key, value) => key === '5a31e1ff_2848484e_NBA');
  // console.log(filteredData);

  function getBetTables(data, key) {
    if (data[key] && data[key]['Bet Tables']) {
      return data[key]['Bet Tables'];
    }
    return null; // or return an empty array [] if that's more appropriate for your handling
  }
  
  const betTables = getBetTables(aggData, matchId);
  console.log(betTables);
  return (
    <ScrollView style={styles.container}>
    
      <Text style={styles.title}>{awayTeam} @ {homeTeam} </Text>
      <Text style={styles.subtitle}>Time: {time}</Text>
      <Text style={styles.subtitle2}>Cover: {team_to_cover} {cover_rating}</Text>
      <Text style={styles.subtitle2}>O/U: {league} {over_score}</Text>
      <Text style={styles.subtitle2}>matchId:  {matchId} </Text>

      <View style={styles.tableHeader}>
        <Text style={styles.headerItem}>Book Name</Text>
        <Text style={styles.headerItem}>{awayAbv} Spread</Text>
        <Text style={styles.headerItem}>{awayAbv} Win</Text>
        <Text style={styles.headerItem}>{homeAbv} Spread</Text>
        <Text style={styles.headerItem}>{homeAbv} Win</Text>
        <Text style={styles.headerItem}>Total</Text>
        <Text style={styles.headerItem}>Over Odds</Text>
        <Text style={styles.headerItem}>Under Odds</Text>
      </View>

      {betTables.map((table, index) => (
        <View key={index} style={styles.tableRow}>
          <Text style={styles.rowItem}>{table['Book Name']}</Text>
          <Text style={styles.rowItem}>{table['Away Spread']} {table['Away Spread Odds']}</Text>
          <Text style={styles.rowItem}>{table['Away ML']}</Text>
          <Text style={styles.rowItem}>{table['Home Spread']} {table['Home Spread Odds']}</Text>
          <Text style={styles.rowItem}>{table['Home ML']}</Text>
          <Text style={styles.rowItem}>{table['Total']}</Text>
          <Text style={styles.rowItem}>{table['Over Total Odds']}</Text>
          <Text style={styles.rowItem}>{table['Under Total Odds']}</Text>
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
    fontSize: 10
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
    fontSize: 12, // Increased font size for accessibility
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default MatchupDetails;
