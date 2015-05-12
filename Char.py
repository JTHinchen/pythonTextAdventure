from random import*
class Char:
    def __init__(self,Game,name,sym):
        self.name=name
        self.sym=sym
        self.inv=[]
        self.pos=Game.world.start  
    def move(self,Game): 
        end=0  
        directions=[(self.pos[0]+1,self.pos[1]),(self.pos[0]-1,self.pos[1]),(self.pos[0],self.pos[1]-1),(self.pos[0],self.pos[1]+1)]
        dkey=['East','West','North','South']
        print ('\nYou are in a maze.')
        for i in Game.obj:
            if self.pos==i:
                print ('There is a', Game.terms[Game.obj[i]],'in the room')
        if self.pos==self.otherChar(Game).pos:
            print (self.otherChar(Game).name, 'is in the room')
        for i in range(4):
            if directions[i] in Game.fix and Game.fix[directions[i]]=='|S':
                print('There is a secret door to the', dkey[i])
            elif directions[i] in Game.world.rooms:
                print('There is a door to the', dkey[i])
        while end==0:
            end=1#
            dirc=input(self.name+': What would you like to do?\n')
            if dirc=='pick up' and self.pos in Game.pickup.keys():
                self.inv.append(Game.terms[Game.obj.pop(self.pos)])
                end=0
            elif dirc=='use' and self.pos in Game.fix.keys():
                if Game.terms[Game.fix[self.pos]]=='door':
                    if 'key' in self.inv:
                        print ('You have opened the door')
                        self.inv.remove('key')
                        Game.nextl=1
                    else:
                        print ('The door is locked')
                        end=0
            elif dirc=='stuff':
                if len(self.inv)>0:
                    print ('You have: ', end="")
                    for i in self.inv:
                        print(i,' ',end="")
                    print()
                else:
                    print ('You have nothing')
                end=0
            elif dirc=='up' and directions[2] in Game.world.rooms:
                self.pos=directions[2]
            elif dirc=='down' and directions[3] in Game.world.rooms:
                self.pos=directions[3]
            elif dirc=='left' and directions[1] in Game.world.rooms:
                self.pos=directions[1]
            elif dirc=='right' and directions[0] in Game.world.rooms:
                self.pos=directions[0]
            elif dirc=='wait':
                end=1
            else:
                print("You can't do that!")
                end=0#
    def otherChar(self,Game):
        if self.name==Game.chars[Game.c1]:
            return Game.c2
        elif self.name==Game.chars[Game.c2]:
            return Game.c1
    def reset (self,Game):
        self.pos=Game.world.start
