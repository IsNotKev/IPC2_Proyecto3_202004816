from enum import auto
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from Factura import Factura,encontrarFecha
import json 
import math
import xml.etree.ElementTree as ET


Facturas = []
entrada = ''
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def rutaInicial():
    return ('Kevin Steve Martinez Lemus - 202004816')

@app.route('/', methods=['POST'])
def rutaPost():
    return ('Este es un Post')

@app.route('/Facturas', methods=['POST'])
def agregarFacturas():
    global Facturas
    global entrada
    Facturas = []

    referencias = []

    xml = request.json['data']
    entrada = xml
    root = ET.fromstring(xml)

    dteleidos = root.findall('DTE')

    for dte in dteleidos:
        #Datos
        fecha = encontrarFecha(dte.findall('TIEMPO')[0].text)
        referencia = dte.findall('REFERENCIA')[0].text
        nemisor = dte.findall('NIT_EMISOR')[0].text
        nreceptor = dte.findall('NIT_RECEPTOR')[0].text
        valor = dte.findall('VALOR')[0].text
        iva = dte.findall('IVA')[0].text
        total = dte.findall('TOTAL')[0].text

        nFactura = Factura(fecha,referencia,nemisor,nreceptor,valor,iva,total)

        #Guardando Facturas
        if len(Facturas) > 0:
            encontrado = False
            for c in Facturas:
                if c[0].fecha == fecha:
                    encontrado = True
                    c.append(nFactura)
            if not encontrado:
                nuevo = [nFactura]
                Facturas.append(nuevo)  
        else:
            nuevo = [nFactura]
            Facturas.append(nuevo) 

        #nFactura.imprimir()

    #print(len(Facturas))

    data = ET.Element('LISTAAUTORIZACIONES')    
    
    
    for factura in Facturas:
        autorizacion = ET.SubElement(data,'AUTORIZACION')
        xfecha = ET.SubElement(autorizacion,'FECHA')
        xfecha.text = factura[0].fecha
        facrec = ET.SubElement(autorizacion,'FACTURAS_RECIBIDAS')
        facrec.text = str(len(factura))

        emisores = []
        receptores = []
        referencias = []
        aprobadas = []

        eriva = 0
        ertotal = 0
        eremisor = 0
        erreceptor = 0
        refdup = 0
        correctas = 0

        contc = 1

        for i in range(len(factura)):
            aceptada = True
            #Verificando iva y total
            if round(float(factura[i].valor)*0.12,2) != float(factura[i].iva):
                eriva += 1
                aceptada = False
            if round(float(factura[i].valor)+round(float(factura[i].valor)*0.12,2),2) != float(factura[i].total):
                ertotal += 1
                aceptada = False

            if not comprobarNit(factura[i].nemisor):
                aceptada = False
                eremisor +=1

            if not comprobarNit(factura[i].nreceptor):
                aceptada = False
                erreceptor +=1

            if len(referencias) > 0:
                for ref in referencias:
                    if ref == factura[i].referencia:
                        refdup += 1
                        aceptada = False
                if aceptada:
                    referencias.append(factura[i].referencia)
            else:
                referencias.append(factura[i].referencia) 
            #Guardando nit emisores
            if len(emisores)>0:
                encontrado = False
                for emisor in emisores:
                    if emisor == factura[i].nemisor:
                        encontrado = True
                if not encontrado:
                    emisores.append(factura[i].nemisor)
            else:
                emisores.append(factura[i].nemisor)
            #Guardando nits receptores
            if len(receptores)>0:
                encontrado = False
                for receptor in receptores:
                    if receptor == factura[i].nreceptor:
                        encontrado = True
                if not encontrado:
                    receptores.append(factura[i].nreceptor)
            else:
                receptores.append(factura[i].nreceptor)

            if  aceptada:
                correctas += 1
                dig = (factura[i].fecha).split('/')
                codaprobacion = ''

                codaprobacion += dig[2]
                codaprobacion += dig[1]
                codaprobacion += dig[0]

                ax = 7-len(str(contc))

                for z in range(ax):
                    codaprobacion += '0'

                codaprobacion += str(contc)
                contc +=1
                factura[i].codaprobacion = codaprobacion
                aprobadas.append(factura[i])
                pass
        
        errores = ET.SubElement(autorizacion,'ERRORES')
        nit_emisor = ET.SubElement(errores,'NIT_EMISOR')
        nit_emisor.text = str(eremisor)
        nit_receptor = ET.SubElement(errores,'NIT_RECEPTORES')
        nit_receptor.text = str(eremisor)
        erriva = ET.SubElement(errores,'IVA')
        erriva.text = str(eriva)
        errtotal = ET.SubElement(errores,'TOTAL')
        errtotal.text = str(ertotal)
        refduplicada = ET.SubElement(errores,'REFERENCIA_DUPLICADA')
        refduplicada.text = str(refdup)

        faccorrectas = ET.SubElement(autorizacion,'FACTURAS_CORRECTAS')
        faccorrectas.text = str(correctas)
        cantemisores = ET.SubElement(autorizacion,'CANTIDAD_EMISORES')
        cantemisores.text = str(len(emisores))
        cantreceptores = ET.SubElement(autorizacion,'CANTIDAD_RECEPTORES')
        cantreceptores.text = str(len(receptores))

        listautorizacion = ET.SubElement(autorizacion,'LISTADO_AUTORIZACIONES')

        for fac in aprobadas:
            #fac.imprimir()
            aprobacion = ET.SubElement(listautorizacion,'APROBACION')
            nitem = ET.SubElement(aprobacion,'NIT_EMISOR')
            nitem.set('ref',fac.referencia)
            nitem.text = fac.nemisor
            c_ap = ET.SubElement(aprobacion,'CODIGO_APROBACION')
            c_ap.text = fac.codaprobacion

    ET.indent(data,space='      ',level=0)
    mydata = ET.tostring(data)
    myfile = open('autorizaciones.xml', "wb")
    myfile.write(mydata)
    myfile.close()
    return jsonify({'Mensaje':'Se guardó la información correctamente','Entrada':entrada})

def comprobarNit(nit):
    cont = 2
    sum = 0
    verificador = nit[len(nit)-1]
    for i in range(len(nit)-2,-1,-1):
        sum += (int(nit[i]) * cont)
        cont += 1
    #print(sum)
    r = sum%11
    #print((11-r)%11,verificador)
    if ((11-r)%11) == 10:
        if verificador == 'K':
            #print('True')
            return True
        else:
            #print('False')
            return False
    else:
        if float(verificador) == ((11-r)%11):
            #print('True')
            return True
        else:
            #print('False')
            return False

@app.route('/Datos', methods=['GET'])
def consultarDatos():
    global entrada
    if entrada != '':
        archivo = open('autorizaciones.xml', 'r')
        contenido = archivo.read()
        archivo.close
        return jsonify({'Respuesta':contenido,'Entrada':entrada})
    else:
        return jsonify({'Respuesta':'No se han ingresado facturas','Entrada':''})

@app.route('/Datos', methods=['DELETE'])
def eliminarDatos():
    global Facturas
    global entrada
    Facturas = []
    entrada = ''
    return jsonify({'Respuesta':'Reset Completado','Entrada':entrada})


if __name__ == "__main__":
    app.run(debug=True)