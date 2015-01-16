from methods import *
from actors import *
from enemies import *

# Target Selector
def targetSelect(enemies):
    if len(enemies) > 1:
        while True:
            print("Pick a Target:")
            n = 1
            for i in enemies:
                print("  ",str(n) + ":",i.name,n)
                n += 1
            target = eval(input("(Pick a number) ")) - 1
            if target in range(len(enemies)):
                target = enemies[target]
                return target
            else:
                text("Incorrect target")
    else:
        return enemies[0]

# Battle Engine
def battle(hero,enemies,escape=True):
    # enemies is a [list] of enemy objects, not strings
    # escape is a boolean, set to False if player cannot escape battle (bosses, etc.), defaults to True
    battleExp = 0
    battleMoney = 0
    turn = 0
    battling = True
    ''' battleExp is a container for all the EXP gained during this battle, used for showing the total at the end of the battle
        battleMoney is a container for all the money gained during the battle, dumps into player's money variable after battle. Note that if a player flees a battle halfway through, they keep EXP, but not any money. Think of it as not being able to loot any bodies.
        turn is a turn counter. Not yet implemented, as there's no call for it yet, but probably will be eventually
        battling is a boolean that acts as the loop condition. Also used inside the loop for escaping
    '''
    
    # Schnazzy battle header
    print("=" * 3)
    print("=" * 4)
    print("=" * 5)
    print("=" * 6)
    print("=" * 7)
    print("=" * 8)
    print("=" * 9)
    print("=" * 10)
    print("=" * 11)
    print("| BATTLE! |")
    print("=" * 11)
    b(1)
    
    # Main battle loop
    while battling:
        # Print player stats
        print("*" * 12)
        print("|" + " " * int((10 - len(hero.name))/2) + hero.name + " " * \
              int((10 - len(hero.name))/2) + "|")
        print("| HP: " + str(hero.health) + "/" + str(hero.maxHealth))
        print("*" * 12)
        b(2)
        print("=" * 24)
        b(2)

        # If there are multiple enemies, number them
        n = 1
        numberedEnemies = []
        for i in enemies:
            numberedEnemies.append(str(i) + " " + str(n))
            n += 1
            
        # Print enemy stats
        for i in enemies:
            if len(enemies) > 1:
                enemyNumber = str(enemies.index(i) + 1)
            else:
                enemyNumber = ""
            print("*" * 12)
            print("| " + i.name + " " + enemyNumber)
            print("| HP: " + str(i.health) + "/" + str(i.maxHealth))
            if i.guarding:
                print("| Defending!")
            print("*" * 12)

        # Lowers the player's guard if they're guarding
        hero.unDefend()

        # Choose a battle command
        escaped = False
        while True:
            battleChoice = options("ATTACK","SPECIAL","DEFEND","EXAMINE","MENU",\
                                   "RUN")
            if battleChoice == "ATTACK":
                hero.attack(targetSelect(enemies))
                break
            elif battleChoice == "SPECIAL":
                text("Special attacks are not yet implemented")
            elif battleChoice == "DEFEND":
                hero.defend()
                break
            elif battleChoice == "EXAMINE":
                hero.examine(targetSelect(enemies))
                break
            elif battleChoice == "RUN":
                escaped = hero.runAway(enemies,escape)
                break
        
        # if an escape attempt was successful, tell the player how much exp they got, then end the battle immediately instead of waiting for all turns to be taken.
        if escaped:
            break
            
        # checks for dead enemies
        for i in enemies:
            if i.health <= 0:
                text(i.name + " was defeated!")
                # EXP is gained in-battle a-la Pokemon, allowing a player to be healed if they level up mid-battle.
                text("You gained " + str(i.expYield) + " Experience")
                hero.exp += i.expYield
                battleExp += i.expYield
                if hero.exp >= hero.expNextLevel:
                    hero.levelUp()
                battleMoney += i.moneyYield
                enemies.remove(i)
                
                
        # If no enemies remain, the battle is won and the battle immediately ends
        if not enemies:
            print("!" * 11)
            print("! VICTORY !")
            print("!" * 11)
            break

        # Each enemy lowers their guard if defending, then takes their turn
        for i in enemies:
            print(i.name,str(enemies.index(i) + 1) + ":")
            i.unDefend()
            i.behavior(hero)
            
        # Checks for dead player
        if hero.health <= 0:
            text(i.name + " was defeated!")
            text("X X X GAME OVER X X X")
            quit()
    
    # Shows player their loot
    # All dropped items will show up here when items are implemented
    print("Total EXP Gained:",battleExp)
    print("Money Collected: $" + str(battleMoney))
    print("Current Health:",str(hero.health) + "/" + str(hero.maxHealth))
    print("=" * 10)
    print("=" * 9)
    print("=" * 8)
    print("=" * 7)
    print("=" * 6)
    print("=" * 5)
    print("=" * 4)
    print("=" * 3)