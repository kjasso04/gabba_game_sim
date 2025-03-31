import sys
import os
import math
import pandas as pd
import random

# Import the Card class from the specified module
from cards.cardClass import Card  

# Get the directory where this script is located
file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct proper paths for the Excel files
crafted_events_path = os.path.join(file_dir, "craftedEvent.xlsx")
range_event_path = os.path.join(file_dir, "rangeEvent.xlsx")

# Load Excel Data using pandas
craftedEvents = pd.read_excel(crafted_events_path, engine="openpyxl")
rangeEvent = pd.read_excel(range_event_path, engine="openpyxl")

# Define the Event class, inheriting from Card
class Event(Card):
    def __init__(self, event_typeA, event_typeB, requiredRoll, canIgnor, ignorRoll, chance, name=None, des=None):
        self.event_typeA = event_typeA
        self.event_typeB = event_typeB
        self.requiredRoll = requiredRoll
        self.canIgnor = canIgnor
        self.ignorRoll = ignorRoll
        self.chance = chance
        self.name = name
        self.des = des
    
    # Method to display card details
    def displayCard(self):
        print('\n')
        
        if self.name:
            print("name: " + str(self.name) + '\n')
        
        if self.des:
            print("description: " + str(self.des) + '\n')
        
        print("event_typeA: " + self.event_typeA + '\n')
        print("event_typeB: " + self.event_typeB + '\n')
        print("requiredRoll: " + str(self.requiredRoll) + '\n')
        print("canIgnor: " + str(self.canIgnor) + '\n')
        if self.canIgnor:
            print("ignorRoll: " + str(self.ignorRoll) + '\n')
        print("chance: " + str(self.chance) + '\n')
        
# Function to determine probability-based boolean outcome
def getBoolonChance(chance):
    """Returns True with a probability of `chance%`."""
    return random.random() < (float(chance) / 100)

# Function to allocate cards based on chances
def allocate_parts(numCards, chances):
    """
    Allocates numCards into groups based on percentage chances, ensuring total remains consistent.
    
    :param numCards: Total number to distribute (can be a string or number)
    :param chances: List of percentage values
    :return: List of allocated numbers (rounded and adjusted)
    """
    numCards = int(numCards)  # Ensure numCards is an integer
    raw_allocations = [numCards * (p / 100) for p in chances]
    rounded_allocations = [int(x) for x in raw_allocations]  # Round down each allocation
    total_allocated = sum(rounded_allocations)
    difference = numCards - total_allocated

    # Adjust allocations to match numCards exactly
    for i in range(abs(difference)):
        index = i % len(rounded_allocations)
        rounded_allocations[index] += 1 if difference > 0 else -1
    
    return rounded_allocations

# Main function to create event dictionary
def main(usedCraftedEvents, numCards):
    eventDict = {}
    
    if usedCraftedEvents:
        # Filter out rows with missing values for essential columns
        essential_columns = ['aType', 'bType', 'rollReq', 'canIgnore', 'roll_Ignore', 'chance']
        filtered_craftedEvents = craftedEvents.dropna(subset=essential_columns)

        # Iterate over filtered events to create event objects
        for index, row in filtered_craftedEvents.iterrows():
            event_typeA = row['aType']
            event_typeB = row['bType']
            requiredRoll = row['rollReq']
            canIgnor = row['canIgnore'] == "yes"
            ignorRoll = row['roll_Ignore'] if pd.notna(row['roll_Ignore']) else None
            chance = row['chance']

            eventKey = (event_typeA, event_typeB)
            if eventKey not in eventDict:
                eventDict[eventKey] = set()
            
            eventDict[eventKey].add(Event(event_typeA, event_typeB, requiredRoll, canIgnor, ignorRoll, chance))
    else:
        # Default event setup when crafted events are not used
        event_types = ["GCard", "none", "G/BCard", "BCard"]
        newlist = [("GCard", "none"), ("GCard", "G/BCard"), ("GCard", "BCard"),
                   ("none", "G/BCard"), ("none", "BCard"), ("G/BCard", "BCard")]
        requiredRoll = [(0, 0)] * 6
        canIgnor = [1] * 6
        ignorRoll = [(0, 0)] * 6
        chance = [0] * 6
        
        for i in range(6):
            event_typeA, event_typeB = newlist[i]
            eventDict[i] = Event(event_typeA, event_typeB, requiredRoll[i], canIgnor[i], ignorRoll[i], chance[i])
    
    # Allocate events based on percentage chances
    groups = allocate_parts(numCards, rangeEvent["chance"].tolist())
    
    for index, row in rangeEvent.iterrows():
        eventA = row['aType']
        eventB = row['bType']
        rollReqMin = row['rollReq(min)']
        rollReqMax = row['rollReq(max)']
        ignorRollMin = row['roll_Ignore(min)']
        ignorRollMax = row['roll_Ignore(max)']
        chanceIgnor = row['chance_Ignore']
        chance = row['chance']
        
        cardset = set()
        
        # Generate event objects based on allocated groups
        for i in range(groups[index]):
            reollReq = random.randint(rollReqMin, rollReqMax)
            canIgnor = getBoolonChance(chanceIgnor)
            ignorRoll = random.randint(ignorRollMin, ignorRollMax)
            cardset.add(Event(eventA, eventB, reollReq, canIgnor, ignorRoll, chance))
        
        eventDict[index] = cardset
    
    return eventDict

# Entry point for script execution
if __name__ == "__main__":
    idk = main(True, 100)  # Example call with crafted events enabled and 100 cards
    for key in idk:
        for card in idk[key]:
            card.displayCard()
