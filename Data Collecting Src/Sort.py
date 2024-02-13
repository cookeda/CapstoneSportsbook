import os

# Sorts unsorted file containing team stats
# Removes unsorted folder
# Must specify stat as type (ex: Cover, Over, etc)
def sortFile(file, type, location):
    if type == "cover":
        cleanfile("../data/cover/" + location + "/Sorted" + file)
        with open("../data/cover/" + file, 'r') as r:
            for line in sorted(r):
                with open("../data/cover/" + location + "/Sorted" + file, 'a') as s:
                    s.write(line)
        cleanfile("../data/cover/" + file)

    if type == "over":
        cleanfile("../data/over" + location + "Sorted" + file)
        with open("../data/over/" + file, 'r') as r:
            for line in sorted(r):
                with open("../data/over/" + location + "/Sorted" + file, 'a') as s:
                    s.write(line)
        cleanfile("../data/over/" + file)
def cleanfile(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        open(file, 'a')

# Calls all method for each file
def main():
    sortFile("10YearCover.jl", "cover", "general")
    sortFile("AllTimeCover.jl", "cover", "general")
    sortFile("CurrentSeasonCover.jl", "cover", "general")
    sortFile("10YearOU.jl", "over", "general")
    sortFile("AllTimeOU.jl", "over", "general")
    sortFile("CurrentSeasonOU.jl", "over", "general")
    sortFile("homeCover.jl", "cover", "home")
    sortFile("homeOver.jl", "over", "home")


if __name__ == '__main__':
    main()