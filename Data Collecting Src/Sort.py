import os

# Sorts unsorted file containing team stats
# Removes unsorted folder
# Must specify stat as type (ex: Cover, Over, etc)
def sortFile(file, type):
    if type == "cover":
        with open("../data/cover/" + file, 'r') as r:
            for line in sorted(r):
                with open("../data/cover/" + "Sorted" + file, 'a') as s:
                    s.write(line)
        os.remove("../data/cover/" + file)

    if type == "over":
        with open("../data/over/" + file, 'r') as r:
            for line in sorted(r):
                with open("../data/over/" + "Sorted" + file, 'a') as s:
                    s.write(line)
        os.remove("../data/over/" + file)

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