from django.db import models
from apps.registro.models import *
from decimal import *
from datetime import datetime
from datetime import date
from utils.validate_files import ContentTypeRestrictedFileField
from utils.HelpMethods.helpers import *

TAMANO_MAXIMO_ARCHIVO = 10485760  # 10 megas
# Create your models here.


class EstadoSolicitud(models.Model):
	nombre = models.CharField(max_length=255)
	descripcion = models.TextField(blank=True)
	codigo = models.CharField(max_length=255,unique=True)

	def __unicode__(self):
		return self.descripcion


## Estado B R M
class EstadoVehiculo(models.Model):
	nombre = models.CharField(max_length=255)
	descripcion = models.TextField(blank=True)
	codigo = models.CharField(max_length=255,unique=True)

	def __unicode__(self):
		return self.descripcion

##Tipo vehiculo sedan, cargar, coupe
class TipoVehiculo(models.Model):
	nombre = models.CharField(max_length=255)
	codigo = models.CharField(max_length=255,unique=True)

	def __unicode__(self):
		return self.nombre + " " + self.codigo

##23-55
class CondicionesGeneralesVehiculo(models.Model):
	parte = models.CharField(max_length=255)
	fk_estado_vehiculo = models.ForeignKey(EstadoVehiculo, blank=True, null=True)
	comentario = models.TextField(blank=True,null=True)
	codigo = models.CharField(max_length=255,unique=True)

	def __unicode__(self):
		return self.parte 

##56-61 3 otros
class MecanicaVehiculo(models.Model):
	parte = models.CharField(max_length=255)
	fk_estado_vehiculo = models.ForeignKey(EstadoVehiculo, blank=True, null=True)
	comentario = models.TextField(blank=True, null=True)
	codigo = models.CharField(max_length=255,unique=True)
	# otro = models.CharField(max_length=255, blank=True)
	def __unicode__(self):
		return self.parte 

##62 - 91 dos 62 radio/antena
class AccesoriosVehiculo(models.Model):
	accesorio = models.CharField(max_length=255)
	existe = models.BooleanField(default=True)
	comentario = models.TextField(blank=True, null=True)
	codigo = models.CharField(max_length=255,unique=True)
	# otro = models.CharField(max_length=255, blank=True)
	def __unicode__(self):
		return self.accesorio

## 92
class DetallesDatos(models.Model):
	pieza = models.CharField(max_length=255)
	tipo_dano = models.CharField(max_length=255, null=True)
	costo_aproximado = models.DecimalField(max_digits=21, decimal_places=2, null=True)
	codigo = models.CharField(max_length=255,unique=True)
	# otro = models.CharField(max_length=255, blank=True)
	def __unicode__(self):
		return self.pieza

# Decimal("{:.2f}".format(format_float(valor)))

# get_file_path_documentos_presentados


class DocumentosPresentados(models.Model):
	nombre = models.CharField(max_length=255)
	recibido = models.BooleanField(default=True)
	codigo = models.CharField(max_length=255,unique=True)

	def __unicode__(self):
		return self.nombre

class TitularVehiculo(models.Model):
	nombre = models.CharField(max_length=255)
	apellido = models.CharField(max_length=255)
	cedula = models.CharField(max_length=255, unique=True)
	telefono = models.CharField(max_length=255, blank=True)
	
	def __unicode__(self):
		return self.nombre + " " + self.apellido


class TrajoVehiculo(models.Model):
	nombre = models.CharField(max_length=255)
	apellido = models.CharField(max_length=255)
	cedula = models.CharField(max_length=255, unique=True)
	parentesco = models.CharField(max_length=255, blank=True)
	
	def __unicode__(self):
		return self.nombre + " " + self.apellido




class Vehiculo(models.Model):
	placa = models.CharField(max_length=255, unique=True)
	fk_titular_vehiculo = models.ForeignKey(TitularVehiculo)
	fk_trajo_vehiculo = models.ForeignKey(TrajoVehiculo, blank=True, null=True)
	cap_puestos = models.IntegerField(null=True)
	cilindros = models.CharField(max_length=255, null=True)
	peso = models.DecimalField(max_digits=21, decimal_places=2, null=True)
	color = models.CharField(max_length=255, null=True)
	kilometraje = models.CharField(max_length=255, null=True)
	serial_carroceria = models.CharField(max_length=255, null=True)
	serial_motor = models.CharField(max_length=255, null=True)
	valor_estimado = models.DecimalField(max_digits=21, decimal_places=2, null=True)
	modelo = models.CharField(max_length=255, null=True)
	marca = models.CharField(max_length=255, null=True)
	fk_inspector = models.ForeignKey(Usuario, null=True)
	fk_tipo_vehiculo = models.ForeignKey(TipoVehiculo, null=True)
	anho = models.IntegerField(null=True)
	condiciones_generales_vehiculo = models.ManyToManyField(CondicionesGeneralesVehiculo)
	mecanica_vehiculo = models.ManyToManyField(MecanicaVehiculo)
	accesorios_vehiculo = models.ManyToManyField(AccesoriosVehiculo)
	detalles_datos = models.ManyToManyField(DetallesDatos)
	documentos_presentados = models.ManyToManyField(DocumentosPresentados)

	def __unicode__(self):
		return self.placa + "" + self.fk_titular_vehiculo.cedula


class MotivoSolicitud(models.Model):
	motivo = models.CharField(max_length=255)
	codigo = models.CharField(max_length=255, unique=True )

	def __unicode__(self):
		return self.motivo + "" + self.codigo


class SolicitudInspeccion(models.Model):
	fk_vehiculo = models.OneToOneField(Vehiculo)
	fk_titular_vehiculo = models.ForeignKey(TitularVehiculo)
	fk_inspector = models.ForeignKey(Usuario)
	siendo_verificada = models.IntegerField() #numero id del inspector verificando la solicitud
	editable = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(['%d/%m/%Y'], blank=True, null=True, auto_now=True)
	fk_estado_solicitud = models.ForeignKey(EstadoSolicitud, default=1)
	fk_motivo_solicitud = models.ForeignKey(MotivoSolicitud)
	observaciones = models.TextField(blank=True,null=True)
	ruta=ContentTypeRestrictedFileField(
        upload_to=get_file_path_solicitud,
        max_length=500,
        content_types='application/pdf',
        blank=True,
        max_upload_size=TAMANO_MAXIMO_ARCHIVO,
        null=True,
    )

	# fecha_creacion = models.DateTimeField(['%d/%m/%Y'], blank=True, null=True, auto_now=True)

	def __unicode__(self):
		return self.placa + "" + self.fk_titular_vehiculo.cedula




