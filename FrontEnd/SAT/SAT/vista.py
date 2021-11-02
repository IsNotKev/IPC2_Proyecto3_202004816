from django.http.response import HttpResponse
from django.shortcuts import render
import requests
import xmltodict
import json


from django.template import loader

def index(request):

    ctx = {}

    return render(request,'index.html',ctx)

def delete(request):
    r = requests.delete('http://127.0.0.1:5000/Datos')
    req = r.json()
    ctx = {'respuesta':req.get('Respuesta'),'entrada':req.get('Entrada')}
    return render(request,'index.html',ctx)


def enviar(request):
    mensaje = request.POST["entrada"]

    if mensaje != '':

        objeto = {
            'data': mensaje
        }
        r = requests.post('http://127.0.0.1:5000/Facturas',json=objeto)
        req = r.json()

        ctx = {'respuesta':req.get('Mensaje'),'entrada':req.get('Entrada')}

        return render(request,'index.html',ctx)
    else:
        ctx = {'respuesta':'No se envió nada','entrada':mensaje}
        return render(request,'index.html',ctx)

def consultar(request):

    r = requests.get('http://127.0.0.1:5000/Datos')
    req = r.json()

    ctx = {'respuesta':req.get('Respuesta'),'entrada':req.get('Entrada')}

    return render(request,'index.html',ctx)