import time
import sys
try:
    from entityClasses import *
    credits = open('credits.txt')
    credits = credits.read()
    future = open('futureAdditions.txt')
    future = future.read()
except:
    print('Failed to import files')
    print('Make sure you extracted the code from the .zip file, and it is all in the same folder')
    input()
    sys.exit()

optScreen = '''
Options:
1] Fight a prebuilt monster
2] Design and fight a custom monster
3] Fight a randomly generated monster
4] Fight a swarm of weak monsters
5] See what will be added in the future
6] Credits
7] Exit the game'''
playerturn = False

def doMap():
    Mob.pushMap()
    Mob.printMap()

def shouldMove(mobID):
    surroundingCoords = [strCoords(Mob.entities[mobID].x+1,Mob.entities[mobID].y),strCoords(Mob.entities[mobID].x-1,Mob.entities[mobID].y),strCoords(Mob.entities[mobID].x,Mob.entities[mobID].y+1),strCoords(Mob.entities[mobID].x,Mob.entities[mobID].y-1)]
    playerCoordsStr = strCoords(Mob.entities['p'].x,Mob.entities['p'].y)
    for L in range(0,len(surroundingCoords)):
        if playerCoordsStr == surroundingCoords[L]:
            return False
        else:
            return True

print('''Welcome to COMBAT SIM v%s!
In this game, you will fight against monsters on a 2D grid
You will take turns moving and fighting
The combat system was inspired by DUNGEONS AND DRAGONS, owned and operated by Wizards of the Coast
=======================================================''' % ('0.1'))
print('--> What is your character\'s name?')
name = input('--> ')

startgm = False
while True:
    # Reset the entities
    Mob.entities = {"p" : Mob("USER", 'p', 5, 10, 15, 15, 10,char = 'P',speed=4)}
    Mob.entities['p'].name = name
    # Open the start screen---------
    print(optScreen)
    startOption = input('--> ')
    if startOption == '1':# Default monsters
        Mob.entities['1'] = Mob("Spider", '1', 5, 10, 1, 1, 10,char='T',speed=6)
        startgm = True
    elif startOption == '2':# Monster creator
        while True:
            mapVal = str(len(Mob.entities)-1)
            opName = input('Name--> ')
            while True:
                try:
                    opAttackDamage = input('Attack damage--> ')
                    opMaxHealth = input('Max health--> ')
                    opX = int(input('X--> '))
                    opY = int(input('Y--> '))
                    opAC = int(input('AC--> '))
                    opSpeed = int(input('Speed--> '))
                except:
                    print('Make sure all of the values are integers')
                else:
                    break
            while True:
                opChar = input('Map Icon--> ')
                if not len(opChar) ==1:
                    print ('--> The map icon needs to be exactly one character')
                elif opChar=='P':
                    print('--> For technical reasons, the character cannot be \'P\'')
                else:
                    break
            try:
                Mob.entities[mapVal] = Mob(opName,mapVal,opAttackDamage,opMaxHealth,opX,opY,opAC,speed=opSpeed,char=opChar)
            except:
                print('--> Something went wrong creating the mob, please try again, or restart the program')
                print('--> If the error persists, please report it with a screenshot on Github')
            
            print('Type c to continue creating mobs, g to start the game, and e to quit')
            while True:
                continq = input('--> ')
                if continq == 'g':
                    print('--> Mob(s) created! Starting game...')
                    br = True
                    startgm = True
                    break
                elif continq == 'c':
                    br = False
                    break
                elif continq == 'e':
                    br = True
                else:
                    print('--> That is not an option')
                    br = False
                    pass
            if br:# Break monster creator
                br = False
                Mob.entities = {}
                break
    
    elif startOption == '3':#Random monster
        print('Coming soon')
    elif startOption == '4':#Weak monsters
        print('Coming soon')
    elif startOption == '5':#Future options
        print(future)
    elif startOption == '6':#Credits
        print(credits)
    elif startOption == '7':#Quit
        break
    #-----------------------------

    #Game loop
    if startgm:
        pDead = False
        while True:
            if len(Mob.entities) <= 1:#Check if only one mob is left or if the player is dead
                startgm = False
                break
        
            doMap()#Push and Print map
            for name,obj in Mob.entities.items():
                dumPlaceholder = name
                print(obj)
            # Player turn--------------
            playerturn = True
            p = Mob.entities['p']
            if p.checkDeath():# Check if player is dead
                print('--> Game over!')
                startgm = False
                break
            
            mvT = p.speed
            options = ['Move','Attack','End your turn']
            
            while playerturn:
                p = Mob.entities['p']
                
                print('Options:')
                for x in range(0,len(options)):
                    print('%s] %s' % (x+1,options[x]))
                gameoption = input('--> ')
                # Move
                if options[int(gameoption)-1] == 'Move' and mvT > 0:
                    psurroundings = {'Right':strCoords(p.x+1,p.y),'Left':strCoords(p.x-1,p.y),'Down':strCoords(p.x,p.y+1),'Up':strCoords(p.x,p.y-1)}
                    if p.x == 1:
                        del psuroundings['Left']
                    elif p.x == 20:
                        del psurroundings['Right']
                    if p.y == 1:
                        del psurroundings['Up']
                    elif p.y == 15:
                        del psurroundings['Down']
                    x=1
                    optionsMap = {}
                    for direction,val in psurroundings.items():
                        if not Mob.battlemap[val] == ' ':
                            del psurroundings[direction]
                        print('%s] %s' % (x,direction))
                        optionsMap[str(x)] = direction
                        x+=1
                    while True:
                        moveoption = input('--> ')
                        try:
                            if bool(optionsMap[moveoption]):
                                break
                        except:
                            print('--> Please enter a valid response')
                        
                    mvT += -1
                    if mvT < 1 :
                        del options[0]
                    if optionsMap[moveoption] == 'Up':
                        p.jump(p.x,p.y-1)
                    elif optionsMap[moveoption] == 'Down':
                        p.jump(p.x,p.y+1)
                    elif optionsMap[moveoption] == 'Left':
                        p.jump(p.x-1,p.y)
                    elif optionsMap[moveoption] == 'Right':
                        p.jump(p.x+1,p.y)
                    doMap()
                # Attack
                elif options[int(gameoption)-1] == 'Attack':
                    attackOptions=[]
                    p.surroundingCoords = [strCoords(p.x+1,p.y),strCoords(p.x-1,p.y),strCoords(p.x,p.y+1),strCoords(p.x,p.y-1)]
                    for name,obj in Mob.entities.items():
                        if obj == p:
                            continue
                        if not strCoords(obj.x,obj.y) in p.surroundingCoords:
                            continue
                        attackOptions.append(obj)
                    if attackOptions == []:
                        continue
                    num = 1
                    for i in attackOptions:
                        print('%s] %s' % (num,i.name))
                        num +=1
                    while True:
                        attackOp = int(input('--> '))-1
                        try:
                            if bool(attackOptions[attackOp]):
                                break
                        except:
                            print('--> Please enter a valid response')
                    p.attack(attackOptions[int(attackOp)].mapName)
                    for i in range (0,len(options)):
                        if options[i] == 'Attack':
                            del options[i]
                            break

                    
                # Exit turn
                elif options[int(gameoption)-1] == 'End your turn':
                    break
                
            # Mob turns-----------------
            # Loop through for each mob
            for mobs in range(1,len(Mob.entities)):
                # Set mobID to match the mapID
                mobID = str(mobs)
                if Mob.entities[mobID].checkDeath():
                    doMap()
            for mobs in range(1,len(Mob.entities)):
                # Set mobID to match the mapID
                mobID = str(mobs)
                if Mob.entities[mobID].checkDeath():
                    continue
                # Move once for each speed
                for sp in range (0,Mob.entities[mobID].speed):
                    Mob.entities[mobID].pathfind(Mob.entities['p'].x,Mob.entities['p'].y)
                    
                    if shouldMove(mobID):
                        Mob.entities[mobID].jump(Mob.entities[mobID].goalx,Mob.entities[mobID].goaly)
                doMap()
                # Attack
                if not shouldMove(mobID):
                    print('Attacking')
                    Mob.entities[mobID].attack('p')
            


print('--> Thanks for playing!')
input()
