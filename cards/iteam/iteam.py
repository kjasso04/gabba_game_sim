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
file_path = os.path.join(file_dir, "iteams.xlsx")

# Read the Excel file using the corrected path
data = pd.read_excel(file_path, engine='openpyxl')

class iteamCard(Card):
    def __init__(self, function, multiUses =False, numUses = 1, Xmin = 0, Xmax = 0, name = None, desc = None ):
    
       print("Xmin:" + str(Xmin))
       print("Xmax:" + str(Xmax) )
   
       self.Xvalue = None
       
       self.function = function
       
       if pd.notna(Xmin) and pd.notna(Xmax):
            try:
                self.Xvalue = random.randint( int(Xmin), int(Xmax) )
                self.function = self.function.replace("{x}", str(self.Xvalue))
            except ValueError:
                print(f"Invalid Xmin or Xmax: {Xmin}, {Xmax}")

       
       
       
       self.name = name
       self.desc = desc
       
       
       if(multiUses):
           self.numUses = numUses
       else:
           self.numUses = 1
       
       
       
       
        

        
       
    def canUse(self):
        if (self.numUses > 0):
            return True
        return False
    
    def useIteam(self):
        if self.canUse():
            print(self.function)
            self.numUses =  self.numUses - 1
        else:
            print("you can't use this iteam")
            
        return self.numUses
    
    def displayCard(self):
        if (self.name):
            print("name: " +str(self.name)+'\n')
        if (self.desc):
            print("description: "+str(self.desc)+ '\n')
            
        print("function: " +str(self.function) + '\n')
        
        print("number of uses: "+ str(self.numUses)+'\n')
        
        
def main():
    iteamDic = {
        "hasMultUses": set(),
        "OneUse":set()
    }

    for index, row in data.iterrows(): # loops throught the row 
        
        # get the information in the colums
        
        
        card_func = row['function']
        isMultiUse = bool(row['multiUses'] == "yes")
        
        card_numUses = row['numUses']
        
        card_mult = bool(row['allowMult'] == "yes")
        max_mult = 0
        if (card_mult):
            max_mult = int(row['maxNumMult'])
        
        xMin  = row["x(min)"]
        xMax = row["x(max)"]

        
        #  check if the row has all if then needed inforation  
        if pd.isna(card_func) or pd.isna(isMultiUse) or pd.isna(card_mult):
            # skips the row if missing one
            continue 
        
        #get the number of duplicate cards that will be genterated 
        numCards = random.randint(1, max_mult) if card_mult else 1
        
        #gets the  name and des ( optional)
        card_name = row['name'] if not pd.isna(row['name']) else None
        card_des = row['description'] if not pd.isna(row['description']) else None
        
        
        
            
        
        for _ in range(numCards):
            new_card = iteamCard(card_func,card_mult,card_numUses, xMin , xMax, card_name, card_des )
            
            #creates a set for each type of card
                
            #add types cards that are the so
            iteamDic["hasMultUses"].add(new_card)
        
        
        if (isMultiUse):
            iteamDic["hasMultUses"].add(iteamCard(card_func,card_mult,card_numUses, xMin , xMax, card_name, card_des ))
        else:
            iteamDic["OneUse"].add(iteamCard(card_func,card_mult,card_numUses, xMin , xMax, card_name, card_des))


    return iteamDic


if __name__ == "__main__":
    main()
        
        