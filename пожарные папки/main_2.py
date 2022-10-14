from reportlab.pdfgen import canvas
from dark import frame
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import pink,black,red,blue,green,brown
from dark import sh
import os
import progress
import time
from progress.bar import IncrementalBar

name = input("Введите название Будующей пожарной папки:  ")
fr = frame()
pdf = canvas.Canvas(name + ".pdf")
f = fr.values
v = fr.index

def bla (a):
    for i in range (len(a.values[0])):
        if str(a.values[0][i]).find('пк') != -1:
            return (i)



def serch_stolb (a):
    for i in range (len(a.values[0])):
        #print(i,a.values[0][i])
        if str(a.values[0][i]).upper().find('ПК') != -1:
            #print("первый i с пикетом",i)
            return(i)

def serch_stolb_2 (a):
    for i in range (len(a.values[0])):
        if str(a.values[0][i]).upper().find('БАЛАНС') != -1:
            return(i)

def c_or_s (i):
    mark = frame()[0][i].upper()
    if mark.find("Б") != -1 or mark.find("Ш")!= -1:
        a = 1
    else:
        a = 0
    color = frame()[serch_stolb_2(frame())][i]
    try:
        kal = color.find("РЭС")
        if kal != -1 :
            b = "orange"
        else:
            b = "white"
    except AttributeError:
        b = "white"
    return (a,b,color)

def analiz_1 (x):
    """ функция для анализа , на входе полка/место лево/право/середина
    на выходе polka mesto расположение
    """
    if x == None or len(x.split("/")) != 2 :
        polka,mesto,L_M_R = 0,0," "
        return polka, mesto, L_M_R
    p = x.split("/")
    polka = p[0]
    m = p[1].split(" ")
    mesto = m[0]
    if str(m[1]).find("лев")!= -1:
        L_M_R = "L"
    elif str(m[1]).find("пр")!= -1:
        L_M_R = "R"
    else:
        L_M_R = "M"
    return polka, mesto, L_M_R

def serch_xy(a,left,right,middle):
    d13 = {"L":left, "M":middle,"R":right}
    d14 = {"L":"Левая сторона", "M":"Середина","R":"Правая сторона"}
    if a[2] == 'L':
        x = left
    elif a[2] == 'R':
        x = right
    elif a[2] == 'M':
        x = middle
    else:
        x = 0
        y = 0
        return x,y
    y = (520 - 52*(int(a[0])-1)-8*(int(a[1])-1))
    pdf.setFont('Rus', 12)
    pdf.drawString(d13.get(a[2])+10,550,d14.get(a[2]))
    return x,y

def triangl(x,y,fil):
    y = y+5
    p = pdf.beginPath()
    p.moveTo(x,y)
    p.lineTo(x+4,y-10)
    p.lineTo(x-4,y-10)
    p.lineTo(x,y)
    pdf.setFillColor(fil)
    pdf.setStrokeColor(black)
    pdf.drawPath(p,fill=1)
    pdf.setFillColor (black)

def polka (a,x,y,crs,fil):
    pdf.setFont('Rus', 10)
    pdf.setStrokeColor(black)
    d1 = {"L":180, "M":260,"R":340} # для координат самих полок
    d12 = {"L":160, "M":250,"R":340+65} # для римских цифер у нарисованных полок
    d2 = {a:760-a*20 for a in range(10)}
    #d3 = {0:"L",1:"M",2:"R"}
    d4 = {1:"I",2:"II",3:"III", 4:"IV", 5:"V", 6:"VI",7:"VII",8:"VIII",9:"IX",10:"X" }
    pdf.setLineWidth(1)
    pdf.line(d1.get(a[2]), d2.get(int(a[0])),d1.get(a[2])+60, d2.get(int(a[0]))) # рисуем полки
    pdf.drawCentredString(d12.get(a[2])+6, d2.get(int(a[0])), d4.get(int(a[0]))) #римские цифры рядом с полками
    pdf.drawCentredString(x,(520 - 52 *(int(a[0])-1)),(d4.get(int(a[0])))) # римские цифры в расшифровке
    pdf.setFont('Rus', 8)
    pdf.drawString(x+13,(520 - (52 *(int(a[0])-1))-8*(int(a[1])-1)),"|"+a[1]+"|")
    pdf.setLineWidth(0.5)
    pdf.line(x+15,(519 - (52 *(int(a[0])-1))-8*(int(a[1])-1)),x+14+120,(519 - (52 *(int(a[0])-1))-8*(int(a[1])-1)))# поддчеркивание расшифровки
    pdf.line(x+15,(519+8 - (52 *(int(a[0])-1))-8*(int(a[1])-1)),x+14+120,(519+8 - (52 *(int(a[0])-1))-8*(int(a[1])-1)))
    if a[2] in "R" and crs == 0:
        triangl(d12.get(a[2]) - 12 - 12*(int(a[1])-1), d2.get(int(a[0]))+6,fil)
    elif a[2] in "R" and crs == 1:
        pdf.setFillColor(fil)
        pdf.circle(d12.get(a[2]) - 12 - 12*(int(a[1])-1), d2.get(int(a[0]))+5,5, stroke=1, fill=1)
        pdf.setFillColor(black)
    elif a[2] not in "R" and crs == 1:
        pdf.setFillColor(fil)
        pdf.circle(d1.get(a[2]) + 8 + 12*(int(a[1])-1), d2.get(int(a[0]))+5,5, stroke=1, fill=1)
        pdf.setFillColor(black)
    elif a[2] not in "R" and crs == 0:
        triangl(d1.get(a[2]) + 8 + 12*(int(a[1])-1), d2.get(int(a[0]))+6,fil)
    if a[2] not in "R":
        pdf.drawString(d1.get(a[2]) + 8 + 12*(int(a[1])-1),760+33, a[1])
    else:
        pdf.drawString(d12.get(a[2]) - 12 - 12*(int(a[1])-1),760+33, a[1])

def analiz_mesto (F):
    d = []
    for i in F:
        a = i[0]+i[1]+i[2]
        d.append(a)
    dL,dM,dR = [], [], []
    for i in d:
        if i.find ("L") != -1:
            c = i[0:2]
            dL.append(c)
        elif i.find ("M") != -1:
            c = i[0:2]
            dM.append(c)
        elif i.find ("R") != -1:
            c = i[0:2]
            dR.append(c)
    dL = sorted(dL)
    dM = sorted(dM)
    dR = sorted(dR)
    return dL,dM,dR

def body(a):
    pdf.setStrokeColor(black)
    pdf.setLineWidth(4)
    pdf.rect(180,570,220,220,stroke = 1, fill = 0)
    pdf.setFont('Rus', 20)
    pdf.drawRightString(580,810,a)
    pdf.setFont('Rus',10)

def basis (left,middle,right,index,marka):
    """ функция главного цикла, служит фундаментом"""
    bar = IncrementalBar('Countdown', max = (len(f[0])-1-serch_stolb_2(frame())))
    d = []
    logic_1 = 0
    max_polka = 0
    max_mesto = 0
    ding_L=0
    ding_M=0
    ding_R=0
    num_2 = serch_stolb_2(frame())
    for i in range(serch_stolb(frame()),len(f[0])):
        pdfmetrics.registerFont(TTFont('Rus', 'DejaVuSerif.ttf'))
        pdf.setFont('Rus', 10)
        bar.next()

        for j in range(len(f)):
            q = f[j][i]
            crss = c_or_s(j)
            crs = crss[0] # треугольник или circle + цвет
            fil = crss[1]
            res = crss[2]

            if str(q).find("ПК") != -1 or str(q).find("пк") != -1 :
                logic_1 = 1
                #print("ding сработала ветка на пикет")
                max_polka = 0
                max_mesto = 0
                piket = q.upper()
                #print(piket)
                body(piket)
            elif logic_1 == 1 and str(q).find("ПК") == -1:
                a = analiz_1(q)
                x,y  = serch_xy(a,left,right,middle)
                z = v[j]
                if x == 0 and y == 0:
                    None
                else:
                    pdf.setFont('Rus', 7)
                    if fil == "white":
                        fill = "black"
                    else:
                        fill = fil
                        z = z + " (" + str(res) + ")"
                        None
                    pdf.setFillColor(fill)
                    pdf.drawString(x+22,y,z)
                    pdf.setFillColor("black")
                    polka(a,x,y,crs,fil)
                if a[2] == "R":
                    ding_R = 1
                else:
                    None
                if a[2] == "L":
                    ding_L = 1
                else:
                    None
                if a[2] == "M":
                    ding_M = 1
                else:
                    None
        pdf.showPage()
        #print("включился шоу",piket)
        logic_1 = 0
        pdf.setStrokeColor(black)
    pdf.save()
    bar.finish()





pdfmetrics.registerFont(TTFont('Rus', 'DejaVuSerif.ttf'))
pdf.setFont('Rus', 25)
pdf.drawString(120,600,"Сечение коллектора")
pdf.drawString(120,550,str(sh()))
pdf.setFont("Rus", 10)
pdf.showPage()

#--------------------------------------------------------условные обозначения---

pdf.setFont('Rus', 25)
pdf.drawString(135,755,"Условные обозначения:")
pdf.setFont('Rus', 20)
pdf.drawString(30,700,"Кабельные линии:")
triangl(50,700-35,"white")
triangl(50,700-35-35,"orange")
pdf.drawString(115-50,700-5-35,"КЛ марки АПвВнг,АПвВгж и др.")
pdf.drawString(115-50,700-40-35,"КЛ ОЭК марки АПвВнг,АПвВгж и др.")

pdf.setFillColor("white")
pdf.circle(100-50,700 - 35*2-35,5, stroke=1, fill=1)
pdf.setFillColor("black")
pdf.drawString(115-50,700-5 -35*2-35,"КЛ марки АСБ,СБ,АСБГ и др.")

pdf.setFillColor("orange")
pdf.circle(100-50,700 - 35*3-35,5, stroke=1, fill=1)
pdf.setFillColor("black")
pdf.drawString(115-50,700-5 - 35*3-35,"КЛ ОЭК марки АСБ,СБ,АСБГ и др.")

pdf.drawString(30,520,"Пикеты :")
pdf.drawString(50,520-35,"ПК - пикет, разметка в коллекторе. 1ПК = 10м.")
pdf.drawString(50,520-35*2,"() - исключая")
pdf.drawString(50,520-35*3,"[] - включая")
pdf.drawString(50,520-35*4,"ГАЛ - галлерея, отходящий тоннель. Может иметь")
pdf.drawString(65,520-35*5,"собственную нумерацию")
pdf.drawString(50,520-35*6,"(пример)")
pdf.drawString(50,520-35*7,"ПК43 ГАЛ (9 - 12] - На пикете 43 отходящий")
pdf.drawString(65,520-35*8,"тоннель. Разрез верен в отходящем тоннеле")
pdf.drawString(65,520-35*9,"от пикета 9 ,исключая пикет 9, до пикета 12,")
pdf.drawString(65,520-35*10,"влючая пикет 12.")
pdf.showPage()

#-------------------------------------------------------------------------------

pdf.setFont('Rus', 20)
pdf.drawString(120,755,"Кабельные линии ОЭК:")
pdf.setFont("Rus", 10)
ddd = 0
dddd = 1
for i in range (len(fr)):
    #print(nana.index[i],nana.values[i][1], nana.values[i][2]
    #print(fr.values[i][2],type(fr.values[i][2])
    if i == 0:
        pdf.drawString(30,700,"№")
        pdf.drawString(50,700,str(fr.index[0]))
        pdf.drawString(250+30,700-ddd*20,str(fr.values[i][1]))
        pdf.drawString(350+30,700-ddd*20,str(fr.values[i][2]))
        ddd+=1
    else:
        None
    if fr.values[i][2] != None and "РЭС" in fr.values[i][2]:
        print(i,fr.values[i][1],fr.values[i][2])
        pdf.drawString(30,700-ddd*20,str(dddd)+")")
        pdf.drawString(50,700-ddd*20,str(fr.index[i]))
        pdf.drawString(250+30,700-ddd*20,str(fr.values[i][1]))
        pdf.drawString(350+30,700-ddd*20,str(fr.values[i][2]))
        dddd +=1
        ddd +=1
    else:
        None


pdf.showPage()

#--------------------------------------------------------------------------

pdf.setFont("Rus", 20)
pdf.drawString(120,755,"Кабельные линии сторонних организаций:")

ddd = 0
dddd = 1
pdf.setFont("Rus", 10)
for i in range (len(fr)):
    if fr.values[i][2] == None or "РЭС" not in fr.values[i][2] :
        if i == 0:
            pdf.drawString(30,700,"№")
            pdf.drawString(50,700,str(fr.index[0]))
            pdf.drawString(250+30,700,str(fr.values[0][1]))
            pdf.drawString(350+30,700,str(fr.values[0][2]))
            ddd+=1
        else:
            pdf.drawString(30,700-ddd*20,str(dddd)+")")
            pdf.drawString(50,700-ddd*20,str(fr.index[i]))
            pdf.drawString(250+30,700-ddd*20,str(fr.values[i][1]))
            pdf.drawString(350+30,700-ddd*20,str(fr.values[i][2]))
            dddd +=1
            ddd +=1

        if 700-ddd*20 < 50:
            ddd = 0
            pdf.showPage()
            pdf.setFont("Rus", 10)
            pdf.drawString(50,700+20,str(fr.index[0]))
            pdf.drawString(250+30,700+20,str(fr.values[0][1]))
            pdf.drawString(350+30,700+20,str(fr.values[0][2]))
        else:
            None
    else:
        None

pdf.showPage()

#-------------------------------------------------------------------------------

basis(40,220,400,frame().index,frame()[0])

os.startfile(name + ".pdf")
