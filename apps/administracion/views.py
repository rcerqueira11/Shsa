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
        context = {

        }

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
        context['tipos_de_usuario'] = TipoUsuario.objects.all()


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

    def get(self, request, *args, **kwargs):
        context = {

        }

    	return render(request, 'administracion/editar_titular.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}


        #if data: 
		#	response['Result'] = 'success'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        #else:
        #    response['Result'] = 'error'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")


        return redirect(reverse_lazy('dashboard'))
        
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

    def get(self, request, *args, **kwargs):
        context = {

        }

    	return render(request, 'administracion/editar_trajo_vehiculo.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}


        #if data: 
		#	response['Result'] = 'success'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        #else:
        #    response['Result'] = 'error'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")


        return redirect(reverse_lazy('dashboard'))


class EditarUsuario(View):
    """
    EditarUsuario
    -------------------------------------------
    Edita quien trajoel vehiculo vehiculo
    si no tienen ninguna solicitud ya en cerrada
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return redirect(reverse_lazy('login'))
    	return super(EditarUsuario, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {

        }

    	return render(request, 'administracion/editar_trajo_vehiculo.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        response = {}


        #if data: 
		#	response['Result'] = 'success'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")
        #else:
        #    response['Result'] = 'error'
        #    response['msj'] = ''
        #    return HttpResponse(json.dumps(response), content_type = "application/json")


        return redirect(reverse_lazy('dashboard'))
