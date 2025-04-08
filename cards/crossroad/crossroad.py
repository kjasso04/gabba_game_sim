import math
import sys
import os
import pandas as pd
import random

# Adjust sys.path for module imports
sys.path.append(os.path.abspath(".."))

# Import Parent Class
from cards.cardClass import Card  

# Get the directory where this script (crossroad.py) is located
file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the correct paths to the Excel files
crafted_event_path = os.path.join(file_dir, "craftedEvent.xlsx")
choice_crossroad_path = os.path.join(file_dir, "choiceCrossroad.xlsx")

# Read Excel files with error handling
try:
    events = pd.read_excel(crafted_event_path, engine='openpyxl')
except FileNotFoundError:
    raise FileNotFoundError(f"Error: File not found at {crafted_event_path}")

try:
    decisions = pd.read_excel(choice_crossroad_path, engine='openpyxl')
except FileNotFoundError:
    raise FileNotFoundError(f"Error: File not found at {choice_crossroad_path}")

# Ensure sys.path is updated only once
if ".." not in sys.path:
    sys.path.append(os.path.abspath(".."))

# Define Cross class
class Cross(Card):
    pass


class CrossEvents(Cross):
    
    
    
    def __init__(self, require, consiquice, name=None, des=None):
        self.require = require
        self.consiquice = consiquice
        self.name = name
        self.des = des
        
        
    def displayCard(self):  # this funcition prints cards information
        print('\n')
        
        if self.name:
            print("name: " + str(self.name)+ '\n')

        
        print("require: " + str(self.require) + '\n')
        print("consiquice: " + str(self.consiquice)+ '\n')
        
        if self.des:
            print("description: " + str(self.des)+ '\n')
        print("type: event \n")
       
 
class CrossChoise(Cross):
    def __init__(self, require, choiceA, choiseB, name=None, des=None):
        self.require = require
        self.choiceA = choiceA
        self.choiseB = choiseB
        self.name = name
        self.des = des
        
    def displayCard(self): # this funcition prints cards information
        print('\n')
        
        if self.name:
            print("name: " + str(self.name)+ '\n')

        
        print("require: " + self.require + '\n')
        print("choiceA: " + self.choiceA+ '\n')
        print("choiseB: " + self.choiseB+ '\n')
        
        if self.des:
            print("description: " + str(self.des)+ '\n')
            
        print("type: event \n")
        
        
            
    
def generateEvents(events, mix = False):
    dicMush = set()
    
    if (mix):
        
        
        requDic = events['require'].dropna().tolist()
        print(requDic)
        consDic = events['consiquice'].dropna().tolist()
        print(consDic)
            
            
       
        #loops throught the min lenght of the rquierments and consiquices
        for x in range(min(len(requDic), len(consDic))):
            
            #getting the random choice
            randRequ = random.choice(requDic)
            randCons = random.choice(consDic)
            
            #adding it to the setß
            dicMush.add( CrossEvents(randRequ,  randCons))
            
            #removes 
            requDic.remove(randRequ)
            consDic.remove(randCons)
        

    else:
        
        #loops throught the row
        for index, row in events.iterrows():
            # skips if missing infomation
            if pd.isna(row['require']) or pd.isna(row['consiquice']):
                continue
            
            name = row['name'] if not pd.isna(row['name']) else None
            des = row['des'] if not pd.isna(row['des']) else None

            dicMush.add(CrossEvents(row['require'], row['consiquice'], row['name'], row['des']))
            
    
       
    
    return dicMush

def generateChoise(decitions, mix = False):
    dicMush = set()
    
    # this mixes the requierments and the outcome 
    if (mix):
        
        #this drops the na values for in the table, 
            # dont need to worry about length cause mixig
        require = [x for x in decitions['require'].dropna().tolist() if x]
        choiceA = [x for x in decitions['choiceA'].dropna().tolist() if x]
        choiceB = [x for x in decitions['choiceB'].dropna().tolist() if x]
        
        #get the colom with the smallest number of elemets to esure say in bounds of table
        numCard  = min(len(require), len(choiceA), len(choiceB))
        
        #this loops throught getting inforation pure row 
        for i in range(numCard):
            ranRequ = random.choice(require)
            ranchoiA= random.choice(choiceA)
            ranchoiB = random.choice(choiceB)
            
            
            dicMush.add(CrossChoise(require[i], choiceA[i], choiceB[i]))
            
            #revmoves from the colom to prevent dups
            require.remove(ranRequ)
            choiceA.remove(ranchoiA)
            choiceB.remove(ranchoiB)
 
    else:
        # this uses the events are stated in the table
        
            #this gets the coloms without null values droping rows that dont have the needed info
        filtered_decitions = decitions.dropna(subset=['require', 'choiceA', 'choiceB'])
        
        #loops throught rows 
        for index, row in filtered_decitions.iterrows():
            require = row['require']
            choiceA = row['choiceA']
            choiceB = row['choiceB']
            
            # drop rows not have all info (should not go off)
            if pd.isna(require) or pd.isna(choiceA) or pd.isna(choiceB):
                continue

            # Assign None if optional fields are missing
            name = row['name'] if pd.notna(row['name']) and row['name'] != "" else None
            des = row['des'] if pd.notna(row['des']) and row['des'] != "" else None
            
            #returns a set 
            dicMush.add(CrossChoise(require, choiceA, choiceB, name, des))
        
    return dicMush
            
            
            
        
    

    
    
    
def main(inculdeEvents,inculdeChoise,mixEvents,mixChoise ):
    mixRequConsqu = False
    
    cardDic ={}

    
    if (inculdeEvents):
        #this generates teh cross road events
        cardDic["event"] = generateEvents(events, mixEvents)
        
    if (inculdeChoise):
         #this generates this cross road choises
        cardDic["choise"] = generateChoise(decisions, mixChoise)
        
    return cardDic
        


        
        
        


    
    
    

    

    

if __name__ == "__main__":
    idk = main()
    
    #print (idk)
    for key in idk:
        #print (key)
        for card in idk[key]:
            #print (card)
            #print(idk[key][card].displayCard()) 
            i = 0
        
            
            

        