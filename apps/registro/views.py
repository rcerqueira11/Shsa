# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, hashers
from django.db import transaction
from django.contrib import messages
from django.core.mail import EmailMessage
from email.MIMEImage import MIMEImage
from django.views.generic import View, FormView,TemplateView,DeleteView
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from settings.settings import BASE_DIR, STATIC_URL
from django.template.loader import get_template
from django.template import Context

# from utils import *
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
from os import path

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
        return redirect(reverse_lazy('login'))


class Login(View):
    """
    Login
    -------------------------------------------
    EN ESTA VISTA SE LOGUEA.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse_lazy('dashboard'))
    	return super(Login, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated():

       
    	return render(request, 'index.html')

    def post(self,request,*args,**kwargs):
        
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
            # return redirect(reverse_lazy('login'))
                # return render(request, 'rcs/dashboard.html',context)
                return redirect(reverse_lazy('dashboard'))
            else:
                return redirect(reverse_lazy('login'))

        else:
            mensaje_error= 'El usuario o contraseña es invalido.'
            errors = {
                'mensaje_error': mensaje_error,
            }
            return render(request, 'index.html', errors)

        # return redirect(reverse_lazy(''))


class Logout(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            mensaje = u'¡Ha cerrado sesión correctamente!'
            messages.info(self.request, mensaje)
            logout(request)
        return redirect(reverse_lazy('login'))


class RegistroUsuario(View):
    def dispatch(self, request, *args, **kwargs):
        # if request.user.username == '' or request.user.is_authenticated() == False:
        #     return redirect(reverse_lazy('logout'))
        # else:
        return super(RegistroUsuario, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        tipo_usuario = TipoUsuario.objects.all().exclud(codigo="ADM").order_by('nombre')

        context = {
            'tipos_de_usuario': tipo_usuario,
        }
        # if request.user.is_authenticated():
        #     mensaje = u'¡Ha cerrado sesión correctamente!'
        #     messages.info(self.request, mensaje)

        return render(request, 'registro/registro.html',context)

        # return redirect(reverse_lazy('login'))
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

                correoTemplate = get_template('correo/usuario_registrado.html')
                context_email = Context({
                        'usuario': usuario_nuevo,
                        'clave': data['password'],
                    })
                contenidoHtmlCorreo = correoTemplate.render(context_email)

                email_enviado = enviar_correo(asunto="Registro de Usuario",contenido=contenidoHtmlCorreo, correo=[email] ,custom_filename='seguros_horizontes_logo.png')


                usuario_nuevo.save()
                login(request,usuario_nuevo)
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

    def post(self, request, *args, **kwargs):
        data = request.POST
        respuesta = {}
        correo =  data['email']
        cedula = data['cedula']


        if Usuario.objects.filter(correo_electronico = correo, cedula=cedula).exists():
            usuario = Usuario.objects.get(correo_electronico = correo, cedula=cedula)
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

        else:
            respuesta['Result'] = 'error'
            respuesta['ERROR_CODE'] = 'DATOS_INVALIDOS'
            respuesta['mensaje'] = 'El correo o la cedula esta incorrecto, verifique los datos y vuelva a intentar.'
            return HttpResponse(json.dumps(respuesta), content_type = "application/json")
# return HttpResponse(json.dumps(data), content_type = "application/json")

def create_new_password():
    serial=[random.choice(string.ascii_letters + string.digits) for n in xrange(8)]
    serial.append(random.choice(string.ascii_uppercase))
    clave=''.join(serial)

    return clave

def enviar_correo(asunto, contenido, correo, custom_filename, adjuntos=[]):
    if not type(custom_filename) is list:
        custom_filename = [custom_filename]

    try:
        msg = EmailMessage(asunto, contenido, to=correo)
        msg.content_subtype = "html"
        # msg.attach_alternative(contenido, "text/html")
        # msg.mixed_subtype = 'related'

        for f in custom_filename:
            fp = open(path.join(BASE_DIR, 'static', 'img', f), 'rb')
            msg_img = MIMEImage(fp.read())
            fp.close()
            msg_img.add_header('Content-ID', '<{}>'.format(f))
            msg.attach(msg_img)

        if adjuntos:
            for ad in adjuntos:
                try:
                    msg.attach_file(ad)
                except Exception as e:
                    msg.attach_file(ad[1:])

        msg.send()
        # if not es_firma:
        #     try:
        #         enviado = msg.send()
        #         if enviado < 1:
        #             from utils.HelpMethods.pagos_util import guardar_correo
        #             guardar_correo(mail=msg, error='NO_ENVIADO')
        #     except Exception as e:
        #         from utils.HelpMethods.pagos_util import guardar_correo
        #         guardar_correo(mail=msg, error=repr(e))
        # else:
        #     from utils.HelpMethods.pagos_util import guardar_correo
        #     guardar_correo(mail=msg, error='GUARDADO_PREVENTIVO_FIRMA')

    except Exception as e:
        print '=======>Error al enviar correo<=========', e
        # raise e
        return False
    return True


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


class EditarCuenta(View):
    """
    EditarCuenta
    -------------------------------------------
    Este views es para editar la informacion del usuario solo email y contrase;a

    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
        return super(EditarCuenta, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        context = {
            'username': request.user.username,
            'usuario': request.user,

        }

        return render(request, 'registro/editar_usuario.html',context)

    def post(self,request,*args,**kwargs):
        #Convertir todo a minuscula y quitar los espacios en blanco
        mutable = request.POST._mutable
        request.POST._mutable = True
       
        if request.POST.get('correo_electronico') != None:
            request.POST['correo_electronico']= request.POST['correo_electronico'].lower().strip()

        request.POST._mutable = mutable
        #Fin convertir todo a minuscula y quitar los espacios en blanco

        data = request.POST
        response = {}

        usuario_existe = Usuario.objects.filter(id = request.user.id).exists()

        if not usuario_existe:
            response['Result'] = 'error'
            response['msj'] = ''
            return HttpResponse(json.dumps(response), content_type = "application/json")

        ### Validando Antiguo usuario y ver que se esta modificando
        usuario_viejo = Usuario.objects.get(id=request.user.id)
        cambiando_correo = True if not usuario_viejo.correo_electronico == data['correo_electronico'] and data['correo_electronico'] != "" else False
        cambiando_password = True if not data['password'] == "" else False

        if Usuario.objects.filter(correo_electronico = data['correo_electronico']).exists():
            data['Result'] = 'ERROR_CORREO'
            data['error'] = '<p class="small_error_letter"> El correo de usuario ya se encuentra registrado. Por favor intente con otro correo <i class="fa fa-times-circle-o fa-lg"></i> </p>'
            return HttpResponse(json.dumps(data), content_type = "application/json")


        ### Validando email
        email = data['correo_electronico']
        existe_correo =Usuario.objects.filter(correo_electronico = email).exists()
        email_valido = validate_email(email) if email != "" else True


        ### Validando que los correos del form son iguales y que las contrase;as tambien son iguales
        email_son_iguales = son_iguales(data['correo_electronico'],data['email2'])
        passwords_son_iguales = son_iguales(data['password'],data['password2'])

        if((not existe_correo) and (email_valido) and email_son_iguales and passwords_son_iguales and usuario_existe):
            with transaction.atomic():

                usuario_modificado = Usuario.objects.get(id = request.user.id)
                if cambiando_correo:
                    usuario_modificado.correo_electronico = email
                if cambiando_password:
                    usuario_modificado.password = hashers.make_password(data['password'])

          
                correoTemplate = get_template('correo/usuario_modificado.html')
                context_email = Context({
                        'usuario': usuario_modificado,
                        'cambio_clave' : cambiando_password,
                        'clave': data['password'],
                    })
                contenidoHtmlCorreo = correoTemplate.render(context_email)

                email_enviado = enviar_correo(asunto="Actualización de datos de usuario",contenido=contenidoHtmlCorreo, correo=[usuario_modificado.correo_electronico] ,custom_filename='seguros_horizontes_logo.png')


                usuario_modificado.save()
                login(request, usuario_modificado) 
                response['Result'] = 'success'
                response['mensaje'] = 'El usuario ha sido modificado correctamente, se le envio información a su correo electronico.'
                return HttpResponse(json.dumps(response), content_type = "application/json")
        else:
            response['Result'] = 'error'
            response['mensaje'] = ''
            return HttpResponse(json.dumps(response), content_type = "application/json")


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
            model_obj = apps.get_model('registro', model_obj)
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

