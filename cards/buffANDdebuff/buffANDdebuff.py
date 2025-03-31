import sys
import os
import pandas as pd
import random

# Adjust sys.path for imports
sys.path.append(os.path.abspath(".."))

# Now import ParentClass
from cards.cardClass import Card




# Load Excel Data
# Get the directory where this script (buffANDdebuff.py) is located
file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the correct path to the Excel file
file_path = os.path.join(file_dir, "buffANDdebuff.xlsx")

# Read the Excel file using the corrected path
data = pd.read_excel(file_path, engine='openpyxl')

# Card Class
class BuffANDdebuff(Card):
    def __init__(self, card_type, card_func, card_chance, min_x=0, max_x=0, min_y=0, max_y=0, card_mult=False, card_minCount=0, card_maxCount=0, card_name=None, card_des=None):
        self.card_type = card_type
        self.card_func = card_func
        self.card_chance = card_chance
        self.card_mult = card_mult
        self.card_minCount = card_minCount
        self.card_maxCount = card_maxCount
        self.card_name = card_name
        self.card_des = card_des
        
        #generates the x value based on the inputed x and y
        self.x_random = random.randint(min_x, max_x) if (card_type in ["GCard", "BCard", "G/BCard"]) else 0
        self.y_random = random.randint(min_y, max_y) if (card_type == "G/BCard") else 0

    def displayCard(self, index=None): # this funcition reutrns a string that shows that cards information
        updated_card_func = ""
        
        if index is not None:
            updated_card_func += f"index: {index}\n"
        updated_card_func += f"chance: {self.card_chance}\n"

        if self.card_name:
            updated_card_func += f"name: {self.card_name}\n"

        if self.card_des:
            updated_card_func += f"description: {self.card_des}\n"

        updated_card_func += f"type: {self.card_type}\n"
        card_func = self.card_func.replace("{x}", str(self.x_random)).replace("{y}", str(self.y_random))
        updated_card_func += f"function: {card_func}\n"

        return updated_card_func


def main():
    BDcardDict = {}

    for index, row in data.iterrows(): # loops throught the row 
        
        # get the information in the colums
        card_type = row['cardType']
        card_func = row['cardFunc']
        card_chance = row['chance']
        card_mult = row['allowMult'] == "yes"
        
        #  check if the row has all if then needed inforation  
        if pd.isna(card_type) or pd.isna(card_func) or pd.isna(card_chance) or pd.isna(row['minCount']) or pd.isna(row['maxCount']):
            # skips the row if missing one
            continue 
        
        #get the number of duplicate cards that will be genterated 
        numCards = random.randint(row['minCount'], row['maxCount']) if card_mult else 1
        
        #gets the  name and des ( optional)
        card_name = row['name'] if not pd.isna(row['name']) else None
        card_des = row['des'] if not pd.isna(row['des']) else None
        
        #get the min and max row infro from the table 
        min_x, max_x = row['x(min)'], row['x(max)']
        
        min_y, max_y = row.get('y(min)', 0), row.get('y(max)', 0)  # Default to 0 if missing

        for _ in range(numCards):
            new_card = BuffANDdebuff(card_type, card_func, card_chance, min_x, max_x, min_y, max_y, card_mult, card_name=card_name, card_des=card_des)
            
            #creates a set for each type of card
            if index not in BDcardDict:
                BDcardDict[card_type] = set()
                
            #add types cards that are the so
            BDcardDict[card_type].add(new_card)



    return BDcardDict


if __name__ == "__main__":
    main()
