#!/bin/python3

import tkinter,copy,time

xx=28
yy=37
cell=16
body=0
superpower=False
hviezdy=0
mapnumber=1
debug=False
tkinter.Tk().title("Pac-Man")
c=tkinter.Canvas(width=cell*xx, height=cell*yy,bg='black')
c.pack()


subor = open('highscore.txt', 'r')
highscore=int(subor.read().replace('\r','').replace('\n', ''))
subor.close


def update_body():
    global body, highscore
    c.delete('body')
    c.create_text(16*7,32,text='Score: '+str(body),fill='white',tags='body', font='Courier 20 bold')
    c.create_text(16*20,32,text='Highscore: '+str(highscore),fill='white',tags='body', font='Courier 20 bold')
    
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
    if event.char=='r':
        pinky.showpath()
    global direction
    direction = ['Left', 'Up', 'Right', 'Down']
    for i in range(len(direction)):
        if event.keysym == direction[i]:
            playerOne.changeDirection(i)
           
def update_all():
    global xx,yy, debug
    val=['X', '.', '#', '*', 'O', '-']
    col=[blank, blank, wall, coin, bodka, blank]
    if debug:
        col=[blank, blank, wall, blank, bodka, blank]
        
    for x in range(xx):
        for y in range(yy):
            for i in range(len(val)):
                if pole[x][y]==val[i]:
                    obrazky[x][y]=c.create_image(x*cell+cell//2, y*cell+cell//2, image=col[i])

def read(filename):
    y=0
    global hviezdy
    with open(filename) as fileobj:
        for line in fileobj:
            x=-1
            for ch in line:
                x+=1
                if ch !='\n':
                    pole[x][y]=ch
                    if ch=='*':
                        hviezdy+=1
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
    time.sleep(3)
    quit()

def colission(hrac, poleobjektov):
    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1] 
    for objekt in poleobjektov:
        one = objekt.x == hrac.x and objekt.y == hrac.y
        two = objekt.x == hrac.x+dx[(hrac.smer+2)%4] and objekt.y == hrac.y+dy[(hrac.smer+2)%4]
        if one or two:
            return objekt
    return False

def close_doors():
    global navigation_map
    navigation_map[13][16]='='
    navigation_map[14][16]='='
    
def open_doors():
    global navigation_map
    navigation_map[13][16]='.'
    navigation_map[14][16]='.'

def bonus():
    global superpower
    superpower=False
    blinky.change_image(blinky.image)
    pinky.change_image(pinky.image)
    inky.change_image(inky.image)
    clyde.change_image(clyde.image)    

def vyhra():
    global body, highscore
    c.delete('all')
    c.create_text(xx*cell//2,yy*cell//5*1,text='YOU WIN',fill='white',font='Courier 35 bold')
    c.create_text(xx*cell//2,yy*cell//5*2,text='Your Score:'+str(body),fill='white',font='Courier 35 bold')
    c.create_text(xx*cell//2,yy*cell//5*3,text='Highscore:'+str(highscore),fill='white',font='Courier 35 bold')
    if body>highscore:   
        subor = open('highscore.txt', 'w')
        subor.write(str(body))
        subor.close()
    c.update()
    time.sleep(3)
    c.delete(playerOne.body)
    c.update()
    quit()

dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1] 
sym= ['l','u','r','d']

img1 = tkinter.PhotoImage(file='images/img1.gif')
img2 = tkinter.PhotoImage(file='images/img2.gif')
img3 = tkinter.PhotoImage(file='images/img3.gif')
hore1 = tkinter.PhotoImage(file='images/hore1.gif')
hore2 = tkinter.PhotoImage(file='images/hore2.gif')
hore3 = tkinter.PhotoImage(file='images/hore3.gif')
doprava1 = tkinter.PhotoImage(file='images/doprava1.gif')
doprava2 = tkinter.PhotoImage(file='images/doprava2.gif')
doprava3 = tkinter.PhotoImage(file='images/doprava3.gif')
dole1 = tkinter.PhotoImage(file='images/dole1.gif')
dole2 = tkinter.PhotoImage(file='images/dole2.gif')
dole3 = tkinter.PhotoImage(file='images/dole3.gif')
pacman=[[img1,img2,img3],[hore1,hore2,hore3],[doprava1,doprava2,doprava3],[dole1,dole2,dole3]]
imgvalue=0

def animacia():
    global pacman, imgvalue
    imgvalue+=1
    imgvalue=imgvalue%3
    playerOne.change_image(pacman[playerOne.smer][imgvalue])
    c.after(70,animacia)

class ghost(object):

    def __init__(self, image, x, y, rot, speed, color):
        global navigation_map
        self.color=color
        self.image = image
        self.x = x
        self.y = y
        self.body=c.create_image(x*cell+cell//2,y*cell+cell//2,image=self.image)
        self.map = copy.deepcopy(navigation_map)
        self.startx=x
        self.starty=y
        self.rotation=rot
        self.avoid=[]
        self.endX = 1
        self.endY = 5
        self.speed=speed
        self.mv=0
        self.resetWait=False
        c.after(1000,self.update)
        
    def direction(self, endX, endY, avoid):
        self.endX = endX
        self.endY = endY
        self.avoid = avoid
        
    def path(self,endX, endY):
        global pole
        self.map = copy.deepcopy(pole)
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1] 
        sym= ['>','v','<','^']  
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
    
    def navigate(self):
        global navigation_map
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1] 
        sym= ['<','^','>','v']

        possible_ways=0
        for rot in [+1, 0, +3]:
            rotation=(self.rotation+rot)%4
            tileX=self.x+dx[rotation]
            tileY=self.y+dy[rotation]
            if navigation_map[tileX][tileY]=='.':
                possible_ways+=1
                self.map[self.x][self.y]=sym[rotation]

        if possible_ways==1 or (self.endX == self.x and self.endY == self.y):
            pass
        
        elif possible_ways>1:
            endX = self.endX
            endY = self.endY

            avoidTails = self.avoid
            for nothing in range(len(avoidTails)+1):
                self.map = copy.deepcopy(navigation_map)
                for avoid in avoidTails:
                    self.map[avoid[0]][avoid[1]]='H'
                    
                table=[[self.x, self.y, self.rotation]]
                SeekPath=True
                while table and SeekPath:
                    new_table=[]
                    for tile in table:
                        for rot in [+1, 0, +3]:
                            rotation=(tile[2]+rot)%4
                            tileX=tile[0]+dx[rotation]
                            tileY=tile[1]+dy[rotation]
                            if self.map[tileX][tileY]=='.':
                                new_table.append([tileX,tileY,rotation])
                                self.map[tileX][tileY]=sym[rotation]
                                if tileX==endX and tileY==endY:
                                    SeekPath=False
                    table=new_table
                if SeekPath==False:
                    break
                else:
                    if avoidTails:
                        #print('Dropping: '+str(avoidTails[-1]))
                        del avoidTails[-1]
                        
            if not SeekPath:
                new_map = copy.deepcopy(navigation_map)
                symReversed= ['>','v','<','^']
                while(not (endX==self.x and endY==self.y)):
                    for i in range(4):
                        if self.map[endX][endY]==symReversed[i]:
                            endX+=dx[i]
                            endY+=dy[i]
                            new_map[endX][endY]=symReversed[i]
                            break
                self.map = new_map
        else:
            pass
            #print('I AM STUCK!')

    def update(self):
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1]
        sym= ['<','^','>','v']
        if self.mv==0:
            global cell
            self.navigate()
            for i in range(4):
                if self.map[self.x][self.y]==sym[i]:
                    c.move(self.body, dx[i]*4, dy[i]*4)
                    self.rotation=i
                    self.x+=dx[i]
                    self.y+=dy[i]
                    self.mv=3
                    break
        else:
            self.mv-=1
            c.move(self.body, dx[self.rotation]*4, dy[self.rotation]*4)
            
        if self.resetWait:
            c.after(3000,self.update)
            self.resetWait=False
        else:
            c.after(self.speed,self.update)


    def showpath(self):
        global xx,yy
        for y in range(yy):
            for x in range(xx):
                print(str(self.map[x][y]) ,end='')
            print('')

    def drawpath(self):
        c.delete(str(self.color))
        global xx,yy, cell
        for y in range(yy):
            for x in range(xx):
                ch=str(self.map[x][y])
                if ch=='<' or ch == '>' or ch=='^' or ch =='v':
                    c.create_text(x*cell+cell//2,y*cell+cell//2, tags=str(self.color), text=str(self.map[x][y]), fill=self.color, font='Arial 15 bold')
            
    def reset(self,val):
        self.mv=0
        self.resetWait=val
        self.x=self.startx
        self.y=self.starty
        c.delete(self.body)
        self.body=c.create_image(self.x*cell+cell//2,self.y*cell+cell//2,image=self.image)
        
    def change_image(self,importimage):
        c.itemconfigure(self.body, image=importimage)
        

class player(object):

    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.body=c.create_image(x*cell+cell//2,y*cell+cell//2,image=self.image)
        self.smer=0
        self.changesmer=0
        self.smerx=-1
        self.smery=0
        self.zivoty=3
        self.startx=x
        self.starty=y
        self.resetWait=False
        self.mv=0
        c.after(1000,self.update)
        
    def change_image(self,importimage):
        c.itemconfig(self.body,image=importimage)
                  
    def strata_zivota(self):
        self.zivoty-=1

        if self.zivoty==0:
            koniec_hry()
        self.update_zivoty()

    def update_zivoty(self):
        c.delete('bodky')
        for i in range(self.zivoty):
            c.create_image(cell+i*27,cell*yy-14,image=img3,tags='bodky')

    def changeDirection(self,changesmer):
        self.changesmer=changesmer

    def update(self):
        if self.mv==0:
            global cell,body,superpower,hviezdy
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
                self.move()
                hviezdy-=1
                if hviezdy==0:
                    vyhra()
            elif pole[self.x+self.smerx][self.y+self.smery]=='O':
                body+=100
                update_body()
                pole[self.x+self.smerx][self.y+self.smery]='.'
                c.itemconfig(obrazky[self.x+self.smerx][self.y+self.smery], image = blank)
                if superpower==False:
                    c.after(6000,bonus)
                superpower=True
                #print('O',end='')
                self.move()
            elif pole[self.x+self.smerx][self.y+self.smery]=='.':
                #print('.',end='')
                self.move()
            pac_man_colission()
        else:        
            self.mv-=1
            c.move(self.body,self.smerx*4,self.smery*4)

        if self.resetWait:
            c.after(3000,self.update)
            self.resetWait=False
        else:
            c.after(20,self.update)
    def move(self):
        self.mv=3
        self.x+=self.smerx
        self.y+=self.smery
        c.move(self.body,self.smerx*4,self.smery*4)

    def reset(self):
        self.mv=0
        self.resetWait=True
        self.x=self.startx
        self.y=self.starty
        c.delete(self.body)
        self.body=c.create_image(self.x*cell+cell//2,self.y*cell+cell//2,image=self.image)
            
pole=dvojpole(xx, yy)
read('maps/map'+str(mapnumber)+'.txt')
navigation_map=dvojpole(xx, yy)
for x in range(xx):
    for y in range(yy):
        if pole[x][y]=='*' or pole[x][y]=='.' or pole[x][y]=='O':
            navigation_map[x][y]='.'
        else:
            navigation_map[x][y]=pole[x][y]

if mapnumber==1:
    wall = tkinter.PhotoImage(file='images/blank.gif')
    plocha = tkinter.PhotoImage(file='images/mapa.png')
    c.create_image(xx*cell//2, yy*cell//2, image=plocha)
    playerOne=player(img1,13,21)
if mapnumber==2:
    wall = tkinter.PhotoImage(file='images/wall.gif')

blank = tkinter.PhotoImage(file='images/blank.gif')
coin = tkinter.PhotoImage(file='images/x.gif')
bodka = tkinter.PhotoImage(file='images/bodka.gif')
obrazky = dvojpole(xx,yy)
update_all()

if mapnumber==2:
    playerOne=player(img1,13,23)
    
playerOne.update_zivoty()

redimg = tkinter.PhotoImage(file='images/red.gif')
blueimg = tkinter.PhotoImage(file='images/blue.gif')
orangeimg = tkinter.PhotoImage(file='images/orange.gif')
pinkimg = tkinter.PhotoImage(file='images/pink.gif')
bonusimg = tkinter.PhotoImage(file='images/bonus.gif')

blinky=ghost(redimg,13,18,1,120//4, 'red')
pinky=ghost(pinkimg,15,18,1, 93//4, 'pink')
inky=ghost(blueimg,14,18,1, 131//4, 'cyan')
clyde=ghost(orangeimg,12,18,1, 84//3, 'orange')

update_body()

c.bind_all("<Key>", callback_key)
c.bind_all("<Button-1>", mouse)

#c.after(3000, open_doors)
animacia()

def pac_man_colission():
    global body, superpower, debug
    if superpower==False:
        blinky.direction(playerOne.x,playerOne.y,[[13,33],[13,9]])
        pinky.direction(playerOne.x,playerOne.y,[[blinky.x,blinky.y]])
        inky.direction(playerOne.x,playerOne.y,[[blinky.x,blinky.y], [pinky.x,pinky.y]])
        clyde.direction(pinky.x,pinky.y,[[playerOne.x,playerOne.y], [inky.x,inky.y], [blinky.x,blinky.y]])
        if colission(playerOne, [blinky, pinky, inky, clyde]) and debug==False:
            clyde.reset(True)
            blinky.reset(True)
            inky.reset(True)
            pinky.reset(True)
            playerOne.strata_zivota()
            playerOne.reset()
            #close_doors()
            #c.after(3000, open_doors)
    else:
        blinky.change_image(bonusimg)
        pinky.change_image(bonusimg)
        inky.change_image(bonusimg)
        clyde.change_image(bonusimg)

        blinky.direction(1,5,[])
        pinky.direction(26,5,[])
        inky.direction(1,33,[])
        clyde.direction(26,33,[])
        hit=colission(playerOne, [blinky, pinky, inky, clyde])
        if hit:
            body+=200
            update_body()
            hit.reset(True)

def path_debug():
    for ghost in [pinky, inky, clyde, blinky]:
        ghost.drawpath()
        c.tag_raise(ghost.body)
    c.after(200,path_debug)
if debug:
    path_debug()

tkinter.mainloop()
