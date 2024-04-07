import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import MatchupStats from './MatchupStats';
import MatchupDetails from './MatchupDetails'; // TODO: Create later 
const Stack = createStackNavigator();

function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="MatchupStats">
        <Stack.Screen name="MatchupStats" component={MatchupStats} options={{ title: 'Matchups' }} />
        <Stack.Screen name="MatchupDetails" component={MatchupDetails} options={{ title: 'Matchup Details' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default AppNavigator;
