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
from settings.settings import BASE_DIR, STATIC_URL
# from utils.HelpMethods.helpers import *
from validate_email import validate_email
from apps.wkhtmltopdf.views import PDFTemplateResponse
from apps.registro.models import *

# from django.contrib.auth.models import 
# from utils.HelpMethods.aes_cipher import encode as secure_value_encode
# from utils.HelpMethods.aes_cipher import decode as secure_value_decode
import json
import random
import string
import logging
import datetime
import os
import sys

# Create your views here.

def authenticate_2(username , password):
    
    if Usuario.objects.filter(username = username).exists():
        usuario = Usuario.objects.get(username = username)
        pwd_valid = hashers.check_password(password, usuario.password)

        if pwd_valid:
            return usuario

    return None   

def consulta_nombre_usuario(request):
    username = request.GET['username']
    data={}

    if Usuario.objects.filter(username = username).exists():
        data['Result'] = 'ocupado'
    else:
        data['Result'] = 'libre'

    return HttpResponse(json.dumps(data), content_type = "application/json")

def consulta_cedula_usuario(request):
    cedula = request.GET['cedula']
    data={}

    if Usuario.objects.filter(cedula = cedula).exists():
        data['Result'] = 'ocupado'
    else:
        data['Result'] = 'libre'

    return HttpResponse(json.dumps(data), content_type = "application/json")

def consulta_correo_usuario(request):
    email = request.GET['email']
    data={}

    if Usuario.objects.filter(correo_electronico = email).exists():
        data['Result'] = 'ocupado'
    else:
        data['Result'] = 'libre'

    return HttpResponse(json.dumps(data), content_type = "application/json")

def son_iguales(valor1, valor2):
    return True if str(valor1) == str(valor2) else False

class DetectarUsuario(View):
    def dispatch(self, request, *args, **kwargs):
        usuario = request.user

        # Verifica si el usuario esta autenticado y esta activo
        # if usuario.is_authenticated() and usuario.fk_status.codigo !="BLOQ":
        #     tipo_usuario = usuario.fk_tipo_usuario.codigo

        #     # Se reinician los intentos para iniciar sesión
        #     if usuario.intentos_login > 0:
        #         usuario.intentos_login = 0
        #         usuario.save()

        #     # Se reinician los intentos para recuparar contraseña
        #     if usuario.intentos_recuperar > 0:
        #         usuario.intentos_recuperar = 0
        #         usuario.save()

        #     # verifica si el usuario es un Usuario turístico
        #     if tipo_usuario == 'USUA':
        #         if usuario.fk_status == Status.objects.get(codigo="NOC") :
        #             return redirect('clave_usuario')
        #         return redirect('dashboard')

        #     # Verifica si el usuario es funcionario
        #     if tipo_usuario == 'FUNC':
        #         if usuario.fk_status == Status.objects.get(codigo="NOC") :
        #             return redirect('clave_funcionario')
        #         return redirect('dashboard')

        # else:
        return redirect(reverse_lazy('registro_login'))


class Login(View):
    """
    Login
    -------------------------------------------
    EN ESTA VISTA SE LOGUEA.
    """

    def dispatch(self, request, *args, **kwargs):
        # import pudb; pu.db
        # if request.user.username == '' or request.user.is_authenticated() == False:
        #     return redirect(reverse_lazy('logout'))
        # else:
        # import pudb; pu.db
        if request.user.is_authenticated():
            return redirect(reverse_lazy('dashboard'))
    	return super(Login, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated():

       
    	return render(request, 'index.html')

    def post(self,request,*args,**kwargs):
        # import pudb; pu.db
        username = request.POST['usuario']
        password = request.POST['password']
        user  = authenticate(username=username,password=password)
        if user is not None:
            
            if user.is_active:
                request.session['usuario'] = user.id #sets the exp. value of the session 
                login(request, user) #the user is now logged in
            # if request.user.is_authenticated():
            #     mensaje = u'¡Ha cerrado sesión correctamente!'
            #     messages.info(self.request, mensaje)
            # return redirect(reverse_lazy('registro_login'))
                # return render(request, 'rcs/dashboard.html',context)
                return redirect(reverse_lazy('dashboard'))
            else:
                return redirect(reverse_lazy('registro_login'))

        else :
            mensaje_error= 'ocurrio un error'
            errors = {
                'mensaje_error': mensaje_error,
            }
            return render(request, 'index.html')

        # return redirect(reverse_lazy(''))


class Logout(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            mensaje = u'¡Ha cerrado sesión correctamente!'
            messages.info(self.request, mensaje)
            logout(request)
        return redirect(reverse_lazy('registro_login'))





class RegistroUsuario(View):
    def dispatch(self, request, *args, **kwargs):
        # if request.user.username == '' or request.user.is_authenticated() == False:
        #     return redirect(reverse_lazy('logout'))
        # else:
        return super(RegistroUsuario, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        tipo_usuario = TipoUsuario.objects.all().order_by('nombre')

        context = {
            'tipos_de_usuario': tipo_usuario,
        }
        # if request.user.is_authenticated():
        #     mensaje = u'¡Ha cerrado sesión correctamente!'
        #     messages.info(self.request, mensaje)

        return render(request, 'registro/registro.html',context)

        # return redirect(reverse_lazy('registro_login'))
    def post(self, request, *args, **kwargs):

        #Convertir todo a minuscula y quitar los espacios en blanco
        mutable = request.POST._mutable
        request.POST._mutable = True

        if request.POST.get('username') != None:
            request.POST['username'] = request.POST['username'].strip()

        if request.POST.get('nombre') != None:
            request.POST['nombre'] = elimina_tildes(request.POST['nombre'].lower().strip())

        if request.POST.get('apellido') != None:
            request.POST['apellido'] = elimina_tildes(request.POST['apellido'].lower().strip())
        
        if request.POST.get('cedula') != None:
            request.POST['cedula'] = request.POST['cedula'].strip()
        
        if request.POST.get('correo_electronico') != None:
            request.POST['correo_electronico']= request.POST['correo_electronico'].lower().strip()

        request.POST._mutable = mutable
        #Fin convertir todo a minuscula y quitar los espacios en blanco


        data = request.POST
        # import pudb; pu.db
        response = {}

        if Usuario.objects.filter(username = data['username']).exists():
            data['Result'] = 'ERROR_USERNAME'
            data['error'] = '<p class="small_error_letter"> El nombre de usuario ya se encuentra registrado. Por favor intente con otro Nombre de Usuario <i class="fa fa-times-circle-o fa-lg"></i> </p>'
            return HttpResponse(json.dumps(data), content_type = "application/json")

        if Usuario.objects.filter(cedula = data['cedula']).exists():
            data['Result'] = 'ERROR_CEDULA'
            data['error'] = '<p class="small_error_letter"> La cedula ya se encuentra registrada. Por favor verificarla. <i class="fa fa-times-circle-o fa-lg"></i> </p>'
            return HttpResponse(json.dumps(data), content_type = "application/json")

        if Usuario.objects.filter(correo_electronico = data['correo_electronico']).exists():
            data['Result'] = 'ERROR_CORREO'
            data['error'] = '<p class="small_error_letter"> El correo de usuario ya se encuentra registrado. Por favor intente con otro correo <i class="fa fa-times-circle-o fa-lg"></i> </p>'
            return HttpResponse(json.dumps(data), content_type = "application/json")

        username = data['username']
        cedula = data['cedula']
        email = data['correo_electronico']

        existe_usuario =Usuario.objects.filter(username = username).exists()
        existe_cedula =Usuario.objects.filter(cedula = cedula).exists()
        existe_correo =Usuario.objects.filter(correo_electronico = email).exists()

        ### Validando email
        email_valido = validate_email(email)

        ### Validando que los correos del form son iguales y que las contrase;as tambien son iguales
        email_son_iguales = son_iguales(data['correo_electronico'],data['email2'])
        passwords_son_iguales = son_iguales(data['password'],data['password2'])


        ##### VALIDAR EL EMAIL

        if((not existe_usuario) and (not existe_correo) and (not existe_cedula) and (email_valido) and email_son_iguales and passwords_son_iguales):
            with transaction.atomic():

                usuario_nuevo = Usuario()
                usuario_nuevo.username = username
                usuario_nuevo.nombre = data['nombre']
                usuario_nuevo.apellido = data['apellido']
                usuario_nuevo.cedula = cedula
                usuario_nuevo.correo_electronico = email
                usuario_nuevo.password = hashers.make_password(data['password'])
                # usuario_nuevo.fk_tipo_usuario = TipoUsuario.objects.get(codigo = data['tipo_usuario'])
                usuario_nuevo.fk_tipo_usuario = TipoUsuario.objects.get(codigo = data['tipo_usuario'])

                ##Falta envia el mail
                usuario_nuevo.save()
                response['Result'] = 'success'
                response['msj'] = ''
                return HttpResponse(json.dumps(response), content_type = "application/json")
        # if
        else:
            response['Result'] = 'error'
            response['msj'] = ''
            return HttpResponse(json.dumps(response), content_type = "application/json")
        # if request.user.is_authenticated():
        #     mensaje = u'¡Ha cerrado sesión correctamente!'
        #     messages.info(self.request, mensaje)

        # return render(request, 'registro/registro.html',context)

        # response
        # return redirect(reverse_lazy('dashboard'))


class RestaurarCuenta(View):
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated():
        #     mensaje = u'¡Ha cerrado sesión correctamente!'
        #     messages.info(self.request, mensaje)
        return render (request, 'registro/restaurar_cuenta.html')

# return HttpResponse(json.dumps(data), content_type = "application/json")


###Va en utils

import unicodedata

def elimina_tildes(s):
    """
    Metodo para eliminar las tildes en cadenas de caracteres que se
    reciben por el parametro s.
    """
    #pre_s = ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
    #final = re.sub(ur'[_]|[^¿%?\w]+', u' ', pre_s)

    nkfd_form = unicodedata.normalize('NFKD', unicode(s))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


#### Fin va en utils
