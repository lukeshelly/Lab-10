
# Luke Shelly
# CSEC 1437 
# Lab 10
# Date: 11/04/2026
# Program: ShellyLLab10.py



import requests
import random
import json


# STEP 1: WEBSITE DICTIONARY

SourcesDnary = {
    "Python": "https://www.python.org/",
    "NIST": "https://www.nist.gov/"
}


# STEP 2: CUSTOM WEBSITE LISTS

Custom1List = [
    ("NASA", "https://www.nasa.gov/"),
    ("NOAA", "https://www.noaa.gov/"),
    ("National Archives", "https://www.archives.gov/")
]

Custom2List = [
    ("CISA", "https://www.cisa.gov/"),
    ("FBI", "https://www.fbi.gov/"),
    ("USA.gov", "https://www.usa.gov/")
]


# STEP 3: PICK ONE WEBSITE FROM EACH LIST

Custom1 = random.choice(Custom1List)
Custom2 = random.choice(Custom2List)

SourcesDnary[Custom1[0]] = Custom1[1]
SourcesDnary[Custom2[0]] = Custom2[1]


# STEP 4: ASK USER FOR WORDS

print("WEBSITE WORD SEARCH PROGRAM")

UserInput = input("Enter up to 10 words separated by commas: ")

UserWords = UserInput.split(",")

SearchWords = []

for Word in UserWords:

    Word = Word.strip().lower()

    NewWord = ""

    for Letter in Word:

        if Letter >= "a" and Letter <= "z":
            NewWord += Letter

    if NewWord != "" and len(SearchWords) < 10:
        SearchWords.append(NewWord)


# STEP 5: CREATE RESULTS DICTIONARY

ResultsDnary = {}

TempFile = "ShellyLTemp.html"
ResultsFile = "ShellyLLab10.json"


# STEP 6: PROCESS EACH WEBSITE

for Source, Link in SourcesDnary.items():

    print("\nProcessing:", Source)

    try:

        # Download the website.
        Page = requests.get(Link, timeout=20)
        Page.raise_for_status()

        Page.encoding = "utf-8"

        # Save the webpage.
        with open(TempFile, "w", encoding="utf-8") as File:
            File.write(Page.text)

        # Read the saved webpage.
        with open(TempFile, "r", encoding="utf-8") as File:
            WebContent = File.read()

        WebContent = WebContent.lower()

        Lines = WebContent.splitlines()


        # STEP 7: FIND NON-ALPHABETIC CHARACTERS

        NonAlphaList = []

        for Line in Lines:

            for Character in Line:

                if Character < "a" or Character > "z":

                    if Character.isprintable():

                        if Character not in NonAlphaList:
                            NonAlphaList.append(Character)


        # STEP 8: MAKE A LIST OF WORDS

        AlphaWordsList = []

        for Line in Lines:

            Word = ""

            for Character in Line:

                if Character in NonAlphaList:

                    if Word != "":
                        AlphaWordsList.append(Word)
                        Word = ""

                else:
                    Word += Character

            if Word != "":
                AlphaWordsList.append(Word)


        # STEP 9: REMOVE DUPLICATES AND SORT

        UniqueWords = []

        for Word in AlphaWordsList:

            if Word not in UniqueWords:
                UniqueWords.append(Word)

        UniqueWords.sort()

        NumberOfWords = len(UniqueWords)


        # STEP 10: COUNT USER SEARCH WORDS

        WordCounts = {}

        for Word in SearchWords:

            WordCounts[Word] = AlphaWordsList.count(Word)


        # STEP 11: SAVE WEBSITE RESULTS

        ResultsDnary[Source] = [
            Link,
            NonAlphaList,
            NumberOfWords,
            UniqueWords,
            WordCounts
        ]

        print("Finished:", Source)

    except requests.exceptions.RequestException as Error:

        print("Could not open website:", Source)
        print(Error)


# STEP 12: SAVE RESULTS TO JSON

with open(ResultsFile, "w", encoding="utf-8") as File:

    json.dump(ResultsDnary, File, indent=4)

print("\nResults saved!")


# STEP 13: READ JSON FILE

with open(ResultsFile, "r", encoding="utf-8") as File:

    SavedResults = json.load(File)


# STEP 14: PRINT RESULTS

print("\nWEBSITE WORD SEARCH RESULTS")

print("-" * 90)

print("Source\t\tUnique Words", end="")

for Word in SearchWords:
    print("\t" + Word, end="")

print("\n" + "-" * 90)


for Source, Data in SavedResults.items():

    Link = Data[0]
    NumberOfWords = Data[2]
    WordCounts = Data[4]

    print(Source, "\t\t", NumberOfWords, end="")

    for Word in SearchWords:
        print("\t", WordCounts[Word], end="")

    print()


# PRINT WEBSITE LINKS

print("\nWEBSITE LINKS")

for Source, Data in SavedResults.items():

    print(Source, ":", Data[0])


# PRINT UNIQUE WORDS

print("\nUNIQUE ALPHABETIC WORDS")

for Source, Data in SavedResults.items():

    print("\nWebsite:", Source)

    print("Number of unique words:", Data[2])

    print(", ".join(Data[3]))


print("\nProgram completed!")
