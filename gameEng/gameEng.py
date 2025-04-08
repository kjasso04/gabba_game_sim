import sys
import os
import math

import pandas as pd
import random


#tilesExcel = pd.read_excel('./tiles.xlsx', engine='openpyxl')
sys.path.append(os.path.abspath(".."))



#classes
from cards.buffANDdebuff.buffANDdebuff import Card
from cards.buffANDdebuff.buffANDdebuff import BuffANDdebuff
from cards.crossroad.crossroad import Cross
from cards.crossroad.crossroad import CrossEvents
from cards.crossroad.crossroad import CrossChoise
from cards.iteam.iteam import iteamCard
from adversary.adversary import adversaryCard


#file code
from cards.iteam import iteam
from cards.buffANDdebuff import buffANDdebuff
from cards.crossroad import crossroad
from cards.event import event
from adversary import adversary

from tiles import tiles




class player:
    def __init__(self, instrument):
        self.buffHand = []
        self.debuffHand = []
        self.item = []
        self.coreSpot = []
        self.hasFound = False
        self.isFliped = False
        self.inCrash = False
        self.coreSpot.append(instrument)  # Use append, not push (Python lists don't have push)
        
    #add item to player
    def addItem(self, item):
        self.item.append(item)
        print("added item"+ str(item.name))
    
    def removeItem(self, item):
        if item in self.item:
            self.item.remove(item)
            print("removed item"+ str(item.name))
        else:
            print("item not found")
            
    # buff or debuff to hand
    def addToHand(self, card):
        #print("card\n")
        if isinstance(card, BuffANDdebuff):
            #print("BuffANDdebuff\n")
            card_type = card.card_type.strip().lower() if isinstance(card.card_type, str) else None
            #print(card_type)
            if card_type.lower() == "gcard":
                #print("gcard\n")
                #print("Adding a buff card to hand.")
                self.buffHand.append(card)
                #print(self.buffHand)
            elif card_type.lower() == "g/bcard" or card_type.lower() == "bcard":
                #print("g/bcard or bcard\n")
                self.debuffHand.append(card)
            else:
                print("Error adding to hand")
        elif isinstance(card, Cross):
            self.coreSpot.append(card)
        else:
            print(f"Trying to add {getattr(card, 'type', 'Unknown')}")

    def removeHand(self, userInput =None):
        removedCard = None
        if userInput == None:
            userInput = int(input("buff: 0 ,debuff: 1 ,cancel: 2"))
        
            
        if userInput == 0 and self.buffHand:
            for i, card in enumerate(self.buffHand, 1):
                print(f"{i}\n{card.displayCard()}\n")

            cardIndex = int(input("Which card would you like to discard? ")) - 1
            if 0 <= cardIndex < len(self.buffHand):
                removedCard = self.buffHand[cardIndex]
                del self.buffHand[cardIndex]
            else:
                print("Invalid index.")
                
        elif userInput == 1 and self.debuffHand:
            for i, card in enumerate(self.debuffHand, 1):
                print(f"{i}\n{card.displayCard()}\n")

            cardIndex = int(input("Which card would you like to discard? ")) - 1
            if 0 <= cardIndex < len(self.debuffHand):
                removedCard =self.debuffHand[cardIndex]
                del self.debuffHand[cardIndex]
            else:
                print("Invalid index.")
        else:
            print("Cancelled or no cards available.")
        
        return removedCard
    
    #show elements in hand
    def showBuffHand(self):
        for i, card in enumerate(self.buffHand, 1):
            print(f"{i}\n{card.displayCard()}\n")
        return self.buffHand
    
    
    def showDebuffHand(self):
        for i, card in enumerate(self.debuffHand, 1):
            print(f"{i}\n{card.displayCard()}\n")
        return self.debuffHand
    
    def showCoreSpot(self):
        for i, card in enumerate(self.coreSpot, 1):
            print(f"{i}\n{card.displayCard()}\n")
        return self.coreSpot
    
    
        
    

class oddPlayer(player):
    def __init__(self,instrument, requirements):
        super().__init__( instrument)
        self.req = requirements
        
    

#gette the deck from the result of the main item functions
import random

def getRandomItems(data):
    resultList = []

    # If input is a dictionary
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if isinstance(value, dict):
                # Recursively flatten nested dictionaries
                data[key] = getRandomItems(value)
            elif isinstance(value, set):
                data[key] = list(value)  # Convert sets to lists

        while data:
            randomKey = random.choice(list(data.keys()))
            val = data[randomKey]

            if isinstance(val, list):
                item = random.choice(val)
                val.remove(item)
                resultList.append(item)
                if not val:
                    del data[randomKey]
            else:
                resultList.append(data.pop(randomKey))

    # If it's a set or list (not dict)
    elif isinstance(data, (set, list)):
        resultList = random.sample(list(data), len(data))

    else:
        # Single item, just return in a list
        resultList = [data]

    return resultList



def gettingEventShit():
    return event
       
            
class gameInformation:
    
    numPlayer = 0
    numTiles = 40
    startingTileChance = 80
    includeCrossEvents = True
    includeCrossChoise = True
    mixCrossEvents = True
    mixCrossChoises = True
    useRangeBuffs = True
    useRangeofCards = 50
    

    players = []
        

    
    gameDecks ={
        tiles:[], #tiles
        Cross:[], #crosroads
        event:[], #events repurpuse for monsters
        BuffANDdebuff:[], #buffs and debuffs
        iteamCard:[], #iteams
        adversaryCard:[], #adversary
    }
    
    discard = {
            tiles:[], #tiles
            Cross:[], #crosroads
            event:[], #events repurpuse for monsters
            BuffANDdebuff:[], #buffs and debuffs
            iteamCard:[], #iteams
            adversaryCard:[], #adversary
        }
    
    def __init__(self):
        
        
        self.getPresets(bool(input("use set up presets: ").lower() == "true"))
        
         
        tilesDic = tiles.main(self.numTiles, self.startingTileChance)
        crossDic = crossroad.main(self.includeCrossEvents, self.includeCrossChoise, self.mixCrossEvents, self.mixCrossChoises)
        

        
        buffANDdebDic = buffANDdebuff.main()
        eventDic =  gettingEventShit().main(self.useRangeBuffs, self.useRangeofCards)
        
        adversaryDic = adversary.main()
        
        iteamDic = iteam.main()
        
        #self.tilesDeck = getRandomItems(tilesDic)
        
        #print ("crossDic: \n")
        
        #print(crossDic)
        
        #self.crossDeck = getRandomItems(crossDic)
        #self.eventDeck = getRandomItems(eventDic)
        #self.buffANDdebuffDeck = getRandomItems(buffANDdebDic["GCard"]) + getRandomItems(buffANDdebDic["BCard"]) + getRandomItems(buffANDdebDic["G/BCard"])
        
        
        
        
        ''''''''''
        
        self.numPlayer = 0
        self.numTiles = 40
        self.startingTileChance = 80
        self.includeCrossEvents = True
        self.includeCrossChoise = True
        self.mixCrossEvents = True
        self.mixCrossChoises = True
        self.useRangeBuffs = True
        self.useRangeofCards = 50
        '''''''''''
        
        '''
        self.players = []
        
        self.tilesDeck = []
        self.buffANDdebuffDeck = []
        self.crossDeck = []
        
        self.iteams = []
        self.adversaryDeck = []
        '''
        
        
        
        
        '''
        for key, value in  adversaryDic.items():
            
            print("key: "+str(key))
            for card in adversaryDic[key]:
                print(card.displayCard())
        '''
        
        
        tilesDic = tiles.main(self.numTiles, self.startingTileChance)
        crossDic = crossroad.main(self.includeCrossEvents, self.includeCrossChoise, self.mixCrossEvents, self.mixCrossChoises)
        

        
        buffANDdebDic = buffANDdebuff.main()
        eventDic =  gettingEventShit().main(self.useRangeBuffs, self.useRangeofCards)
        
        
        adversaryDic = adversary.main()
        
        
        self.gameDecks ={
            tiles:getRandomItems(tilesDic), #tiles
            Cross:getRandomItems(crossDic), #crosroads
            event:getRandomItems(eventDic), #events repurpuse for monsters
            BuffANDdebuff:getRandomItems(buffANDdebDic), #buffs and debuffs
            iteamCard:getRandomItems(iteamDic), #iteams
            adversaryCard:[] #adversary
            
        }
        
        self.gameDic ={
            tiles: tilesDic, #tiles
            Cross: crossDic, #crosroads
            event: eventDic, #events repurpuse for monsters
            BuffANDdebuff: buffANDdebDic, #buffs and debuffs 
            iteamCard: iteamDic,
            adversaryCard: adversaryDic
        }
        
        self.discard = {
            tiles:[], #tiles
            Cross:[], #crosroads
            event:[], #events repurpuse for monsters
            BuffANDdebuff:[], #buffs and debuffs
            iteamCard:[],
            adversaryCard:[], #adversary
        }
        
        print("\n setting up game: \n")
       
        
       
        #print ("crossDeck: \n")
        
        #print(crossDeck)
        
        '''
        print(buffANDdebDic.keys())
        for set in buffANDdebDic.keys():
            for card in buffANDdebDic[set]:
                print(card.displayCard())
        '''
    

    def getPresets(self, usePresets):
        
        
        if (usePresets):
            #game peraiters
            self.numPlayer = int(input("how many players: "))
            
        else:
            #create new game
            
            self.numPlayer = int(input("how many players: "))
            
            
            self.numTiles  = int(input("how many tiles: "))
            self.startingTileChance = int(input("chance tiles: "))
            
            
            # cross
            self.includeCrossEvents = bool(input("inlcude cross events: ").lower() =="true" ) 
            self.includeCrossChoise = bool(input ("inlcude cross choices: ").lower() == "true")
            
            if ( self.includeCrossEvents):
                self.mixCrossEvents = bool(input("mix cross events: ").lower() =="true" ) 
            else:
                self.mixCrossEvents =False
                
            if (self.includeCrossChoise ):
                self.mixCrossChoises = bool(input ("mix cross choices: ").lower() == "true")
            else:
                self.mixCrossChoises =False
            
            #buff and debuff
            #mixBuffAndDebuff = bool(input("mix buffs: ").lower() =="true" ) 
            
            #evets
            self.useRangeBuffs =  bool(input("generate events based on range: ").lower() == "true")
            
            if self.useRangeBuffs:
                self.useRangeofCards = int(input("how many generated cards: "))
            else:
                self.useRangeofCards = None
                
     
                
    def handDecks (self,cardType):

        
        if (len(self.gameDecks[cardType]) == 0):
            if (len(self.discard[cardType]) > 0):
                
                
                newList = random.shuffle(self.discard[cardType])
                #print("resuffle newList: " + str(newList))
                #print("discardDeck: "+ str(discardDeck))
                self.discard[cardType][:] = []
                return newList
            else:
                newList = getRandomItems(self.gameDic[cardType])
                #print("newGen newList: " + str(newList))
                return newList
        
    
    
    
    
    
    
    
    
    def setUpPlayer(self,numPlayer,instrument, reqOdd):
        listPlayer =[]
        
        for i in range(numPlayer):
            listPlayer.append(player(instrument))
            
        oddPlayerIndex= random.choice(range(len(listPlayer)))

        listPlayer[oddPlayerIndex] = oddPlayer(instrument, reqOdd)
        
        return listPlayer



    def manageHand(player, handType):
        
        if (handType == 0):
            if (len(player.buffHand()) > 0):
                player.removeHand(0)
        
        elif (handType == 1): #debuff
            if (len(player.buffHand()) > 0):
                player.removeHand(0)
                
        

    def handEventCards(eventCard):
                
        eventCard.displayCard()
        
        while(True):
            outcome = int(input("what is the out come 1 or 2:  "))
            if (outcome == 1):
                print("\n")
                print()
                return  eventCard.event_typeA.lower()
            elif (outcome == 2):
                print("\n")
                return eventCard.event_typeB.lower()

        
    
        
    def discardHandle(self, disIteam):
        if isinstance(disIteam, Card) or isinstance(disIteam, tiles):
            self.discard[type(disIteam)].append(disIteam)
        else:
            print("invalid input")

            
        
        
    def drawCard(self):
        while True:
            deckNumber = int(input("which deck do you want to draw from| avdersay 1, iteams: 2, Buff or Debuff: 3, crossroad: 4, cancel: 5"))
            if deckNumber == 1:
                
                return self.gameDecks[adversary].pop(0)if  self.gameDecks[adversary] else None
            elif deckNumber == 2:
                return self.gameDecks[BuffANDdebuff].pop(0) if self.gameDecks[BuffANDdebuff] else None
            elif deckNumber == 3:
                return self.gameDecks[iteamCard].pop(0) if self.gameDecks[iteamCard] else None
            elif deckNumber == 4:
                return self.gameDecks[Cross].pop(0) if self.gameDecks[Cross] else None
            elif deckNumber == 5:
                print("cancled")
                return None
            else:
                print("Invalid deck number")
                

    def main(self):
        pass    
    
        
def handTiles(gameStore,tile):
    currCard = ""
    if tile.color == "RED":
        return (gameStore.gameDecks[adversary].pop(0))
    
        

        #discard[3][0].append( buffDeck[0])
        #buffDeck.pop(0)
        
    elif tile.color == "YELLOW":
        return (gameStore.gameDecks[iteam].pop(0))
        
    
    elif tile.color == "MAGENTA":
    
        return (gameStore.gameDecks[BuffANDdebuff].pop(0))
    
    return currCard
    
    
    


def main():
    
    #gameStorage.getPresets(bool(input("use set up presets: ").lower() == "true"))
    
    '''
    # Game parameters
    numPlayer = 4  # Number of players

    # Tile settings
    numTiles = 40  # Total number of tiles on the board
    startingTileChance = 80  # Chance (%) for a tile to be active at the start

    # Cross event settings
    includeCrossEvents = True  # Include cross events in the game
    includeCrossChoice = True  # Include choices during cross events

    if includeCrossEvents:
        mixCrossEvents = True  # Mix the order of cross events
    else:
        mixCrossEvents = False

    if includeCrossChoice:
        mixCrossChoices = True  # Mix the order of cross choices
    else:
        mixCrossChoices = False

    # Buff/Debuff settings
    # mixBuffAndDebuff = False  # Enable this if buffs/debuffs should be mixed

    # Event generation
    useRangeBuffs = True  # Generate events based on player range or tile index

    if useRangeBuffs:
        useRangeofCards = 50  # Number of generated cards based on range
    else:
        useRangeofCards = None
    '''

    
    #establish decks
    
    
    
    
    
    
    
            
    #def readTitelTypes()
    
    
            
            
        
    
    
    
    
    
    
    
    #/////////running code/////////////
    gameStorage = gameInformation()
    
    
    listPlayer = gameStorage.setUpPlayer(gameStorage.numPlayer, "instrument", "placeHolder")
    
    gameStorage.players[:] = listPlayer
    #print ( "listPlayer: " + str(listPlayer) )
    
    isGameComplet = False
    
    print("alltypes")
    for card in gameStorage.gameDecks[BuffANDdebuff]:
        print(card.displayCard())
    
    
        
    indexPlayer  = -1
    print ("idmam: " + str(gameStorage.numPlayer))
    for i in range(gameStorage.numPlayer):
        gameStorage.players.append(player("placeHolder"))
        
    

    
    
    while(not isGameComplet):
        
        
        
        indexPlayer = (indexPlayer + 1) % gameStorage.numPlayer
        
        print("indexPlayer: " + str(indexPlayer))
        
        currPlayer = gameStorage.players[indexPlayer]
        
        currCrossRoad = gameStorage.gameDecks[Cross][0]
        
        print(currCrossRoad.displayCard())
        
        
        #print(currCrossRoad.displayCard())
        
        gameStorage.gameDecks[Cross].pop(0)
        
        
         
        
        action =-1
        
        cardType =""
        currCard = None
        
        while (action != 0 and action != 9):
            for keys, vales in gameStorage.gameDecks.items():

                
                if len(vales) == 0:
                    outputdeck = gameStorage.handDecks(keys)  # Make sure this returns an iterable
                    
                    if isinstance(outputdeck, list):  # Ensure outputdeck is a list before assigning
                        gameStorage.gameDecks[keys][:] = outputdeck  # Modify the original list in place
                        #print(f"Updated {dictionary} deck: {deck}")
                        gameStorage.discard[keys][:] = []
                    else:
                        print(f"Error: handDecks returned a non-list value: {outputdeck}")

            
            
            action =  int(input("what action| 0: finish turn, 1: move, 2: addCrossroadDebuff, 3: addCard, 4: discard, 5: show buff's, 6: show debuffs, 7: show instrement, 8: show card , 9: finish game  \n"))
            print("\n")
            
            if (action == 1):
                
                drawnTile = gameStorage.gameDecks[tiles].pop(0)
                gameStorage.discard[tiles].append(drawnTile)
                
                
                print("tile, " + str(drawnTile.color)  + "\n")
                print(drawnTile.displayTiles())
                
                currCard = handTiles(gameStorage,drawnTile )
                
                
                
                print('\n')
                
                '''''''''
                if drawnTile.color == "GREEN":
                    currCard = (buffDeck[0])
                    #currPlayer.addToHand(currCard)
                    cardType = "gcard"
                    
   
                    #discard[3][0].append( buffDeck[0])
                    #buffDeck.pop(0)
                
                    
                    
                elif drawnTile.color == "RED":
                    currCard = (debuffDeck[0])
                    #currPlayer.addToHand(currCard)
                    cardType = "bcard"

                    #if (len(player.buffHand()) > 0):
                    #    remvedCard = currPlayer.removeHand(0)
                    
                    #discard[3][1].append( debuffDeck[0])
                    #debuffDeck.pop(0)
                    
                elif drawnTile.color == "MAGENTA":
                    currCard =(buffANDdebuffDeck[0])
                    #currPlayer.addToHand(currCard)
                    cardType = "g/bcard"
                    
                    #discard[3][2].append( buffANDdebuffDeck[0])
                    #buffANDdebuffDeck.pop(0)
                
                elif drawnTile.color == "CYAN":
                    
                    eventCard = eventDeck[0]
                    
                    eventOutcome = handEventCards(eventCard)
                    
                    if  eventOutcome == "gcard":
                        print ("buffDeck")
                        card = (buffDeck[0])
                        #currPlayer.addToHand(currCard)
                        
                        print(card.displayCard() + "\n")
                        
                    elif eventOutcome == "bcard":
                        print ("bcard: "+ str(debuffDeck))
                        card = (debuffDeck[0])
                        #currPlayer.addToHand(currCard)
                        
                        print(card.displayCard() + "\n")

                    elif eventOutcome == "g/bcard":
                        
                        print( "buffANDdebuffDeck: " + str(buffANDdebuffDeck))
                        card = (buffANDdebuffDeck[0])
                        #currPlayer.addToHand(currCard)
                        
                        print(card.displayCard() + "\n")
                    else:
                        card = None
                    
                    currCard = card
                    
                    
                    discard[2].append(eventDeck[0])
                    eventDeck.pop(0)
                '''''''''
                    
                        
                    
                    
            elif (action == 2):
                currPlayer.addToHand(currCrossRoad)
                
            elif (action == 3):
                
                #print(str(type(currPlayer)) + "\n")
                
                if (currCard != None):
                    #print("card Not none\n")
                    currPlayer.addToHand(currCard)
                    
                        
                else:
                    print("there is no current card")
                
                currCard =None     
            elif (action == 4):
                
                remCard = currPlayer.removeHand()
                gameStorage.discardHandle(remCard)
                
                '''''''''
                if (remCard):
                    
                    if (remCard.card_type.lower() == "gcard"):
                        discard[3][0].append( remCard)
                        buffDeck.pop(0)
                        
                        
                    elif remCard.card_type.lower() == "bcard":
                        discard[3][1].append( remCard)
                        buffDeck.pop(0)
                        
                        
                    elif  remCard.card_type.lower() == "g/bcard":
                        discard[3][2].append( buffANDdebuffDeck[0])
                        buffANDdebuffDeck.pop(0)
                '''''''''
                
                
            elif (action == 5):
                for card in currPlayer.buffHand:
                    print(card.displayCard())
                    print("\n")
                    
            elif(action == 6):
                for card in currPlayer.debuffHand:
                    print(card.displayCard())
                    print("\n")
                    
            elif(action == 7):
                print(currPlayer.coreSpot)
                print("\n")
                
            elif(action == 8):
                if (currCard):
                    print(currCard.displayCard())
                else:
                    print("no current card \n")
                
            elif(action == 9):
                break
            
            elif (action == 0):
                print("next Player \n")
            else:
                print("not a valid input")
                
        gameStorage.discard[Cross].append(currCrossRoad)
        
        if (action ==9):
            isGameComplet = True
        
     
        #action =  int(input("what action| 0: finish turn, 1: move, 2: addCrossroadDebuff, 3: addCard, 4: discard, 5: show buff's, 6: show debuffs, 7: show instrement, 8: show card , 9: finish game  \n"))
           
                
       
                
                
                
                
                
                
                    
                
                
                
            
            
        
if __name__ == "__main__":
    main()
