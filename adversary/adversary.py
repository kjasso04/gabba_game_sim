import sys
import os
import math

import pandas as pd
import random

sys.path.append(os.path.abspath(".."))

file_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(file_dir, "adversary.xlsx")

# Read the Excel file using the corrected path
data = pd.read_excel(file_path, engine='openpyxl')

from cards.buffANDdebuff.buffANDdebuff import BuffANDdebuff


class adversaryCard:
    def __init__(self, behavior, roll,  debfunction, min_x=None, max_x = None, min_y = None, max_y = None, name=None, desc=None):
        #self.function = function
        
        self.behavior = behavior
        self.roll = roll
        
        
        self.debfunction = debfunction

        self.name = name
        self.desc = desc
        
        self.card_chance = "adversary"  # double-check what "adver" should be
        
        self.debuffCard = None
        
        if ((min_x is not None and  max_x is not None) and (min_y is not None and  max_y is not None)):
            self.debuffCard = BuffANDdebuff("BCard",self.debfunction, self.card_chance, min_x, max_x,  min_y, max_y)
        elif (min_x is not None and  max_x is not None):
            self.debuffCard = BuffANDdebuff("BCard",self.debfunction, self.card_chance, min_x, max_x)
        else:
            self.debuffCard = BuffANDdebuff("BCard",self.debfunction, self.card_chance)
        
        
        

        
        
    

    
    def displayCard(self):
        if (self.name is not None):
            print("name: " + str(self.name) )
        if (self.desc is not None):
            print("descriptoin: "+ str(self.desc) )
        print("behavor: " + str(self.behavior) +"\n")
        print("required roll: "+ str(self.roll)  + "\n")
        print ("debuff function: \n")
        print(self.debuffCard.displayCard())
        print("\n")
        
        
    
    def interact(self, input = None):
        self.displayCard()
        if (input is None):
            input = int(input("input you roll: \n"))
        return (self.roll <= input)
    
    def getDebuffCard(self):
        return self.debuffCard
    
    
        
            
def main():
    adversaryDic = {
        "enemy": set()
    }
    
    for index, row in data.iterrows():
        card_behavior = row['behavior']
        card_roll = row['roll']
        card_debuffFun = row['debuff Function']
        card_min_x = row['min_x']
        card_max_x = row['max_x']
        card_min_y = row.get('min_y', 0 )
        card_max_y = row.get('max_y', 0 )
        
        #get the number of duplicate cards that will be genterated 
        card_name = row['name'] if not pd.isna(row['name']) else None
        card_description = row['description'] if not pd.isna(row['description']) else None
        
        if pd.isna(card_behavior) or pd.isna(card_roll) or pd.isna(card_debuffFun) or pd.isna(card_min_x) or pd.isna(card_max_x) :
            continue
            
    
        
    
        
        
        adversaryDic["enemy"].add(adversaryCard(card_behavior, card_roll, card_debuffFun, card_min_x, card_max_x, card_min_y, card_max_y, card_name, card_description))
    return (adversaryDic)
        

    
    
    
    


if __name__ == "__main__":
    main()