import os

# Sorts unsorted file containing team stats
# Removes unsorted folder
# Must specify stat as type (ex: Cover, Over, etc)
def sortFile(file, type, location, league):
    if type == "cover":
        cleanfile("../data/" + league + "/cover/" + location + "/Sorted" + file)
        try:
            with open("../data/" + league + "/cover/" + file, 'r') as r:
                for line in sorted(r):
                    with open("../data/" + league + "/cover/" + location + "/Sorted" + file, 'a') as s:
                        s.write(line)
            cleanfile("../data/" + league + "/cover/" + file)
        except FileNotFoundError:
            print("File not found " + file)

    if type == "over":
        cleanfile("../data/" + league + "/over/" + location + "/Sorted" + file)
        try:
            with open("../data/" + league + "/over/" + file, 'r') as r:
                for line in sorted(r):
                    with open("../data/" + league + "/over/" + location + "/Sorted" + file, 'a') as s:
                        s.write(line)
            cleanfile("../data/" + league + "/over/" + file)
        except FileNotFoundError:
            print("File not found: " + file)
def cleanfile(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        open(file, 'a')


# Calls all method for each file
# TODO: Make it to where sortFile scans for all available files and sorts them
# TODO: IE: 1 line of code that calls sortFile and sorts everything regardless of what is there or not
# TODO: This will make it easier when implementing new data
# TODO: Maybe do this same in alg.py?
def main():
    i = 0
    league = "NBA"
    while i < 3:
        sortFile("10YearCover.jl", "cover", "general", league)
        sortFile("AllTimeCover.jl", "cover", "general", league)
        sortFile("CurrentSeasonCover.jl", "cover", "general", league)
        sortFile("10YearOU.jl", "over", "general", league)
        sortFile("AllTimeOU.jl", "over", "general", league)
        sortFile("CurrentSeasonOU.jl", "over", "general", league)
        sortFile("homeCover.jl", "cover", "home", league)
        sortFile("homeOver.jl", "over", "home", league)
        sortFile("awayCover.jl", "cover", "away", league)
        sortFile("awayOver.jl", "over", "away", league)
        i += 1
        if i == 1:
            league = "CBB"
        elif i == 2:
            league = "MLB"

if __name__ == '__main__':
    main()