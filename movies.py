# Jordan Coats
# Final Project
# 5/1/2019

# The objective of this project is to write a program in Python that will read in a data
# file with movies that were released between 2000 and 2009 and display information
# requested by the user.

# The general outline was adapted from the World Series lab.


def openFile():
    # To open the file
    goodFile = False
    while goodFile == False:
        fname = input("Enter file name: ")
        try:
            movieFile = open(fname, "r")
            goodFile = True
        except IOError:
            print("Invalid filename, please try again.")
    return movieFile


def getData():
    # This function will get the data from the data file - be sure to look at the format of the data in the
    # file and read each line as we did with the phone search program in class.
    # The function should return the list of title, genre, runtime, mpaa_rating, studio, thtr_rel_year.
    movieFile = openFile()
    titleList = []
    genreList = []
    runtimeList = []
    ratingList = []
    studioList = []
    yearList = []
    # Skips the first line with header data
    movieFile.readline()
    for line in movieFile:
        line = line.strip()
        title, genre, runtime, mpaa_rating, studio, thtr_rel_year = line.split(",")
        titleList.append(title)
        genreList.append(genre)
        runtimeList.append(int(runtime))
        ratingList.append(mpaa_rating)
        studioList.append(studio)
        yearList.append(int(thtr_rel_year))
    movieFile.close()
    return (titleList, genreList, runtimeList, ratingList, studioList, yearList)


def getChoice():
    # This function displays the menu of choices for the user.
    # It reads in the user's choice and returns it as an integer.
    print("\n")
    print("Make a selection from the following choices:\n")
    print("1 - Find all films of a certain genre")
    print("2 - Find all films with a certain rating")
    print("3 - Find the longest film made by a specific studio")
    print("4 - Search for a film by title")
    print("5 - Find average runtime of all films made in a given year range")
    print("6 - Sort all lists by runtime and write the results to a new file")
    print("7 - Find Studio with most movies")
    print("8 - Quit\n")
    while True:
        try:
            choice = int(input("Enter your choice --> "))
            if choice > 8 or choice < 1:
                raise ValueError
            print("")
            return choice
        except ValueError:
            print("Please enter a number from above.")
    print("")


def findTarget(targetList, targetType):
    # Locates targets in a list and returns their index. Parameters are a list and what it is looking for.
    index = []
    value = False
    while value == False:
        try:
            # By formatting the input with targetType this function can be used for both option 1 and 2.
            target = input("Enter {0}: ".format(targetType))
            if target not in targetList:
                raise ValueError
            else:
                value = True
        except ValueError:
            print("{0} is not a valid choice.".format(target))

    for i in range(len(targetList)):
        if targetList[i] == target:
            index.append(i)
    return index


def findLongest(studioList, runtimeList):
    # Finds the movie with the longest runtime and returns the index. Parameters are the studios and runtimes.
    index = []
    value = False
    while value == False:
        try:
            target = input("Enter studio name: ")
            if target not in studioList:
                raise ValueError
            else:
                value = True
        except ValueError:
            print("{0} is not a valid choice.".format(target))
    longestMovie = 0
    location = 0
    for i in range(len(runtimeList)):
        if studioList[i] == target:
            if (runtimeList[i]) > longestMovie:
                longestMovie = runtimeList[i]
                location = i
    index.append(location)
    return index


def binaryTitle(titleList):
    # This code is adapted from the phone binary search.
    # Uses binary search to find a single movie title's index from the title list.
    index = []
    value = False
    while value == False:
        try:
            title = input("Enter title: ")
            if title not in titleList:
                raise ValueError
            else:
                value = True
        except ValueError:
            print("{0} is not a valid choice.".format(title))
    # left side of list
    left = 0
    # right side of the list
    right = len(titleList) - 1
    found = 0
    while right >= left and found == 0:
        # find the middle of the list
        location = (left + right) // 2
        if titleList[location] == title:
            found = 1
        elif title < titleList[location]:
            right = location - 1
        else:
            left = location + 1
    else:
        index.append(location)
        return index


def getYear(yearList, prevYear, entry):
    # Gets the year for the avgYearRun function by taking in the year list (for validity), the previous year (zero if first time), and then the actual entry year.
    value = False
    while value == False:
        try:
            # Format handles this function so that it can be used for both years.
            year = int(input("Enter the {0} year: ".format(entry)))
            # Checks to make sure that the previous year isn't greater, prevYear defaults to zero for first year.
            if year < prevYear:
                raise ValueError
            # Validates the year.
            elif year in yearList:
                value = True
            else:
                raise ValueError
            return year
        except ValueError:
            print("Input is not valid.")


def avgYearRun(yearList, runtimeList, yearOne, yearTwo):
    # Takes the two years, grabs all data inbetween them, averages it from the two years and the range of runtime.
    summation = []
    for i in range(len(yearList)):
        if yearOne + i <= yearTwo:
            for j in range(len(yearList)):
                if yearList[j] == yearOne + i:
                    summation.append(runtimeList[j])
    # Using sum() to add all the numbers up and then dividing by the len()
    average = sum(summation) / len(summation)
    return average


def bubbleSort(theList):
    # bubbleSort from Sample Code, adapted to give indexes instead from whatever list is input.
    # bubbleSort takes everything one by one and sorts each "bubble" of two if they aren't in order.
    # It is not the most efficent sort but the code is simple to manipulate for our purpose.
    index = []
    # Makes a copy of the list so it doesn't motify the actual list.
    newList = theList.copy()
    # Feeds the index list the length of theList
    for i in range(0, len(newList)):
        index.append(i)
    for n in range(0, len(newList)):
        # Modified bubbleSort to also sort the index list the same way.
        temp = 0
        tempIndex = 0
        for i in range(1, len(newList)):
            temp = newList[i]
            tempIndex = index[i]
            # comparison
            if newList[i] < newList[i - 1]:
                # swap
                newList[i] = newList[i - 1]
                newList[i - 1] = temp
                index[i] = index[i - 1]
                index[i - 1] = tempIndex
    return index


def sortRuntime(
    theIndex, titleList, genreList, runtimeList, ratingList, studioList, yearList
):
    # After the bubbleSort has the index we now just take everything in and write it using the index list as the key.
    outName = input("Enter name of output file: ")
    outFile = open(outName, "w")
    # Writes the same header line so that the output list can be used by the program as well.
    outFile.write("title,genre,runtime,mpaa_rating,studio,thtr_rel_year" + "\n")
    for i in range(0, len(yearList)):
        outFile.write(
            titleList[theIndex[i]]
            + ","
            + genreList[theIndex[i]]
            + ","
            + str(runtimeList[theIndex[i]])
            + ","
            + ratingList[theIndex[i]]
            + ","
            + studioList[theIndex[i]]
            + ","
            + str(yearList[theIndex[i]])
            + "\n"
        )
    outFile.close()
    print("Your file has been created.")


def printMovies(
    index, titleList, genreList, runtimeList, ratingList, studioList, yearList
):
    # Prints most functions out with a varying width of columns by whatever index key it is given.
    print("The films that meet your criteria are: \n")
    print(
        "{0:<45}{1:<10}{2:<5}{3:<10}{4:<30}{5:<}".format(
            "TITLE", "GENRE", "TIME", "RATING", "STUDIO", "YEAR"
        )
    )
    for i in range(len(index)):
        print(
            "{0:<45}{1:<10}{2:<5}{3:<10}{4:<20}{5:<}".format(
                titleList[index[i]],
                genreList[index[i]],
                runtimeList[index[i]],
                ratingList[index[i]],
                studioList[index[i]],
                yearList[index[i]],
            )
        
        )

def mostMovies(studioList):
    # Finds the studio that appears the most in the list using the python's count function.
    # Keeps track of how many counts there are for the most counted.
    temp = 0
    for i in range(len(studioList)):
        # freq is the count of times a studio appears in the list for each poisiton.
        freq = studioList.count(studioList[i])
        # if the freq overcomes the temp then it is replaced so that next time it will be compared to the new highest.
        if freq > temp:
            temp = freq
            # makes the studio to studioList[i] so it holds the name of the most counted until replaced or returned.
            studio = studioList[i]
    return studio


def main():
    titleList, genreList, runtimeList, ratingList, studioList, yearList = getData()
    # Call the function to get the data from the data file and store the results in 7 lists.
    choice = getChoice()
    while choice != 8:
        if choice == 1:
            genreIndex = findTarget(genreList, "genre")
            printMovies(
                genreIndex,
                titleList,
                genreList,
                runtimeList,
                ratingList,
                studioList,
                yearList,
            )
            choice = getChoice()
        elif choice == 2:
            ratingIndex = findTarget(ratingList, "rating")
            printMovies(
                ratingIndex,
                titleList,
                genreList,
                runtimeList,
                ratingList,
                studioList,
                yearList,
            )
            choice = getChoice()
        elif choice == 3:
            longestIndex = findLongest(studioList, runtimeList)
            printMovies(
                longestIndex,
                titleList,
                genreList,
                runtimeList,
                ratingList,
                studioList,
                yearList,
            )
            choice = getChoice()
        elif choice == 4:
            titleIndex = binaryTitle(titleList)
            printMovies(
                titleIndex,
                titleList,
                genreList,
                runtimeList,
                ratingList,
                studioList,
                yearList,
            )
            choice = getChoice()
        elif choice == 5:
            print("Please enter the years in chronological order: ")
            yearOne = getYear(yearList, 0, "first")
            yearTwo = getYear(yearList, yearOne, "second")
            average = avgYearRun(yearList, runtimeList, yearOne, yearTwo)
            print(
                # Limits the average to only two decimal places.
                "The average runtime between {0} and {1} is {2:.2f} minutes long.".format(
                    yearOne, yearTwo, average
                )
            )
            choice = getChoice()
        elif choice == 6:
            theIndex = bubbleSort(runtimeList)
            sortRuntime(
                theIndex,
                titleList,
                genreList,
                runtimeList,
                ratingList,
                studioList,
                yearList,
            )
            choice = getChoice()
        elif choice == 7:
            print(
                "The studio with the most movies is {0}.".format(mostMovies(studioList))
            )
            choice = getChoice()
        else:
            print("Choice not valid.")
            choice = getChoice()
    print("Good-bye")


# Auto starts the program.
main()
