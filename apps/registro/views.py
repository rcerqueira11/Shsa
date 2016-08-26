# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, hashers
from django.contrib import messages
from django.views.generic import View, FormView,TemplateView,DeleteView
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings

from apps.wkhtmltopdf.views import PDFTemplateResponse
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
        # if request.user.username == '' or request.user.is_authenticated() == False:
        #     return redirect(reverse_lazy('registro_logout'))
        # else:
    	return super(Login, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
    	# print "Hello World"
        context={}
        if settings.SECURE_SSL_REDIRECT == True:
                media_url = 'https://'
        else:
            media_url = 'http://'
        data={}
        media_url = media_url+request.META['HTTP_HOST']

        context['http_host']= media_url
        response = PDFTemplateResponse(request=request,
                                   template='index.html',
                                   filename="planilla_registro_carro.pdf",
                                   context= context,
                                   show_content_in_browser=True,
                                   cmd_options={'margin-top': 10,'page-size': 'A4','quiet': True},
                                   # current_app= rcs,
                                   header_template='hf.html', 
                                   footer_template='hf.html',
                                   )
        return response
    	# return render(request, 'index.html',context)


class Logout(View):
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated():
        #     mensaje = u'¡Ha cerrado sesión correctamente!'
        #     messages.info(self.request, mensaje)
        return redirect(reverse_lazy('registro_login'))
