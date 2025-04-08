import sys
import os
import math

import pandas as pd
import random


# Get the directory where this script (tiles.py) is located
file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the correct path to the Excel file
tiles_file_path = os.path.join(file_dir, "tiles.xlsx")

# Read the Excel file with error handling
try:
    tilesExcel = pd.read_excel(tiles_file_path, engine='openpyxl')
except FileNotFoundError:
    raise FileNotFoundError(f"Error: File not found at {tiles_file_path}")


Color = {
    "BLACK": '\033[30m',
    "RED" : '\033[31m',
    "GREEN" :'\033[32m',
    "YELLOW" : '\033[33m',
    "BLUE" : '\033[34m',
    "MAGENTA" : '\033[35m',
    "CYAN" : '\033[36m',
    "WHITE" : '\033[37m',
    "RESET" : '\033[0m'
}


class Tile:
    
    
    
    def assign_color_or_item(self):
        otherColor = []
        # 40% chance for otherColor to be not white (assuming white is the default color)
        other_color_chance = random.randint(1, 100)
        if other_color_chance <= 40:
            # 30% chance for it to be red, yellow, or magenta
            otherColor.append(random.choice(["RED", "YELLOW", "MAGENTA"]))
            
        else:
            otherColor.append("white")  # Default to white if not 40%
            
        item_chance = random.randint(1, 100)
        if (other_color_chance <= 40 and item_chance <= 30) or (other_color_chance >= 40 and item_chance <= 40):
                otherColor.append(random.choice(["RED", "YELLOW", "MAGENTA"]))
        else:
            otherColor.append("white")  # If not in 30%, set to white
        
        return  otherColor

        

    
    
    
    def __init__(self, color, happen):
        self.color = color
        self.happen = happen
        self.door = [True, False, False, False]  # Now an instance attribute
        
        
    
    def genDoors(self, startChance, chanceDecrease, order=[3, 2, 1]):
        chance = startChance
        for i in order:
            self.door[i] = random.random() < chance
            #print (chance)
            #print(self.door[i])
            #print(self.door)
            if self.door[i]:
                chance *= chanceDecrease
                
        #print ("\n")
        return self  # Return self to be used in the dictionary

    def displayTiles(self):
        
        tileString = f"{Color[self.color]}[=][_][=]\n"

        tileString += "[_]" if self.door[1] else "[=]"
        tileString += " █ "
        tileString += "[_]\n" if self.door[2] else "[=]\n"

        tileString += "[=][_][=]\n" if self.door[3] else f"[=][=][=]\n"
        
        tileString += f"{Color['RESET']}\n"
        
        tileString += f"other colors: {self.assign_color_or_item()}"
        
        
        

        return tileString  # Return the string instead of printing


 
            
def allocate_parts(totalNum, chances):
    """
    Allocates numCards into groups based on percentage chances, ensuring total remains consistent.
    
    :param numCards: Total number to distribute (can be a string or number)
    :param chances: List of percentage values
    :return: List of allocated numbers (rounded and adjusted)
    """
    # Ensure numCards is numeric
    totalNum = int(totalNum)  # Convert to integer if it's a string

    # Calculate the raw allocations as floats
    raw_allocations = [totalNum * (p / 100) for p in chances]

    # Round down each allocation (but not rounding the sum yet)
    rounded_allocations = [int(x) for x in raw_allocations]

    # Calculate the current total and the difference with numCards
    total_allocated = sum(rounded_allocations)
    difference = totalNum - total_allocated

    # Distribute the difference across the allocations
    for i in range(abs(difference)):
        index = i % len(rounded_allocations)  # Distribute adjustments
        rounded_allocations[index] += 1 if difference > 0 else -1

    return rounded_allocations 

def main(numCard,startChance ):
    
    

    
    cardDic = {}

    
    

    groups = allocate_parts(numCard, tilesExcel["chance"])

    for index, row in tilesExcel.iterrows():
        for _ in range(groups[index]):
            if row["color"] not in cardDic:
                cardDic[row["color"]] = set()
            
            # Create a new Tile object and store it properly
            cardDic[row["color"]].add(Tile(row["color"], row["happen"]).genDoors(startChance/100, .5 ))

    return cardDic


            
if __name__ == "__main__":
    card_dict = main()
    i = 0
    for key, cards in card_dict.items():
        for card in cards:
            i += 1
            #print(str(i) + '\n')
            #print(card.displayTiles())
            

            
            
            
        
            
            
    
    #def chanceEqu(x):
        
