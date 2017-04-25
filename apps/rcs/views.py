# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, hashers
from django.db import transaction
from django.contrib import messages
from django.views.generic import View, FormView,TemplateView,DeleteView
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.contrib.auth.decorators import login_required
# from django.apps import apps
from apps.wkhtmltopdf.views import PDFTemplateResponse
from apps.registro.models import *
from apps.rcs.models import *
# from utils.HelpMethods.aes_cipher import encode as secure_value_encode
# from utils.HelpMethods.aes_cipher import decode as secure_value_decode
import json
import random
import string
import logging
import datetime
import os
import sys

from os import path

# Create your views here.

class VerPlanillaSeguroCarro(View):

    def dispatch(self, request, *args, **kwargs):
        print "holis"
        return super(VerPlanillaSeguroCarro, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        context={}
        if settings.SECURE_SSL_REDIRECT == True:
                media_url = 'https://'
        else:
            media_url = 'http://'
        data={}
        media_url = media_url+request.META['HTTP_HOST']

        context['http_host']= media_url
        response = PDFTemplateResponse(request=request,
                                   template='rcs/solo_visualizar_planilla_registro_carro_seguro.html',
                                   filename="planilla_registro_carro.pdf",
                                   context= context,
                                   show_content_in_browser=True,
                                   cmd_options={'margin-top': 10,'page-size': 'A4','quiet': True},
                            
                                   )
        return response

    
    # def __init__(self, *args, **kwargs):
    #   kwargs['max_length'] = 104
    #   super(VerPlanillaSeguroCarro, self).__init__(*args, **kwargs)
            # acta_recepcion = ActaRecepcion(nombre='ejemplo',fk_solicitud_rtn=Solicitud,fecha=datetime.now())
            # acta_recepcion.save()
        # direc = ('recepcion_juridico.pdf',ContentFile(response.rendered_content))


            # data['Result'] = "success"
            # pdf_dir = acta_recepcion.ruta.url
            # data['pdf_dir'] = pdf_dir
            # if not enviar_correo_planillas(usuario=registro_pst.usuario, adj=[pdf_dir], template_name='correo/correo_planilla_recepcion.html',asunto='Planilla de recepción'):
            #     data = {}
            #     data['Result'] = 'error'
            #     data['Message'] = 'Correo invalido4'
            #     data['codigo_error'] = 'CORREO_INVALIDO'

            #     return HttpResponse(json.dumps(data), content_type = "application/json")
        # solicitud.ruta.save('PlanillaSolicitud.pdf', ContentFile(file_pdf.getvalue()))
        # data['Result'] = "success"
        # data['pdf_dir'] = 'planilla_multa_omision'
        # return HttpResponse(json.dumps(data), content_type = "application/json")
        # return render(request,"solo_visualizar_planilla_registro_carro_seguro.html",context)

# @login_required
class Dashboard(View):
    """docstring for Dashboard"""
    # @login_required
    def dispatch(self, request, *args, **kwargs):
        # print "holis2"
        if not request.user.is_authenticated():
            return redirect(reverse_lazy('login'))
        return super(Dashboard, self).dispatch(request, *args, **kwargs)

        
    def get(self, request, *args, **kwargs):
        nombre = request.user.nombre
        username = request.user.username
        context = {
            'nombre': nombre,
            'username': username,
        }
        return render(request, 'rcs/dashboard.html',context)



class GestionSolicitudAbierta(View):
    """
    GestionSolicitudAbierta
    -------------------------------------------
    Gestiona las solicitudes en estatus abierta
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(GestionSolicitudAbierta, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        condiciones = CondicionesGeneralesVehiculo.objects.all()
        mecanicas = MecanicaVehiculo.objects.all()
        accesorios = AccesoriosVehiculo.objects.all()
        detalles = DetallesDatos.objects.all()
        estados_vehiculo = EstadoVehiculo.objects.all()
        context = {
            'condiciones': condiciones,
            'mecanicas': mecanicas,
            'accesorios': accesorios,
            'detalles': detalles,
            'estados_vehiculo': estados_vehiculo,
        }

        return render(request, 'rcs/inspector/flujo_solicitud/nueva_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}
        observacion = "observacion_"
        radio = "radio_"
        mecanicas = MecanicaVehiculo.objects.all()
        vehiculo = Vehiculo.objects.get(id=1)
        # mecanica_vehiculo
        import pudb; pu.db
        with transaction.atomic():
            for mecanica in mecanicas:
                # mec_sol
                mecanica.observacion = data[observacion+mecanica.codigo]
                mecanica.fk_estado_vehiculo_id = EstadoVehiculo.objects.get(codigo = data[radio+mecanica.codigo])
                mecanica.save()
                ##Agregando mecanica a many to many field de vehiculo
                vehiculo.mecanica_vehiculo.add(mecanica)
            # print data[observacion+mecanica.codigo]
            # print data[radio+mecanica.codigo]


        #if data: 
        #   response['Result'] = 'success'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        #else:
        #    response['Result'] = 'error'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")


        return redirect(reverse_lazy('condiciones_vehiculo'))







class CondicionVehiculoSolicitud(View):
    """
    CondicionVehiculoSolicitud
    -------------------------------------------
    paso 2 inclusion de condiciones del vehiculo en vehiculo/solicitud
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(CondicionVehiculoSolicitud, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        condiciones = CondicionesGeneralesVehiculo.objects.all()
        estados_vehiculo = EstadoVehiculo.objects.all()
        context = {
            'condiciones': condiciones,
            'estados_vehiculo': estados_vehiculo,
        }

        return render(request, 'rcs/inspector/flujo_solicitud/condiciones_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}


        #if data: 
        #    response['Result'] = 'success'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        #else:
        #    response['Result'] = 'error'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")


        return redirect(reverse_lazy('mecanica_vehiculo'))



class MecanicaVehiculoSolicitud(View):
    """
    MecanicaVehiculoSolicitud
    -------------------------------------------
    paso 3 inclusion de mecanica en vehiculo/solicitud
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(MecanicaVehiculoSolicitud, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        mecanicas = MecanicaVehiculo.objects.all()
        estados_vehiculo = EstadoVehiculo.objects.all()
        context = {
            'mecanicas': mecanicas,
            'estados_vehiculo': estados_vehiculo,
        }


        return render(request, 'rcs/inspector/flujo_solicitud/mecanica_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}


        #if data: 
        #    response['Result'] = 'success'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        #else:
        #    response['Result'] = 'error'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")


        return redirect(reverse_lazy('accesorios_vehiculo'))

class AccesoriosVehiculoSolicitud(View):
    """
    AccesoriosVehiculoSolicitud
    -------------------------------------------
    paso 4 colocan los accesorios dentro de vehiculo/solcitud
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(AccesoriosVehiculoSolicitud, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        accesorios = AccesoriosVehiculo.objects.all()
        estados_vehiculo = EstadoVehiculo.objects.all()
        context = {
            'accesorios': accesorios,
            'estados_vehiculo': estados_vehiculo,
        }


        return render(request, 'rcs/inspector/flujo_solicitud/accesorios_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}


        #if data: 
        #    response['Result'] = 'success'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        #else:
        #    response['Result'] = 'error'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")


        return redirect(reverse_lazy('documentos_vehiculo'))


class DetallesVehiculoSolicitud(View):
    """
    DetallesVehiculoSolicitud
    -------------------------------------------
    paso 5 Detalles que tenga el vehiculo/solicitud
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(DetallesVehiculoSolicitud, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {

        }

        return render(request, 'rcs/inspector/flujo_solicitud/detalles_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}


        #if data: 
        #    response['Result'] = 'success'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        #else:
        #    response['Result'] = 'error'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")


        return redirect(reverse_lazy('template_dir'))

class DocumentosVehiculoSolicitud(View):
    """
    DocumentosVehiculoSolicitud
    -------------------------------------------
    paso 6 donde se checkean los documentos que trajo para el vehiculo/solicitud
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(DocumentosVehiculoSolicitud, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        documentos = DocumentosPresentados.objects.all()
        context = {
            'documentos': documentos,
        }


        return render(request, 'rcs/inspector/flujo_solicitud/documentos_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}


        #if data: 
        #    response['Result'] = 'success'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        #else:
        #    response['Result'] = 'error'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")


        # vista_previa_solicitud
        return redirect(reverse_lazy('dashboard'))
