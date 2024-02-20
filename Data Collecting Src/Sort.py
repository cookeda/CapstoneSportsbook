import os

# Sorts unsorted file containing team stats
# Removes unsorted folder
# Must specify stat as type (ex: Cover, Over, etc)
def sortFile(file, type, location):
    if type == "cover":
        cleanfile("../data/cover/" + location + "/Sorted" + file)
        try:
            with open("../data/cover/" + file, 'r') as r:
                for line in sorted(r):
                    with open("../data/cover/" + location + "/Sorted" + file, 'a') as s:
                        s.write(line)
            cleanfile("../data/cover/" + file)
        except FileNotFoundError:
            print("File not found")

    if type == "over":
        cleanfile("../data/over/" + location + "/Sorted" + file)
        try:
            with open("../data/over/" + file, 'r') as r:
                for line in sorted(r):
                    with open("../data/over/" + location + "/Sorted" + file, 'a') as s:
                        s.write(line)
            cleanfile("../data/over/" + file)
        except FileNotFoundError:
            print("File not found")
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
    sortFile("10YearCover.jl", "cover", "general")
    sortFile("AllTimeCover.jl", "cover", "general")
    sortFile("CurrentSeasonCover.jl", "cover", "general")
    sortFile("10YearOU.jl", "over", "general")
    sortFile("AllTimeOU.jl", "over", "general")
    sortFile("CurrentSeasonOU.jl", "over", "general")
    sortFile("homeCover.jl", "cover", "home")
    sortFile("homeOver.jl", "over", "home")
    sortFile("awayCover.jl", "cover", "away")
    sortFile("awayOver.jl", "over", "away")


if __name__ == '__main__':
    main()