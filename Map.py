from random import*
class Map:
    def __init__(self):
        XMax=10                                                                 #Maximum length/height of map
        YMax=10
        chance=12                                                               #base chance (1/chance) that a given room will be generated
        minRooms=15                                                             #minimum number of rooms created
        self.grid={}
        for i in range(XMax):                                                   #creates x by y gird of rooms, all turned OFF
            for j in range(YMax):
                self.grid[(i,j)]=0 
        self.start=(int(XMax/2),int(YMax/2))                                    #room in center is turned ON
        self.grid[self.start]=1
        self.rooms=[self.start]
        self.emprm=[]                                                           #ugh theres no good way to pass by value is there
        end=0
        n=0
        while end==0:                                                           #repeats until desired number of rooms is reached or surpassed
            for room in self.rooms:                                             #checks all ON rooms
                for empty in self.sideCheck(room):                              #checks list of OFF rooms bordering current ON
                    #chanceMod=chance/(len(sideCheck(empty,self.grid))+1)       #modifies chance room will be generated, currently gives higher chance torooms bordering more OFFs
                    if len(self.sideCheck(empty))<3:                            #The current mod creates generally non-looping, very branched narrow paths
                           chanceMod=100000
                    else:
                           chanceMod=2
                    if randrange(chanceMod)==0:                                 #turns room ON and adds to list of ONs
                        self.grid[empty]=1
                        self.rooms.append(empty)
                        self.emprm.append(empty)
                        n+=1
            if n>=minRooms:
                end=1
    def sideCheck(self,room):                                              #takes a room (coords) and grid (list of room coords) and returns the rooms adjacent (up down left right) that are turned OFF
        openBorders=[]
        borders=[(room[0]+1,room[1]),(room[0]-1,room[1]),(room[0],room[1]-1),(room[0],room[1]+1)]
        for room in borders:
            if room in self.grid and self.grid[room]==0:
                openBorders.append(room)
        return openBorders
