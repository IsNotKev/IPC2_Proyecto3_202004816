from django.http.response import HttpResponse
from django.shortcuts import render
import requests
import matplotlib.pyplot as plt


from django.template import loader

def index(request):
    r = requests.get('http://127.0.0.1:5000/Entrada')
    req = r.json()
    ctx = {'entrada':req.get('entrada'),'fechas':req.get('Fechas')}
    return render(request,'index.html',ctx)

def delete(request):
    r = requests.delete('http://127.0.0.1:5000/Datos')
    req = r.json()
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

    fig, ax = plt.subplots()
    # Dibujar puntos
    ax.scatter(x = [1, 2, 3], y = [3, 2, 1])
    # Guardar el gráfico en formato png
    plt.savefig('SAT/static/diagrama-dispersion.png')
    # Mostrar el gráfico
    #plt.show()

    mensaje = request.POST["fec"]
    print(mensaje)
    objeto = {
            'fecha': mensaje
        }


    r = requests.post('http://127.0.0.1:5000/resumenIVA',json=objeto)
    req = r.json()

    facs = req.get('facturas')
    nits = []
    for fac in facs:
        if len(nits) > 0:
            #for n in nits:
            #    if fac[1] 
            pass
        else:
            nits.append(fac[1])




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
    ctx = {'facturas':req.get('facturas'),'tipo':'Resumen por rango de fechas','tot':m}

    return render(request,'resumen.html',ctx)