import datetime
from difflib import SequenceMatcher

#Divided things into functions to make it easier to manage. The sentenceChecker function is used if the user wants to input a sentence. It then formats the sentence to be ready for spellchecking before returning an array of every word of the sentence.
def sentenceChecker():
    sentence = input("Enter sentence to spellcheck: ") #The user enters a sentence and it's stored in a variable.
    print("The sentence you entered was " + sentence)
    sentence = str.lower(sentence) #Turns all letters into lower case ones. That way they match the case of the words in the dictionary.
    words = sentence.split() #The sentence is divided into an array of words.
    words = sentenceFormatter(words)#Function to get rid of all the non alpha characters.
    return words

def fileChecker():
    filePath = input("Enter the directory path to the file to spellcheck: ") #The user enters a sentence and it's stored in a variable.
    print("The directory path you entered was " + filePath)

    file = open(filePath,"r")
    fileSentences = file.read()
    file.close()
    
    fileSentences = str.lower(fileSentences) #Turns all letters into lower case ones. That way they match the case of the words in the dictionary.
    words = fileSentences.split() #The sentence is divided into an array of words.My Name is The Kira of the 1999Diamond was Unbreakabl5e
    words = sentenceFormatter(words)
    return words #Then returns the list of words to the rest of the program for it to be used.


def sentenceFormatter(array):
    #sentence formatting block. Gets rid off all the non alpha characters.
    for i in range(0,len(array)):
        fixedWord = "" #Start with empty string that gets added to everytime there's a letter present. Hence ignoring the rest of the characters.
        for j in range(0,len(array[i])):
            if(str.isalpha(array[i][j])):
                fixedWord=fixedWord + array[i][j]
        array[i] = fixedWord #After getting all the alpha characters and ignoring all the non-alpha characters, it replaces the original word with the new one.
    array = list(filter(None,array)) #The filter() function gets rid of any empty string elements in the array.
    return array #Then returns the list of words to the rest of the program for it to be used.


def wordMatch(words):
    dictionary = open("dictionary.txt","r")
    dic = dictionary.read().split() #The dictionary is turned into an array of words so it's easier to compare it to the sentence the user has inputted.
    dictionary.close()

    #Variables for statistics
    correct = 0
    ignored = 0
    added = 0
    marked = 0
    
    startTime = datetime.datetime.now()
    for i in range(0,len(words)):
        speltCorrectly = False  #This variable is to determine whether the current word is in the dictionary or not. This also resets the variable for each word so it can test each word seperately.
        for j in range(0,len(dic)):
            if words[i]==dic[j]:
                correct = correct + 1
                speltCorrectly = True #The word is compared to every word in the dictionary with a linear search as it's much more simpler than looking at the word letter by letter or using a binary search. If it finds a match, the variable becomes True.
        if speltCorrectly == False:
            print()
            print(words[i] + " not found in dictionary.")
            replaced=False #This variable lets the program know if the word it's looking at has been replaced by a different word. Once it becomes True, the program knows to move onto the next word.
            for j in range(0,len(dic)): #Look at each word that might be a possible replacement and ask the user if they want to replace the word. If not, then the word will be marked.
                score = SequenceMatcher(None, words[i], dic[j]).ratio()
                if score>=0.8 and replaced==False:#0.8 is a good number to get words that are quite similar but not too high that it'll struggle to find replacements.
                    replaceLoop=True
                    while replaceLoop==True:
                        replace = input("Do you wish to replace " + words[i] + " with " + dic[j] + "? Y/N  ")
                        if str.lower(replace)=="y":
                            words[i] = dic[j]
                            replaced=True
                            replaceLoop=False
                        elif str.lower(replace)=="n":
                            replaceLoop=False

            if replaced==False:
                marking=True
                while marking==True:
                    print("1. Ignore the word\n2. Mark the word as incorrect\n3. Add word to dictionary.")
                    markChoice = input("Enter choice: ")
                    if markChoice=="1":         #If statements to determine how the incorrect word should be marked as the user doesn't want to replace the word.
                        words[i] = "!" + words[i] + "!"
                        marking = False
                        ignored = ignored + 1
                    elif markChoice=="2":
                        words[i] = "?" + words[i] + "?"
                        marking = False
                        marked = marked + 1
                    elif markChoice=="3":
                        dictionary = open("dictionary.txt","a")
                        dictionary.write("\n" + words[i])
                        words[i] = "*" + words[i] + "*"
                        marking = False
                        added = added + 1
            
    endTime = datetime.datetime.now()#Calculations to determine the time it took to spellcheck.
    elapsedTime = endTime - startTime
    elapsedTime = elapsedTime.total_seconds()
    print("\nTotal elapsed time: " + str(elapsedTime) + " seconds")#Printing out all the statistics about the spellchecking process.
    print("Number of words: " + str(len(words)))
    print("Number of correctly spelt words: " + str(correct))
    print("Number of incorrectly spelt words: " + str(len(words) - correct))
    print("\nNumber of ignored words: " + str(ignored))
    print("Number of marked words: " + str(marked))
    print("Number of words added to dictionary: " + str(added))

    if spellOption=="file":
        spellCheckedFile(words,correct,ignored,added,marked)
    if spellOption=="sentence":
        new_sentence = "" #Create a new sentence as python would print each word on a seperate line if I try to use the for loop to print out the sentence.
        for i in range(0,len(words)):
            new_sentence = new_sentence + words[i] + " "
        print(new_sentence)


def spellCheckedFile(content,correct,ignored,added,marked): #Simple function that creates a new file and writes down the spellchecked version of the previous file and a few statistics.
    file = open("SpellcheckedFile.txt","w")
    file.write(str(datetime.datetime.now().strftime("%c")))#Writes down date and time. Change the %c if a different format of date and time is required.
    file.write("\nNumber of words: " + str(len(words)) + "\nNumber of correctly spelt words: " + str(correct) + "\nNumber of incorrectly spelt words: " + str(len(words) - correct) + "\nNumber of ignored words: " + str(ignored) + "\nNumber of marked words: " + str(marked) + "\nNumber of words added to dictionary: " + str(added) + "\n\n")
    for i in range(0,len(content)):#Small loop to input all the data from the array into the file.
        file.write(content[i] + " ")
    file.close()


#Start of the Program
repeat = True #Variable to keep the app going until the user wants to quit.
while repeat==True:
    spellOption="repeat"#This variable lets the while loop know to continuously repeat until a valid choice has been made.
    while spellOption=="repeat":
        print("\nSPELL CHECKER\n\n1. Check a sentence\n2. Check a file")
        optionChoice = input("\nEnter a choice: ")
        if optionChoice == "1":
            words = sentenceChecker()#After a valid choice is made, one of two functions is activated. The sentence one or the file one, depending on their choice.
            spellOption="sentence"#This variable lets the program know whether it will have to create a new text document or not. It'll create one for a file but not for a sentence.
        elif optionChoice == "2":
            words = fileChecker()
            spellOption="file"
        else:
            print("Please enter a valid input.")#Error message.

    wordMatch(words) #Function to spellcheck the words given by the user by matching each word to the dictionary.
    
    quit = input("\nPress q [enter] to quit or any other key [enter] to go again: ")
    if quit=="q":
        repeat=False
