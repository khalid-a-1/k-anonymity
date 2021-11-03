#this just takes 3 qids and will return any unique combos, so we should not be 

import pandas as pd 
import datetime 
from datetime import date
pd.options.mode.chained_assignment = None  # default='warn'

df = pd.read_csv("combine_data_since_2000_PROCESSED_2018-04-26.csv")

#supress certain columns b/c sensative data or for inference control
df.drop(["Player","Pfr_ID","Year"],axis=1,inplace = True)




k = 2
qid = ["Pos","Forty","Round"] #replace this with any qids and it will work the same

def pos(p):
    # Combine Categories in order to reach k = 2
    OB = ["RB","FB","QB"] #Offensive backs 
    OL = ["OL","G","C","OT","OG","LS","TE"] #Offensive Line
    DL =["NT","DT","DE","EDGE"] #Defensive Line
    LM = OL + DL #Linemen
    DB = ["CB","DB","SS","FS","LB","ILB","OLB","MLB","S"] #defensive backs
    KP = ["K","P",] #Kicker and Punter
    WRDB = DB + ["WR"] #Wide Receivers and Defensive Backs (They share a lot in common)
    
    if p in LM:
        return "LM"
    elif p in WRDB:
        return "WR/DB"
    elif p in OB:
        return "OB"
    elif p in KP:
        return "K/P"
    
    return p

def pos2(p):
    # Combine Categories even more in order to reach k = 9
    OB = ["RB","FB","QB"]
    OL = ["OL","G","C","OT","OG","LS","TE"]
    DL =["NT","DT","DE","EDGE"]
    LM = OL + DL
    DB = ["CB","DB","SS","FS","LB","ILB","OLB","MLB","S"]
    KP = ["K","P",]
    WRDB = DB + ["WR"]
    KPOBLM = KP + OB +LM #Had to combine these in order to reach k =9
    
    if p in WRDB:
        return "WR/DB"
    elif p in KPOBLM:
        return "OB/K/P/LM"
    elif p in KP:
        return "K/P"
    
    return p


    
def roundD(r):
    #Generalizes Rounds into 3 different values
    if r>3:
        return "4-8"
    elif r >=1: 
        return "1-3"
    else:
        return "Undrafted"
def roundD2(r):
    #Generalizes Rounds into 2 different values
    if r>3:
        return "4-8/Undrafted"
    elif r >=1: 
        return "1-3"
    else:
        return "4-8/Undrafted"

def forty(s):
    #Generalizes the forty times into 7 different values.
    s = s - (s%.1) # get rid of second decimal
    s = round(s,1)
    if(s >4.87):
        return "4.87+"
    elif (s >= 4.7):
        return "4.70-4.85"
    elif (s >= 4.5):
        return "4.60-4.99"
    elif (s >= 4.3):
        return "4.40-4.59"
    elif (s >= 4.1):
        return "4.20-4.39"
    elif (s > 4.0):
        return "4.00-4.19"
    else:
        return "<4.00"


AmountPerCombo = {}
def frequency():
    for row in range(1,len(df)):
        s="" # a string of values ex: LM ; 4.87+ ; 1-2
        for quasi in qid:
            s += str(df[quasi][row])+" ; "
        if(s in AmountPerCombo): # if someone has this identity then we add it to the count
            AmountPerCombo[s] = AmountPerCombo[s] + 1
        else: #if they are the first one to have this combo
            AmountPerCombo[s] = 1

    count = 0
    for combo in AmountPerCombo:

        if AmountPerCombo[combo] <= k:
            print(combo)
            count = count +1

    if (count == 0):
        print("Achieves K anomynity for K =",k)
    
    



def k2(): 
    #Combined a lot of positions into bulk like Linemen (LM)
    global k 
    k = 2
    df["Forty"] = df["Forty"].apply(forty)
    df["Round"] = df["Round"].apply(roundD)
    df["Pos"]= df["Pos"].apply(pos)
    #Local Generalization
    for row in range(1,len(df)):
        if df["Pos"][row] == "K/P":
            if ("4." in df["Forty"][row]):
                df["Forty"][row] = "<5"
        if df["Pos"][row] == "OB":
            if ("4.4" in df["Forty"][row] or "4.2" in df["Forty"][row]):
                df["Forty"][row] = "4-4.5"
    frequency()
    df.to_csv(r'k2.csv', index = False)
    print("File k2.csv created")


def k4():
    #Changes 
    #Combined rounds 4-8 and undrafted to make 4-8/undrafted
    #Generalized OB forty speed more by making the 4-4.5 to <4.5
    #Generalized all WR/DB speeds that are over 4.7 to just be >4.7

    global k 
    k = 4
    df["Forty"] = df["Forty"].apply(forty)
    df["Round"] = df["Round"].apply(roundD2)
    df["Pos"]= df["Pos"].apply(pos)
    for row in range(1,len(df)):
        if df["Pos"][row] == "K/P":
            if ("4." in df["Forty"][row]):
                df["Forty"][row] = "<5"
        if df["Pos"][row] == "OB":
            if ("4.4" in df["Forty"][row] or "4.2" in df["Forty"][row] or "4.0" in df["Forty"][row]):
                df["Forty"][row] = "<4.5"
        if df["Pos"][row] == "WR/DB":
            if ("4.7" in df["Forty"][row] or "4.8" in df["Forty"][row]):
                df["Forty"][row] = ">4.7"
    frequency()
    df.to_csv(r'k4.csv', index = False)
    print("File k4.csv created")

def k9():
    #Changes 
    #Combined OB, K/P, & LM into one category in pos2()
    #Generalized OB/K/P/LM forty speed more by making them all now if it is under 4.5 to be <4.5
    #Generalized all WR/DB speeds even more by combining the 4.4-4.59 and the 4.2-4.39: 4.2-4.59
    global k 
    k = 9
    df["Forty"] = df["Forty"].apply(forty)
    df["Round"] = df["Round"].apply(roundD2)
    df["Pos"]= df["Pos"].apply(pos2)
    #Local Generalization
    for row in range(1,len(df)):
        if df["Pos"][row] == "K/P":
            if ("4." in df["Forty"][row] or "4." in df["Forty"][row] ):
                df["Forty"][row] = "<5"
        if df["Pos"][row] == "OB/K/P/LM":
            if ("4.4" in df["Forty"][row] or "4.2" in df["Forty"][row] or "4.0" in df["Forty"][row]):
                df["Forty"][row] = "<4.5"
        if df["Pos"][row] == "WR/DB":
            if ("4.7" in df["Forty"][row] or "4.8" in df["Forty"][row]):
                df["Forty"][row] = ">4.7"
            elif("4.4" in df["Forty"][row] or "4.2" in df["Forty"][row]):
                df["Forty"][row] = "4.2-4.59"
    frequency()
    df.to_csv(r'k9.csv', index = False)
    print("File k9.csv created")

#Uncomment a function call to anonamyze the data according to each K value
#Run one at a time 
#k = 2
# k2()
#k = 4
# k4()
#k = 9
k9()