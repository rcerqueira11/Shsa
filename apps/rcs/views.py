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
from django.apps import apps
from django.core.files.base import ContentFile
from django.db.models import Q
# from django.apps import apps
from apps.wkhtmltopdf.views import PDFTemplateResponse
from apps.registro.models import *
from apps.rcs.models import *
from utils.HelpMethods.aes_cipher import encode as secure_value_encode
from utils.HelpMethods.aes_cipher import decode as secure_value_decode
import json
import random
import string
import logging
import datetime
import os
import sys

from os import path

# Create your views here.

def format_float(X):
    X = X.replace(" ","")
    X = X.replace(".","")
    X = X.replace(",",".")

    return float(X)

def mas_una_solicitud_titular(x):
    cant = len(SolicitudInspeccion.objects.filter(fk_titular_vehiculo=x))
    return True if cant > 1 else False

def mas_una_solicitud_trajo(x):
    cant = len(SolicitudInspeccion.objects.filter(fk_trajo_vehiculo=x))
    return True if cant > 1 else False

def mas_una_solicitud_placa(x):
    cant = len(SolicitudInspeccion.objects.filter(fk_vehiculo__placa=x))
    return True if cant > 1 else False


def verificar_codigo_detalle(request):
    data = request.GET
    respuesta = {}
    solicitud = SolicitudInspeccion.objects.get(id=data['id_solicitud'])
    vehiculo= solicitud.fk_vehiculo
    detalles = vehiculo.detalles_datos.all()
    codigos_detalles_vehiculo = [x.codigo for x in detalles]

    validacion = True if DetallesDatos.objects.filter(codigo=data['codigo_verif']).exists() else False
    codigo_es_mio = True if data['codigo_verif'] in codigos_detalles_vehiculo else False

    if validacion:
        if not codigo_es_mio:
            respuesta['results'] = 'success'
            respuesta['existe'] = validacion
        else:
            respuesta['results'] = 'success'
            respuesta['existe'] = False
    else:
        respuesta['results'] = 'success'
        respuesta['existe'] = validacion
    return HttpResponse(json.dumps(respuesta), content_type = "application/json")

def verificar_placa_carro(request):
    data = request.GET
    placa = data['placa']
    respuesta = {}
    if Vehiculo.objects.filter(placa=placa).exists():
        titular = Vehiculo.objects.get(placa=placa).fk_titular_vehiculo
        respuesta['results'] = 'success'
        respuesta['nombre'] = titular.nombre
        respuesta['apellido'] = titular.apellido
        respuesta['telefono'] = titular.telefono
        respuesta['cedula'] = titular.cedula
    else:
        respuesta['results'] = 'success_no_existe'
    return HttpResponse(json.dumps(respuesta), content_type = "application/json")

def verificar_titular_cedula(request):
    data = request.GET
    cedula = data['cedula']
    respuesta = {}
    if TitularVehiculo.objects.filter(cedula=cedula).exists():
        titular = TitularVehiculo.objects.get(cedula=cedula)
        respuesta['results'] = 'success'
        respuesta['nombre'] = titular.nombre
        respuesta['apellido'] = titular.apellido
        respuesta['telefono'] = titular.telefono
    else:
        respuesta['results'] = 'success_no_existe'
    return HttpResponse(json.dumps(respuesta), content_type = "application/json")

def verificar_trajo_cedula(request):
    data = request.GET
    cedula = data['cedula']
    respuesta = {}
    if TrajoVehiculo.objects.filter(cedula=cedula).exists():
        titular = TrajoVehiculo.objects.get(cedula=cedula)
        respuesta['results'] = 'success'
        respuesta['nombre'] = titular.nombre
        respuesta['apellido'] = titular.apellido
        respuesta['parentesco'] = titular.parentesco
    else:
        respuesta['results'] = 'success_no_existe'
    return HttpResponse(json.dumps(respuesta), content_type = "application/json")

class VerPlanillaSeguroCarro(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(reverse_lazy('login'))
        return super(VerPlanillaSeguroCarro, self).dispatch(request, *args, **kwargs)

    def get_context(self, request,data):

        id_sol = secure_value_decode(data['sol_id']) if 'sol_id' in data else request.session['sol_id']
        solicitud = SolicitudInspeccion.objects.get(id=id_sol)
        vehiculo = solicitud.fk_vehiculo
        condiciones_generales_vehiculo = vehiculo.condiciones_generales_vehiculo.all().exclude(fk_estado_vehiculo_id=None)
        mecanica_vehiculo = vehiculo.mecanica_vehiculo.all().exclude(fk_estado_vehiculo_id=None)
        accesorios_vehiculo = vehiculo.accesorios_vehiculo.all().exclude(observacion=None)
        detalles_datos = vehiculo.detalles_datos.all()
        documentos_presentados = vehiculo.documentos_presentados.all()
        # trajo_vehiculo = vehiculo.fk_trajo_vehiculo
        trajo_vehiculo = solicitud.fk_trajo_vehiculo
        titular_vehiculo = solicitud.fk_titular_vehiculo

        context = {
            'nombre': request.user.nombre,
            'username': request.user.username,        
            'condiciones': condiciones_generales_vehiculo,
            'accesorios': accesorios_vehiculo,
            'detalles': detalles_datos,
            'documentos': documentos_presentados,
            'mecanicas': mecanica_vehiculo,
            'vehiculo': vehiculo,
            'trajo_alguien_mas': False if trajo_vehiculo is None else True,
            'trajo_vehiculo': trajo_vehiculo,
            'titular_vehiculo': titular_vehiculo,
            'solicitud':solicitud,
            'estado_solicitud':solicitud.fk_estado_solicitud.codigo,
            }

        return context
    
    def get(self, request, *args, **kwargs):
        data = request.GET

        context = self.get_context(request,data)
        context['nombre'] = request.user.nombre
        context['username'] = request.user.username

        return render(request, 'rcs/inspector/flujo_solicitud/vista_previa_solicitud.html',context)

    def post(self, request, *args, **kwargs):
        # context={}
        data = request.POST
        id_sol = data['id_solicitud']
        solicitud = SolicitudInspeccion.objects.get(id=id_sol)
        context = self.get_context(request,request)
        if settings.SECURE_SSL_REDIRECT == True:
                media_url = 'https://'
        else:
            media_url = 'http://'
        respuesta={}
        media_url = media_url+request.META['HTTP_HOST']

        context['http_host']= media_url
        response = PDFTemplateResponse(request=request,
                                   template='rcs/solo_visualizar_planilla_registro_carro_seguro.html',
                                   filename="planilla_registro_carro.pdf",
                                   context= context,
                                   show_content_in_browser=True,
                                   cmd_options={'margin-top': 10,'page-size': 'A4','quiet': True},
                            
                                   )
        codigo_actual = solicitud.fk_estado_solicitud.codigo
        codigo_siguiente = 'PEND_GEST' if codigo_actual == 'PEND_INSP' else 'CERRADA'
        solicitud.fk_estado_solicitud = EstadoSolicitud.objects.get(codigo=codigo_siguiente)
        

        with transaction.atomic():
            solicitud.ruta.delete()
            solicitud.ruta.save('Inspeccion_placa_'+solicitud.fk_vehiculo.placa+'.pdf',ContentFile(response.rendered_content))

            solicitud.save()


        # return response
    # def __init__(self, *args, **kwargs):
    #   kwargs['max_length'] = 104
    #   super(VerPlanillaSeguroCarro, self).__init__(*args, **kwargs)
            # acta_recepcion = ActaRecepcion(nombre='ejemplo',fk_solicitud_rtn=Solicitud,fecha=datetime.now())
            # acta_recepcion.save()
        # direc = ('recepcion_juridico.pdf',ContentFile(response.rendered_content))


        respuesta['results'] = "success"
        pdf_dir = solicitud.ruta.url
        respuesta['pdf_dir'] = pdf_dir
        return HttpResponse(json.dumps(respuesta), content_type = "application/json")
            # if not enviar_correo_planillas(usuario=registro_pst.usuario, adj=[pdf_dir], template_name='correo/correo_planilla_recepcion.html',asunto='Planilla de recepción'):
            #     data = {}
            #     data['results'] = 'error'
            #     data['Message'] = 'Correo invalido4'
            #     data['codigo_error'] = 'CORREO_INVALIDO'

            #     return HttpResponse(json.dumps(data), content_type = "application/json")
        # solicitud.ruta.save('PlanillaSolicitud.pdf', ContentFile(file_pdf.getvalue()))
        # data['results'] = "success"
        # data['pdf_dir'] = 'planilla_multa_omision'
        # return HttpResponse(json.dumps(data), content_type = "application/json")
        # return render(request,"solo_visualizar_planilla_registro_carro_seguro.html",context)


class FiltroBusqueda(View):
    """
        Vista para filtrar registros de forma genérica
    """

    def dispatch(self, request, *args, **kwargs):

        if request.user.username == '' or request.user.is_authenticated() == False:
            return redirect(reverse_lazy('registro_logout'))

        return super(FiltroBusqueda, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        filtro = {}
        parametros = {}
        data_filter = []

        # se obtienen los parametros de busquedas provenientes del formulario
        # de búsqueda
        parametros = request.GET
        parametros = parametros.copy()
        parametros['usuario'] = request.user
        # el modelo a consultar se obtiene de la variable 'filter_code', al
        # mismo se le pasan los parametros de busqueda recibidos
        model_obj = parametros.get('filter_obj', None)
        filter_code = parametros.get('filter_code', None)
        if model_obj and filter_code:
            model_obj = apps.get_model('rcs', model_obj)
            instance = model_obj()
            data_filter = model_obj.filtro(instance,parametros, filter_code)

            # si obtenemos resultados en el filtro de busqueda, se procede a
            # paginarlo
            if data_filter[1]:
                paginator = Paginator(data_filter[1], 6)

                try:
                    page = request.GET.get('page', 1)
                    page_filter = paginator.page(page)
                except PageNotAnInteger:
                    page = 0
                    page_filter = paginator.page(1)
                except EmptyPage:
                    page_filter = paginator.page(paginator.num_pages)

                try:
                    filtro['previous_page'] = page_filter.previous_page_number()
                except EmptyPage:
                    filtro['previous_page'] = False
                try:
                    filtro['next_page'] = page_filter.next_page_number()
                except EmptyPage:
                    filtro['next_page'] = False

                filtro['total_pages'] = paginator.num_pages
                filtro['page_number'] = page_filter.number
                filtro['data'] = json.dumps(page_filter.object_list)
                filtro['order'] = data_filter[0]

            return HttpResponse(json.dumps(filtro), content_type="application/json")
        else:
            return HttpResponse(json.dumps({}), content_type="application/json")


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


class BandejaSolicitudes(View):
    """
    BandejaSolicitudes
    -------------------------------------------
    Bandeja donde se muestran las solicitudes de inspeccion realizadas
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(BandejaSolicitudes, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        context['nombre'] = request.user.nombre
        context['username'] = request.user.username
        context['estado_solicitudes'] = EstadoSolicitud.objects.all()
        


        if 'sol_id' in request.session:
            del request.session['sol_id']

        return render(request, 'rcs/inspector/bandeja_solicitudes.html',context)

class SolicitarInspeccion(View):
    """
    SolicitarInspeccion 
    -------------------------------------------
    Gestiona las solicitudes en estatus abierta, paso 1 datos del vehiculo
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(SolicitarInspeccion, self).dispatch(request, *args, **kwargs)


    def get_context(self, data):
        motivo = MotivoSolicitud.objects.all()
         
        context = {
            'motivos_de_visita': motivo,
            'nombre': data.user.nombre,
            'username': data.user.username,
        }
        
        return context

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios
        for key in data:
            value = data.get(key, None)
            if 'radio_titular' in data:
                if data['radio_titular'] == 'false':
                    if not value.strip():
                        errors[key] = 'El campo no debe estar vacío'
                else:
                    if not 'trajo' in key:
                        if not value.strip():
                            errors[key] = 'El campo no debe estar vacío'
            else:
                if not value.strip():
                    errors[key] = 'El campo no debe estar vacío'
        return errors

    def get(self, request, *args, **kwargs):
        data = {}
        context = self.get_context(request)
        
        #obtener datos que requieran ser pre-cargados en el formulario (ejemplo: editar registro) y guardarlos en form_data
        form_data = {}

        #"form_data" representa un diccionario cuyas claves son los nombres de los inputs html del formulario y sus valores 
        #son tuplas donde almacenan los valores y los errores de los inputs respectivamente

        context['form_data'] = form_data

        return render(request, 'rcs/taquilla/crear_ticket.html',context)

    def post(self,request,*args,**kwargs):


        data = request.POST
        response = {}

        errors = self.validate(data)

        if not errors:

            #procesar y guardar data del formulario en BD
            solicitud = SolicitudInspeccion()
            vehiculo = Vehiculo()
            titular_vehiculo = TitularVehiculo()
            trajo_vehiculo = TrajoVehiculo()


            nombre_titular = data['nombre_titular']
            apellido_titular = data['apellido_titular']
            cedula_titular = data['cedula_titular']
            telefono_titular = data['telefono_titular']
            placa = data['placa']
            motivo_visita = data['motivo_visita']
            nombre_trajo_vehiculo = data['nombre_trajo_vehiculo']
            apellido_trajo_vehiculo = data['apellido_trajo_vehiculo']
            cedula_trajo_vehiculo = data['cedula_trajo_vehiculo']
            parentesco_trajo_vehiculo = data['parentesco_trajo_vehiculo']
            if SolicitudInspeccion.objects.filter(Q(fk_vehiculo__placa=placa),Q(fk_titular_vehiculo__cedula=cedula_titular),~Q(fk_estado_solicitud__codigo="CERRADA")).exists():
                respuesta = {}
                respuesta['results'] = "error"
                respuesta['mensaje'] = "No se puede crear otra solicitud para el mismo carro mientras una esté en proceso."
                return HttpResponse(json.dumps(respuesta), content_type="application/json")

            with transaction.atomic():
                if TitularVehiculo.objects.filter(cedula=cedula_titular).exists():
                    titular_vehiculo=TitularVehiculo.objects.get(cedula=cedula_titular)
                else:
                    titular_vehiculo.nombre = nombre_titular
                    titular_vehiculo.apellido = apellido_titular
                    titular_vehiculo.cedula = cedula_titular
                    titular_vehiculo.telefono = telefono_titular
                    titular_vehiculo.save()

                if data['nombre_trajo_vehiculo'].strip() != "":
                    
                    if TrajoVehiculo.objects.filter(cedula=cedula_trajo_vehiculo).exists():
                        trajo_vehiculo= TrajoVehiculo.objects.get(cedula=cedula_trajo_vehiculo)
                    else:
                        trajo_vehiculo.nombre =  nombre_trajo_vehiculo
                        trajo_vehiculo.apellido = apellido_trajo_vehiculo
                        trajo_vehiculo.cedula = cedula_trajo_vehiculo
                        trajo_vehiculo.parentesco = parentesco_trajo_vehiculo
                        trajo_vehiculo.save()
                    # vehiculo.fk_trajo_vehiculo = trajo_vehiculo
                    solicitud.fk_trajo_vehiculo = trajo_vehiculo
                    


                vehiculo.placa = placa
                vehiculo.fk_titular_vehiculo = titular_vehiculo
                vehiculo.save()

                solicitud.fk_vehiculo = vehiculo
                solicitud.fk_titular_vehiculo = titular_vehiculo
                solicitud.fk_motivo_solicitud = MotivoSolicitud.objects.get(codigo = motivo_visita) 
                solicitud.save()

            respuesta={'results': 'success',}
            return HttpResponse(json.dumps(respuesta), content_type="application/json")
        else:
            # context = self.get_context(request)

            # form_data = {}
            # for key, value in data.iteritems():
            #     if key in errors.keys():
            #         form_data[key] = (value, errors[key])
            #     else:
            #         form_data[key] = (value, '')

            # context['form_data'] = form_data

            # return render(request, 'rcs/taquilla/crear_ticket.html', context)
            response['errors'] = errors

            return HttpResponse(json.dumps(response), content_type = "application/json")

## Views de Flujo
class GestionSolicitudAbierta(View):
    """
    GestionSolicitudAbierta
    -------------------------------------------
    Gestiona las solicitudes en estatus abierta, paso 1 datos del vehiculo
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(GestionSolicitudAbierta, self).dispatch(request, *args, **kwargs)

    def get_context(self, request,data):
        # id_solicitud = 1
        # data = request.GET
        id_sol = secure_value_decode(data['sol_id']) if 'sol_id' in data else request.session['sol_id']
        solicitud = SolicitudInspeccion.objects.get(id=id_sol)
        request.session['sol_id'] = id_sol
        vehiculo = Vehiculo.objects.get(id=solicitud.fk_vehiculo.id)
        tipo_vehiculo = TipoVehiculo.objects.all()
        titular_vehiculo = solicitud.fk_titular_vehiculo
        # trajo_vehiculo = vehiculo.fk_trajo_vehiculo
        trajo_vehiculo = solicitud.fk_trajo_vehiculo
        tipo_manejo = TipoManejo.objects.all()
        context = {
            'vehiculo': vehiculo,
            'tipos_de_vehiculo': tipo_vehiculo,
            'tipos_de_manejo': tipo_manejo,
            'titular_vehiculo': titular_vehiculo,
            'trajo_vehiculo': trajo_vehiculo,
            'trajo_alguien_mas': False if trajo_vehiculo is None else True,
            'solicitud': solicitud,
            'nombre': data.user.nombre if 'user' in data else "",
            'username': data.user.username if 'user' in data else "",
        }
        
        return context

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios
        for key in data:
            value = data.get(key, None)
            if not value.strip():
                errors[key] = 'El campo no debe estar vacío'

        return errors

    def get(self, request, *args, **kwargs):
        data = request.GET

        context = self.get_context(request,data)
        
        #obtener datos que requieran ser pre-cargados en el formulario (ejemplo: editar registro) y guardarlos en form_data
        form_data = {}

        #"form_data" representa un diccionario cuyas claves son los nombres de los inputs html del formulario y sus valores 
        #son tuplas donde almacenan los valores y los errores de los inputs respectivamente

        context['nombre'] = request.user.nombre
        context['username'] = request.user.username
        context['form_data'] = form_data


        return render(request, 'rcs/inspector/flujo_solicitud/nueva_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}

        errors = self.validate(data)

        if not errors:
            solicitud = SolicitudInspeccion.objects.get(id= data['id_solicitud'])
            vehiculo = solicitud.fk_vehiculo
            with transaction.atomic():
                vehiculo.cap_puestos = data['cap_puestos']
                vehiculo.cilindros = data['cilindros']
                vehiculo.peso = data['peso']
                vehiculo.color = data['color']
                vehiculo.kilometraje = data['kilometraje']
                vehiculo.serial_carroceria = data['serial_carroceria']
                vehiculo.serial_motor = data['serial_motor']
                vehiculo.valor_estimado = data['valor_estimado']
                vehiculo.modelo = data['modelo']
                vehiculo.marca = data['marca']
                vehiculo.anho = data['anho']

                vehiculo.fk_inspector = Usuario.objects.get(id=request.user.id)
                vehiculo.fk_tipo_vehiculo = TipoVehiculo.objects.get(codigo=data['tipo_vehiculo'])
                vehiculo.fk_tipo_manejo = TipoManejo.objects.get(codigo=data['tipo_manejo'])

                solicitud.fk_inspector = Usuario.objects.get(id=request.user.id)

                solicitud.save()
                vehiculo.save()
                # print data[observacion+mecanica.codigo]
                # print data[radio+mecanica.codigo]

            return redirect('/rcs/condiciones_vehiculo/')

        else:
            context = self.get_context(request,request)

            form_data = {}
            for key, value in data.iteritems():
                if key in errors.keys():
                    form_data[key] = (value, errors[key])
                else:
                    form_data[key] = (value, '')

            context['form_data'] = form_data

            return render(request, 'rcs/inspector/flujo_solicitud/nueva_solicitud.html',context)
        #if data: 
        #   response['Result'] = 'success'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        #else:
        #    response['Result'] = 'error'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        

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

    def tiene_condiciones(self,id_sol):
        solicitud = SolicitudInspeccion.objects.get(id=id_sol)
        vehiculo = Vehiculo.objects.get(id=solicitud.fk_vehiculo.id)
        return vehiculo.condiciones_generales_vehiculo.all().exists()

    def get_context(self, request,data):
        # id_solicitud = 1
        id_sol = data['sol_id'] if 'sol_id' in data else request.session['sol_id']
        solicitud = SolicitudInspeccion.objects.get(id=id_sol)
        vehiculo = Vehiculo.objects.get(id=solicitud.fk_vehiculo.id)
        if vehiculo.condiciones_generales_vehiculo.all().exists():
            condiciones = vehiculo.condiciones_generales_vehiculo.all().order_by('id')
        else:
            condiciones = CondicionesGeneralesBase.objects.all().order_by('id')

        estados_vehiculo = EstadoVehiculo.objects.all()
        context = {
            'condiciones': condiciones,
            'estados_vehiculo': estados_vehiculo,
            'vehiculo': vehiculo,
            'solicitud': solicitud,
            'nombre': data.user.nombre if 'user' in data else "",
            'username': data.user.username if 'user' in data else "",
        }
        
        return context

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios
        
        for key in data:
            value = data.get(key, None)

            if 'observacion_OTRO' in key:
                codigo = key.split('_',1)[1] 
                if data['radio_'+codigo].strip() !="" and data['observacion_'+codigo].strip()=="":
                    errors[key] = 'El campo no debe estar vacío'
                    
            if not value.strip() and not 'observacion' in key and not 'OTRO' in key :
                errors[key] = 'El campo no debe estar vacío'

        return errors

    def get(self, request, *args, **kwargs):
        data = request.GET

        context = self.get_context(request,data)
        
        #obtener datos que requieran ser pre-cargados en el formulario (ejemplo: editar registro) y guardarlos en form_data
        form_data = {}

        #"form_data" representa un diccionario cuyas claves son los nombres de los inputs html del formulario y sus valores 
        #son tuplas donde almacenan los valores y los errores de los inputs respectivamente

        context['nombre'] = request.user.nombre
        context['username'] = request.user.username
        context['form_data'] = form_data


        return render(request, 'rcs/inspector/flujo_solicitud/condiciones_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}
        observacion = "observacion_"
        radio = "radio_"
        solicitud = SolicitudInspeccion.objects.get(id= data['id_solicitud'])
        vehiculo = solicitud.fk_vehiculo

        if self.tiene_condiciones(solicitud.id):
            condiciones = vehiculo.condiciones_generales_vehiculo.all()
        else:
            condiciones = CondicionesGeneralesBase.objects.all()



        mutable = request.POST._mutable
        request.POST._mutable = True
        for condicion in condiciones:
            codigo = radio+condicion.codigo
            if not codigo in data:
                data[codigo] = ""

        request.POST._mutable = mutable


        errors = self.validate(data)
        if not errors:
            solicitud = SolicitudInspeccion.objects.get(id= data['id_solicitud'])
            vehiculo = solicitud.fk_vehiculo
            with transaction.atomic():
                tenia_condiciones = self.tiene_condiciones(solicitud.id)
                vehiculo.condiciones_generales_vehiculo.clear()
                for condicion in condiciones:

                    if tenia_condiciones:
                        codigo_nuevo = condicion.codigo
                    else:
                        codigo_nuevo = condicion.codigo+'_'+str(vehiculo.id)

                    if data[radio+condicion.codigo].strip() != "":
                        fk_estado_vehiculo_id = EstadoVehiculo.objects.get(codigo = data[radio+condicion.codigo])
                        if CondicionesGeneralesVehiculo.objects.filter(codigo=codigo_nuevo).exists():
                            condicion_ = CondicionesGeneralesVehiculo.objects.get(codigo=codigo_nuevo)
                            condicion_.observacion = data[observacion+condicion.codigo]
                            condicion_.fk_estado_vehiculo= fk_estado_vehiculo_id
                        else:    
                            condicion_ = CondicionesGeneralesVehiculo(codigo=codigo_nuevo, observacion = data[observacion+condicion.codigo], fk_estado_vehiculo= fk_estado_vehiculo_id,parte=condicion.parte)
                        condicion_.save()

                        ##Agregando condicion a many to many field de vehiculo
                        vehiculo.condiciones_generales_vehiculo.add(condicion_)

                vehiculo.save()


            return redirect(reverse_lazy('mecanica_vehiculo'))
        else:
            context = self.get_context(request,request)

            form_data = {}
            for key, value in data.iteritems():
                if key in errors.keys():
                    form_data[key] = (value, errors[key])
                else:
                    form_data[key] = (value, '')

            context['form_data'] = form_data
            return render(request, 'rcs/inspector/flujo_solicitud/condiciones_solicitud.html',context)


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

    def tiene_mecanicas(self,id_sol):
        solicitud = SolicitudInspeccion.objects.get(id=id_sol)
        vehiculo = Vehiculo.objects.get(id=solicitud.fk_vehiculo.id)
        return vehiculo.mecanica_vehiculo.all().exists()

    def get_context(self, request,data):
        id_sol = data['sol_id'] if 'sol_id' in data else request.session['sol_id']
        solicitud = SolicitudInspeccion.objects.get(id=id_sol)
        vehiculo = Vehiculo.objects.get(id=solicitud.fk_vehiculo.id)
        if vehiculo.mecanica_vehiculo.all().exists():
            mecanicas = vehiculo.mecanica_vehiculo.all().order_by('id')
        else:
            mecanicas = MecanicaBase.objects.all().order_by('id')
            
        estados_vehiculo = EstadoVehiculo.objects.all()
        context = {
            'mecanicas': mecanicas,
            'estados_vehiculo': estados_vehiculo,
            'vehiculo': vehiculo,
            'solicitud': solicitud,
            'nombre': data.user.nombre if 'user' in data else "",
            'username': data.user.username if 'user' in data else "",

        }
        
        return context

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios
        for key in data:
            value = data.get(key, None)
            if 'observacion_OTRO' in key:
                codigo = key.split('_',1)[1] 
                if data['radio_'+codigo].strip() !="" and data['observacion_'+codigo].strip()=="":
                    errors[key] = 'El campo no debe estar vacío'
                    
            if not value.strip() and not 'observacion' in key and not 'OTRO' in key :
                errors[key] = 'El campo no debe estar vacío'

        return errors

    def get(self, request, *args, **kwargs):
        data = request.GET

        context = self.get_context(request,data)
        
        #obtener datos que requieran ser pre-cargados en el formulario (ejemplo: editar registro) y guardarlos en form_data
        form_data = {}

        #"form_data" representa un diccionario cuyas claves son los nombres de los inputs html del formulario y sus valores 
        #son tuplas donde almacenan los valores y los errores de los inputs respectivamente

        context['nombre'] = request.user.nombre
        context['username'] = request.user.username
        context['form_data'] = form_data

        return render(request, 'rcs/inspector/flujo_solicitud/mecanica_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}
        observacion = "observacion_"
        radio = "radio_"
        solicitud = SolicitudInspeccion.objects.get(id= data['id_solicitud'])
        vehiculo = solicitud.fk_vehiculo
        if self.tiene_mecanicas(solicitud.id):
            mecanicas = vehiculo.mecanica_vehiculo.all()
        else:
            mecanicas = MecanicaBase.objects.all()

        mutable = request.POST._mutable
        request.POST._mutable = True
        for mecanica in mecanicas:
            codigo = radio+mecanica.codigo
            if not codigo in data:
                data[codigo] = ""

        request.POST._mutable = mutable

        errors = self.validate(data)

        if not errors:
            solicitud = SolicitudInspeccion.objects.get(id= data['id_solicitud'])
            vehiculo = solicitud.fk_vehiculo
            # mecanica_vehiculo
            with transaction.atomic():
                tenia_mecanicas = self.tiene_mecanicas(solicitud.id)
                vehiculo.mecanica_vehiculo.clear()
                for mecanica in mecanicas:

                    if tenia_mecanicas:
                        codigo_nuevo = mecanica.codigo
                    else:
                        codigo_nuevo = mecanica.codigo+'_'+str(vehiculo.id)
                    # mec_sol
                    if data[radio+mecanica.codigo].strip() != "":
                        fk_estado_vehiculo_id = EstadoVehiculo.objects.get(codigo = data[radio+mecanica.codigo])
                        
                        if MecanicaVehiculo.objects.filter(codigo=codigo_nuevo).exists():
                            mecanica = MecanicaVehiculo.objects.get(codigo=codigo_nuevo)
                            mecanica.observacion = data[observacion+mecanica.codigo]
                            mecanica.fk_estado_vehiculo= fk_estado_vehiculo_id
                        else:    
                            mecanica = MecanicaVehiculo(codigo=codigo_nuevo, observacion = data[observacion+mecanica.codigo], fk_estado_vehiculo= fk_estado_vehiculo_id,parte=mecanica.parte)
                        mecanica.save()
                        ##Agregando mecanica a many to many field de vehiculo
                        vehiculo.mecanica_vehiculo.add(mecanica)
                vehiculo.save()


            return redirect(reverse_lazy('accesorios_vehiculo'))
        else:
            context = self.get_context(request,request)
            form_data = {}
            for key, value in data.iteritems():
                if key in errors.keys():
                    form_data[key] = (value, errors[key])
                else:
                    form_data[key] = (value, '')

            context['form_data'] = form_data
            return render(request, 'rcs/inspector/flujo_solicitud/mecanica_solicitud.html',context)


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

    def tiene_accesorios(self,id_sol):
        solicitud = SolicitudInspeccion.objects.get(id=id_sol)
        vehiculo = Vehiculo.objects.get(id=solicitud.fk_vehiculo.id)
        return vehiculo.accesorios_vehiculo.all().exists()

    def get_context(self, request, data):
        id_sol = data['sol_id'] if 'sol_id' in data else request.session['sol_id']
        solicitud = SolicitudInspeccion.objects.get(id=id_sol)
        vehiculo = Vehiculo.objects.get(id=solicitud.fk_vehiculo.id)

        if vehiculo.accesorios_vehiculo.all().exists():
            accesorios = vehiculo.accesorios_vehiculo.all().order_by('id')
        else:
            accesorios = AccesoriosBase.objects.all().order_by('id')
        
        estados_vehiculo = EstadoVehiculo.objects.all()
        context = {
            'accesorios': accesorios,
            'estados_vehiculo': estados_vehiculo,
            'vehiculo': vehiculo,
            'solicitud': solicitud,
            'nombre': data.user.nombre if 'user' in data else "",
            'username': data.user.username if 'user' in data else "",

        }
        
        return context

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios

        for key in data:
            value = data.get(key, None)
            if 'observacion_OTRO' in key:
                codigo = key.split('_',1)[1] 
                if data['radio_'+codigo].strip() !="" and data['observacion_'+codigo].strip()=="":
                    errors[key] = 'El campo no debe estar vacío'
                    
            if not value.strip() and not 'observacion' in key and not 'OTRO' in key :
                errors[key] = 'El campo no debe estar vacío'

            if 'observacion_RADIO_ANT' in key:
                    if not value.strip():
                        errors[key] = 'El campo no debe estar vacío'

        return errors

    def get(self, request, *args, **kwargs):
        data = request.GET

        context = self.get_context(request,data)
        
        #obtener datos que requieran ser pre-cargados en el formulario (ejemplo: editar registro) y guardarlos en form_data
        form_data = {}

        #"form_data" representa un diccionario cuyas claves son los nombres de los inputs html del formulario y sus valores 
        #son tuplas donde almacenan los valores y los errores de los inputs respectivamente

        context['nombre'] = request.user.nombre
        context['username'] = request.user.username
        context['form_data'] = form_data


        return render(request, 'rcs/inspector/flujo_solicitud/accesorios_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}
        observacion = "observacion_"
        radio = "radio_"
        solicitud = SolicitudInspeccion.objects.get(id= data['id_solicitud'])
        vehiculo = solicitud.fk_vehiculo

        if self.tiene_accesorios(solicitud.id):
            accesorios = vehiculo.accesorios_vehiculo.all()
        else:
            accesorios = AccesoriosBase.objects.all()

        mutable = request.POST._mutable
        request.POST._mutable = True
        for accesorio in accesorios:
            codigo = radio+accesorio.codigo
            if not codigo in data:
                data[codigo] = ""

        request.POST._mutable = mutable
        errors = self.validate(data)

        # accesorios 
        if not errors:
            solicitud = SolicitudInspeccion.objects.get(id= data['id_solicitud'])
            vehiculo = solicitud.fk_vehiculo
            with transaction.atomic():
                tenia_accesorios = self.tiene_accesorios(solicitud.id)
                vehiculo.accesorios_vehiculo.clear()
                for accesorio in accesorios:

                    if tenia_accesorios:
                        codigo_nuevo = accesorio.codigo
                    else:
                        codigo_nuevo = accesorio.codigo+'_'+str(vehiculo.id)
                    # mec_sol
                    if data[radio+accesorio.codigo].strip() != "":
                        accesorio_existe = True if data[radio+accesorio.codigo] == 'true' else False
                        
                        if AccesoriosVehiculo.objects.filter(codigo=codigo_nuevo).exists():
                            accesorio_ = AccesoriosVehiculo.objects.get(codigo=codigo_nuevo)
                            accesorio_.observacion = data[observacion+accesorio.codigo]
                            accesorio_.existe = accesorio_existe
                        else:    
                            accesorio_ = AccesoriosVehiculo(codigo=codigo_nuevo, observacion = data[observacion+accesorio.codigo], existe= accesorio_existe,accesorio=accesorio.accesorio)
                        
                        accesorio_.save()
                        ##Agregando accesorio a many to many field de vehiculo
                        vehiculo.accesorios_vehiculo.add(accesorio_)

                vehiculo.save()
            return redirect(reverse_lazy('detalles_vehiculo'))
        else:
            context = self.get_context(request,request)

            form_data = {}
            for key, value in data.iteritems():
                if key in errors.keys():
                    form_data[key] = (value, errors[key])
                else:
                    form_data[key] = (value, '')

            context['form_data'] = form_data
        return render(request, 'rcs/inspector/flujo_solicitud/accesorios_solicitud.html',context)


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

    def get_context(self,request, data):
        id_solicitud = data['sol_id'] if 'sol_id' in data else request.session['sol_id']

        solicitud = SolicitudInspeccion.objects.get(id=id_solicitud)
            
        vehiculo = Vehiculo.objects.get(id=solicitud.fk_vehiculo.id)
        # cantidad_detalles = range(1,data['cantidad_detalles']) if 'cantidad_detalles' in data else range(1,2)
        detalles_vehiculo = vehiculo.detalles_datos.all()
        estados_vehiculo = EstadoVehiculo.objects.all()
        context = {
            'estados_vehiculo': estados_vehiculo,
            'vehiculo': vehiculo,
            'solicitud': solicitud,
            'detalles_vehiculo': detalles_vehiculo,
            'nombre': data.user.nombre if 'user' in data else "",
            'username': data.user.username if 'user' in data else "",
            # 'cantidad': cantidad_detalles,
        }
        
        return context

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios

        for key in data:
            value = data.get(key, None)
                    
            if not value.strip():
                errors[key] = 'El campo no debe estar vacío'

        return errors

    def get(self, request, *args, **kwargs):
        data = request.GET

        # cantidad_detalles = range(1,data['cantidad_detalles']+1) if 'cantidad_detalles' in data else range(1,3)
        # context = self.get_context(data,cantidad_detalles)
        context = self.get_context(request,data)
        
        #obtener datos que requieran ser pre-cargados en el formulario (ejemplo: editar registro) y guardarlos en form_data
        form_data = {}

        #"form_data" representa un diccionario cuyas claves son los nombres de los inputs html del formulario y sus valores 
        #son tuplas donde almacenan los valores y los errores de los inputs respectivamente

        context['nombre'] = request.user.nombre
        # context['cantidad'] = cantidad_detalles
        context['username'] = request.user.username
        context['form_data'] = form_data

        return render(request, 'rcs/inspector/flujo_solicitud/detalles_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}
        # cantidad_detalles = data['cantidad_detalles']
        # errors = self.validate(data)
        numero_agregados = data['contador_agregados']
        solicitud = SolicitudInspeccion.objects.get(id= data['id_solicitud'])
        vehiculo = solicitud.fk_vehiculo

        with transaction.atomic():
            detalles_vehiculo = vehiculo.detalles_datos.all()
            for detalle in detalles_vehiculo:
                det = DetallesDatos.objects.get(codigo = detalle.codigo)
                det.delete()
            vehiculo.detalles_datos.clear()
            for i in xrange(int(numero_agregados)+1):
                if "pieza_"+str(i) in data:
                    detalles = DetallesDatos()
                    pieza = data['pieza_'+str(i)]
                    tipo_dano  = data['dano_'+str(i)]
                    costo_aproximado = data['costo_'+str(i)]
                    codigo = data['codigo_'+str(i)]
                    detalles.pieza = pieza
                    detalles.tipo_dano = tipo_dano
                    detalles.costo_aproximado = costo_aproximado
                    detalles.codigo = codigo
                    detalles.save()
                    vehiculo.detalles_datos.add(detalles)

                # mec_sol
                    # accesorio.save()
                ##Agregando accesorio a many to many field de vehiculo
                # vehiculo.accesorios_vehiculo.add(accesorio)
            vehiculo.save()

        return redirect(reverse_lazy('documentos_vehiculo'))


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


    def tiene_documentos(self,id_sol):
        solicitud = SolicitudInspeccion.objects.get(id=id_sol)
        vehiculo = Vehiculo.objects.get(id=solicitud.fk_vehiculo.id)
        return vehiculo.documentos_presentados.all().exists()

    def get_context(self,request, data):
        id_solicitud = data['sol_id'] if 'sol_id' in data else request.session['sol_id']

        solicitud = SolicitudInspeccion.objects.get(id=id_solicitud)
        vehiculo = Vehiculo.objects.get(id=solicitud.fk_vehiculo.id)

        if vehiculo.documentos_presentados.all().exists():
            documentos = vehiculo.documentos_presentados.all().order_by('id')
        else:
            documentos = DocumentosPresentadosBase.objects.all().order_by('id')

        context = {
            'documentos': documentos,
            'vehiculo': vehiculo,
            'solicitud': solicitud,
            'nombre': data.user.nombre if 'user' in data else "",
            'username': data.user.username if 'user' in data else "",

        }
        
        return context

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios

        for key in data:
            value = data.get(key, None)
                    
            if not value.strip():
                errors[key] = 'El campo no debe estar vacío'

        return errors

    def get(self, request, *args, **kwargs):
        
        data = request.GET

        context = self.get_context(request,data)
        
        #obtener datos que requieran ser pre-cargados en el formulario (ejemplo: editar registro) y guardarlos en form_data
        form_data = {}

        #"form_data" representa un diccionario cuyas claves son los nombres de los inputs html del formulario y sus valores 
        #son tuplas donde almacenan los valores y los errores de los inputs respectivamente

        context['nombre'] = request.user.nombre
        context['username'] = request.user.username
        context['form_data'] = form_data


        return render(request, 'rcs/inspector/flujo_solicitud/documentos_solicitud.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}

        radio = "radio_"
        # accesorios = AccesoriosVehiculo.objects.all()
        solicitud = SolicitudInspeccion.objects.get(id= data['id_solicitud'])
        vehiculo = solicitud.fk_vehiculo


        if self.tiene_documentos(solicitud.id):
            documentos = vehiculo.documentos_presentados.all()
        else:
            documentos = DocumentosPresentadosBase.objects.all()

        mutable = request.POST._mutable
        request.POST._mutable = True
        for documento in documentos:
            codigo = radio+documento.codigo
            if not codigo in data:
                data[codigo] = ""

        request.POST._mutable = mutable
        errors = self.validate(data)

        # documentos 
        if not errors:
            solicitud = SolicitudInspeccion.objects.get(id= data['id_solicitud'])
            vehiculo = solicitud.fk_vehiculo
            with transaction.atomic():
                tenia_documentos = self.tiene_documentos(solicitud.id)
                vehiculo.documentos_presentados.clear()

                for documento in documentos:
                    # mec_sol
                    if tenia_documentos:
                        codigo_nuevo = documento.codigo
                    else:
                        codigo_nuevo = documento.codigo+'_'+str(vehiculo.id)

                    documento_recibido = True if data[radio+documento.codigo] == 'true' else False
                    if DocumentosPresentados.objects.filter(codigo=codigo_nuevo).exists():
                            documento = DocumentosPresentados.objects.get(codigo=codigo_nuevo)
                            documento.recibido = documento_recibido
                    else:    
                        documento = DocumentosPresentados(codigo=codigo_nuevo, recibido= documento_recibido,nombre=documento.nombre)
                        

                    documento.save()
                    ##Agregando documento a many to many field de vehiculo
                    vehiculo.documentos_presentados.add(documento)
                vehiculo.save()
            return redirect(reverse_lazy('planilla_seguro_carro'))
        else:
            context = self.get_context(request,request)

            form_data = {}
            for key, value in data.iteritems():
                if key in errors.keys():
                    form_data[key] = (value, errors[key])
                else:
                    form_data[key] = (value, '')

            context['form_data'] = form_data
        return render(request, 'rcs/inspector/flujo_solicitud/documentos_solicitud.html',context)

## Fin Views de Flujo




class BandejaTickets(View):
    """
    BandejaTickets
    -------------------------------------------
    Bandeja donde se muestran las solicitudes de inspeccion realizadas
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(BandejaTickets, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        context['nombre'] = request.user.nombre
        context['username'] = request.user.username

        return render(request, 'rcs/taquilla/bandeja_taquilla.html',context)


class EditarTicket(View):
    """
    EditarTicket 
    -------------------------------------------
    Gestiona las solicitudes en estatus abierta, paso 1 datos del vehiculo
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(EditarTicket, self).dispatch(request, *args, **kwargs)


    def get_context(self, data):
        motivo = MotivoSolicitud.objects.all()
        # import pudb; pu.db
        # data = request.GET
        id_sol = secure_value_decode(data.GET['sol_id'])
        solicitud = SolicitudInspeccion.objects.get(id= id_sol)
        context = {
            'motivos_de_visita': motivo,
            'nombre': data.user.nombre,
            'username': data.user.username,
            'solicitud': solicitud,
            'trajo_vehiculo': solicitud.fk_trajo_vehiculo,
            'titular_vehiculo': solicitud.fk_titular_vehiculo,
            'existe_trajo_vehiculo': False if solicitud.fk_trajo_vehiculo== None else True
        }
        
        return context

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios
        for key in data:
            value = data.get(key, None)
            if 'radio_titular' in data:
                if data['radio_titular'] == 'false':
                    if not value.strip():
                        errors[key] = 'El campo no debe estar vacío'
                else:
                    if not 'trajo' in key:
                        if not value.strip():
                            errors[key] = 'El campo no debe estar vacío'
            else:
                if not value.strip():
                    errors[key] = 'El campo no debe estar vacío'
        return errors

    def get(self, request, *args, **kwargs):
        data = {}
        context = self.get_context(request)
        
        #obtener datos que requieran ser pre-cargados en el formulario (ejemplo: editar registro) y guardarlos en form_data
        form_data = {}

        #"form_data" representa un diccionario cuyas claves son los nombres de los inputs html del formulario y sus valores 
        #son tuplas donde almacenan los valores y los errores de los inputs respectivamente
        import pudb; pu.db
        # mas_una_solictud_titular
        # mas_una_solictud_trajo
        # mas_una_solictud_placa
        context['form_data'] = form_data

        return render(request, 'rcs/taquilla/editar_ticket.html',context)

    def post(self,request,*args,**kwargs):


        data = request.POST
        response = {}

        errors = self.validate(data)

        if not errors:

            #procesar y guardar data del formulario en BD
            solicitud = SolicitudInspeccion()
            vehiculo = Vehiculo()
            titular_vehiculo = TitularVehiculo()
            trajo_vehiculo = TrajoVehiculo()


            nombre_titular = data['nombre_titular']
            apellido_titular = data['apellido_titular']
            cedula_titular = data['cedula_titular']
            telefono_titular = data['telefono_titular']
            placa = data['placa']
            motivo_visita = data['motivo_visita']
            nombre_trajo_vehiculo = data['nombre_trajo_vehiculo']
            apellido_trajo_vehiculo = data['apellido_trajo_vehiculo']
            cedula_trajo_vehiculo = data['cedula_trajo_vehiculo']
            parentesco_trajo_vehiculo = data['parentesco_trajo_vehiculo']
            if SolicitudInspeccion.objects.filter(Q(fk_vehiculo__placa=placa),Q(fk_titular_vehiculo__cedula=cedula_titular),~Q(fk_estado_solicitud__codigo="CERRADA")).exists():
                respuesta = {}
                respuesta['results'] = "error"
                respuesta['mensaje'] = "No se puede crear otra solicitud para el mismo carro mientras una esté en proceso."
                return HttpResponse(json.dumps(respuesta), content_type="application/json")

            with transaction.atomic():
                if TitularVehiculo.objects.filter(cedula=cedula_titular).exists():
                    titular_vehiculo=TitularVehiculo.objects.get(cedula=cedula_titular)
                else:
                    titular_vehiculo.nombre = nombre_titular
                    titular_vehiculo.apellido = apellido_titular
                    titular_vehiculo.cedula = cedula_titular
                    titular_vehiculo.telefono = telefono_titular
                    titular_vehiculo.save()

                if data['nombre_trajo_vehiculo'].strip() != "":
                    
                    if TrajoVehiculo.objects.filter(cedula=cedula_trajo_vehiculo).exists():
                        trajo_vehiculo= TrajoVehiculo.objects.get(cedula=cedula_trajo_vehiculo)
                    else:
                        trajo_vehiculo.nombre =  nombre_trajo_vehiculo
                        trajo_vehiculo.apellido = apellido_trajo_vehiculo
                        trajo_vehiculo.cedula = cedula_trajo_vehiculo
                        trajo_vehiculo.parentesco = parentesco_trajo_vehiculo
                        trajo_vehiculo.save()
                    # vehiculo.fk_trajo_vehiculo = trajo_vehiculo
                    solicitud.fk_trajo_vehiculo = trajo_vehiculo
                    


                vehiculo.placa = placa
                vehiculo.fk_titular_vehiculo = titular_vehiculo
                vehiculo.save()

                solicitud.fk_vehiculo = vehiculo
                solicitud.fk_titular_vehiculo = titular_vehiculo
                solicitud.fk_motivo_solicitud = MotivoSolicitud.objects.get(codigo = motivo_visita) 
                solicitud.save()

            respuesta={'results': 'success',}
            return HttpResponse(json.dumps(respuesta), content_type="application/json")
        else:
           
            response['errors'] = errors

            return HttpResponse(json.dumps(response), content_type = "application/json")


def cancela_ticket(request):
    """
    CancelarTicket 
    -------------------------------------------
    Cancela los tickets que esten abiertos
    """

    data = request.GET
    id_sol = secure_value_decode(str(data['sol_id']))
    solicitud = SolicitudInspeccion.objects.get(id=id_sol)

    with transaction.atomic():
        if not mas_una_solicitud_placa(solicitud.fk_vehiculo.placa):
            solicitud.fk_vehiculo.delete() 
        if not mas_una_solicitud_titular(solicitud.fk_titular_vehiculo):
            solicitud.fk_titular_vehiculo.delete()

        if solicitud.fk_trajo_vehiculo!=None:
            if not mas_una_solicitud_trajo(solicitud.fk_trajo_vehiculo):
                solicitud.fk_trajo_vehiculo.delete()
        solicitud.delete()


    respuesta={'results': 'success',}
    return HttpResponse(json.dumps(respuesta), content_type="application/json")
