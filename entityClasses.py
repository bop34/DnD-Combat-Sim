# Import the classes to be used later
try:
    import random
    import time
except ModuleNotFoundError:
    print('Failed to import background modules')
    
def strCoords(x,y):
    return str(x) + ',' + str(y)
# Mob class, which contains monsters
class Mob():
    entities = {}
    # Do not make more than 26!
    mapWidth = 20
    mapWidth +=1
    mapHeight = 15
    mapHeight +=1
    battlemap = {}
    # Define all mob properties
    def __init__ (self, name, mapName, damage, maxHealth, x, y, ac, attackBonus = 0, health = -1, nextMove = 'y', char = '֍',speed = 1):
        self.name = name
        self.attackDamage = damage
        self.maxHealth = maxHealth
        self.x = x
        self.y = y
        self.ac = ac
        self.attackBonus = attackBonus
        self.nextMove = nextMove
        self.char = char
        self.mapName = mapName
        self.speed = speed
        if health == -1:
            self.health = self.maxHealth
        else:
            self.health = health
            
    # Return basic mob info, for testing
    def __str__ (self):
        return """%s--> %s/%s""" % (self.name, str(self.health), str(self.maxHealth))
    
    # Attack another mob, rolling for damage
    def attack(self,target,attackType='m'): # This will be expanded upon to add ranged attacks later
        self.attackRoll = random.randint(1,20)
        self.damage = random.randint(1,4) + self.attackDamage
        if attackType == 'm':
            self.surroundingCoords = [strCoords(self.x+1,self.y),strCoords(self.x-1,self.y),strCoords(self.x,self.y+1),strCoords(self.x,self.y-1)]
            if strCoords(Mob.entities[target].x,Mob.entities[target].y) in self.surroundingCoords:
                self.canAttack = True
            else:
                self.canAttack = False
                print('--> Attack failed. Please report an issue on github with a screenshot detailed information if the error continues')
        else:
            self.canAttack = True

        if self.canAttack:
            if Mob.entities[target].ac <=  self.attackRoll:
                Mob.entities[target].health = Mob.entities[target].health - self.damage
                print('--> '+self.name + " rolled a " + str(self.attackRoll) + " to hit " + Mob.entities[target].name + ", and did " +str(self.damage) + " damage")
            else:
                print('--> '+self.name + " rolled a " + str(self.attackRoll) + " to hit " + Mob.entities[target].name + " but missed.")
            
    # A function to run when the mob is at 0 hp
    def die(self): # Done
        print ('--> '+self.name + ' dropped to 0 hp and died')
        del Mob.entities[self.mapName]

    # Fill the map and loop through it, adding the Mobs. Barriers will be added soon
    def pushMap(): # Done
        # Reset the map
        Mob.battlemap = {}
        # Repeat for the height of the map
        for y in range (1,Mob.mapHeight):
            # Repeat through the selected width of the map
            for x in range(1,Mob.mapWidth):
                # Set the selected coordinate to empty
                Mob.battlemap[str(x) + ',' + str(y)] = ' '
        # Repeat through the entity dict
        for entName,obj in Mob.entities.items():
            # Set the selected coordinate to the entity's icon
            Mob.battlemap[str(obj.x) + ',' + str(obj.y)] = obj.char
    
    def printMap(): # Done
        # Add letter selectors
        letters = '   '
        for x in range (1,Mob.mapWidth):
            letters = letters + chr(x+64)
        print (letters)
        # Print a line below the letters
        print ('  '+'_' * (Mob.mapWidth+1))
        # Loop through the map height
        for y in range(1,Mob.mapHeight):
            # Add a starting line
            line = str(y) + ' ' * (2-len(str(y))) + '|'
            # Repeat through the width
            for x in range(1,Mob.mapWidth):
                line = line + Mob.battlemap[str(x) + ',' + str(y)]
            line = line +'|'
            print(line)
        print('  '+ '¯' * (Mob.mapWidth+1))
        
    def jump(self,targetX,targetY): # Done
        # Only jump if the selected spot is empty, stopping off map movement and conflicting spaces
        if Mob.battlemap[str(targetX) + ',' + str(targetY)] == ' ':
            self.x = targetX
            self.y = targetY
        else:
            print('--> '+self.name + "tried to move but failed")

    def pathfind(self, x,y): # Done
        if self.nextMove == 'x':
            if x < self.x:
                self.goalx = self.x-1
            elif x > self.x:
                self.goalx = self.x+1
            self.nextMove = 'y'
            self.goaly = self.y
        elif self.nextMove == 'y':
            if y < self.y:
                self.goaly = self.y-1
            elif y > self.y:
                self.goaly = self.y+1
            self.nextMove = 'x'
            self.goalx = self.x
        else:
            print('--> The pathfinding failed due to RAM corruption')            
            print('--> It will try to fix itself, but if the issue continues, please report it on Github with a screenshot')
            if random.randint(1,2) == 1:
                self.nextMove = 'x'
            else:
                self.nextMove = 'y'

        # Run every game loop to check if the mob is dead
    def checkDeath(self):
        if self.health<=0:
            self.die()
            return True
        
def findCoords(x,y): # Done
    try:
        coords = str(x)+','+str(y)
        selectedLocation = Mob.battlemap(coords)
    except KeyError:
        print('The selected coordinates do not exist')
    if selectedLocation == ' ':
        print(coords + ' is empty')
    else:
        print(coords + ' contains ' + selectedLocation)
