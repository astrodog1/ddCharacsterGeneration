import random
from dataclasses import dataclass, field
from typing import List, Dict

def roll(dice: str) -> int:
    n, d = map(int, dice.lower().split("d"))
    return sum(random.randint(1, d) for _ in range(n))

@dataclass
class RogueStats:
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

def generate_rogue_stats() -> RogueStats:
    return RogueStats(
        STR=roll("3d6"),
        DEX=roll("3d6") + 2,
        CON=roll("3d6"),
        WIS=roll("3d6"),
        INT=roll("3d6"),
        CHA=roll("3d6"),
        PER=roll("3d6"),
        REP=2,
        SS=2,
        playerclass='urchin',
        LIT=roll("1d20")
    )



streetUrchin_assignments = [
    #jobDesc            ,jobDC      ,SurvDC     ,lvlDC  ,JailDC     ,gpDC   ,GuildDC
    ("Beg"              ,6          ,2          ,19     ,1          ,"1d10" , 20)
    ,("Pickpocket"      ,12         ,3          ,19     ,2          ,"1d10", 18)
    ,("Intimidate"      ,14         ,3          ,18     ,3          ,"1d10", 15)
    ,("Steal"           ,18         ,3          ,17     ,4          ,"2d10", 15)
    ,("Highwayman"      ,19         ,3          ,17     ,3          ,"2d10", 15)
    ,("Murder"          ,20         ,4          ,16     ,6          ,"2d10", 10)
]
#desc,Assginroll,survival,levelup,avoidJail,gp,guildDC
rogue_assignments = [  
    #jobDesc                ,jobDC      ,SurvDC     ,lvlDC  ,JailDC     ,gpDC   ,GuildDC    
    ("Beg"                  ,6          ,2          ,19     ,1          ,"2d10"  ,99)
    ,("Pickpocket"          ,9          ,3          ,19     ,2          ,"2d10"  ,99)
    ,("Smuggling"           ,12         ,3          ,19     ,2          ,"2d10"  ,99)
    ,("Highwayman"          ,14         ,4          ,16     ,2          ,"3d10" ,99)
    ,("Petty Burglary"      ,15         ,3          ,17     ,2          ,"2d10" ,99)
    ,("Grand Burglary"      ,16         ,4          ,16     ,3          ,"4d10" ,99)
    ,("Extortion"           ,17         ,3          ,17     ,3          ,"2d10" ,99)
    ,("Protection Rackets"  ,18         ,3          ,17     ,2          ,"2d10" ,99)
    ,("Kidnapping"          ,19         ,4          ,15     ,4          ,"8d10" ,99)
    ,("Assassination"       ,20         ,6          ,14     ,4          ,"10d10",99)
]
# @dataclass is used to automatically generate special methods like __init__, __repr__, etc.
#from typing import Callable
@dataclass
class RogueCadet:
    id: int
    stats: RogueStats
    age: int = 12
    level: int = 0
    gp: int = 0
    rep: float = 2.0
    playerClass: str = 'urchin'
    jail_log: List[str] = field(default_factory=list)
    quarters: List[Dict] = field(default_factory=list)
    

# '->' means the function returns a RogueCadet object
def run_rogue_sim() -> RogueCadet:
    count = 1
    while True:  #sim loop
        cadet = RogueCadet(id=count, stats=generate_rogue_stats())
        cadet.rep = cadet.stats.REP
        year, quarter = 1, 1  #restart year/qtr for each cadet

        while True:  #cadet loop
            qtrAssignRoll = roll("1d20") 
            if cadet.playerClass == 'urchin':
                assignment = streetUrchin_assignments
            else:
                assignment = rogue_assignments

            #determine qtr assignment
            for item in assignment:
                if qtrAssignRoll <= item[1]:
                    qtrAssignmentRoll = item
                    break
            
            #desc   ,Assginroll ,survival   ,levelup    ,avoidJail  ,gp     ,guildDC
            jobdesc, jobDC      ,sDC        ,lDC        ,jDC        ,gp_fn  ,gDC        = qtrAssignmentRoll

            # Survival rolls
            survival_rolls = [random.randint(1, 20) for _ in range(cadet.level + 1)]
            survived = any(r >= sDC for r in survival_rolls)
            if not survived:
                break

            # Jail----------------------------------------
            jail_roll = random.randint(1, 20)
            jailed = jail_roll < jDC
            if jailed:
                cadet.age += 1
                cadet.rep -= 0.5
                cadet.jail_log.append(jobdesc)
                #gp = 0
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
            if cadet.playerClass == 'urchin':
                guild_roll = random.randint(1, 20)
                if guild_roll >= gDC:
                    cadet.playerClass = 'rogue'
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
            if cadet.level >= 4:
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
    cadet = run_rogue_sim()
    # print(f"\n🎲 Rogue Cadet #{cadet.id} reached Level 4 with {cadet.gp} gp!")
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
