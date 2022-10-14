from work import DIKT_2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import pink,black,red,blue,green,brown
import os
from reportlab.lib.units import inch
from work import DIKT_2
from work2 import DIKT_3
from work3 import dates
import sys
from PyPDF2 import PdfFileMerger



def merg(a):
    from PyPDF2 import PdfFileMerger
    merger = PdfFileMerger()

    for pdf in a:
        merger.append(pdf)
    merger.write("result.pdf")
    merger.close()


def supsup(name,date,logic):
    pdfmetrics.registerFont (TTFont('Rus', '7454.ttf'))
    pdf = canvas.Canvas (name + "_от_" + date +".pdf")
    from work import DIKT_2
    from work2 import DIKT_3
    dic2 = name
    dic3 = dic2.replace(" ","")
    a=DIKT_2[dic2]
    if a == [('',None, None)] or a == [('',"None", None)]:
        a = [('нет дефектов','нет','нет')]
    else:
        None
    b,c ={},{}
#------------------------------------------------------------------------------


    dic2 = name
    pdfmetrics.registerFont (TTFont('Rus', '7454.ttf'))
    pdf.setStrokeColor (black)
    textobject = pdf.beginText()
    textobject.setFont ('Rus',20)
    textobject.setTextOrigin (0.7*inch,10.4*inch)
    textobject.textLines ('''Акт осмотра кабельных линий АО "ОЭК" СРЭС''')
    textobject.setTextOrigin(2.1*inch,10.05*inch)
    textobject.textLines ('''в подземном сооружении.''')
    textobject.setTextOrigin (0.7*inch, 9.5*inch)
    textobject.setFont ('Rus', 12)
    textobject.textLines (date+ " " + '''был произведен плановый осмотр кабельных линий в подземном''')
    textobject.setTextOrigin (0.5*inch,9.3*inch)
    textobject.textLines ('''сооружении общегородского кабельного коллектора'''+ " \""+ name + '\".')
    textobject.setTextOrigin (0.5*inch,8.9*inch)
    textobject.textLines ("""Перечень осмотренных кабельный линий: """)
    textobject.setTextOrigin (0.5*inch,8.5*inch)
    pdf.drawText (textobject)

#-------------------------------------------------------------------------------
    #Удалим мусор
    for i in a:
        pdf.setFont("Rus", 12)
        if b.get(i[1]) == None:
            b[i[1]] = [(i[0].replace("\n",""), i[2].replace("\n",""))]
        else:
            b[i[1]].append((str(i[0]).replace("\n",""),str(i[2]).replace("\n","")))

#-------------------------------------------------------------------------------

            # Все отступы для формирования таблицы
    zebra,otstup = 8.3,0.22 # зебра это координаты Y с которых начинает строку цикл отступ это расстояние между строками
    cobra_1 = 2.7 # кобра_1  это отступ слева для расположения дефекта
    cobra_2 = 3.5 # кобра_2 это отступ слева для сущности дефекта
    cobra_3 = 8 # Отступ слева у таблицы
    micro = 0.06 # микроотступ от зебры по вертикале в табличке

#-------------------------------------------------------------------------------

    num = 0
    new = []
    pdf.setStrokeColor (black)
    textobject = pdf.beginText()
    for i in DIKT_3[dic3]:
        num += 1
        if num < 10:
            pdf.drawString((0.5)*inch, (zebra + otstup)*inch, str(num)+") ")
            pdf.drawString((0.75)*inch, (zebra + otstup)*inch, str(i[1]))
        else:
            pdf.drawString((0.5)*inch, (zebra + otstup)*inch, str(num)+") "+str(i[1]))
        pdf.drawString((cobra_1+0.7)*inch, (zebra + otstup)*inch,"["+str(i[0]+"]"))
        pdf.drawString((cobra_2+1.4)*inch, (zebra + otstup)*inch, str(i[2]))
        pdf.line(0.5*inch,(zebra + otstup-micro)*inch,(cobra_3-2.5)*inch,(zebra + otstup-micro)*inch)
        zebra -= otstup
    if a ==[('нет дефектов','нет','нет')]:
        pdf.drawString(0.5*inch, zebra*inch,"В ходе осмотра нарушения не обнаружены.")
        textobject = pdf.beginText()
        textobject.setTextOrigin (0.5*inch,(2*otstup)*inch)
        textobject.textLines("""осмотр принял ст. мастер СРЭС                                                                               ________Хорхорин С.А.
        осмотр произвел мастер уч. СРЭС                                                                           __________Куруц Ф.И.
        _______________________________                                                                           ____________________""")
        pdf.drawText (textobject)
        pdf.save()
        if logic == 0:
            os.startfile (name + "_от_" + date +".pdf")
        else:
            None
        return name + "_от_" + date +".pdf"
    else:
        None

    pdf.drawString(0.5*inch, zebra*inch,"В ходе осмотра выявлены следующие дефекты:")
    zebra = zebra - otstup

#-------------------------------------------------------------------------------
    # шапка для таблички

    pdf.line(0.5*inch, (zebra-micro+otstup)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)
    pdf.drawString((0.5+0.2)*inch,zebra*inch, "Наименование")
    pdf.drawString((cobra_1+0.25)*inch,zebra*inch, "ПК")
    pdf.drawString((cobra_2+0.2)*inch,zebra*inch, "Сущность дефекта")

    pdf.line(0.5*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro)*inch)
    pdf.line(0.5*inch, (zebra-micro)*inch, 0.5*inch, (zebra-micro+otstup)*inch)
    pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro+otstup)*inch)

    pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro)*inch)
    pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro+otstup)*inch)

    pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro)*inch)
    pdf.line(cobra_3*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)

    zebra = zebra -otstup
    pdf.line(0.5*inch, (zebra-micro+otstup)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)

#------------------------------------------------------------------------------
    zzzz = 0
    nanana = 0
    for n in b:
        zzzz += (len(b.get(n))) # это работает совместо с nanana для того,
        #что бы при переносе стр. если кончились дефекты пустая шапка не рисовалась
#------------------------------------------------------------------------------
    for i in b:
        pdf.drawString(0.5*inch,zebra*inch,i)
        nanana+= (len(b.get(i)))
        if len(b.get(i)) < 2 :
            if len(str(b.get(i)[0][1])) < 55:
                pdf.drawString(cobra_1*inch,zebra*inch, str(b.get(i)[0][0]))
                pdf.drawString(cobra_2*inch,zebra*inch, str(b.get(i)[0][1]))

                pdf.line(0.5*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro)*inch)
                pdf.line(0.5*inch, (zebra-micro)*inch, 0.5*inch, (zebra-micro+otstup)*inch)
                pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro+otstup)*inch)

                pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro)*inch)
                pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro+otstup)*inch)

                pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro)*inch)
                pdf.line(cobra_3*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)


                zebra -= otstup

            else:
                nana = str(b.get(i)[0][1])
                x = nana.rfind(' ',1,55)

                pdf.drawString(cobra_1*inch,zebra*inch, str(b.get(i)[0][0]))
                pdf.drawString(cobra_2*inch,zebra*inch, str(b.get(i)[0][1])[:x])

                pdf.line(0.5*inch, (zebra-micro)*inch, 0.5*inch, (zebra-micro+otstup)*inch)
                pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro+otstup)*inch)
                pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro+otstup)*inch)
                pdf.line(cobra_3*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)

                zebra -= otstup
                pdf.drawString(cobra_2*inch,zebra*inch, str(b.get(i)[0][1])[x:])

                pdf.line(0.5*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro)*inch)
                pdf.line(0.5*inch, (zebra-micro)*inch, 0.5*inch, (zebra-micro+otstup)*inch)
                pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro+otstup)*inch)

                pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro)*inch)
                pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro+otstup)*inch)

                pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro)*inch)
                pdf.line(cobra_3*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)
                zebra -= otstup

        else:
            for j in range (len(b.get(i))):
                if len(str(b.get(i)[j][1])) < 54:

                    pdf.drawString(cobra_1*inch,zebra*inch, str(b.get(i)[j][0]))
                    pdf.drawString(cobra_2*inch,zebra*inch, str(b.get(i)[j][1]))

                    pdf.line(0.5*inch, (zebra-micro)*inch, 0.5*inch, (zebra-micro+otstup)*inch)

                    pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro)*inch)
                    pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro+otstup)*inch)

                    pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro+otstup)*inch)

                    pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro)*inch)
                    pdf.line(cobra_3*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)

                    zebra -= otstup

                else:

                    nana = str(b.get(i)[j][1])
                    x = nana.rfind(' ',1,55)
                    pdf.drawString(cobra_1*inch,zebra*inch, str(b.get(i)[j][0]))
                    pdf.drawString(cobra_2*inch,zebra*inch, str(b.get(i)[j][1])[:x])

                    pdf.line(0.5*inch, (zebra-micro)*inch, 0.5*inch, (zebra-micro+otstup)*inch)
                    pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro+otstup)*inch)
                    pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro+otstup)*inch)

                    pdf.line(cobra_3*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)

                    zebra -= otstup

                    pdf.line(0.5*inch, (zebra-micro)*inch, 0.5*inch, (zebra-micro+otstup)*inch)

                    pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro)*inch)
                    pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro+otstup)*inch)

                    pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro+otstup)*inch)
                    pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro)*inch)
                    pdf.line(cobra_3*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)

                    pdf.drawString(cobra_2*inch,zebra*inch, str(b.get(i)[j][1])[x:])
                    zebra -= otstup

            pdf.line(0.5*inch, (zebra-micro+otstup)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)
            pdf.line(0.5*inch, (zebra-micro+otstup)*inch, 0.5*inch, (zebra-micro+otstup+otstup)*inch)
            pdf.line(cobra_1*inch, (zebra-micro+otstup)*inch, cobra_1*inch, (zebra-micro+otstup+otstup)*inch)
            pdf.line(cobra_2*inch, (zebra-micro+otstup)*inch, cobra_2*inch, (zebra-micro+otstup+otstup)*inch)
            pdf.line(cobra_3*inch, (zebra-micro+otstup)*inch, cobra_3*inch, (zebra-micro+otstup+otstup)*inch)

        if zebra <1.35:
            pdf.showPage()
            zebra = 11
            pdf.setFont("Rus", 12)
            if nanana < zzzz:
                pdf.line(0.5*inch, (zebra-micro+otstup)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)
                pdf.drawString((0.5+0.2)*inch,zebra*inch, "Наименование")
                pdf.drawString((cobra_1+0.25)*inch, zebra*inch, "ПК")
                pdf.drawString((cobra_2+0.2)*inch, zebra*inch, "Сущность дефекта")

                pdf.line(0.5*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro)*inch)
                pdf.line(0.5*inch, (zebra-micro)*inch, 0.5*inch, (zebra-micro+otstup)*inch)
                pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_1*inch, (zebra-micro+otstup)*inch)

                pdf.line(cobra_1*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro)*inch)
                pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_2*inch, (zebra-micro+otstup)*inch)

                pdf.line(cobra_2*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro)*inch)
                pdf.line(cobra_3*inch, (zebra-micro)*inch, cobra_3*inch, (zebra-micro+otstup)*inch)
                zebra = zebra - otstup
            else:
                None
        else:
            None

#-------------------------------------------------------------------------------

    textobject = pdf.beginText()
    textobject.setTextOrigin (0.5*inch,(2*otstup)*inch)
    textobject.textLines("""обход принял ст. мастер СРЭС                                                                               ________Хорхорин С.А.
    обход произвел мастер уч. СРЭС                                                                           __________Куруц Ф.И.
    ______________________________                                                                           ____________________""")
    pdf.drawText (textobject)
    pdf.save()
    if logic == 0:
        os.startfile (name + "_от_" + date +".pdf")
    else:
        None
    return name + "_от_" + date +".pdf"

#-------------------------------------------------------------------------------
def supersort(a):
    """ сортировка листов осмотра по дате
    value это даты
    key это коллектора
    """
    print("supersort used")
    d = {}
    test=1
    data_list = []
    return_list = []
    print("a= ",len(a))
    for i in a:
        key = i.split("_")[0]
        value = str(i.split("_")[2])[:-4].split(".")
        if test < 10 :
            id = "0" + str(test)
        else:
            id = test
        value = int(str(value[2])+str(value[1])+str(value[0])+str(id))
        d[value] = key #
        data_list.append(value)
        test+=1
    data_list.sort()
    for k in data_list:
        i = str(k)[:-2]
        return_list.append(str(d[k])+"_от_"+str(i)[6:]+"."+str(i)[4:6]+"."+str(i)[:4]+".pdf")
    print (len(return_list))
    return return_list

def start_function():
    n=0
    a = input("Введите наименование коллектора/ЗА ПОЛГОДА/ЗА ГОД: ")
    dict_to_merger = []
    if a == "ЗА ГОД":
        logic = 1
        for j in range(2):
             for i in dates(j):
                 gg = supsup(i, dates(j)[i], logic)
                 dict_to_merger.append(gg)
                 n+=1
        merg(supersort(dict_to_merger))
        quest = input("Открыть итоговый файл? да - y/пробел , нет - любой символ")
        if quest == "y" or quest == " ":
            os.startfile ("result" +".pdf")
        else:
            None
        [os.remove(j) for j in dict_to_merger]

    elif a == "ЗА ПОЛГОДА":
        logic = 1
        logic2=int(input("Введите полугодие 0 - первое , 1 - второе:  "))
        j = logic2
        for i in dates(j):
            n+=1
            gg = supsup(i,dates(j)[i],logic)
            dict_to_merger.append(gg)
        merg(supersort(dict_to_merger))
        [os.remove(j) for j in dict_to_merger]
        quest = input("Открыть итоговый файл? y/n")
        if quest == "y" or quest == " ":
            os.startfile ("result" +".pdf")
        else:
            None
    else:
        b = input("Введите дату производства осмотра: ")
        logic = 0
        supsup(a,b,logic)

start_function()

#-------------------------------------------------------------------------------
