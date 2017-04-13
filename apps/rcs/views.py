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
	# 	kwargs['max_length'] = 104
	# 	super(VerPlanillaSeguroCarro, self).__init__(*args, **kwargs)
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
		return super(Dashboard, self).dispatch(request, *args, **kwargs)

		
	def get(self, request, *args, **kwargs):
		nombre = request.user.nombre
		username = request.user.username
		context = {
			'nombre': nombre,
			'username': username,
		}
		# import pudb; pu.db
		return render(request, 'rcs/dashboard.html',context)
