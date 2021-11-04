from django.http.response import HttpResponse
from django.shortcuts import render
import requests
import matplotlib.pyplot as plt
import os
from os import remove
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


from django.template import loader

def index(request):
    r = requests.get('http://127.0.0.1:5000/Entrada')
    req = r.json()
    ctx = {'entrada':req.get('entrada'),'fechas':req.get('Fechas')}
    return render(request,'index.html',ctx)

def delete(request):
    r = requests.delete('http://127.0.0.1:5000/Datos')
    req = r.json()

    if os.path.isfile('SAT/static/resumenMovs.png'):
        remove('SAT/static/resumenMovs.png')

    if os.path.isfile('SAT/static/resumenRango.png'):
        remove('SAT/static/resumenRango.png')

    if os.path.isfile('SAT/static/reporte.pdf'):
        remove('SAT/static/reporte.pdf')

    ctx = {'respuesta':req.get('Respuesta'),'entrada':req.get('Entrada'),'fechas':req.get('Fechas')}
    return render(request,'index.html',ctx)


def enviar(request):
    mensaje = request.POST["entrada"]

    if mensaje != '':

        objeto = {
            'data': mensaje
        }
        r = requests.post('http://127.0.0.1:5000/Facturas',json=objeto)
        req = r.json()

        ctx = {'respuesta':req.get('Mensaje'),'entrada':req.get('Entrada'),'fechas':req.get('Fechas')}

        return render(request,'index.html',ctx)
    else:
        ctx = {'respuesta':'No se envió nada','entrada':mensaje}
        return render(request,'index.html',ctx)

def consultar(request):

    r = requests.get('http://127.0.0.1:5000/Datos')
    req = r.json()

    ctx = {'respuesta':req.get('Respuesta'),'entrada':req.get('Entrada'),'fechas':req.get('Fechas')}

    return render(request,'index.html',ctx)

def resumenIVA(request):

    mensaje = request.POST["fec"]
    #print(mensaje)
    objeto = {
            'fecha': mensaje
        }


    r = requests.post('http://127.0.0.1:5000/resumenIVA',json=objeto)
    req = r.json()

    facs = req.get('facturas')
    nits = []
    for fac in facs:
        encontrado1 = False
        encontrado2 = False
        if len(nits) > 0:
            for n in nits:
                if fac[1] == n[0]:
                    encontrado1 = True
                    n.append(fac[1])
                if fac[2] == n[0]:
                    encontrado2 = True
                    n.append(fac[2])
            
            if not encontrado1:
                nits.append([fac[1]])
            if not encontrado2:
                nits.append([fac[1]])
        else:
            if fac[1] == fac[2]:
                nits.append([fac[1],fac[2]])
            else:
                nits.append([fac[1]])
                nits.append([fac[2]])

    #print(nits)

    x = []
    y = []

    for no in nits:
        x.append(no[0])
        y.append(len(no))

    fig, ax = plt.subplots()
    # Dibujar puntos
    ax.bar(x,y)
    #Titulo
    ax.set_title('Fecha : '+mensaje, loc = "center", fontdict = {'fontsize':15, 'fontweight':'bold', 'color':'tab:blue'})
    ax.set_xlabel("Nits")
    ax.set_ylabel("Cantidad de Movimientos")
    # Guardar el gráfico en formato png
    plt.savefig('SAT/static/resumenMovs.png')
    # Mostrar el gráfico
    #plt.show()

    ctx = {'facturas':req.get('facturas'),'tipo':'Resumen de IVA por fecha y NIT'}

    return render(request,'resumen.html',ctx)

def resumenFecha(request):

    inicio = request.POST["inicio"]
    fin = request.POST["fin"]

    tot = request.POST["tot"]

    if tot == 'Total con IVA':
        iv = 'con'
        m = 'Total Con IVA'
    else:
        iv = 'sin'
        m = 'Total Sin IVA'

    objeto = {
        'inicio':inicio,
        'fin' : fin,
        'iva': iv
    }

    r = requests.post('http://127.0.0.1:5000/resumenFecha',json=objeto)
    req = r.json()

    facs = req.get('facturas')
    x = []
    y = []
    for fac in facs:
        x.append(fac[0])
        y.append(fac[2])

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    #Titulo
    ax.set_title('Fecha : '+inicio+' a '+fin, loc = "center", fontdict = {'fontsize':15, 'fontweight':'bold', 'color':'tab:blue'})
    ax.set_xlabel("Fechas")
    ax.set_ylabel(m)
    # Guardar el gráfico en formato png
    plt.savefig('SAT/static/resumenRango.png')
    # Mostrar el gráfico
    #plt.show()

    ctx = {'facturas':req.get('facturas'),'tipo':'Resumen por rango de fechas','tot':m}

    return render(request,'resumen.html',ctx)

def reporte(request):
    r = requests.get('http://127.0.0.1:5000/Datos')
    req = r.json()
    text1 = str(req.get('Respuesta'))
    w, h = A4
    c = canvas.Canvas("SAT/static/reporte.pdf", pagesize=A4)
    c.drawString(50, h - 50, "Gráficas")
    c.drawImage("SAT/static/resumenMovs.png", 125, h - 400, width=325, height=325)
    c.drawImage("SAT/static/resumenRango.png", 125, h - 750, width=325, height=325)
    c.showPage()
    c.drawString(50, h - 50, "Archivo de Salida")
    pag = ''
    cont = 0
    for letra in text1:
        pag += letra
        if letra == '\n':
            cont +=1
        if cont > 50:
            text = c.beginText(50, h - 100)
            text.setFont("Times-Roman", 11)
            text.textLines(pag)
            c.drawText(text)
            c.showPage()
            cont = 0
            pag = ''
    text = c.beginText(50, h - 100)
    text.setFont("Times-Roman", 11)
    text.textLines(pag)
    c.drawText(text)
    
    c.save()
    return render(request,'reporte.html')