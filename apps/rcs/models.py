from django.db import models
from apps.registro.models import *
from decimal import *
# Create your models here.


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
	fk_estado_vehiculo = models.ForeignKey(EstadoVehiculo, blank=True)
	comentario = models.TextField(blank=True)
	codigo = models.CharField(max_length=255,unique=True)

	def __unicode__(self):
		return self.parte 

##56-61 3 otros
class MecanicaVehiculo(models.Model):
	parte = models.CharField(max_length=255)
	fk_estado_vehiculo = models.ForeignKey(EstadoVehiculo, blank=True)
	comentario = models.TextField(blank=True)
	codigo = models.CharField(max_length=255,unique=True)
	# otro = models.CharField(max_length=255, blank=True)
	def __unicode__(self):
		return self.parte 

##62 - 91 dos 62 radio/antena
class AccesoriosVehiculo(models.Model):
	accesorio = models.CharField(max_length=255)
	existe = models.BooleanField(default=True)
	comentario = models.TextField(blank=True)
	codigo = models.CharField(max_length=255,unique=True)
	# otro = models.CharField(max_length=255, blank=True)
	def __unicode__(self):
		return self.accesorio

## 92
class DetallesDatos(models.Model):
	pieza = models.CharField(max_length=255)
	tipo_dano = models.BooleanField(default=True)
	costo_aproximado = models.DecimalField(max_digits=21, decimal_places=2)
	# codigo = models.CharField(max_length=255,unique=True)
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
	nombre = models.CharField(max_length=255, null=False)
	apellido = models.CharField(max_length=255, null=False)
	cedula = models.CharField(max_length=255, null=False, unique=True)
	telefono = models.CharField(max_length=255, blank=True)
	
	def __unicode__(self):
		return self.nombre + " " + self.apellido


class TrajoVehiculo(models.Model):
	nombre = models.CharField(max_length=255, null=False)
	apellido = models.CharField(max_length=255, null=False)
	cedula = models.CharField(max_length=255, null=False, unique=True)
	parentesco = models.CharField(max_length=255, blank=True)
	
	def __unicode__(self):
		return self.nombre + " " + self.apellido




class Vehiculo(models.Model):
	placa = models.CharField(max_length=255, unique=True, null=False)
	fk_titular_vehiculo = models.ForeignKey(TitularVehiculo)
	fk_trajo_vehiculo = models.ForeignKey(TrajoVehiculo, blank=True)
	cilindros = models.CharField(max_length=255, null=False)
	color = models.CharField(max_length=255, null=False)
	kilometraje = models.CharField(max_length=255, null=False)
	serial_carroceria = models.CharField(max_length=255, null=False)
	serial_motor = models.CharField(max_length=255, null=False)
	modelo = models.CharField(max_length=255, null=False)
	marca = models.CharField(max_length=255, null=False)
	fk_inspector = models.ForeignKey(Usuario)



	def __unicode__(self):
		return self.placa + "" + self.fk_titular_vehiculo.cedula



