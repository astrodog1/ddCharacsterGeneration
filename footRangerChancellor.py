# Mage simulator
import argparse
import random
import numbers
from dataclasses import dataclass, field
from typing import List, Dict

#global vars
CharClass: str
MusterOutLevel: int

def getPlayerClass() -> str:
    global CharClass
    return CharClass

def roll(dice: str) -> int:
    n, d = map(int, dice.lower().split("d"))
    return sum(random.randint(1, d) for _ in range(n))

@dataclass
class ClassStats:
    STR: int
    DEX: int
    CON: int
    WIS: int
    INT: int
    CHA: int
    PER: int
    REP: float
    SS: int
    playerclass: str
    LIT: int
    K_Lore: int 
    K_Beast: int 
    K_Runes: int 


def generateClassStats(CharClass) -> ClassStats:
    return ClassStats(
        STR=roll("3d6") + 2 if CharClass in ("guards") else 0,
        DEX=roll("3d6") + 2 if CharClass in ("ranger","rogue") else 0,
        CON=roll("3d6") + 2 if CharClass in ("guards") else 0,
        WIS=roll("3d6") + 2 if CharClass in ("cleric", "paladin") else 0,
        INT=roll("3d6") + 2 if CharClass in ("mage") else 0,
        CHA=roll("3d6") + 2 if CharClass in ("paladin") else 0,
        PER=roll("3d6") + 2 if CharClass in ("ranger") else 0,
        REP=roll("1d6") + 2 if CharClass in ("guards") else 0,
        SS=roll("1d6")  + 2 if CharClass in ("guards") else 0,
        playerclass=CharClass,  # default class
        LIT=0, # Literacy skill, set to 0 initially
        K_Lore=roll("1d6") + 2 if CharClass in ("cleric") else 0,
        K_Beast=roll("1d6") + 2 if CharClass in ("ranger") else 0,
        K_Runes=roll("1d6") + 2 if CharClass in ("mage") else 0
    )

# Assignment		Survive	    Levelup	    stockade	Heroism  	Rangers Guards  gpSaved
FootAssignments = [
("Training"	            ,1	    ,19	        ,1	        ,99         ,99     ,99     ,"1d10")
,("Garrison"	        ,12	    ,20	        ,2	        ,20	        ,99	    ,99     ,"1d10")
,("Border"	            ,15	    ,18	        ,2	        ,19	        ,99     ,99     ,"1d10")
,("Convoy duty"	        ,16	    ,17         ,1	        ,19         ,20     ,20     ,"1d10")
,("Combat-raid"	        ,19	    ,12	        ,1          ,17	        ,15	    ,15	    ,"1d100")
,("Combat-melee"	    ,20	    ,10	        ,1          ,17	        ,17	    ,17	    ,"1d100")
]

# Stockade	
FootStockadeOffense = [
(1-10	,"drunk on duty")
,(11-16	,"brawling")
,(17-19	,"AWOL")
,(20	,"Insubordination")
]

#Raid/Melee	
FootRaidMelee = [
(1-12	,"human tribe")
,(13-16	,"goblins")
,(17-18	,"orcs")
,(19-20	,"lizardmen")
]

#assign     roll		Survive	Level	Heroism     gpSaved
RangerAssignments = [
("Training"	            ,1	    ,2	   ,19	        ,"1D20")
,("Escort"	            ,10	    ,2	   ,17	        ,"1D20")
,("Scout"	            ,16	    ,5	   ,19	        ,"1D20")
,("Raid"	            ,19	    ,5	   ,17	        ,"1D20")
,("Rescue"	            ,20		,6	   ,10	        ,"1D20")
]

#Scout/Raid/Rescue				
RangerScoutRaidRescue = [
(1-12	            ,"human tribe"			,"Land")
,(14	            ,"goblins"			    ,"Land")
,(16	            ,"orcs"		            ,"Land") 
,(17	            ,"lizardmin"			,"Land")
,(18	            ,"fey/orcs"			    ,"Land")
,(19	            ,"fey/gnolls"			,"Land")
,(20	            ,"fey/other"			,"Air")
]

# Guards Assignment             roll    survive	Level	Heroism     gpSaved
GuardsAssignment= [
("Training"		                ,1	    ,1	    ,19	        ,0      ,"1d25")
,("Escort"		                ,8	    ,2	    ,18	        ,20     ,"1d25")
,("Battle-minor"		        ,12	    ,5	    ,16	        ,17     ,"1d25")
,("Battle-major"		        ,15	    ,6	    ,13	        ,15     ,"1d25")
,("Research mission-Lore"		,16	    ,4	    ,14         ,14     ,"1d100")
,("Research mission-Beastery"   ,17	    ,4	    ,14	        ,14     ,"1d100")
,("Research mission-Runes"		,18	    ,4	    ,14	        ,14     ,"1d100")
,("Rare magical component quest",19	    ,4	    ,14	        ,14     ,"1d100")
,("Fortification Assault"		,20	    ,7	    ,10	        ,13     ,"1d100")
]

#roll        who            	,where
GuardRaidMelee = [
(3	        ,"human tribe" 		,"Land")
,(6	        ,"human tribe" 		,"underground")
,(10	    ,"goblins"		    ,"Land")
,(12	    ,"goblins"		    ,"Underground")
,(14	    ,"orcs"             ,"Land")			
,(16	    ,"orcs"             ,"Underground")			
,(18	    ,"lizardmen"        ,"Land")			
,(20	    ,"lizardmen"        ,"Underground")			
]



#Item               ,chance/year    ,qtyRoll   ,description
MusteringOut = [
("Weapon"            ,.03           ,None       ,"A weapon of your choice, suitable for a mage."),
("Armor"             ,.01           ,None       ,"Some form of mage armor at DM discretion."),
("misc. magic item"  ,.01           ,None       ,"A minor magic item, such as a 1-3 scrolls or potions."),
("+1 Int"            ,.30           ,None       ,"A +1 to your Intelligence score, representing your mastery of magic."),
("gems and Jewelry"  ,None          ,"5d4"      ,"A small amount of gems or jewelry, no item > 100 gp value"),
("indebted"		     ,.01	        ,None       ,"you owe someone money and have a finite time period to pay back"),
("infavored"		,.01            ,None       ,"you owe someone a favor they will call in at some point in the future"),
("debtor"			,.01	        ,None       ,"some owes you money that needs your action to collect"),
("favored"			,.01	        ,None       ,"someone owes you a favor that you can call in at some point in the future")
]

# Literacy skill (1d20 + 4)
#roll	        ,description											,AffectRep,AffectSocial,AffectGP
Literacy = [
(18	,"Capable of written correspondence and basic math"					        ,None,None,None),
(19	,"Neighborhood go-to for literary needs" 							        ,1,1,.10),	
(20	,"borough go-to for literary needs" 								        ,2,2,.25),	
(22	,"You were first to solve scroll translation mystery!" 						,2,2,.25),	
(23	,"You placed 1st in annual mage academy debate competition!"				,3,3,.25),	
(24	,"Your interpretation of a famous ancient scroll was talked about throughout the seven kingdoms!" ,3,3,.25)	
]

# @dataclass is used to automatically generate special methods like __init__, __repr__, etc.
#from typing import Callable
@dataclass
class Cadet:
    id: int
    stats: ClassStats
    age: int = 12
    level: int = 0
    gp: int = 0
    rep: float = 2.0
    playerClass: str = getPlayerClass()  # default class
    # jail_log: List[str] = field(default_factory=list)
    quarters: List[Dict] = field(default_factory=list)
    
#getAssignment(CharClass: str) -> List[Dict]:
def getAssignment(CharClass: str) -> List[tuple]:
    if CharClass == "ranger":
        return RangerAssignments
    elif CharClass == "guards":
        return GuardsAssignment
    else:
        return FootAssignments  
    


# '->' means the function returns a Cadet object    parser = argparse.ArgumentParser(description="")
def runClassSim() -> Cadet:
    count = 1
    while True:  #sim loop
        cadet = Cadet(id=count, stats=generateClassStats(CharClass))
        cadet.rep = cadet.stats.REP
        year, quarter = 1, 1  #restart year/qtr for each cadet

        while True:  #cadet loop
            levelbegin = cadet.level
            qtrAssignRoll = roll("1d20") 
            assignment = mageAssignments

            #determine qtr assignment
            for item in assignment:
                if qtrAssignRoll <= item[1]:
                    qtrAssignmentRoll = item
                    break
            
            #Assignment ,Band		,Survijobdescve	,Lvl Up		,GP         
            jobdesc     ,jobDC      ,sDC        ,lDC        ,gp_fn   = qtrAssignmentRoll

            lvl_roll = random.randint(1, 20)
            survival_rolls = [random.randint(1, 20) for _ in range(cadet.level + 1)]            

            # one roll/lMage Rare magical component expeditionevel
            survived = any(r >= sDC for r in survival_rolls)
            if not survived:
                print(f"Cadet {cadet.id} failed to survive in year {year} quarter {quarter}.")
                break

            #diplomatic mission
            if 'Diplomacy' in jobdesc:
                # roll for diplomatic mission
                diplomatic_roll = roll("1d20")
                for mission in MageDiplomaticMission:
                    if diplomatic_roll <= mission[0]:
                        if 'local' in jobdesc:
                            jobdesc = f"{jobdesc} - {mission[1]}"
                        else:
                            jobdesc = f"{jobdesc} - {mission[2]}"
                        break

            #MageResearchMissions
            if 'Research mission' in jobdesc:
                if 'Lore' in jobdesc:
                    cadet.stats.K_Lore += 1
                elif 'Beastery' in jobdesc:
                    cadet.stats.K_Beast += 1
                elif 'Runes' in jobdesc:
                    cadet.stats.K_Runes += 1

            #Mage Rare magical component expedition
            if 'magical component quest' in jobdesc:
                cadet.stats.K_Lore += 2
                cadet.stats.K_Beast += 2
                cadet.stats.K_Runes += 2

            #gp saved
            gp_ = roll(gp_fn)
            cadet.gp = cadet.gp + gp_

            # Level up only if < lvl 4----------------------------------------
            if cadet.level < MusterOutLevel:
                if lvl_roll >= lDC:
                    cadet.level += 1

            cadet.quarters.append({
                "CadetAttempt": cadet.id,
                "class": cadet.playerClass,
                "levelbegin": levelbegin,                
                "levelend": cadet.level,
                "Y": year,
                "Q": f"Q{quarter}",
                "Job": jobdesc,
                "Surv": '+',
                "LvlUp": "+" if lvl_roll >= lDC else "-",
                "GP": gp_,
                "Rep": cadet.rep,
            })

            # Exit conditions
            if cadet.rep < 1:
                break
            if cadet.level >= MusterOutLevel:
                if quarter == 4:
                    return cadet
                else:
                    quarter += 1
                    continue

            # Quarter tracking
            quarter += 1
            if quarter > 4:
                year += 1
                quarter = 1
        count += 1

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="")
    # parser.add_argument("Class",type=str,help="class to generate")
    # parser.add_argument("Level",type=int,help="musterOutLevel")
    # args = parser.parse_args()  
    # CharClass = args.Class
    # MusterOutLevel=args.Level

    CharClass = "mage"
    MusterOutLevel=4


    print(f"Inputs: {CharClass}/{MusterOutLevel}")
    
    
    cadet = runClassSim()

    print(
        f"{'cadet':<8}"
        f"{'class':<10}"
        f"{'YQ':<7}"
        f"{'lvl':<6}"        
        f"{'Assign':<50}"
        f"{'S':<2}"
        f"{'Rep':<4}"        
        f"{'lvl':^5}"
        f"{'gp':<5}"
        )

    for q in cadet.quarters:
        #print(f"cadet:{q['CadetAttempt']} | {q['class']}:{q['levelbegin']}/{q['levelend']} | Y{q['Y']}{q['Q']} {q['Job']} | Surv:{q['Surv']} | Jail:{q['Jail']} | LvlUp:{q['LvlUp']} | gulded:{q['guilded']} | GP saved:{q['GP']}")
        #print(f"cadet:{q['CadetAttempt']:<8} | {q['class']}:{q['levelbegin']}/{q['levelend']} | Y{q['Y']}{q['Q']} {q['Job']} | Surv:{q['Surv']} | Jail:{q['Jail']} | LvlUp:{q['LvlUp']} | gulded:{q['guilded']} | GP saved:{q['GP']}")        
        print(
        f"{q['CadetAttempt']:<8}"
        f"{q['class']:<10}"
        f"Y{q['Y']}{q['Q']:<5}"        
        f"{q['levelbegin']}/{q['levelend']:<4}"
        f"{q['Job']:<50}"
        f"{q['Surv']:<2}"
        f"{q['Rep']:<4}"                
        f"{q['LvlUp']:^5}"
         f"{q['GP']:<5}"
)
        
#musterOut
#0                  #1              #2          #3
#Item               ,chance/year    ,qtyRoll   ,description
for item in MusteringOut:
    if item[1] is not None:
        myd100 = roll("1d100")
        myChance = int(item[1] * cadet.quarters[-1]['Y'] * 100)
        receivedItem = True if myd100 <= myChance else False
        myRoll = 'Roll: ' + str(myd100) + ' vs ' + str(myChance) + '% '
        print(myRoll + ' ' 
              +str(item[0]) + ' ' 
              + (' - received' if receivedItem else '- not received')) 

    else:
        print(str(item[2]) + ' ' + item[0] )   
#literacy
literacy_roll = roll("1d20") + 4
