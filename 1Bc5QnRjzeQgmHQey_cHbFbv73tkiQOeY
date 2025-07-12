# Cleric~Paladin simulator
import argparse
import random
from dataclasses import dataclass, field
from typing import List, Dict

#global vars
CharClass: str
MusterOutLevel: int


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
    K_Lore: int = 3
    K_Beast: int = 3
    K_Runes: int = 3

def generateClassStats() -> ClassStats:
    return ClassStats(
        STR=roll("3d6"),
        DEX=roll("3d6"),
        CON=roll("3d6"),
        WIS=roll("3d6") +2,
        INT=roll("3d6"),
        CHA=roll("3d6"),
        PER=roll("3d6"),
        REP=2,
        SS=2,
        playerclass='urchin',
        LIT=roll("1d20")
    )


#Assignment		                    ,Band		,Survive,	lvl up		,Avoid Reformatory 	,Heroism	,GP saved	,Paladin Invite
clericAssignments = [
("Seminary"		                    ,3		    ,1		    ,19		    ,1			        ,99		    ,"1d20"		,99),
("Tend flock"		                ,6		    ,1		    ,19		    ,1			        ,20		    ,"1d20"		,99),
("Attache"    	                    ,8		    ,1		    ,17		    ,1			        ,19		    ,"1d20"		,19),
("Healing party"	                ,10		    ,5		    ,13		    ,1			        ,18		    ,"1d20"		,15),
("Exorcism"		                    ,11	        ,6		    ,8		    ,4			        ,15		    ,"1d20"		,10),
("Ritual Scriptorium"	            ,14		    ,1  		,18		    ,1			        ,99		    ,"1d20"		,99),
("Sacred Pilgrimage"	            ,16		    ,1		    ,15		    ,3			        ,17		    ,"2d10"		,14),
("Festival Ordainment"	            ,18		    ,1		    ,17		    ,1  			    ,19		    ,"1d20"		,99),
("Vigil for the Fallen"	            ,20		    ,4		    ,13		    ,2			        ,16		    ,"1d20"		,12)
]

#Assignment			            ,Band		,Survive		,Lvl Up		,Avoid Reformatory  ,Heroism	,GP         ,Paladin Invite
PaladinAssignments = [
("Training"			            ,5		    ,1  			,18		    ,1                  ,99		    ,"1d20"    ,99),
("Guard duty"			        ,9		    ,1  			,18		    ,1                  ,20		    ,"1d20"    ,99),
("Escort (Diplomacy-local)"	    ,13		    ,1			    ,18		    ,1                  ,19		    ,"1d20"    ,99),
("Escort (Diplomacy-Foreign)"	,15		    ,2			    ,18		    ,1                  ,19		    ,"1d20"    ,99),
("Research mission - Lore"		,16		    ,3			    ,10		    ,1                  ,16		    ,"1d100"   ,99),
("Research mission - Beastery"	,17		    ,6			    ,10		    ,1                  ,16		    ,"1d100"   ,99),
("Research mission - Runes" 	,18		    ,6			    ,10		    ,1                  ,14		    ,"1d100"   ,99),
("Rare magical component quest"	,19		    ,7			    ,8		    ,1                  ,16		    ,"1d100"   ,99),
("Battle"				        ,20		    ,7			    ,8		    ,1                  ,10		    ,"1d100"   ,99)
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
    playerClass: str = 'urchin'
    jail_log: List[str] = field(default_factory=list)
    quarters: List[Dict] = field(default_factory=list)
    

# '->' means the function returns a Cadet object
def runClassSim() -> Cadet:
    count = 1
    while True:  #sim loop
        cadet = Cadet(id=count, stats=generateClassStats())
        cadet.rep = cadet.stats.REP
        year, quarter = 1, 1  #restart year/qtr for each cadet

        while True:  #cadet loop
            qtrAssignRoll = roll("1d20") 
            if cadet.playerClass == 'cleric':
                assignment = clericAssignments
            else:
                assignment = PaladinAssignments

            #determine qtr assignment
            for item in assignment:
                if qtrAssignRoll <= item[1]:
                    qtrAssignmentRoll = item
                    break
            
            #Assignment ,Band		,Survive	,Lvl Up		,Avoid Reformatory  ,Heroism	,GP         ,Paladin Invite
            jobdesc     ,jobDC      ,sDC        ,lDC        ,jDC                ,hDC        ,gp_fn      ,gDC        = qtrAssignmentRoll

            # one roll/level
            survival_rolls = [random.randint(1, 20) for _ in range(cadet.level + 1)]
            survived = any(r >= sDC for r in survival_rolls)
            if not survived:
                break

            # Reformatory----------------------------------------
            jail_roll = random.randint(1, 20)
            jailed = jail_roll < jDC
            if jailed:
                cadet.age += 1
                cadet.rep -= 0.5
                cadet.jail_log.append(jobdesc)
                gp_ = 0
            else:
                #gp saved
                gp_ = roll(gp_fn)
                cadet.gp = cadet.gp + gp_

            # Level up only if < lvl 4----------------------------------------
            levelbegin = cadet.level
            if cadet.level <4:
                lvl_roll = random.randint(1, 20)
                if lvl_roll >= lDC:
                    cadet.level += 1

            #guild invite logic----------------------------------------
            #if not already a member roll invite
            guilded = "-"
            if cadet.playerClass == 'cleric':
                guild_roll = random.randint(1, 20)
                if guild_roll >= gDC:
                    cadet.playerClass = 'Paladin'
                    guilded = "+"

            cadet.quarters.append({
                "CadetAttempt": cadet.id,
                "class": cadet.playerClass,
                "levelbegin": levelbegin,                
                "levelend": cadet.level,
                "Y": year,
                "Q": f"Q{quarter}",
                "Job": jobdesc,
                "Surv": '+',
                "Jail": "+" if jailed else "-",
                "LvlUp": "+" if lvl_roll >= lDC else "-",
                "GP": gp_,
                "guilded": guilded

            })

            # Exit conditions
            if cadet.rep < -3:
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
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--characterClass",type=str,help="class to generate", default="footSoldier")
    parser.add_argument("--MusterOutLevel",type=int,help="musterOutLevel", default=4)
    args = parser.parse_args()  
    CharClass = args.characterClass
    MusterOutLevel=args.MusterOutLevel
    
    cadet = runClassSim()
    for q in cadet.quarters:
        #print(f"cadet:{q['CadetAttempt']} | {q['class']}:{q['levelbegin']}/{q['levelend']} | Y{q['Y']}{q['Q']} {q['Job']} | Surv:{q['Surv']} | Jail:{q['Jail']} | LvlUp:{q['LvlUp']} | gulded:{q['guilded']} | GP saved:{q['GP']}")
        #print(f"cadet:{q['CadetAttempt']:<8} | {q['class']}:{q['levelbegin']}/{q['levelend']} | Y{q['Y']}{q['Q']} {q['Job']} | Surv:{q['Surv']} | Jail:{q['Jail']} | LvlUp:{q['LvlUp']} | gulded:{q['guilded']} | GP saved:{q['GP']}")        

        
        print(
        f"cadet:{q['CadetAttempt']:<8} | "
        f"{q['class']}:{q['levelbegin']}/{q['levelend']} | "
        f"Y{q['Y']}{q['Q']} {q['Job']} | "
        f"Surv:{q['Surv']} | "
        f"Jail:{q['Jail']} | "
        f"LvlUp:{q['LvlUp']} | "
        f"gulded:{q['guilded']} | "
        f"GP saved:{q['GP']}"
)
        





