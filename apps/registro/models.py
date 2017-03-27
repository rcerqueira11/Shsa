from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
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
	nombre_usuario = models.CharField(max_length=255,unique=True)
	fk_tipo_usuario = models.ForeignKey(TipoUsuario)
	#chequear esto
	fk_status = models.ForeignKey(Status, db_column='fk_status', default=1) 
	nombre = models.CharField(max_length=255, null=False)
	apellido = models.CharField(max_length=255, null=False)
	cedula = models.CharField(max_length=255, null=False, unique=True)
	correo_electronico = models.EmailField(max_length=255, blank=True, unique=True)
	intentos_login = models.IntegerField(default=0)
	#hello

	USERNAME_FIELD = 'nombre_usuario'
	REQUIRED_FIELDS = ['correo_electronico']
	is_active = models.BooleanField(default=True)


	def email_user(self, subject, message, from_email=None):
		"""
		Sends an email to this User.
		"""
		send_mail(subject, message, from_email, [self.email])
