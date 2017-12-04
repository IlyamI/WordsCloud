
import tkinter
import random
# import time
import os
import json

wordsList=[]
wd=os.getcwd().replace("\\","/")+"/"
# print(wd)
nodeInfoLabel=None
infoText='Sample text'

class myWordsCloud():
    def __init__(self):
        self.nodeList=[]
        self.randomNodes=0

    def addNode(self,node):
        self.nodeList.append(node)

    # def nodeClick(self,obj):
    #     o=obj
    #     pass

class Node():
    def __init__(self,obj):
        self.x=0
        self.y=0
        self.vX=0
        self.vY=0
        self.age=0
        self.nodeLinks={}
        self.obj=obj
        self.id=obj.winfo_id()
        self.rank=0

def ticker():
    root.after(100,ticker)

    if cloud.randomNodes==0:
        randomNodes(cloud)
    else:
        c = str(root.winfo_geometry())
        c = c.replace("x", " ")
        c = c.replace("+", " ")
        rootW,rootH,rootX, rootY = map(int, c.split())
        # print(rootX, rootY, rootW, rootH)

        for x in cloud.nodeList:
# Позиционирование элемента соглано предыдущим расчетам
            if x.age>3:
                x.obj.destroy()
                cloud.nodeList.remove(x)

            newX=x.obj.winfo_x()+x.vX
            newY=x.obj.winfo_y()+x.vY

            if newX<=0:
                newX=0
            if newX>=rootW-x.obj.winfo_width():
                newX=rootW-x.obj.winfo_width()
            if newY<=0:
                newY=0
            if newY>=rootH-x.obj.winfo_height():
                newY=rootH-x.obj.winfo_height()
            x.obj.place(x= newX,y=newY)

# Обнудяем горизонтальные скорости
            x.vX=0
            x.vY=0

# Проверка на пересечение (наложение) элементов

            for y in cloud.nodeList:
                if x.id!=y.id:    # исключаем проверку с самим собой
                    x1=x.obj.winfo_x()
                    y1=x.obj.winfo_y()
                    w1=x.obj.winfo_width()+5                    # зазор между объектами
                    h1=x.obj.winfo_height()+5                   # зазор между объектами
                    cx1=x1+w1/2
                    cy1=y1+h1/2

                    x2=y.obj.winfo_x()
                    y2=y.obj.winfo_y()
                    w2=y.obj.winfo_width()+5
                    h2=y.obj.winfo_height()+5
                    cx2=x2+w2/2
                    cy2=y2+h2/2

                    if x1<=x2:   # эмуляция сортировки
                        if (x1+w1)>=x2:          # пересечение по горизонтали
                            if y1<=y2:
                                if (y1+h1)>y2:
                                    if cx1<cx2:
                                        x.vX-=1
                                        y.vX+=1
                                        if cy1<cy2:
                                            x.vY-=1
                                            y.vY+=1
                                        else:
                                            x.vY+=1
                                            y.vY-=1
                                    else:
                                        x.vX+=1
                                        y.vX-=1
                                        if cy1<cy2:
                                            x.vY-=1
                                            y.vY+=1
                                        else:
                                            x.vY+=1
                                            y.vY-=1
                            if y1>=y2:
                                if (y2+h2)>y1:
                                    if cx1<cx2:
                                        x.vX-=1
                                        y.vX+=1
                                        if cy1<cy2:
                                            x.vY-=1
                                            y.vY+=1
                                        else:
                                            x.vY+=1
                                            y.vY-=1
                                    else:
                                        x.vX+=1
                                        y.vX-=1
                                        if cy1<cy2:
                                            x.vY-=1
                                            y.vY+=1
                                        else:
                                            x.vY+=1
                                            y.vY-=1

def nodeClick(event):
    for x in cloud.nodeList:
        x.age+=1
        if x.id==event.widget.winfo_id():
            print(x.obj['text'],"\n=========")
            # print(x.obj.winfo_geometry())
            event.widget.lift()
            with open(wd+"/data/"+str(x.obj['text'])[0].upper()+"/"+str(x.obj['text'])+".txt","r") as nodeFile:
                nodeInfo=json.loads(nodeFile.read())
                for x in nodeInfo['Links']:
                    print(x)
                    nodeExists = 0
                    for y in cloud.nodeList:
                        if y.obj['text']==x:
                            y.rank+=1
                            y.age=0
                            nodeExists=1

                    if nodeExists==0:
                        cloud.addNode(Node(createWordLink(root, x)))
                pass

def showInfoNode(event):
    for x in cloud.nodeList:
        if x.id == event.widget.winfo_id():
            event.widget.lift()
            nodeInfoLabel.lift()
            # c = str(root.winfo_geometry())
            # c = c.replace("x", " ")
            # c = c.replace("+", " ")
            # rootW, rootH, rootX, rootY = map(int, c.split())
            #
            c = str(event.widget.winfo_geometry())
            c = c.replace("x", " ")
            c = c.replace("+", " ")
            wW,wH,wX,wY=map(int, c.split())
            if event.x<=2 or event.y<=2 or event.x>=wW-2 or event.y>=wH-2:
                nodeInfoLabel.place(x=-500, y=-500)
            else:
                nodeInfoLabel.place(x=wX+wW, y=wY)
    pass

def createWordsList():
    dic = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    wordsCount=random.randint(5,10)

    while wordsCount>0:
        wordLen = round(random.randint(1, len(dic))/2)+1
        word=list()
        for i in range(1,wordLen):
            word.append(random.choice(dic))

        wordsList.append(''.join(map(str,word)))
        wordsCount-=1

def createWordLink(root,word):
    l=tkinter.Label(root)
    l['background']='#DAD1FC'
    l['borderwidth']=2
    l['cursor']='hand2'
    l['relief']='groove'
    l['text']=word
    l['padx']=5
    l['pady']=5
    l.bind("<Button-1>",nodeClick)
    l.bind("<Motion>",showInfoNode)

    l.pack()
    # l.update()

    return l

def randomNodes(cloud):

    c = str(root.winfo_geometry())
    c=c.replace("x"," ")
    c=c.replace("+", " ")
    rootW, rootH, rootX, rootY=map(int,c.split())

    for x in cloud.nodeList:
        c=x.obj.winfo_geometry()
        if c[:3]!="1x1":
            c = c.replace("x", " ")
            c = c.replace("+", " ")

            x.obj.place(x=(random.randint(int(c.split()[2]),rootX)-int(c.split()[2])),y=(random.randint(int(c.split()[3]),rootY)-int(c.split()[3])))
            cloud.randomNodes=1

def createInfoLabel(root):
    l=tkinter.Label(root)
    l['bg']='#FFFFFF'
    l['relief']='groove'
    l['text']=infoText
    l.place(x=-500,y=-500)
    return l

createWordsList()

# print(wordsList)

root=tkinter.Tk()

# for x in root.config():
#     print("{}={}".format(x, root[x]))
#

screenX=int(root.winfo_screenwidth())
screenY=int(root.winfo_screenheight())

# print(root.winfo_screenwidth())
# print(root.winfo_screenheight())

rootPoint=str(round(screenX/3))+"x"+str(round(screenY/3))+"+"+str(round(screenX/3))+"+"+str(round(screenY/3))

# print(rootPoint)
# root.geometry("500x400+50+50")

root.geometry(rootPoint)
root['background']='#FFFBCE'

cloud=myWordsCloud()

for x in wordsList:
    cloud.addNode(Node(createWordLink(root,x)))

cloud.addNode(Node(createWordLink(root,"Амфора")))
nodeInfoLabel=createInfoLabel(root)

root.after_idle(ticker)
# root.bind("<Configure>",randomNodes())
root.mainloop()


