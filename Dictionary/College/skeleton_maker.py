import json

# List of school names (replace with your actual school names)
#schools = [f"School{i}" for i in range(1, 301)]
schools = [
    "Abilene Christian Wildcats", "Air Force Falcons", "Akron Zips",
    "Alabama A&M Bulldogs", "Alabama Crimson Tide", "Alabama St. Hornets",
    "Albany Great Danes", "Alcorn St. Braves", "American Eagles",
    "Appalachian St. Mountaineers", "Little Rock Trojans", "Arizona Wildcats",
    "Arizona State Sun Devils", "Arkansas-Pine Bluff Golden Lions",
    "Arkansas Razorbacks", "Arkansas St. Red Wolves", "Army Black Knights",
    "Auburn Tigers", "Austin Peay Governors", "Ball St. Cardinals",
    "Baylor Bears", "Bellarmine Knights", "Belmont Bruins",
    "Bethune-Cookman Wildcats", "Binghamton Bearcats", "Boise St. Broncos",
    "Boston College Eagles", "Boston U Terriers", "Bowling Green Falcons",
    "Bradley Braves", "Brown Bears", "Bryant Bulldogs", "Bucknell Bison",
    "Buffalo Bulls", "Butler Bulldogs", "Brigham Young Cougars",
    "California Baptist Lancers", "Cal Poly SLO Mustangs", "CSU Northridge Matadors",
    "California Golden Bears", "Campbell Fighting Camels", "Canisius Golden Griffins",
    "Central Arkansas Bears", "Central Conn. St. Blue Devils", "Central Michigan Chippewas",
    "Charleston Southern Buccaneers", "Charlotte 49ers", "Chattanooga Mocs",
    "Chicago St. Cougars", "Cincinnati Bearcats", "The Citadel Bulldogs",
    "Clemson Tigers", "Cleveland St. Vikings", "Coastal Carolina Chanticleers",
    "Charleston Cougars", "Colgate Raiders", "Colorado Buffaloes",
    "Colorado St. Rams", "Columbia Lions", "Connecticut Huskies",
    "Coppin St. Eagles", "Cornell Big Red", "Creighton Bluejays",
    "CSU Bakersfield Roadrunners", "CSU Fullerton Titans", "Dartmouth Big Green",
    "Davidson Wildcats", "Dayton Flyers", "Delaware Blue Hens",
    "Delaware State Hornets", "Denver Pioneers", "DePaul Blue Demons",
    "Detroit Mercy Titans", "Drake Bulldogs", "Drexel Dragons",
    "Duke Blue Devils", "Duquesne Dukes", "East Carolina Pirates",
    "Eastern Illinois Panthers", "Eastern Kentucky Colonels", "Eastern Michigan Eagles",
    "East Tennessee St. Buccaneers", "Eastern Washington Eagles", "Elon University Phoenix",
    "Evansville Purple Aces", "Fairleigh Dickinson Knights", "Fairfield Stags",
    "Florida Atlantic Owls", "Florida Gulf Coast Eagles", "Florida Gators",
    "Florida A&M Rattlers", "Florida International Panthers", "Florida State Seminoles",
    "Fordham Rams", "Fresno St. Bulldogs", "Furman Paladins",
    "Georgia Southern Eagles", "Georgia Tech Yellow Jackets", "Gardner-Webb Runnin' Bulldogs",
    "George Mason Patriots", "George Washington Revolutionaries", "Georgetown Hoyas",
    "Georgia Bulldogs", "Georgia St. Panthers", "Gonzaga Bulldogs",
    "Grambling State Tigers", "Grand Canyon Antelopes", "Hampton Pirates",
    "Harvard Crimson", "Hawaii Rainbow Warriors", "High Point Panthers",
    "Hofstra Pride", "Holy Cross Crusaders", "Houston Cougars",
    "Howard Bison", "Houston Christian Huskies", "Idaho Vandals",
    "Idaho State Bengals", "Illinois-Chicago Flames", "Illinois Fighting Illini",
    "Illinois St. Redbirds", "Incarnate Word Cardinals", "Indiana Hoosiers",
    "Indiana St. Sycamores", "Iona Gaels", "Iowa Hawkeyes",
    "Iowa State Cyclones", "Purdue Fort Wayne Mastodons", "IUPUI Jaguars",
    "Jackson State Tigers", "Jacksonville Dolphins", "James Madison Dukes",
    "Jacksonville St. Gamecocks", "Kansas Jayhawks", "Kansas City Roos",
    "Kansas State Wildcats", "Kennesaw St. Owls", "Kent St. Golden Flashes",
    "Kentucky Wildcats", "La Salle Explorers", "Louisiana Tech Bulldogs",
    "Lafayette Leopards", "Lamar Cardinals", "Le Moyne Dolphins",
    "Lehigh Mountain Hawks", "Long Beach St. Beach", "Liberty Flames",
    "Lindenwood Lions", "Lipscomb Bisons", "LIU Sharks",
    "Longwood Lancers", "UL Lafayette Ragin' Cajuns", "Louisville Cardinals",
    "Loyola Marymount Lions", "Loyola-Chicago Ramblers", "Loyola (MD) Greyhounds",
    "Louisiana State Tigers", "Maine Black Bears", "Manhattan Jaspers",
    "Marist Red Foxes", "Marquette Golden Eagles", "Marshall Thundering Herd",
    "Maryland Terrapins", "UMBC Retrievers", "Maryland-Eastern Shore Hawks",
    "Massachusetts Lowell River Hawks", "McNeese St. Cowboys", "Memphis Tigers",
    "Mercer Bears", "Merrimack Warriors", "Miami Hurricanes",
    "Miami (OH) RedHawks", "Michigan Wolverines", "Michigan St. Spartans",
    "Middle Tennessee St. Blue Raiders", "Minnesota Golden Gophers", "Mississippi State Bulldogs",
    "Mississippi Valley State Delta Devils", "Mississippi Rebels", "Missouri Tigers",
    "Missouri St. Bears", "Monmouth-NJ Hawks", "Montana Grizzlies",
    "Montana St. Bobcats", "Morehead St. Eagles", "Morgan St. Bears",
    "Mount St. Mary's Mountaineers", "Murray St. Racers", "North Alabama Lions",
    "Northern Arizona Lumberjacks", "North Carolina Tar Heels", "Northern Colorado Bears",
    "North Dakota State Bison", "North Florida Ospreys", "New Hampshire Wildcats",
    "Northern Illinois Huskies", "Northern Iowa Panthers", "Northern Kentucky Norse",
    "New Mexico St. Aggies", "Navy Midshipmen", "North Carolina A&T Aggies",
    "North Carolina Central Eagles", "NC State Wolfpack", "UNC Asheville Bulldogs",
    "UNC Greensboro Spartans", "UNC Wilmington Seahawks", "Nebraska Omaha Mavericks",
    "Nebraska Cornhuskers", "Nevada Wolf Pack", "New Mexico Lobos",
    "New Orleans Privateers", "Niagara Purple Eagles", "Nicholls State Colonels",
    "NJIT Highlanders", "Norfolk State Spartans", "North Dakota Fighting Hawks",
    "North Texas Mean Green", "Northeastern Huskies", "Northwestern Wildcats",
    "Notre Dame Fighting Irish", "Northwestern St. Demons", "Oakland Golden Grizzlies",
    "Ohio Bobcats", "Ohio St. Buckeyes", "Oklahoma Sooners",
    "Oklahoma State Cowboys", "Old Dominion Monarchs", "Oral Roberts Golden Eagles",
    "Oregon Ducks", "Oregon St. Beavers", "Pacific Tigers",
    "Penn St. Nittany Lions", "Pepperdine Waves", "Pittsburgh Panthers",
    "Portland Pilots", "Portland St. Vikings", "Prairie View A&M Panthers",
    "Presbyterian Blue Hose", "Princeton Tigers", "Providence Friars",
    "Purdue Boilermakers", "Queens University of Charlotte Royals", "Quinnipiac Bobcats",
    "Radford Highlanders", "Rhode Island Rams", "Rice Owls",
    "Richmond Spiders", "Rider Broncs", "Robert Morris Colonials",
    "Rutgers Scarlet Knights", "South Alabama Jaguars", "South Carolina State Bulldogs",
    "South Carolina Gamecocks", "South Dakota State Jackrabbits", "South Florida Bulls",
    "Southern Illinois Salukis", "Southern Indiana Screaming Eagles", "Southern Methodist Mustangs",
    "Southern Miss Golden Eagles", "Southern Utah Thunderbirds", "Sacramento State Hornets",
    "Sacred Heart Pioneers", "Saint Louis Billikens", "Sam Houston St. Bearkats",
    "Samford Bulldogs", "San Diego Toreros", "San Diego St. Aztecs",
    "San Francisco Dons", "San Jose St. Spartans", "Santa Clara Broncos",
    "South Carolina Upstate Spartans", "Southeastern Louisiana Lions", "SE Missouri St. Redhawks",
    "Seattle Redhawks", "Seton Hall Pirates", "Siena Saints",
    "SIU Edwardsville Cougars", "South Dakota Coyotes", "Southern Jaguars",
    "St. Bonaventure Bonnies", "St. Francis (PA) Red Flash", "St. John's Red Storm",
    "Saint Joseph's Hawks", "Saint Mary's Gaels", "Saint Peter's Peacocks",
    "St. Thomas (MN) Tommies", "Stanford Cardinal", "Stephen F. Austin Lumberjacks",
    "Stetson Hatters", "Stonehill Skyhawks", "Stony Brook Seawolves",
    "Syracuse Orange", "Tarleton State Texans", "Temple Owls",
    "Tennessee Volunteers", "Texas Longhorns", "Texas A&M Aggies",
    "Texas State Bobcats", "Texas Tech Red Raiders", "Tenn-Martin Skyhawks",
    "Tennessee St. Tigers", "Tennessee Tech Golden Eagles", "Toledo Rockets",
    "Towson Tigers", "Troy Trojans", "Tulane Green Wave",
    "Tulsa Golden Hurricane", "Texas A&M-CC Islanders", "Texas A&M Commerce Lions",
    "Texas Christian Horned Frogs", "Texas-El Paso Miners", "Texas Southern Tigers",
    "Texas-Arlington Mavericks", "Texas Rio Grande Valley Vaqueros", "Massachusetts Minutemen",
    "Pennsylvania Quakers", "UAB Blazers", "UC Davis Aggies",
    "UC Irvine Anteaters", "UC Riverside Highlanders", "Central Florida Knights",
    "UCLA Bruins", "UC Santa Barbara Gauchos", "UC San Diego Tritons",
    "UL Monroe Warhawks", "UNLV Rebels", "Southern California Trojans",
    "Utah Utes", "Utah St. Aggies", "Utah Tech Trailblazers",
    "Utah Valley Wolverines", "Texas-San Antonio Roadrunners", "Virginia Tech Hokies",
    "Valparaiso Beacons", "Vanderbilt Commodores", "VCU Rams",
    "Vermont Catamounts", "Villanova Wildcats", "Virginia Cavaliers",
    "VMI Keydets", "Western Carolina Catamounts", "Western Illinois Leathernecks",
    "Western Kentucky Hilltoppers", "Western Michigan Broncos", "West Virginia Mountaineers",
    "Wagner Seahawks", "Wake Forest Demon Deacons", "Washington St. Cougars",
    "Washington Huskies", "Weber St. Wildcats", "Green Bay Phoenix",
    "Milwaukee Panthers", "Wichita St. Shockers", "Winthrop Eagles",
    "Wisconsin Badgers", "William & Mary Tribe", "Wofford Terriers",
    "Wright St. Raiders", "Wyoming Cowboys", "Xavier Musketeers",
    "Yale Bulldogs", "Youngstown St. Penguins"
]


# Dictionary to hold all the data
data = {}

# Populate the dictionary with school names and blank stats
for x in range(0, len(schools)):
    data[x]={
        "Team Rankings Name": schools[x],
        "DraftKings Name": "",
        "FanDuel Name": "",
        "BetMGM Name": "",
        "Pinnacle Name": "",
        "TeamID": ""
    }

# Save the dictionary to a JSON file
with open('College/NCAAB_Teams.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Skeleton JSON file created successfully.")