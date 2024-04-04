# Read the contents of the uploaded file
file_path = 'game_results.txt'

# Define a function to apply the star rating logic for Cover and Over Score
def apply_star_rating_cover(cover_rating):
    if cover_rating >= 7:
        return 3
    elif 4 <= cover_rating < 7:
        return 2
    else:
        return 1

def apply_star_rating_over(over_score):
    if over_score >= 8 or over_score <= 2:
        return 3
    elif over_score >= 6 or over_score <= 4:
        return 2
    else:
        return 1

# Read the file and apply the star rating logic
star_ratings = []

def extract_team_to_cover(line):

    """Safely extract the team recommended to cover the spread from a given line."""

    try:

        return line.split("Bet on ")[1].split(" to cover")[0].strip()

    except IndexError:

        return "Team recommendation missing"



corrected_star_ratings_v2 = []


# Re-opening the file to re-process with the corrected logic

with open(file_path, 'r') as file:

    for line in file.readlines():

        if "Cover Rating" in line and "Over Score" in line:

            # Extract game info and team to cover

            game_info = line.split(":")[0].strip()

            team_to_cover = extract_team_to_cover(line)

            

            # Extract Cover Rating and Over Score

            cover_rating = float(line.split("Cover Rating - ")[1].split(",")[0])

            over_score = float(line.split("Over Score - ")[1].split("\n")[0])

            

            # Apply corrected star rating logic

            cover_star = apply_star_rating_cover(cover_rating)

            over_star = apply_star_rating_over(over_score)

            

            corrected_star_ratings_v2.append((game_info, cover_rating, f'Cover Star: {cover_star}', over_score, f'Over Star: {over_star}'))



# Attempting to display the processed results again

print(corrected_star_ratings_v2)