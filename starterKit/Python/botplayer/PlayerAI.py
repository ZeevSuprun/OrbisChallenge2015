from PythonClientAPI.libs.Game.Enums import *
import time

class PlayerAI:

    def __init__(self):
        # Initialize any objects or variables you need here.
        self.shieldtime = 0
        self.lastconstraint = 0
        pass

    def createMaze(self, gameboard):
        '''This function creates and returns a 2D array of integers, gameMap,
           that contains 0 where there are empty spaces, 1 where there are walls, 2 where there are turrets
            3 where there are powerups.'''
        gameMap = [[0 for col in range(gameboard.width)] for row in range(gameboard.height)]

        for wall in gameboard.walls:
            gameMap[wall.y][wall.x] = 1
        for turret in gameboard.turrets:
            gameMap[turret.y][turret.x] = 2
        for p_up in gameboard.power_ups:
            gameMap[p_up.y][p_up.x] = 3

        #for row in range(gameboard.height):
        #    for col in range (gameboard.width):
        #        print(gameMap[row][col], end="")
        #print("\n")

        return gameMap

    def cR(self, col1, row1, col2, row2, gameMap):
        #Helper function for clearRange that checks if
        #  there are any blocked points between p1 and p2, without wrapping around.
        distance = 0

        if (col1 == col2 and row1 == row2):
            #The 2 points are the same.
            return -1
        elif col1 == col2:
            #The 2 points are in the same row.
            iterator = 1
            if(row2 < row1):
                iterator = -1
            #Iterator is needed to make the range function work with y2 smaller than y1
            for row in range(row1, row2, iterator):
                distance += 1
                if (gameMap[row][col1] == 1 or gameMap[row][col1] == 2):
                    #There is a wall or a turret between y1 and y2, so there is no clear path.
                    return -1

            #For loop has finished executing
            return abs(distance)
        elif row1 == row2:
            #the 2 points are in the same row.
            iterator = 1
            if(col2 < col1):
                iterator = -1
            for col in range(col1, col2, iterator):
                distance += 1
                if (gameMap[row1][col] == 1 or gameMap[row1][col] == 2):
                    #There is a wall or a turret between y1 and y2, so there is no clear path.
                    return -1
            return abs(distance)
        else:
            #They are neither in the same row nor in the same column
            return -1

    def clearRange(self, x1, y1, x2, y2, gameMap, gameboard):
        #if there is a clear path vertical/horizontal path from (x1, y1) and (x2, y2),
        #then return (pathLength, Direction) (where direction is from point 1 to point 2
        #if there is no clear path, return (-1, UP)
        #This function will be used to see if there's a clear path to shoot a turret or if we're within turret range.
        distance = 0
        clearDir = Direction.UP
        if (x1 == x2 and y1 == y2):
            #The 2 points are the same.
            return (-1, Direction.UP)
        elif x1 == x2:
            distance = self.cR(x1, y1, x2, y2, gameMap)

            if (distance != -1):
                #There is a clear path from point 1 to point 2 without wrapping around.
                if(y2 > y1):
                    clearDir = Direction.RIGHT
                else:
                    clearDir = Direction.LEFT
                return (distance, clearDir)
            else:
                #There is no direct clear path without wrapping around, but there might be one with wrapping around
                if (y1 < y2):
                    #y1 is closer to the 0 than y2 is, start by looking between y1 and 0
                    d1 = self.cR(x1, y1, x1, 0, gameMap) #d1 is the distance between y1 and 0, or -1 if it's not clear
                    if (d1 == -1):
                        #There is no wraparound path
                        return (-1, Direction.UP)
                    d2 = self.cR(x1, gameboard.width -1, x2, y2) #d2 is the distance between end column and y2, or -1 if it's not clear
                    if (d2 == -1):
                        #There is no wraparound path
                        return (-1, Direction.UP)
                    #if the program has reached this point, there is a wraparound path
                    return (d1 + d2, Direction.LEFT)
                else:
                    #y1 is closer to the end than y2, start by looking between y1 and end
                    d1 = self.cR(x1, y1, 0, gameboard.width -1, gameMap) #d1 is the distance between y1 and end, or -1 if it's not clear
                    if (d1 == -1):
                        #There is no wraparound path
                        return (-1, Direction.UP)
                    d2 = self.cR(x1, 0, x2, y2) #d2 is the distance between 0 and y2
                    if (d2 == -1):
                        #There is no wraparound path
                        return (-1, Direction.UP)
                    #if the program has reached this point, there is a wraparound path
                    return (d1 + d2, Direction.RIGHT)
        elif y1 == y2:

            #the 2 points are in the same row.
            distance = self.cR(x1, y1, x2, y2, gameMap)
            if (distance != -1):
                if(x2 > x1):
                    clearDir = Direction.DOWN
                else:
                    clearDir = Direction.UP
                return (distance, clearDir)
            else:
                if(x1 < x2):
                    #x1 is closer to 0 than x2 is.
                    d1 = self.cR(x1, y1, 0, y2, gameMap)
                    if (d1 == -1):
                        #There is no wraparound path
                        return (-1, Direction.UP)
                    d2 = self.cR(gameboard.height - 1, y1, x2, y2, gameMap)
                    if (d2 == -1):
                        #There is no wraparound path
                        return (-1, Direction.UP)
                    #if the program has reached this point, there is a wraparound path
                    return (d1 + d2, Direction.UP)
                else:
                    #x1 is closer to end than x2 is.
                    d1 = self.cR(x1, y1, gameboard.height - 1, y2, gameMap)
                    if (d1 == -1):
                        #There is no wraparound path
                        return (-1, Direction.UP)
                    d2 = self.cR(0, y1, x2, y2)
                    if (d2 == -1):
                        #There is no wraparound path
                        return (-1, Direction.UP)
                    #if the program has reached this point, there is a wraparound path
                    return (d1 + d2, Direction.UP)
        else:
            #They are neither in the same row nor in the same column
            return (-1, Direction.UP)

    def findPowerUps(self, player, gameMap, gameboard):
        #pathfinding algorithm that leads the robot to collect powerups and nothing else.
        #uses breadth first search: expand outwards until it hits a powerup.
        if not(len(gameboard.power_ups) > 0):
            #if no powerups left, do nothing
            #print("There are no power ups")
            return Move.NONE

        positions = {(player.y, player.x) : ""}
        #Positions is a dictionary. Key is a position, value is the string the bot took to get there.
        #the value is a string is a combination of 'w', 'a', 's' and 'd'
        while (len(positions) < gameboard.width*gameboard.height):
            for p in positions.copy():
                #for p in the keys of positions
                row = p[0]
                col = p[1]
                #Note: this pathfinding algorithm isn't including map wraparound yet.


                #print(positions)
                #Check if this point is a victory point.
                if (gameMap[row][col] == 3):
                    #print(positions.get(p))
                    #Start along the path the first character in it.
                    if(positions.get(p).startswith('d') and player.direction == Direction.RIGHT):
                        return Move.FORWARD
                    elif(positions.get(p).startswith('d') and player.direction != Direction.RIGHT):
                        return Move.FACE_RIGHT
                    elif(positions.get(p).startswith('a') and player.direction == Direction.LEFT):
                        return Move.FORWARD
                    elif(positions.get(p).startswith('a') and player.direction != Direction.LEFT):
                        return Move.FACE_LEFT
                    elif(positions.get(p).startswith('w') and player.direction == Direction.UP):
                        return Move.FORWARD
                    elif(positions.get(p).startswith('w') and player.direction != Direction.UP):
                        return Move.FACE_UP
                    elif(positions.get(p).startswith('s') and player.direction == Direction.DOWN):
                        return Move.FORWARD
                    elif(positions.get(p).startswith('s') and player.direction != Direction.DOWN):
                        return Move.FACE_DOWN
                    else:
                        return Move.SHOOT

                canGoRight = not(col + 1 >= gameboard.width or gameMap[row][col+1] in {1, 2} or (row,col+1) in positions.keys())
                canGoLeft = not(col - 1 < 0 or gameMap[row][col-1] in {1, 2} or (row, col-1) in positions.keys())
                canGoUp = not(row - 1 < 0 or gameMap[row-1][col] in {1, 2} or (row-1, col) in positions.keys())
                canGoDown = not(row + 1 >= gameboard.height or gameMap[row+1][col] in {1, 2} or (row+1, col) in positions.keys())

                #going left/right/up/down doesn't meet a win condition, add in
                if(canGoRight):
                    positions[(row,col+1)] = positions.get(p) + 'd'
                if(canGoLeft):
                    positions[(row,col-1)] = positions.get(p) + 'a'
                if(canGoUp):
                    positions[(row-1,col)] = positions.get(p) + 'w'
                if(canGoDown):
                    positions[(row+1,col)] = positions.get(p) + 's'

        return Move.NONE


    '''
    def get_move(self, gameboard, player, opponent):
        t1 = time.time() #FOR TESTING PURPOSES ONLY DELETE BEFORE SUBMISSION

        #The features of the gameboard, stored in a 2D integer array, used for pathfinding.
        gameMap = self.createMaze(gameboard)
        nextPathPoint = self.findPowerUps(player, gameMap, gameboard)
        print(nextPathPoint)
        return nextPathPoint
    '''

    '''
        # Step 1: Figure out which moves are valid based on the powerups we have.
        numTeleporters = len(gameboard.teleport_locations)
        print('The number of teleporters is: ' + str(numTeleporters))
        possibleMoves = {Move.FACE_UP, Move.FACE_DOWN, Move.FACE_LEFT, Move.FACE_RIGHT, Move.NONE, Move.SHOOT,
                         Move.FORWARD}
        if player.shield_count > 0 :
            possibleMoves.add(Move.SHIELD)
        if player.laser_count > 0:
            possibleMoves.add(Move.LASER)
        if player.teleport_count > 0:
            teleports = [Move.TELEPORT_0, Move.TELEPORT_1, Move.TELEPORT_2, Move.TELEPORT_3, Move.TELEPORT_4, Move.TELEPORT_5]
            for i in range(0, numTeleporters):
                possibleMoves.add(teleports[i])

        #If we are facing a wall, then Move.Forward is not a valid
        #possibleMoves Now contains all valid player moves.


        powerUpsPresent = False
        if (len(gameboard.power_ups) > 0):
            powerUpsPresent = True
        activeTurretsPresent = False


        print(time.time() - t1)            #FOR TESTING PURPOSES ONLY DELETE BEFORE SUBMISSION
        if(player.direction) == Direction.UP:
            return Move.FACE_DOWN
        else:
            return Move.FACE_UP
    '''

    def nextPos(self, x, y, direction ,gameboard):
        #Function returns the next position of the moving directional game object player
        a=[0,0]
        if(direction)==Direction.UP:
            if y==0:
                y=gameboard.height
            y=y-1
        elif(direction)==Direction.DOWN:
            y=y+1
            if y==gameboard.height:
                y=0
        elif(direction)==Direction.LEFT:
            if x==0:
                x=gameboard.width
            x=x-1
        elif(direction)==Direction.RIGHT:
            x=x+1
            if x==gameboard.width:
                x=0
        a[0]=x
        a[1]=y
        return a


    def turretSpotCheck(self,x,y,gamemap,gameboard):
        turret=gameboard.turrets
        sol=[0,-1,0]
        for i in range(len(turret)):
            ran2=self.clearRange(turret[i].x,turret[i].y,x,y,gamemap, gameboard)
            ran=ran2[0]
            seqlen=turret[i].fire_time+turret[i].cooldown_time
            seq=gameboard.current_turn%(seqlen)#seq is indicator of where it is in cycle
            #if seq less than fire time it is firing
            if (turret[i].is_dead):
                pass
            elif ran!=-1 and ran<4 and (seq < turret[i].fire_time):#If turret firing next turn and we are in range
                sol[0]=1
                sol[1]=0
                sol[2]=i
                return sol
            elif ran==-1:
                pass
            elif ran>4:
                if sol[0]==0:
                    sol[2]=i
            elif (seqlen-seq)<sol[1]:
                sol[0]=1
                sol[1]=seqlen-seq
                sol[2]=i
        return sol

    def checkSafe(self,x,y,orientation,shieldtime,opponent,player,gameboard,gameMap):#5-0
        #return 0 if safe, 1 if dangerous, 2-5 special conditions
        OpNext=self.nextPos(opponent.x, opponent.y, opponent.direction,gameboard)
        if(shieldtime<2):
            if (OpNext[0]==x and OpNext[1]==y):
                return 1
            if opponent.laser_count!=0:
                inrange=self.clearRange(player.x,player.y,opponent.x,opponent.y,gameMap, gameboard)
                if inrange[0]<=4:
                    return 1
            bullet=gameboard.bullets
            for i in range(len(bullet)):
                bulletdirrection=bullet[i].direction
                bulletnex=self.nextPos(bullet[i].x, bullet[i].y, bullet[i].direction, gameboard)
                #bulletnexobj=DirectionalGameObject{bulletnex[0],bulletnex[1],bullet[i].direction}
                bulletnexnex=self.nextPos(bulletnex[0],bulletnex[1],bullet[i].direction,gameboard)
                if (bulletnex[0]==x or bulletnex[1]==y):
                    return 1
                if (bulletnexnex[0]==x or bulletnexnex[1]==y):
                    return 2
            tsafe=self.turretSpotCheck(x,y,gameMap,gameboard)
            if tsafe[0]==1:
            #check if this is a turret range location
                if tsafe[1]==0:
                #check if its pattern has a dangerous label for next turn
                    return(1)
                inrange=self.clearRange(player.x,player.y,opponent.x,opponent.y,gameMap, gameboard)
                if inrange[1]==orientation:
                #elif we are looking in its direction
                    if tsafe[1]<2:
                        return 2#means we should turn left or right
                    return 3 #(golden opportunity to fire if 3 is returned)
                else:
                    if tsafe[1]<3:
                            return 5#means we should move forward
                    return 4 #Golden opportunity to turn towards it
        return 0

    def Constraints(self,player,shieldtime,opponent,gameboard,gameMap,lastConstraint):
        x=self.checkSafe(player.x,player.y,player.direction,shieldtime,opponent,player,gameboard,gameMap)
        forward=self.nextPos(player.x,player.y,player.direction,gameboard)
        opforward=self.nextPos(opponent.x,opponent.y,opponent.direction,gameboard)
        y=self.checkSafe(forward[0],forward[1],player.direction,shieldtime,opponent,player,gameboard,gameMap)
        if(x==1):
            if y==1:
                if player.tereport_count>0:
                    return 6 #teleport somewhere safe
                if player.shield_count>0:
                    return 3 #activate shield
                return 0 #all moves will lose a life
            return 5#move forward
        elif(x==2):
            return 2
        elif (x==3):
            if lastConstraint!=1:
                return 1 #fire
            return 0
        elif (x==4):
            return 10 #there is a turret in range and time to turn, turn towards the turret,
        if (forward[0]==opponent.x and forward[1]==opponent.y) or (forward[0]==opforward[0] and forward[1]==opforward[1]):
        #check if an oponent is in the spot in front of you or he is facing that location
            return 1 #1 means we win if we fire
        if shieldtime>1:
            tsafe=self.turretSpotCheck(player.x,player.y,gameMap,gameboard)
            if tsafe[0]==1:
            #check if our location is a turret range location
                if tsafe[1]==0:
                    return 9#9 means stay within turrets line of fire
            tsafefor=self.turretSpotCheck(forward[0],forward[1],gameMap,gameboard)
            if tsafefor[0]==1:
            #check if forward is a turret range location
                if tsafe[1]==0:
                #check if its pattern has a dangerous label for next turn
                    return 5#5 means move forward
            if opponent.laser_count!=0:
            #check if the opponent is with the lazer extension
                inrange=self.clearRange(player.x,player.y,opponent.x,opponent.y,gameMap, gameboard)
                if inrange[0]<=4:
                    return 4#means we should stay in oponents line of fire forward
                forinrange=self.clearRange(forward[0],forward[1],opponent.x,opponent.y,gameMap, gameboard)
                if forinrange[0]<=4:
                #assuming he is stationary, can we get within range of him by moving forward
                    return 5#means we should move forward
        if player.shield_count!=0:
        #check if we have a shield in inventory
            tsafe=self.turretSpotCheck(player.x,player.y,gameMap,gameboard)
            if tsafe[0]==1:
            #check if our location is a turret range location
                if tsafe[1]==0:
                #check if its pattern has a dangerous label for next turn
                    return 3#3 means activate shield
            if opponent.laser_count!=0:
            #check if the opponent is with the lazer extension
                inrange=self.clearRange(player.x,player.y,opponent.x,opponent.y,gameMap, gameboard)
                if inrange[0]<=4:
                #assuming he is stationary, are we within range of him by staying still
                    return 7#means we should avoid opponent if possible, otherwise we have a shield we can activate
        if (player.laser_count!=0 and opponent.shield_active==0):
        #check if we have a lazer in inventory and oponent has no active shield
            inrange=self.clearRange(player.x,player.y,opponent.x,opponent.y,gameMap, gameboard)
            if (inrange[0]<=4 and opponent.shield_count==0):
            #check if opponent is in range and has no shield in inventory
                return 8 #means we should activate lazer
            inrange=self.clearRange(player.x,player.y,opforward[0],opforward[1],gameMap, gameboard)
            if inrange[0]<=4:
            #check if opponent forward is in range
                return 8 #means we should activate lazer
            tsafe=self.turretSpotCheck(player.x,player.y,gameMap,gameboard)
            if tsafe[0]==1:
            #check if turret is in range
                return 8 #means we should activate lazer
        return 0 #0 means zeev is free to move

    def get_move(self, gameboard, player, opponent):
            '''
            t1 = time.time() #FOR TESTING PURPOSES ONLY DELETE BEFORE SUBMISSION

            #The features of the gameboard, stored in a 2D integer array, used for pathfinding.


            # Step 1: Figure out which moves are valid based on the powerups we have.
            possibleMoves={}

            print('The number of teleporters is: ' + str(numTeleporters))
            numTeleporters = len(gameboard.teleport_locations)
            '''
            gameMap = self.createMaze(gameboard)

            constraint=self.Constraints(player,self.shieldtime,opponent,gameboard,gameMap,self.lastconstraint)
            self.lastconstraint=constraint

            possibleMoves = {}

            if constraint==1:
                return Move.SHOOT
            elif constraint==2:
                if player.direction==Direction.UP or player.direction==Direction.DOWN:
                    possibleMoves ={Move.FACE_LEFT, Move.Face_RIGHT}
                else:
                    possibleMoves ={Move.FACE_UP, Move.Face_DOWN}
            elif constraint==3:
                return Move.SHIELD
            elif constraint==4:
                possibleMoves = {Move.FACE_UP, Move.FACE_DOWN, Move.FACE_LEFT, Move.FACE_RIGHT, Move.NONE, Move.SHOOT}
                #Removed forward from possible moves
            elif constraint==5:
                return Move.FORWARD
            elif constraint==6:
                teleports=gameboard.teleport_locations
                for i in range(len(teleports)):
                    safety=self.checkSafe(teleports[i][0],teleports[i][1],player.direction,self.shieldtime,opponent,player,gameboard,gameMap)
                    if safety !=1:
                        if i==0:
                            return Move.TELEPORT_0
                        elif i==1:
                            return Move.TELEPORT_1
                        elif i==2:
                            return Move.TELEPORT_2
                        elif i==3:
                            return Move.TELEPORT_3
                        elif i==4:
                            return Move.TELEPORT_4
                        elif i==5:
                            return Move.TELEPORT_5
                    if player.shield_count!=0:
                        return Move.SHIELD
                    possibleMoves = {Move.FACE_UP, Move.FACE_DOWN, Move.FACE_LEFT, Move.FACE_RIGHT, Move.NONE, Move.SHOOT, Move.FORWARD}
            elif constraint==7:
                forward=self.nextPos(player.x,player.y,player.direction,gameboard)
                safety=self.checkSafe(forward[0], forward[1], player.direction, self.shieldtime, opponent, player, gameboard, gameMap)
                if safety !=  1:
                    return Move.FORWARD
                return Move.SHIELD
            elif constraint==8:
                return Move.LASER
            elif constraint==9:
                possibleMoves = {Move.FACE_UP, Move.FACE_DOWN, Move.FACE_LEFT, Move.FACE_RIGHT, Move.NONE, Move.SHOOT}
                #Removed forward from possible moves
            elif constraint==10:
                inrange=self.clearRange(player.x,player.y,opponent.x,opponent.y,gameMap, gameboard)
                if inrange[2]==Direction.UP:
                    return Move.FACE_UP
                elif inrange[2]==Direction.DOWN:
                    return Move.FACE_DOWN
                elif inrange[2]==Direction.LEFT:
                    return Move.FACE_LEFT
                return Move.FACE_RIGHT
                #use inrange to find out where the turret is, turn in that direction
            else:
                possibleMoves = {Move.FACE_UP, Move.FACE_DOWN, Move.FACE_LEFT, Move.FACE_RIGHT, Move.NONE, Move.SHOOT, Move.FORWARD}

            #pathfinding.
            nextPathPoint = self.findPowerUps(player, gameMap, gameboard)
            if nextPathPoint in possibleMoves:
                return nextPathPoint
            elif len(possibleMoves) == 0:
                return Move.NONE
            else:
                return possibleMoves.pop()
