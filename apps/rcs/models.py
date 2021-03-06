# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models import *
from decimal import *
from datetime import datetime
from datetime import date
from utils.validate_files import ContentTypeRestrictedFileField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.HelpMethods.helpers import *
from django.apps import apps
from utils.HelpMethods.aes_cipher import encode as secure_value_encode
from utils.HelpMethods.aes_cipher import decode as secure_value_decode
from utils.HelpMethods.helpers import get_file_path_solicitud
from settings.settings import MEDIA_URL



import urllib
import operator

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
    clase = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return self.nombre + " " + "'" +self.codigo+ "'" 

##Tipo vehiculo sedan, cargar, coupe
class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255,unique=True)

    def __unicode__(self):
        return self.nombre + " " + self.codigo

##Tipo manejo automatico, sincronico
class TipoManejo(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255,unique=True)

    def __unicode__(self):
        return self.nombre + " " + self.codigo

##23-55
class CondicionesGeneralesBase(models.Model):
    parte = models.CharField(max_length=255)
    fk_estado_vehiculo = models.ForeignKey(EstadoVehiculo, blank=True, null=True)
    observacion = models.TextField(blank=True,null=True)
    codigo = models.CharField(max_length=255,unique=True)

    def __unicode__(self):
        return self.parte 

class CondicionesGeneralesVehiculo(models.Model):
    parte = models.CharField(max_length=255)
    fk_estado_vehiculo = models.ForeignKey(EstadoVehiculo, blank=True, null=True)
    observacion = models.TextField(blank=True,null=True)
    codigo = models.CharField(max_length=255,unique=True)

    def __unicode__(self):
        return self.parte 

##56-61 3 otros
class MecanicaBase(models.Model):
    parte = models.CharField(max_length=255)
    fk_estado_vehiculo = models.ForeignKey(EstadoVehiculo, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=255,unique=True)
    # otro = models.CharField(max_length=255, blank=True)
    def __unicode__(self):
        return self.parte 

class MecanicaVehiculo(models.Model):
    parte = models.CharField(max_length=255)
    fk_estado_vehiculo = models.ForeignKey(EstadoVehiculo, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=255,unique=True)
    # otro = models.CharField(max_length=255, blank=True)
    def __unicode__(self):
        return self.parte 

##62 - 91 dos 62 radio/antena
class AccesoriosBase(models.Model):
    accesorio = models.CharField(max_length=255)
    existe = models.BooleanField(default=True)
    observacion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=255,unique=True)
    # otro = models.CharField(max_length=255, blank=True)
    def __unicode__(self):
        return self.accesorio


class AccesoriosVehiculo(models.Model):
    accesorio = models.CharField(max_length=255)
    existe = models.BooleanField(default=True)
    observacion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=255,unique=True)
    # otro = models.CharField(max_length=255, blank=True)
    def __unicode__(self):
        return self.accesorio

## 92
class DetallesDatos(models.Model):
    pieza = models.CharField(max_length=255)
    tipo_dano = models.CharField(max_length=255, null=True)
    costo_aproximado = models.DecimalField(max_digits=21, decimal_places=2, null=True)
    ##PENDIENTE GUARDAR CON EL ID DEL VEHICULO
    codigo = models.CharField(max_length=255)
    # otro = models.CharField(max_length=255, blank=True)
    def __unicode__(self):
        return self.codigo+ " " + self.pieza

# Decimal("{:.2f}".format(format_float(valor)))

# get_file_path_documentos_presentados


class DocumentosPresentadosBase(models.Model):
    nombre = models.CharField(max_length=255)
    recibido = models.BooleanField(default=False)
    codigo = models.CharField(max_length=255,unique=True)

    def __unicode__(self):
        return self.nombre

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

    def filtro(instance,param, filter_code):
        """Método que filtra y retorna las declaraciones realizadas por los usuarios del sistema"""
        # se definen las variables asociadas a las condiciones de la busqueda y
        # el arreglo de columns para establecer los campos a consultar
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
            if filter_code == 'TITULARES_VEHICULOS':
                placa= param.get('placa', None)
                cedula= param.get('cedula', None)
                nombre= param.get('nombre', None)
                apellido= param.get('apellido', None)
                telefono= param.get('telefono', None)
                if placa:
                    condiciones.append(Q(fk_vehiculo__placa__icontains=placa))

                if cedula:
                    condiciones.append(Q(cedula__icontains=cedula))

                if nombre:
                    condiciones.append(Q(nombre__icontains=nombre))

                if apellido:
                    condiciones.append(Q(apellido__icontains=apellido))

                if telefono:
                    if "_" in telefono:
                        telefono = telefono[:telefono.find("_")]
                    condiciones.append(Q(telefono__icontains=telefono))
        
        # NOTA: dependiendo del 'filter_code' se define las condiciones
        # adicionales de la consulta
        if filter_code == "TITULARES_VEHICULOS":
            # select['fecha_declaracion'] = "to_char(fecha_declaracion, 'DD/MM/YYYY')"
            columns = ['id','cedula','nombre','apellido','telefono',]

            # se guardan las columnas a eliminar/agregar en el arreglo
            # 'columns'
            remove_add_header = (
                ['id','apellido'], #columnas eliminar
                ['options'],#columnas agregar
            )

        # si tenemos condiciones, se procede a realizar el la consulta con las
        # mismas
        if len(condiciones) > 0:
            datos_filtrados = TitularVehiculo.objects.extra(select=select)\
                               .values(*columns)\
                               .filter(reduce(operator.and_, condiciones))
            # en caso contrario se obtienen todos los registros pertenecientes
            # al modelo
        else:
            datos_filtrados = TitularVehiculo.objects.extra(select=select).values(*columns).all()

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
            tiene_sol_cerrada = SolicitudInspeccion.objects.filter(fk_titular_vehiculo=d['id'],fk_estado_solicitud__codigo="CERRADA").exists()
            d['id'] = secure_value_encode(str(d['id']))
            # d['fk_seccion__fk_estado_seccion__nombre'] = d['fk_seccion__fk_estado_seccion__nombre'].upper() 
            # d['fk_seccion__fk_estado_seccion__nombre']
            # NOTA: dependiendo del 'filter_code' se definen los botones de la
            # tabla en el template
            d['nombre'] = d['nombre'] +" "+ d['apellido']
            if filter_code == "TITULARES_VEHICULOS":

                d['options'] = []

                d['options'].append({
                    'tooltip': 'Editar Titular',
                    'icon': 'fa fa-pencil-square-o white-icon',
                    'class': 'btn btn-info editar_boton',
                    'href': '/administracion/editar_titular/?'+urllib.urlencode({"titular_id":d['id']}),
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


class Parentesco(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255, unique=True )

    def __unicode__(self):
        return self.nombre + " " + self.codigo

class TrajoVehiculo(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    cedula = models.CharField(max_length=255, unique=True)
    # parentesco = models.CharField(max_length=255, blank=True)
    fk_parentesco = models.ForeignKey(Parentesco)
    
    def __unicode__(self):
        return self.nombre + " " + self.apellido

    def filtro(instance,param, filter_code):
        """Método que filtra y retorna las declaraciones realizadas por los usuarios del sistema"""
        # se definen las variables asociadas a las condiciones de la busqueda y
        # el arreglo de columns para establecer los campos a consultar
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
            if filter_code == 'TRAJO_VEHICULO':
                # placa= param.get('placa', None)
                cedula= param.get('cedula', None)
                nombre= param.get('nombre', None)
                apellido= param.get('apellido', None)

                parentesco= param.getlist('parentesco',None) if  param.getlist('parentesco',None) else  param.getlist('parentesco[]',None)


                # if placa:
                    # condiciones.append(Q(fk_vehiculo__placa__icontains=placa))
# 
                if cedula:
                    condiciones.append(Q(cedula__icontains=cedula))

                if nombre:
                    condiciones.append(Q(nombre__icontains=nombre))
                if apellido:
                    condiciones.append(Q(apellido__icontains=apellido))
                if parentesco:
                    condiciones.append(Q(fk_parentesco__codigo__in=parentesco))
                    # condiciones.append(Q(fk_parentesco__codigo=parentesco))

        
        # NOTA: dependiendo del 'filter_code' se define las condiciones
        # adicionales de la consulta
        if filter_code == "TRAJO_VEHICULO":
            # select['fecha_declaracion'] = "to_char(fecha_declaracion, 'DD/MM/YYYY')"
            columns = ['id','cedula','nombre','apellido','fk_parentesco',]

            # se guardan las columnas a eliminar/agregar en el arreglo
            # 'columns'
            remove_add_header = (
                ['id','apellido'], #columnas eliminar
                ['options'],#columnas agregar
            )

        # si tenemos condiciones, se procede a realizar el la consulta con las
        # mismas
        if len(condiciones) > 0:
            datos_filtrados = TrajoVehiculo.objects.extra(select=select)\
                               .values(*columns)\
                               .filter(reduce(operator.and_, condiciones))
            # en caso contrario se obtienen todos los registros pertenecientes
            # al modelo
        else:
            datos_filtrados = TrajoVehiculo.objects.extra(select=select).values(*columns).all()

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
            tiene_sol_cerrada = SolicitudInspeccion.objects.filter(fk_trajo_vehiculo=d['id'],fk_estado_solicitud__codigo="CERRADA").exists()
            d['id'] = secure_value_encode(str(d['id']))
            # d['fk_seccion__fk_estado_seccion__nombre'] = d['fk_seccion__fk_estado_seccion__nombre'].upper() 
            # d['fk_seccion__fk_estado_seccion__nombre']
            # NOTA: dependiendo del 'filter_code' se definen los botones de la
            # tabla en el template
            d['nombre'] = d['nombre'] +" "+ d['apellido']
            d['fk_parentesco'] = Parentesco.objects.get(id = d['fk_parentesco']).nombre
            if filter_code == "TRAJO_VEHICULO":

                d['options'] = []

                d['options'].append({
                    'tooltip': 'Editar Persona',
                    'icon': 'fa fa-pencil-square-o white-icon',
                    'class': 'btn btn-info editar_boton',
                    'href': '/administracion/editar_trajo_vehiculo/?'+urllib.urlencode({"trajo_vehiculo_id":d['id']}),
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

class MarcaVehiculo(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255, unique=True )

    def __unicode__(self):
        return self.nombre + " " + self.codigo

class ModeloVehiculo(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255, unique=True )
    fk_marca_vehiculo = models.ForeignKey(MarcaVehiculo)

    def __unicode__(self):
        return self.nombre + " " + self.codigo


class Vehiculo(models.Model):
    placa = models.CharField(max_length=255, unique=True)
    fk_titular_vehiculo = models.ForeignKey(TitularVehiculo)
    cap_puestos = models.IntegerField(null=True)
    cilindros = models.CharField(max_length=255, null=True)
    peso =  models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True)
    kilometraje = models.CharField(max_length=255, null=True)
    serial_carroceria = models.CharField(max_length=255, null=True)
    serial_motor = models.CharField(max_length=255, null=True)
    valor_estimado = models.DecimalField(max_digits=21, decimal_places=2, null=True)
    # modelo = models.CharField(max_length=255, null=True)
    # marca = models.CharField(max_length=255, null=True)
    fk_marca = models.ForeignKey(MarcaVehiculo, null=True)
    fk_modelo = models.ForeignKey(ModeloVehiculo, null=True)
    fk_inspector = models.ForeignKey(Usuario, null=True)
    fk_tipo_vehiculo = models.ForeignKey(TipoVehiculo, null=True)
    fk_tipo_manejo = models.ForeignKey(TipoManejo, null=True)
    anho = models.IntegerField(null=True)
    condiciones_generales_vehiculo = models.ManyToManyField(CondicionesGeneralesVehiculo)
    mecanica_vehiculo = models.ManyToManyField(MecanicaVehiculo)
    accesorios_vehiculo = models.ManyToManyField(AccesoriosVehiculo)
    detalles_datos = models.ManyToManyField(DetallesDatos)
    documentos_presentados = models.ManyToManyField(DocumentosPresentados)

    def __unicode__(self):
        return "Placa: "+ self.placa + " Cedula: " + self.fk_titular_vehiculo.cedula


class MotivoSolicitud(models.Model):
    motivo = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255, unique=True )

    def __unicode__(self):
        return self.motivo + " " + self.codigo


class SolicitudInspeccion(models.Model):
    numero_ticket = models.CharField(max_length=255, unique=True)
    fk_vehiculo = models.ForeignKey(Vehiculo)
    fk_titular_vehiculo = models.ForeignKey(TitularVehiculo)
    fk_trajo_vehiculo = models.ForeignKey(TrajoVehiculo, blank=True, null=True)
    fk_inspector = models.ForeignKey(Usuario,null=True)
    siendo_verificada = models.IntegerField(blank=True,null=True) #numero id del inspector verificando la solicitud
    fecha_creacion = models.DateTimeField(['%d/%m/%Y'], blank=True, null=True, auto_now=True)
    fk_estado_solicitud = models.ForeignKey(EstadoSolicitud, default=1)
    fk_motivo_solicitud = models.ForeignKey(MotivoSolicitud)
    observaciones = models.TextField(blank=True,null=True)
    codigo = models.CharField(max_length=255)
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
        return self.fk_vehiculo.placa + "" + self.fk_titular_vehiculo.cedula

    def filtro(instance,param, filter_code):
        """Método que filtra y retorna las declaraciones realizadas por los usuarios del sistema"""
        # se definen las variables asociadas a las condiciones de la busqueda y
        # el arreglo de columns para establecer los campos a consultar
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
            if filter_code == 'SOL_INSP_INSP':
                placa= param.get('placa', None)
                cedula= param.get('cedula', None)
                estado_sol= param.get('estado_sol', None)
                numero_ticket= param.get('numero_ticket', None)

                if placa:
                    condiciones.append(Q(fk_vehiculo__placa__icontains=placa))

                if cedula:
                    condiciones.append(Q(fk_titular_vechiculo__cedula__icontains=cedula))

                if estado_sol:
                    condiciones.append(Q(fk_estado_solicitud__codigo=estado_sol))
                
                if numero_ticket:
                    condiciones.append(Q(numero_ticket__icontains=numero_ticket))


            if filter_code == 'TICKETS_ABIERTOS':
                placa= param.get('placa', None)
                cedula= param.get('cedula', None)
                estado_sol= param.get('estado_sol', None)
                numero_ticket= param.get('numero_ticket', None)

                if placa:
                    condiciones.append(Q(fk_vehiculo__placa__icontains=placa))

                if cedula:
                    condiciones.append(Q(fk_titular_vehiculo__cedula__icontains=cedula))

                if numero_ticket:
                    condiciones.append(Q(numero_ticket__icontains=numero_ticket))

                condiciones.append(Q(fk_estado_solicitud__codigo="PEND_INSP"))
                condiciones.append(Q(fk_vehiculo__peso=None))
                condiciones.append(Q(fk_vehiculo__color=None))

        # condiciones= vehiculo.condiciones_generales_vehiculo.all().exists()
        # mecanica= vehiculo.mecanica_vehiculo.all().exists()
        # accesorios= vehiculo.accesorios_vehiculo.all().exists()
        # detalles= vehiculo.detalles_datos.all().exists()
        # documentos= vehiculo.documentos_presentados.all().exists()

                # if 'configurable' in param:
                #     condiciones.append(Q(fk_seccion__configurable=True))
                # else:
                #     condiciones.append(Q(fk_seccion__configurable=False))

        # NOTA: dependiendo del 'filter_code' se define las condiciones
        # adicionales de la consulta
        if filter_code == "SOL_INSP_INSP":
            # select['fecha_declaracion'] = "to_char(fecha_declaracion, 'DD/MM/YYYY')"
            columns = ['id','numero_ticket','fk_vehiculo__placa','fk_titular_vehiculo__cedula','fk_titular_vehiculo__nombre','fk_estado_solicitud__codigo','ruta',]

            # se guardan las columnas a eliminar/agregar en el arreglo
            # 'columns'
            remove_add_header = (
                ['id','ruta'], #columnas eliminar
                ['options'],#columnas agregar
            )

        if filter_code == "TICKETS_ABIERTOS":
            # select['fecha_declaracion'] = "to_char(fecha_declaracion, 'DD/MM/YYYY')"
            columns = ['id','numero_ticket','fk_vehiculo__placa','fk_titular_vehiculo__cedula','fk_titular_vehiculo__nombre','fk_estado_solicitud__codigo']

            # se guardan las columnas a eliminar/agregar en el arreglo
            # 'columns'
            remove_add_header = (
                ['id',], #columnas eliminar
                ['options'],#columnas agregar
            )
        # si tenemos condiciones, se procede a realizar el la consulta con las
        # mismas
        if len(condiciones) > 0:
            datos_filtrados = SolicitudInspeccion.objects.extra(select=select)\
                               .values(*columns)\
                               .filter(reduce(operator.and_, condiciones))
            # en caso contrario se obtienen todos los registros pertenecientes
            # al modelo
        else:
            datos_filtrados = SolicitudInspeccion.objects.extra(select=select).values(*columns).all()

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

            d['id'] = secure_value_encode(str(d['id']))
            # d['fk_seccion__fk_estado_seccion__nombre'] = d['fk_seccion__fk_estado_seccion__nombre'].upper() 
            # d['fk_seccion__fk_estado_seccion__nombre']
            # NOTA: dependiendo del 'filter_code' se definen los botones de la
            # tabla en el template
            if filter_code == "SOL_INSP_INSP":

                d['options'] = []

                if d['fk_estado_solicitud__codigo'] == 'PEND_INSP' or d['fk_estado_solicitud__codigo'] == 'PEND_GEST':
                    d['options'].append({
                        'tooltip': 'Gestionar Solicitud',
                        'icon': 'fa fa-pencil-square-o white-icon',
                                'class': 'btn btn-info editar_boton',
                                'href': '/rcs/gestion_ticket/?'+urllib.urlencode({"sol_id":d['id']}),
                                'status': 'disabled' if d['fk_estado_solicitud__codigo'] == 'CERRADA' else '',
                    })
                
                if d['fk_estado_solicitud__codigo'] == 'PEND_GEST' or d['fk_estado_solicitud__codigo'] == 'CERRADA':
                    d['options'].append({
                        'href': MEDIA_URL+str(d['ruta']),
                        'tooltip': 'Ver detalle solicitud',
                        'target': '_blank',
                        'icon': 'fa fa-search',
                        'class': 'btn btn-warning',
                        'status': '',
                    })    
                
                if d['fk_estado_solicitud__codigo'] == 'PEND_INSP':
                    d['fk_estado_solicitud__codigo'] = "ABIERTA"

                if d['fk_estado_solicitud__codigo'] == 'PEND_GEST':
                    d['fk_estado_solicitud__codigo'] = "POR GESTIONAR"

                if d['fk_estado_solicitud__codigo'] == 'CERRADA':
                    d['fk_estado_solicitud__codigo'] = "CERRADA"

            if filter_code == "TICKETS_ABIERTOS":
                en_rev = en_revision(d['id'])
                if d['fk_estado_solicitud__codigo'] == 'PEND_INSP':
                    d['fk_estado_solicitud__codigo'] = "ABIERTA"

                if d['fk_estado_solicitud__codigo'] == 'PEND_GEST':
                    d['fk_estado_solicitud__codigo'] = "POR GESTIONAR"

                if d['fk_estado_solicitud__codigo'] == 'CERRADA':
                    d['fk_estado_solicitud__codigo'] = "CERRADA"
                d['options'] = []

                d['options'].append({
                    'tooltip': 'Cancelar Solicitud',
                    'icon': 'fa fa-minus-circle white-icon',
                    'class': 'btn btn-danger eliminar_boton',
                    'target-modal': 'modal-verificacion-eliminar',
                    'status': '',
                    'data-ref': '/rcs/cancelar_ticket/?'+urllib.urlencode({"sol_id":d['id']}),
                            # 'href': '/rcs/cancelar_ticket/?'+urllib.urlencode({"sol_id":d['id']}),
                })
             
                
                

            d['id'] = str(cont)
            cont = cont + 1

        # al final se devuelve una tupa, donde 'columns' representa el orden en
        # que se renderiza el resultado almacenado en el segundo valor

        return (columns, datos_filtrados)



