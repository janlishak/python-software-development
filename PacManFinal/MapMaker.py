def dvojpole(xx, yy):
    pole=[]
    for x in range(xx):
        pole2=[]
        for y in range(yy):
            pole2.append("X")
        pole.append(pole2)
    return(pole)


def save(myPole,filename):
    xx = len(myPole)
    yy = len(myPole[0])
    with open(filename, 'w') as f:
        for y in range(yy):
            for x in range(xx):
                f.write(str(myPole[x][y]))
                print(str(myPole[x][y]) ,end='')
            f.write('\n')
            print('')
    print('\nMap has been saved to ' + filename + '.')

def read(filename):
    y=0
    with open(filename) as fileobj:
        for line in fileobj:
            x=-1
            for ch in line:
                print(ch,end='')
                x+=1
                if ch !='\n':
                    pole[x][y]=ch
                    print('',end='')
            y+=1
            
def checktile(mapa,x,y):
    if mapa[x][y]=='*' or mapa[x][y]=='.' or mapa[x][y]=='O':
        return True
    else:
        return False

if __name__ == "__main__":
    import tkinter, copy

    xx = 28
    yy = 37
    cell = 16
    c = tkinter.Canvas(width=cell*xx, height=cell*yy)
    c.pack()
    
    def callback_key(event):
        #print(event)
        global pole
        x=event.x//cell
        y=event.y//cell
        key=['1', '2', '3', '4', '5', '6']
        val=['X', '.', '#', '*', 'O', '-']
        for i in range(len(key)):
            if event.char == key[i]:
                #print(x,y)
                pole[x][y]=val[i]
                update(x,y)
                break

    def update(x,y):
        global xx,yy
        c.delete('bunka')
        val=['X', '.', '#', '*', 'O', '-']
        col=['black', 'gray', 'blue', 'white', 'pink', 'purple']
        for i in range(len(val)):
            if pole[x][y]==val[i]:
                c.create_rectangle(x*cell,y*cell,(x+1)*cell,(y+1)*cell, fill=col[i])

    def update_all():
        global xx,yy
        c.delete('bunka')
        val=['X', '.', '#', '*', 'O', '-']
        col=['black', 'gray', 'blue', 'white', 'pink', 'purple']
        for x in range(xx):
            for y in range(yy):
                for i in range(len(val)):
                    if pole[x][y]==val[i]:c.create_rectangle(x*cell,y*cell,(x+1)*cell,(y+1)*cell, fill=col[i])

    def mouse(event):
        print(event.x//cell,event.y//cell)

    pole=dvojpole(xx,yy)
    print('Loading map...\n')
    read('map1.txt')
    update_all()
    c.bind_all("<Key>", callback_key)
    c.bind_all("<Button-1>", mouse)
    print('\nTo change tile move mouse to desired tile and press number 1 to 6.')
    print('1=Nothing, 2=Free tile without coin, 3=Wall, 4=Coin, 5=Power up and 6 = door')
    print("To save the map to a text file write: save(pole,filename). \nExample: save(pole, 'new_map.txt'")
    tkinter.mainloop()
