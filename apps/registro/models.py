# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager
from utils.validate_files import ContentTypeRestrictedFileField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.HelpMethods.helpers import *
from django.apps import apps
from utils.HelpMethods.aes_cipher import encode as secure_value_encode
from utils.HelpMethods.aes_cipher import decode as secure_value_decode
from settings.settings import MEDIA_URL

# Create your models here.

class TipoUsuario(models.Model):
	nombre = models.CharField(max_length=255)
	descripcion = models.TextField(blank=True)
	codigo = models.CharField(max_length=255,unique=True)

	def __unicode__(self):
		return self.nombre

class Status(models.Model):
	nombre = models.CharField(max_length=255, blank=True)
	codigo = models.CharField(max_length=255, unique=True)
	descripcion = models.TextField(blank=True)

class Usuario(AbstractBaseUser):
	username = models.CharField(max_length=255,unique=True)
	fk_tipo_usuario = models.ForeignKey(TipoUsuario)
	#chequear esto
	fk_status = models.ForeignKey(Status, db_column='fk_status', default=1) 
	nombre = models.CharField(max_length=255, null=False)
	apellido = models.CharField(max_length=255, null=False)
	cedula = models.CharField(max_length=255, null=False, unique=True)
	correo_electronico = models.EmailField(max_length=255, blank=True, unique=True)
	intentos_login = models.IntegerField(default=0)
	objects = UserManager()
	#hello

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['correo_electronico']
	is_active = models.BooleanField(default=True)


	def email_user(self, subject, message, from_email=None):
		"""
		Sends an email to this User.
		"""
		send_mail(subject, message, from_email, [self.email])

	def filtro(instance,param, filter_code):
		#Método que filtra y retorna las declaraciones realizadas por los usuarios del sistema
		# se definen las variables asociadas a las condiciones de la busqueda y
		# el arreglo de columns para establecer los campos a consultar
		from apps.rcs.models import *
		select = {}
		exclude = []
		condiciones = []
		columns = []
		remove_add_header = ([], [])

		# si se reciben parametros de busqueda, se procede a llenar el arreglo
		# de condiciones

		if param:
			# se obtienen los parametros de busqueda relacionados al modelo actual dependiendo del 'filter_code'
			# NOTA: dependiendo del 'filter_code' se extraen los parametros de
			# la consulta
			if filter_code == 'BAN_USUARIOS':
				# placa= param.get('placa', None)
				cedula= param.get('cedula', None)
				correo= param.get('correo', None)
				tipo_usuario= param.get('tipo_usuario', None)
				nombre= param.get('nombre', None)
				apellido= param.get('apellido', None)

				# if placa:
					# condiciones.append(Q(fk_vehiculo__placa__icontains=placa))
# 
				if cedula:
					condiciones.append(Q(cedula__icontains=cedula))
				if nombre:
					condiciones.append(Q(nombre__icontains=nombre))
				if apellido:
					condiciones.append(Q(apellido__icontains=apellido))
				if correo:
					condiciones.append(Q(correo_electronico__icontains=parentesco))
				if tipo_usuario:
					condiciones.append(Q(fk_tipo_usuario__codigo=tipo_usuario))


				condiciones.append(~Q(fk_tipo_usuario__codigo="ADM"))

		
		# NOTA: dependiendo del 'filter_code' se define las condiciones
		# adicionales de la consulta
		if filter_code == "BAN_USUARIOS":
			# select['fecha_declaracion'] = "to_char(fecha_declaracion, 'DD/MM/YYYY')"
			columns = ['id','username', 'cedula','nombre', 'apellido','fk_tipo_usuario','correo_electronico',]

			# se guardan las columnas a eliminar/agregar en el arreglo
			# 'columns'
			remove_add_header = (
				['id','last_login','intentos_login','password', 'is_active'], #columnas eliminar
				['options'],#columnas agregar
			)

		# si tenemos condiciones, se procede a realizar el la consulta con las
		# mismas
		if len(condiciones) > 0:
			datos_filtrados = Usuario.objects.extra(select=select)\
							   .values(*columns)\
							   .filter(reduce(operator.and_, condiciones))
			# en caso contrario se obtienen todos los registros pertenecientes
			# al modelo
		else:
			datos_filtrados = Usuario.objects.extra(select=select).values(*columns).all()

		# se procede a eliminar/agregar las columnas que van o no van a ser
		# visualizadas en el template
		# -- diferencia --
		columns = [x for x in columns if x not in remove_add_header[0]]
		columns = columns + remove_add_header[1]  # -- unión --

		cont = 1
		for d in datos_filtrados:
			# se codifica el ID por medida de seguridad
			#
			# siendo_usado = False
			# rec = seccion.objects.filter(fk_forma=d['id'])
			# if rec:
			#     siendo_usado = True
			# if d['last_login'] != None:
			# 	d['last_login'] = d['last_login'].date().isoformat()
			# 	fecha = d['last_login'].split('-')
			# 	d['last_login'] = fecha[2] + '/' + fecha[1] + '/' + fecha[0]
			# else:
			# 	d['last_login'] = ""
			d['fk_tipo_usuario'] = TipoUsuario.objects.get(id=d['fk_tipo_usuario']).nombre
			tiene_sol_cerrada = SolicitudInspeccion.objects.filter(fk_inspector=d['id'],fk_estado_solicitud__codigo="CERRADA").exists()
			d['id'] = secure_value_encode(str(d['id']))
			# d['fk_seccion__fk_estado_seccion__nombre'] = d['fk_seccion__fk_estado_seccion__nombre'].upper() 
			# d['fk_seccion__fk_estado_seccion__nombre']
			# NOTA: dependiendo del 'filter_code' se definen los botones de la
			# tabla en el template
			if filter_code == "BAN_USUARIOS":

				d['options'] = []

				d['options'].append({
					'tooltip': 'Gestionar Solicitud',
					'icon': 'fa fa-pencil-square-o white-icon',
					'class': 'btn btn-info editar_boton',
					'href': '/administracion/editar_usuario/?'+urllib.urlencode({"usuario_id":d['id']}),
					'status': 'disabled' if tiene_sol_cerrada else '',
					})
				
				# d['options'].append({
				#     'tooltip': 'Cancelar Solicitud',
				#     'icon': 'fa fa-minus-circle white-icon',
				#     'class': 'btn btn-danger eliminar_boton',
				#     'target-modal': 'modal-verificacion-eliminar',
				#     'status': '',
				#     'data-ref': '/rcs/cancelar_ticket/?'+urllib.urlencode({"sol_id":d['id']}),
				#             # 'href': '/rcs/cancelar_ticket/?'+urllib.urlencode({"sol_id":d['id']}),
				# })
			 
				
				

			d['id'] = str(cont)
			cont = cont + 1

		# al final se devuelve una tupa, donde 'columns' representa el orden en
		# que se renderiza el resultado almacenado en el segundo valor

		return (columns, datos_filtrados)