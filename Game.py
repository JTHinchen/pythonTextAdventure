from random import*
from Map import*
from Char import*

class Game:
    def __init__(self):
        self.world=Map()
        self.c1=Char(self,"Char 1",'|/')
        self.c2=Char(self,"Char 2",'|\\')
        self.chars={self.c1:self.c1.name,self.c2:self.c2.name}
        self.terms={'|k':'key','|D':'door','|S':'Secret Door'}
        self.newLev()
    def newLev (self):
        self.world=Map()       
        self.nextl=0
        self.obj={}
        self.fix={}
        self.pickup={}
        self.putIn('|k',self.pickup)
        self.putIn('|D',self.fix)
        self.addSecs()
        self.obj=self.pickup.copy()
        self.obj.update(self.fix)
        for char in self.chars:
            char.reset(self)
    def display(self):                                                   #makes X grid, demonstration only (could do a minimap I guess)
        d={}
        for i in range(10):                                                     #i and j are switched from tradtional vector notation. oops.
            d[i]=[]
            for j in range (10):
                if self.world.grid[(j,i)]==1:
                    d[i].append('|O')
                else:
                    d[i].append('| ')
        for i in self.obj:
            d[i[1]][i[0]]=self.obj[i]
        d[self.c1.pos[1]][self.c1.pos[0]]=self.c1.sym
        d[self.c2.pos[1]][self.c2.pos[0]]=self.c2.sym
        if self.c1.pos==self.c2.pos:
            d[self.c2.pos[1]][self.c2.pos[0]]='|X'
        for i in range(10):
            for j in range(10):
                print (d[i][j],end="")
            print()
    def addSecs(self):
        for i in range(randrange(5)+5):
            self.putIn('|S',self.fix)
    def putIn(self,sym,lis):
        pos=self.world.emprm[randrange(len(self.world.emprm))]
        lis[pos]=sym 
        self.world.emprm.remove(pos)
    def run(self):
        end=0
        while end!='no':
            for i in self.chars:
                self.display()
                i.move(self)
                if self.nextl==1:
                    end=input("Continue?\n")
                    if end=='no':
                        break
                    self.newLev()
        print ('Bye!')                 

a=Game()
a.run()
