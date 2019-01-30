from random import randint
from PIL import Image
import winsound
import os

class Player:
    def __init__ (self):
        self.lvl = 1
        self.exp = 0
        self.coins = 10
        
    def winGame (self):
        self.exp += 100
        self.coins += 10
        self.checkLevelUp()
        
    def useHint (self):
        self.coins -= 5
        
    def checkLevelUp (self):
        if (self.lvl == 1 and self.exp >= 100) or (self.lvl == 2 and self.exp >= 300):
            print("Congratulations! You have reached a new level!\nReward: 20 Coins")
            self.lvl += 1
            self.coins += 20
    
    def getExp(self):
        return self.exp

    def getLvl(self):
        return self.lvl

    def getCoins(self):
        return self.coins

    
class Word:
    def __init__ (self, word, player, hint1 = None, hint2 = None):
        self.player = player
        self.word = word
        self.checkWord = word.lower()
        self.hangmanWord = []
        self.hintCount = 1
        self.hint1 = hint1
        self.hint2 = hint2
        self.guessedLetters = []
        self.guessesLeft = 7
        self.initializeHangmanWord()

    def initializeHangmanWord (self):
        for letter in self.word:
            if (letter.isalpha()):
                self.hangmanWord.append("_")
            else:
                self.hangmanWord.append(letter)
        
    def replaceLetter (self, letter):
        if (letter.isalpha() == False):
            print("Invalid input!")
            return
        elif (letter in self.guessedLetters):
            print("This letter has already been guessed!")
            return
        elif (letter not in self.checkWord):
            self.wrongGuess(letter)
            return
        for i in range(0,len(self.checkWord),1):
            if self.checkWord[i] == letter:
                self.hangmanWord[i] = letter
        self.guessedLetters.append(letter)
        
    def wrongGuess (self, letter):
        print("Wrong Guess!")
        self.guessedLetters.append(letter)
        self.guessesLeft -= 1
        
    def showFirstHint (self):
        if self.hint1 == None:
            print("No additional hints are available for this word")
            print("")
            return
        print(self.hint1)
        print("")
    
    def hintUsed (self):
        if self.player.coins < 5:
            print("Not enough coins!")
            return
        if (self.hintCount == 3):
            print("Maximum amount of hints used!")
            return
        elif (self.hintCount == 1):
            if self.hint2 == None:
                print("No additional hints are available for this word")
                return
            if '.jpg' in self.hint2 or '.png' in self.hint2:
                image = Image.open(self.hint2)
                image.show()
            elif '.wav' in self.hint2:
                winsound.PlaySound(self.hint2, winsound.SND_FILENAME)
            else:
                print("Additional Hint:", end = ' ')
                print(self.hint2)
            self.player.useHint()
        else:
            for letter in self.checkWord:
                if (self.checkWord.count(letter) <= 2 and letter not in self.hangmanWord):
                    self.player.useHint()
                    self.replaceLetter(letter)
                    break
        self.hintCount += 1
            
    def showHangmanWord (self):
        for letter in self.hangmanWord:
            print(letter, end = " ")
        print()

    def checkWin(self):
        hangmanWord = ""
        for letter in self.hangmanWord:
            hangmanWord += letter
        if (hangmanWord.lower() == self.checkWord):
            print("Correct Answer!")
            print("Your rewards: 100 Exp Points and 10 coins")
            self.player.winGame()
            return True
        elif (self.guessesLeft == 0):
            print("You ran out of guesses!\nTry again next time!")
            return False
        return None

    def showInfo (self):
        print("Guesses Left:", self.guessesLeft)
        print("Wrong Guessed Letters:", end = " ")
        for letter in self.guessedLetters:
            if letter not in self.hangmanWord:
                print(letter, end = " ")
        print()

        
class Hangman:
    def __init__(self):
        self.player = Player()
        self.category = open("Category.txt", "r")
        self.start()
        
    def start (self):
        print("Hello challenger, welcome to Hangman World!")
        print("Choose one of the following modes to play:")
        print("1. Single Player")
        print("2. Two Players (Unlocks at Lvl 2)")
        print("3. Create New Category (Unlocks at Lvl 3)")
        print("\nCurrent Level:", self.player.getLvl(), "\nExp Points:", self.player.getExp(), "\nCoins:", self.player.getCoins(), "\n")
        choice = str(input())
        self.startValidInput(choice)

    def startValidInput (self, choice):
        if (choice == '1'):
            os.system('cls||clear')
            self.singlePlayerStart()
        elif (choice == '2'):
            if (self.player.getLvl() < 2):
                print("You need to reach Level 2 to unlock this mode!\n")
                self.start()
                return
            else:
                os.system('cls||clear')
                self.twoPlayer()
        elif (choice == '3'):
            if (self.player.getLvl() < 3):
                print("You need to reach Level 3 to unlock this mode!\n")
                self.start()
                return
            else:
                os.system('cls||clear')
                self.createCategory()
        else:
            print("Invalid input!\n")
            self.start()
            return

    def singlePlayerStart (self):
        self.category.seek(0)
        categoryList = []
        print("Please type the name of the category you wish to play:")
        for category in self.category:
            category = category.replace('\n','')
            categoryList.append(category.upper())
            print(category)
        print()
        choice = str(input())
        choice = choice.upper()
        while (choice not in categoryList):
            print("This category does not exist")
            choice = str(input())
            choice = choice.upper()
        self.singlePlayer(choice)

    def singlePlayer (self, categoryChosen):
        count = 1
        text = categoryChosen + ".txt"
        category = open(text, "r")
        numWords = int(category.readline())
        randomNum = randint(1,numWords)
        for words in category:
            if count == randomNum:
                words = words.replace('\n','')
                wordInfo = words.split(",")
                word = Word(wordInfo[0], self.player, wordInfo[1], wordInfo[2])
                break
            count += 1
        while (word.checkWin() == None):
            print("Hint:", end = " ")
            word.showFirstHint()
            word.showHangmanWord()
            print()
            word.showInfo()
            print("Level:", self.player.getLvl(), "\nExp Points:", self.player.getExp(), "\nCoins:", self.player.getCoins())
            print("Type hint to use additional hint (costs 5 coins)\n")
            letter = str(input())
            letter = letter.lower()
            if letter == 'hint':
                word.hintUsed()
            else:
                word.replaceLetter(letter)
        
        if self.mainMenu() == True:
            os.system('cls||clear')
            category.close()
            self.start()
        else:
            category.seek(0)
            self.singlePlayer(categoryChosen)
                    
    def twoPlayer (self):
        print("Player 1's Turn")
        while (True):
            print("Please type in the word you want the other player to guess: ")
            word = str(input())
            print("Is this the word you want to let the other player guess? (y/n)")
            print(word)
            choice = str(input())
            choice = choice.lower()
            while (choice != 'y' and choice != 'n'):
                print("Invalid Input!")
                choice = str(input())
                choice = choice.lower()
            if choice == 'y':
                break
            else:
                continue
        print("Hint: ")
        hint = str(input())
        word = Word(word, self.player, hint)
        os.system('cls||clear')
        print("Player 2's Turn")
        while (word.checkWin() == None):
            print("Hint:", end = " ")
            word.showFirstHint()
            word.showHangmanWord()
            print()
            word.showInfo()
            print("Level:", self.player.getLvl(), "\nExp Points:", self.player.getExp(), "\nCoins:", self.player.getCoins())
            letter = str(input())
            word.replaceLetter(letter.lower())
            
        if self.mainMenu() == True:
            os.system('cls||clear')
            self.start()
        else:
            self.twoPlayer()
        
    def mainMenu (self):
        print("Please select what you want to do next:")
        print("1. Main Menu")
        print("2. Continue")
        choice = str(input())
        while (choice != '1' and choice != '2'):
            print("Invalid Input!")
            choice = str(input())
        if choice == '1':
            return True
        else:
            return False

    def createCategory (self):
        words = []
        print("Please enter the name of the category you wish to create:")
        name = str(input())
        name = name + ".txt"
        print("Please enter the number of words in this category")
        num = str(input())
        while (num.isdigit() == False):
            print("Please enter a number!")
            num = str(input())
        print("Please enter the hangman word and its 2 hints separated by a comma.")
        print("For example: word,hint1,hint2")
        print("If you want the hint to be an image or an audio file (must be in .wav format), please put the location of the filename in the hint")
        print("Press enter to type in the next hangman word")
        for i in range (int(num)):
            text = str(input())
            while (len(text) == 0 or ',' not in text or text.count(',') < 2):
                print("Invalid input!")
                text = str(input())
            words.append(text)
        newCategory = open(name, "w")
        newCategory.write(num)
        newCategory.write('\n')
        for word in words:
            newCategory.write(word)
            newCategory.write('\n')
        newCategory.close()
        self.category.close()
        self.category = open("Category.txt", "a")
        self.category.write(name.replace('.txt', ''))
        self.category.write('\n')
        self.category.close()
        self.category = open("Category.txt", "r")
        os.system('cls||clear')
        self.start()
        
Hangman()

        
        
        
