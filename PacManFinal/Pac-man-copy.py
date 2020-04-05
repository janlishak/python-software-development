import tkinter,copy,time

xx=28
yy=37
cell=16
c=tkinter.Canvas(width=cell*xx, height=cell*yy,bg='black')
c.pack()
body=0

plocha = tkinter.PhotoImage(file='mapa.png')
c.create_image(xx*cell//2, yy*cell//2, image=plocha)

def update_body():
    global body
    c.delete('body')
    c.create_text(16*14,32,text=str(body),fill='white',tags='body', font='Arial 25')

def dvojpole(xx, yy):
    pole=[]
    for x in range(xx):
        pole2=[]
        for y in range(yy):
            pole2.append("X")
        pole.append(pole2)
    return(pole)

def callback_key(event):
    #print(event)
    direction = ['Left', 'Up', 'Right', 'Down']
    for i in range(len(direction)):
        if event.keysym == direction[i]:
            playerOne.changeDirection(i)




blank = tkinter.PhotoImage(file='blank.gif')
coin = tkinter.PhotoImage(file='x.gif')
obrazky = dvojpole(xx,yy)
           
def update_all():
    global xx,yy
    val=['X', '.', '#', '*', 'O', '-']
    col=[blank, blank, blank, coin, blank, blank]
    for x in range(xx):
        for y in range(yy):
            for i in range(len(val)):
                if pole[x][y]==val[i]:
                    obrazky[x][y]=c.create_image(x*cell+cell//2, y*cell+cell//2, image=col[i])

def read(filename):
    y=0
    with open(filename) as fileobj:
        for line in fileobj:
            x=-1
            for ch in line:
                x+=1
                if ch !='\n':
                    pole[x][y]=ch
            y+=1

def mouse(event):
    print(event.x//cell,event.y//cell)

def checktile(mapa,x,y):
    if mapa[x][y]=='*' or mapa[x][y]=='.' or mapa[x][y]=='O':
        return True
    else:
        return False

def koniec_hry():
    c.delete('all')
    c.create_text(xx*cell//2,yy*cell//2,text='YOU SUCK',fill='white',font='Arial 40')
    c.update()
    c.after(3000,quit())
    
class ghost(object):

    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.body=c.create_image(x*cell+cell//2,y*cell+cell//2,image=self.image)
        self.map = copy.deepcopy(pole)
        self.lastx=100
        self.lasty=100
        
    def path(self,endX, endY):
        global pole
        self.map = copy.deepcopy(pole)
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1] 
        sym= ['>','!','<','^']  
        table=[[endX,endY]]
        self.map[endX][endY]='G'
        
        loop=True
        if endX==self.x and endY==self.y:
            loop=False 
        while(loop):
            new_table=[]
            for tile in table:
                for i in range(4):
                    tilex=tile[0]+dx[i]
                    tiley=tile[1]+dy[i] 
                    if checktile(self.map,tilex,tiley):
                        new_table.append([tilex,tiley])                        
                        self.map[tilex][tiley]=sym[i]
                        if tilex==self.x and tiley==self.y:
                            loop=False
            table=new_table
            if not table:
                loop=False

    def path_oneway(self,endX, endY, **kwargs):
        avoid = kwargs.get('avoid', False)
        global pole
        self.map = copy.deepcopy(pole)
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1] 
        sym= ['<','^','>','!']
        symReversed= ['>','!','<','^']
        table=[]
        self.map[self.x][self.y]='G'

        for i in range(4):
            tilex=self.x+dx[i]
            tiley=self.y+dy[i] 
            if checktile(self.map,tilex,tiley):
                if avoid:
                    if tilex==avoid[0] and tiley==avoid[1]:
                        continue
                if tilex==self.lastx and tiley==self.lasty:
                    continue
                table.append([tilex,tiley])
                self.map[tilex][tiley]=sym[i]

        print('loptrue')
        loop=True
        while(loop):
            new_table=[]
            for tile in table:
                ff=True
                for i in range(4):
                    tilex=tile[0]+dx[i]
                    tiley=tile[1]+dy[i] 
                    if checktile(self.map,tilex,tiley):
                        ff=False
                        new_table.append([tilex,tiley])
                        self.map[tilex][tiley]=sym[i]
                        if tilex==endX and tiley==endY:
                            loop=False
                if ff:
                    if avoid:
                        if tilex==avoid[0] and tiley==avoid[1]:
                            table=new_table
            if not table:
                loop=False

        new_map = copy.deepcopy(pole)
        while(not (endX==self.x and endY==self.y)):
            for i in range(4):
                if self.map[endX][endY]==symReversed[i]:
                    endX+=dx[i]
                    endY+=dy[i]
                    new_map[endX][endY]=symReversed[i]

                    break
                
        self.map = new_map
        
 
    def update(self):
        global cell
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1] 
        sym= ['<','^','>','!']
        for i in range(4):
            if self.map[self.x][self.y]==sym[i]:
                c.move(self.body, dx[i]*cell, dy[i]*cell)
                self.lastx=self.x
                self.lasty=self.y
                self.x+=dx[i]
                self.y+=dy[i]
                break


    def showpath(self):
        global xx,yy
        for y in range(yy):
            for x in range(xx):
                print(str(self.map[x][y]) ,end='')
            print('')

class player(object):

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.body=c.create_oval(x*cell,y*cell,(x+1)*cell,(y+1)*cell,fill=self.color)
        self.smer=0
        self.changesmer=0
        self.smerx=-1
        self.smery=0
        self.zivoty=3

    def strata_zivota():
        self.zivoty-=1
        if self.zivoty==0:
            koniec_hry()


    def changeDirection(self,changesmer):
        self.changesmer=changesmer

    def update(self):
        global cell,body
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1]
        if self.smer!=self.changesmer:
            short = pole[self.x+dx[self.changesmer]][self.y+dy[self.changesmer]]
            if short=='*' or short=='O' or short=='.':
                         self.smer=self.changesmer
        self.smerx=dx[self.smer]
        self.smery=dy[self.smer]

        if pole[self.x+self.smerx][self.y+self.smery]=='*':
            body+=10
            update_body()
            pole[self.x+self.smerx][self.y+self.smery]='.'
            c.itemconfig(obrazky[self.x+self.smerx][self.y+self.smery], image = blank)
            #print('*',end='')
            self.move()
        elif pole[self.x+self.smerx][self.y+self.smery]=='O':
            body+=10
            update_body()
            #print('O',end='')
            self.move()
        elif pole[self.x+self.smerx][self.y+self.smery]=='.':
            #print('.',end='')
            self.move()
    def move(self):
        c.move(self.body,self.smerx*cell,self.smery*cell)
        self.x+=self.smerx
        self.y+=self.smery
            
def timer():
    
    blinky.path(playerOne.x,playerOne.y)
    pinky.path(playerOne.x,playerOne.y)
    inky.path(playerOne.x,playerOne.y)
    clyde.path(playerOne.x,playerOne.y) 
    
    playerOne.update()
    blinky.update()
    pinky.update()
    inky.update()
    clyde.update()       
##    pinkX=jano.x
##    pinkY=jano.y
##    pinkS=jano.smer
##    dx = [-1, 0, 1, 0]
##    dy = [0, -1, 0, 1]
##    direction = ['Left', 'Up', 'Right', 'Down']
##    for i in range(6):
##        for rot in [+1, 0, -1, +2]:
##            rotation=(pinkS+rot+4)%4
##            short=pole[pinkX+dx[rotation]][pinkY+dy[rotation]]
##            if short=='*' or short=='O' or short=='.':
##                #print(direction[rotation])
##                pinkX=pinkX+dx[rotation]
##                pinkY=pinkY+dy[rotation]
##                pinkS=rotation
##                break
##
##    pinky.path_oneway(pinkX,pinkY)
##    if checktile(pinky.map,pinky.x,pinky.y):
##        pinky.path(jano.x,jano.y)
##
## outisde timer #pinky=ghost('pink',1,5)
    c.after(50,timer)




   
pole=dvojpole(xx, yy)
c.bind_all("<Key>", callback_key)
c.bind_all("<Button-1>", mouse)
read('map.txt')
update_all()

playerOne=player('yellow',21,22)

redimg = tkinter.PhotoImage(file='red.gif')
blueimg = tkinter.PhotoImage(file='blue.gif')
orangeimg = tkinter.PhotoImage(file='orange.gif')
pinkimg = tkinter.PhotoImage(file='pink.gif')

blinky=ghost(redimg,1,8)
pinky=ghost(pinkimg,26,33)
inky=ghost(blueimg,1,33)
clyde=ghost(orangeimg,12,24)

update_body()
timer()

