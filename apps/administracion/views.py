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
from apps.registro.views import create_new_password
from utils.HelpMethods.aes_cipher import encode as secure_value_encode
from utils.HelpMethods.aes_cipher import decode as secure_value_decode
from utils.HelpMethods.helpers import enviar_correo
import json
import random
import string
import logging
import datetime
import os
import sys

from os import path
# Create your views here.

def iguales_(value1, value2):
    val1 = str(value1)
    val2 = str(value2)
    return val1 == val2

class BandejaTitulares(View):
    """
    BandejaTitulares
    -------------------------------------------
    bandeja donde se muestran los titulares de vehiculos para que puedan ser editados
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(BandejaTitulares, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        context = {}
        context['nombre'] = request.user.nombre
        context['username'] = request.user.username

        return render(request, 'administracion/bandeja_titulares.html',context)


class BandejaTrajoVehiculo(View):
    """
    BandejaTrajoVehiculo
    -------------------------------------------
    bandeja donde se muestran los que trajeron los vehiculos para que puedan ser editados
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(BandejaTrajoVehiculo, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        context['nombre'] = request.user.nombre
        context['username'] = request.user.username

        return render(request, 'administracion/bandeja_trajo_vehiculo.html',context)


class BandejaUsuarios(View):
    """
    BandejaUsuarios
    -------------------------------------------
    bandeja donde se muestran los usuarios de la aplicacion para que puedan ser editados
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(BandejaUsuarios, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {

        }
        context = {}
        context['nombre'] = request.user.nombre
        context['username'] = request.user.username
        context['tipos_de_usuario'] = TipoUsuario.objects.all().exclude(codigo="ADM").order_by('id')


        return render(request, 'administracion/bandeja_usuarios.html',context)




class EditarTitular(View):
    """
    EditarTitular
    -------------------------------------------
    Edita titular de un vehiculo
    si no tienen ninguna solicitud ya en cerrada
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(EditarTitular, self).dispatch(request, *args, **kwargs)

    def get_context(self, data):
        id_titular = secure_value_decode(data.GET['titular_id'])
        titular_vehiculo = TitularVehiculo.objects.get(id= id_titular) 
        context = {
            'nombre': data.user.nombre if 'user' in data else "",
            'username': data.user.username if 'user' in data else "",
            'titular_vehiculo': titular_vehiculo,
        }
        
        
        return context

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios
        for key in data:
            value = data.get(key, None)
            if "cedula" in key:
                cant_usu = TitularVehiculo.objects.filter(cedula = value)
                if len(cant_usu) > 0:
                    if str(cant_usu[0].id) != str(data['id_titular_vehiculo']):
                        errors[key] = 'Esta cedula la posee otra persona.'
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
        context['nombre'] = request.user.nombre
        context['username'] = request.user.username
        context['form_data'] = form_data


        return render(request, 'administracion/editar_titular.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}

        errors = self.validate(data)

        if not errors:
            cedula_nuevo = data['cedula_titular']
            nombre_nuevo = data['nombre_titular']
            apellido_nuevo = data['apellido_titular']
            telefono_nuevo = data['telefono_titular']
            titular_vehiculo_editar =  TitularVehiculo.objects.get(id= data['id_titular_vehiculo'])

            if (titular_vehiculo_editar.nombre ==  nombre_nuevo) and (titular_vehiculo_editar.apellido ==  apellido_nuevo) and (titular_vehiculo_editar.cedula ==  cedula_nuevo) and (titular_vehiculo_editar.telefono ==  telefono_nuevo):
                response={'results':'data_igual', }
                response['mensaje'] = "No hay nada nuevo que guardar."
                return HttpResponse(json.dumps(response), content_type = "application/json")
            else:

                titular_vehiculo_editar.nombre =  nombre_nuevo
                titular_vehiculo_editar.apellido =  apellido_nuevo
                titular_vehiculo_editar.cedula =  cedula_nuevo
                titular_vehiculo_editar.telefono =  telefono_nuevo
                with transaction.atomic():
                    titular_vehiculo_editar.save()

                response={'results':'success', }
                return HttpResponse(json.dumps(response), content_type = "application/json")
        else:
                   
            response['errors'] = errors
            response['mensaje'] = "Errores en la edición favor verificar los datos suministrados."
            return HttpResponse(json.dumps(response), content_type = "application/json")

class EditarTrajoVehiculo(View):
    """
    EditarTrajoVehiculo
    -------------------------------------------
    Edita quien trajoel vehiculo vehiculo
    si no tienen ninguna solicitud ya en cerrada
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(EditarTrajoVehiculo, self).dispatch(request, *args, **kwargs)

    def get_context(self, data):
        id_trajo_vehiculo = secure_value_decode(data.GET['trajo_vehiculo_id'])
        trajo_vehiculo = TrajoVehiculo.objects.get(id= id_trajo_vehiculo) 
        context = {
            'nombre': data.user.nombre if 'user' in data else "",
            'username': data.user.username if 'user' in data else "",
            'trajo_vehiculo': trajo_vehiculo,
        }
        
        
        return context

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios

        for key in data:
            value = data.get(key, None)
            if "cedula" in key:
                cant_usu = TrajoVehiculo.objects.filter(cedula = value)
                if len(cant_usu) > 0:
                    if str(cant_usu[0].id) != str(data['id_trajo_vehiculo']):
                        errors[key] = 'Esta cedula la posee otra persona.'
                    
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
        context['nombre'] = request.user.nombre
        context['username'] = request.user.username
        context['form_data'] = form_data


        return render(request, 'administracion/editar_trajo_vehiculo.html',context)

    def post(self,request,*args,**kwargs):

        data = request.POST
        response = {}

        errors = self.validate(data)
        if not errors:
            nombre_nuevo = data['nombre_trajo_vehiculo']
            apellido_nuevo = data['apellido_trajo_vehiculo']
            cedula_nuevo = data['cedula_trajo_vehiculo']
            parentesco_nuevo = data['parentesco_trajo_vehiculo']
            trajo_vehiculo_editar =  TrajoVehiculo.objects.get(id= data['id_trajo_vehiculo'])

            if (trajo_vehiculo_editar.nombre ==  nombre_nuevo) and (trajo_vehiculo_editar.apellido ==  apellido_nuevo) and (trajo_vehiculo_editar.cedula ==  cedula_nuevo) and (trajo_vehiculo_editar.parentesco ==  parentesco_nuevo):
                response={'results':'data_igual', }
                response['mensaje'] = "No hay nada nuevo que guardar."
                return HttpResponse(json.dumps(response), content_type = "application/json")
            else:

                trajo_vehiculo_editar.nombre =  nombre_nuevo
                trajo_vehiculo_editar.apellido =  apellido_nuevo
                trajo_vehiculo_editar.cedula =  cedula_nuevo
                trajo_vehiculo_editar.parentesco =  parentesco_nuevo
                with transaction.atomic():
                    trajo_vehiculo_editar.save()

                response={'results':'success', }
                return HttpResponse(json.dumps(response), content_type = "application/json")
        else:
                   
            response['errors'] = errors
            response['mensaje'] = "Errores en la edición favor verificar los datos suministrados."
            return HttpResponse(json.dumps(response), content_type = "application/json")


class EditarUsuario(View):
    """
    EditarUsuario
    -------------------------------------------
    Edita los usuarios registrados que utilizan el sistema
    inspectores y taquilleros
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(EditarUsuario, self).dispatch(request, *args, **kwargs)

    def get_context(self, data):
        id_usuario = secure_value_decode(data.GET['usuario_id'])
        usuario = Usuario.objects.get(id= id_usuario) 
        tipo_usuario = TipoUsuario.objects.all().exclude(codigo="ADM").order_by('nombre')
        context = {
            'nombre': data.user.nombre if 'user' in data else "",
            'username': data.user.username if 'user' in data else "",
            'usuario': usuario,
            'tipos_de_usuario': tipo_usuario,
        }
        
        
        return context

    def reset_user(self,request,usuario_id):

        usuario = Usuario.objects.get(id=usuario_id)
        correo = usuario.correo_electronico
        clave_nueva = create_new_password()
        usuario.set_password(clave_nueva)
    
        correoTemplate = get_template('correo/usuario_recuperar_clave.html')
        context_email = Context({
                'usuario': usuario,
                'clave': clave_nueva,
            })
        contenidoHtmlCorreo = correoTemplate.render(context_email)
        
        email_enviado = enviar_correo(asunto="Recuperar Cuenta",contenido=contenidoHtmlCorreo, correo=[correo] ,custom_filename='seguros_horizontes_logo.png')

        if not email_enviado:
            respuesta['Result'] = 'error'
            respuesta['ERROR_CODE'] = 'NO_MAIL_SEND'
            respuesta['mensaje'] = 'El correo no pudo ser enviado, favor intentar mas tarde.'
            return HttpResponse(json.dumps(respuesta), content_type = "application/json")
        
        usuario.save()
        respuesta = {}
        respuesta['Result'] = 'success'
        return HttpResponse(json.dumps(respuesta), content_type = "application/json")

    def validate(self, data):
        errors = {}

        #obtener errores y guardarlos en el diccionario "errors" en donde los "key" son los nombre de los inputs html
        #Ejemplo: validar que los campos no estén vacios
        for key in data:
            value = data.get(key, None)
            if 'correo' in key:
                if not Usuario.objects.filter(~Q(id=data['id_usuario']),Q(correo_electronico=data['correo_electronico'])).exists():
                    if str(data['correo_electronico']) != str(data['email2']):
                        errors[key] = 'Este correo no es igual al de confirmación'
                else:
                    errors[key] = 'Este correo ya se encuentra registrado por otro usuario.'
            if 'email' in key:
                if not Usuario.objects.filter(~Q(id=data['id_usuario']),Q(correo_electronico=data['email2'])).exists():
                    if str(data['correo_electronico']) != str(data['email2']):
                        errors[key] = 'El correo de confirmación no es igual al correo principal'
                else:
                    errors[key] = 'Este correo ya se encuentra registrado por otro usuario.'

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
        context['nombre'] = request.user.nombre
        context['username'] = request.user.username
        context['form_data'] = form_data

        return render(request, 'administracion/editar_usuarios.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}
        errors = self.validate(data)

        if not errors:
            usuario = Usuario.objects.get(id=data['id_usuario'])
            correo_nuevo = data['correo_electronico']
            nombre_nuevo = data['nombre']
            apellido_nuevo = data['apellido']
            tipo_usuario_nuevo = TipoUsuario.objects.get(codigo=data['tipo_usuario'])

            corre_iguales = iguales_(correo_nuevo,usuario.correo_electronico)
            nombre_iguales = iguales_(nombre_nuevo,usuario.nombre)
            apellido_iguales = iguales_(apellido_nuevo, usuario.apellido)
            tipo_usuario_iguales = iguales_(data['tipo_usuario'],usuario.fk_tipo_usuario.codigo)


            if corre_iguales and nombre_iguales and apellido_iguales and tipo_usuario_iguales and (not 'reiniciar' in data ):
                response={'results':'data_igual', }
                response['mensaje'] = "No hay nada nuevo que guardar."
                return HttpResponse(json.dumps(response), content_type = "application/json")
            usuario.nombre = nombre_nuevo
            usuario.apellido = apellido_nuevo
            usuario.correo_electronico = correo_nuevo
            usuario.fk_tipo_usuario = tipo_usuario_nuevo

            with transaction.atomic():
                usuario.save()

                if 'reiniciar' in data:
                    # pass
                    self.reset_user(request,usuario.id)

            response={'results': 'success',}
            return HttpResponse(json.dumps(response), content_type = "application/json")
        else:
                   
            response['errors'] = errors
            return HttpResponse(json.dumps(response), content_type = "application/json")
