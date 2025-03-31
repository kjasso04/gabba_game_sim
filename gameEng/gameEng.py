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


from cards.buffANDdebuff import buffANDdebuff
from cards.crossroad import crossroad
from cards.event import event

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
    
    def addToHand(self, card):
        if isinstance(card, BuffANDdebuff):
            card_type = card.card_type.strip().lower() if isinstance(card.card_type, str) else None
            print(card_type)
            if card_type.lower() == "gcard":
                print("Adding a buff card to hand.")
                self.buffHand.append(card)
                print(self.buffHand)
            elif card_type.lower() == "g/bcard" or card_type.lower() == "bcard":
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
        
    

class oddPlayer(player):
    def __init__(self,instrument, requirements):
        super().__init__( instrument)
        self.req = requirements
        
    


def getRandomItems(data):
    resultList = []
    
    if isinstance(data, dict):
        #print("1")
        data = {k: list(v) if isinstance(v, set) else v for k, v in data.items()}  # Convert sets to lists to allow modification
        #print(data)
        while data:
            randomKey = random.choice(list(data.keys()))
            
            if isinstance(data[randomKey], list):  # Check if value is a list
                item = random.choice(data[randomKey])
                data[randomKey].remove(item)
                resultList.append(item)

                if not data[randomKey]:  # Remove key if list is empty
                    del data[randomKey]
            else:
                resultList.append(data.pop(randomKey))  # Remove single item directly
        
        
    else :
        resultList = random.sample(data, len(data))  # Shuffle list items randomly
    
    #print(str(resultList)+ "\n")
        
    

    return resultList


def setUpPlayer(numPlayer,instrument, reqOdd):
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
            
    
def gettingEventShit():
    return event


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
       
            
        



def main():
    
    #game peraiters
    numPlayer = int(input("how many players: "))
    
    #tiles
    numTiles  = int(input("how many tiles: "))
    startingTileChance = int(input("chance tiles: "))
    
    
    # cross
    includeCrossEvents = bool(input("inlcude cross events: ").lower() =="true" ) 
    includeCrossChoise = bool(input ("inlcude cross choices: ").lower() == "true")
    
    if ( includeCrossEvents):
        mixCrossEvents = bool(input("mix cross events: ").lower() =="true" ) 
    else:
        mixCrossEvents =False
        
    if (includeCrossChoise ):
        mixCrossChoises = bool(input ("mix cross choices: ").lower() == "true")
    else:
        mixCrossChoises =False
    
    #buff and debuff
    #mixBuffAndDebuff = bool(input("mix buffs: ").lower() =="true" ) 
    
    #evets
    useRangeBuffs = bool(input("generate events based on range: ").lower() == "true")
    
    if useRangeBuffs:
        useRangeofCards = int(input("how many generated cards: "))
    else:
        useRangeofCards = None
        
    
    
    #establish decks
    
    tilesDic = tiles.main(numTiles, startingTileChance)
    crossDic = crossroad.main(includeCrossEvents, includeCrossChoise, mixCrossEvents, mixCrossChoises)
    

    
    buffANDdebDic = buffANDdebuff.main()
    eventDic =  gettingEventShit().main(useRangeBuffs, useRangeofCards)
    
    tilesDeck = getRandomItems(tilesDic)
    
    #print ("crossDic: \n")
    
    #print(crossDic)
    
    crossDeck = getRandomItems(crossDic)
    eventDeck = getRandomItems(eventDic)
    
    #print ("crossDeck: \n")
    
    #print(crossDeck)
    
    '''''''''
    print(buffANDdebDic.keys())
    for set in buffANDdebDic.keys():
        for card in buffANDdebDic[set]:
            print(card.displayCard())
    '''''''''
    
    buffDeck = getRandomItems(buffANDdebDic["GCard"])
    debuffDeck = getRandomItems(buffANDdebDic["BCard"])
    buffANDdebuffDeck = getRandomItems(buffANDdebDic["G/BCard"])
    
    discard = {
        0:[], #tiles
        1:[], #crosroads
        2:[], #events
        3:{   #debuffDeck
            0:[], #Buff
            1:[], #Debuff
            2:[]  #B/D
        }, 
        
    }
    
    
    
    def handDecks (dictionary, deckList, discardDeck):
        if ( isinstance(deckList, list)):
            if (len(deckList) == 0):
                if (len(discardDeck) > 0):
                    
                    random.shuffle(discardDeck)
                    newList = discardDeck
                    #print("resuffle newList: " + str(newList))
                    #print("discardDeck: "+ str(discardDeck))
                    return newList
                else:
                    newList = getRandomItems(dictionary)
                    #print("newGen newList: " + str(newList))
                    return newList
                    
        
        else: 
            print("you fuck up")
    
    
    
    
    
    
    
    #/////////running code/////////////
    
    
    listPlayer = setUpPlayer(numPlayer, "instrument" ,  "PlayHolder")
    
    #print ( "listPlayer: " + str(listPlayer) )
    
    isGameComplet = False
    
    
        
    indexPlayer  = -1
    
    

    
    
    while(not isGameComplet):
        
        indexPlayer = (indexPlayer + 1) % numPlayer
        
        print("indexPlayer: " + str(indexPlayer))
        
        currPlayer = listPlayer[indexPlayer]
        
        currCrossRoad = crossDeck[0]
        
        print(currCrossRoad.displayCard())
        
        
        #print(currCrossRoad.displayCard())
        
        crossDeck.pop(0)
        
        
         
        
        action =-1
        
        cardType =""
        currCard = None
        
        while (action != 0 and action != 9):
            
            
            
            
            for dictionary, deck, discard_pile in [
                (tilesDic, tilesDeck, discard[0]),
                (crossDic, crossDeck, discard[1]),
                (eventDic, eventDeck, discard[2]),
                (buffANDdebDic["GCard"], buffDeck, discard[3][0]),
                (buffANDdebDic["BCard"], debuffDeck, discard[3][1]),
                (buffANDdebDic["G/BCard"], buffANDdebuffDeck, discard[3][2]),
            ]:
                if len(deck) == 0:
                    outputdeck = handDecks(dictionary, deck, discard_pile)  # Make sure this returns an iterable
                    
                    if isinstance(outputdeck, list):  # Ensure outputdeck is a list before assigning
                        deck[:] = outputdeck  # Modify the original list in place
                        #print(f"Updated {dictionary} deck: {deck}")
                        discard_pile[:] = []
                    else:
                        print(f"Error: handDecks returned a non-list value: {outputdeck}")

            
            
            action =  int(input("what action| 0: finish turn, 1: move, 2: addCrossroadDebuff, 3: addCard, 4: discard, 5: show buff's, 6: show debuffs, 7: show instrement, 8: show card , 9: finish game  \n"))
            print("\n")
            
            if (action == 1):
                
                drawnTile = tilesDeck[0]
                discard[0].append(drawnTile)
                tilesDeck.pop(0)
                
                print("tile, " + str(drawnTile.color)  + "\n")
                print(drawnTile.displayTiles())
                
                print('\n')
                
                
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
                    
                        
                    
                    
            elif (action == 2):
                currPlayer.addToHand(currCrossRoad)
                
            elif (action == 3):
                
                if (currCard != None):
                    if (cardType == "gcard"):
                        currPlayer.addToHand(currCard)
                        
                    elif(cardType == "g/bcard"):
                        currPlayer.addToHand(currCard)
                        
                        
                    elif (cardType == "bcard"):
                        currPlayer.addToHand(currCard)
                        
                else:
                    print("there is no current card")
                
                currCard =None     
            elif (action == 4):
                remCard = currPlayer.removeHand()
                
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
                
        discard[1].append(currCrossRoad)
        
        if (action ==9):
            isGameComplet = True
        
     
        #action =  int(input("what action| 0: finish turn, 1: move, 2: addCrossroadDebuff, 3: addCard, 4: discard, 5: show buff's, 6: show debuffs, 7: show instrement, 8: show card , 9: finish game  \n"))
           
                
       
                
                
                
                
                
                
                    
                
                
                
            
            
        
if __name__ == "__main__":
    main()
