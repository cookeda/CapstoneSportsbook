import os

# Sorts unsorted file containing team stats
# Removes unsorted folder
# Must specify stat as type (ex: Cover, Over, etc)
def sortFile(file, type):
    if type == "cover":
        cleanfile("../data/cover/general/Sorted" + file)
        with open("../data/cover/" + file, 'r') as r:
            for line in sorted(r):
                with open("../data/cover/general/Sorted" + file, 'a') as s:
                    s.write(line)
        cleanfile("../data/cover/" + file)

    if type == "over":
        cleanfile("../data/over/general/Sorted" + file)
        with open("../data/over/" + file, 'r') as r:
            for line in sorted(r):
                with open("../data/over/general/Sorted" + file, 'a') as s:
                    s.write(line)
        cleanfile("../data/over/" + file)
def cleanfile(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        open(file, 'a')

# Calls all method for each file
def main():
    sortFile("10YearCover.jl", "cover")
    sortFile("AllTimeCover.jl", "cover")
    sortFile("CurrentSeasonCover.jl", "cover")
    sortFile("10YearOU.jl", "over")
    sortFile("AllTimeOU.jl", "over")
    sortFile("CurrentSeasonOU.jl", "over")


if __name__ == '__main__':
    main()