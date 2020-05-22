#!/bin/python3
import tkinter, random, time

riadky=10
stlpce=10

canvas=tkinter.Canvas(width=stlpce*50, height=stlpce*50, bg='darkgray')
canvas.pack()

mina=tkinter.PhotoImage(file='mine.png')
vlajka=tkinter.PhotoImage(file='flag.png')
pocet_stuknutych_policok=0

dvojrozmerne_pole = []
for y in range(riadky):
    jeden_stlpec = []
    for x in range(stlpce):
        jeden_stlpec.append(0)
    dvojrozmerne_pole.append(jeden_stlpec)

dvojrozmerne_pole_stuknute = []
for y in range(riadky):
    jeden_stlpec = []
    for x in range(stlpce):
        jeden_stlpec.append(0)
    dvojrozmerne_pole_stuknute.append(jeden_stlpec)

for y in range(10):
    canvas.create_line(0, y*50, 10*50, y*50, fill='gray')
    
for x in range(10):
    canvas.create_line(x*50, 0, x*50, 10*50, fill='gray')

pocet_min=10
while pocet_min>0:
    x=random.randrange(10)
    y=random.randrange(10)
    if dvojrozmerne_pole[x][y]==0:
        dvojrozmerne_pole[x][y]=1
        pocet_min-=1
        
def pocet_min_okolo(policko_x,policko_y):
    global dvojrozmerne_pole, riadky, stlpce
    pocet=0
    for x in range(-1+policko_x,2+policko_x):
        for y in range(-1+policko_y,2+policko_y):
            if x < stlpce and x >= 0:
                if y < riadky and y >= 0:
                    if dvojrozmerne_pole[x][y]==1:
                        pocet+=1           
    return(pocet)

def vykresli_vsetky_miny():
    for x in range(stlpce):
        for y in range(riadky):
            if dvojrozmerne_pole[x][y]==1:
                canvas.create_image((x*50)+25, (y*50)+25,image=mina)
                
def skus(x,y):
    global pocet_stuknutych_policok
    if dvojrozmerne_pole_stuknute[x][y]==0:
        dvojrozmerne_pole_stuknute[x][y]=1
        pocet_stuknutych_policok+=1
        canvas.create_rectangle(x*50, y*50, x*50+50, y*50+50, fill='lightgray', outline='gray')
        if dvojrozmerne_pole[x][y]==0:
            if pocet_min_okolo(x,y)==0:
                for tuk_x in range(-1+x,2+x):
                    for tuk_y in range(-1+y,2+y):
                        if tuk_x < stlpce and tuk_x >= 0:
                            if tuk_y < riadky and tuk_y >= 0:
                                skus(tuk_x, tuk_y)
            else:
                canvas.create_text(x*50+25, y*50+25, text=str(pocet_min_okolo(x,y)), font='Courier 20 bold')
                                
        else:
            vykresli_vsetky_miny()
            canvas.update()
            time.sleep(3)
            quit()

        if pocet_stuknutych_policok==90:
            vykresli_vsetky_miny()
            canvas.create_text(250,250,text='You Win!', font='Arial 70 bold', fill='white')
            canvas.update()
            time.sleep(3)
            quit()
            
def right_click(klik):
    x=klik.x//50
    y=klik.y//50
    if dvojrozmerne_pole_stuknute[x][y]==0:
        dvojrozmerne_pole_stuknute[x][y]=2
        canvas.create_image((x*50)+25, (y*50)+25,image=vlajka)

    elif dvojrozmerne_pole_stuknute[x][y]==2:
        dvojrozmerne_pole_stuknute[x][y]=0
        canvas.create_rectangle(x*50, y*50, x*50+50, y*50+50, fill='darkgray', outline='gray')
    
def left_click(klik):
    skus(klik.x//50, klik.y//50)
    
canvas.bind_all('<Button-1>', left_click)
canvas.bind_all('<Button-3>', right_click)
#vykresli_vsetky_miny

tkinter.mainloop()
