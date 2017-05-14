# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from email.MIMEImage import MIMEImage
from settings.settings import BASE_DIR, EMAIL_HOST_USER, STATIC_URL
from datetime import datetime
from datetime import date, timedelta
from django.db.models import Q
from os import path
from django.template.loader import get_template
from django.template import Context
from hashlib import sha1
from utils.HelpMethods.aes_cipher import encode as secure_value_encode
from utils.HelpMethods.aes_cipher import decode as secure_value_decode
from apps.registro.models import *


import unicodedata
import re

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import csv


def gen_path_str_from_key_str(key_str):
    hash_str = sha1(key_str).hexdigest()
    return '-'.join(hash_str[i:i + 4] for i in xrange(0, 40, 4))

def normalize_filename(string="", pass_blank_name=False):
    try:
        re = ''.join(e if ord(e) < 128 else '' for e in string if e.isalnum() or e == ".")
        if len(re):
            return re
        elif not pass_blank_name:
            return "archivo_%s" % (datetime.now().strftime('%d%m%Y'))
        else:
            return ''
    except Exception, e:
        raise e

def elimina_tildes(s):
    """
    Metodo para eliminar las tildes en cadenas de caracteres que se
    reciben por el parametro s.
    """
    #pre_s = ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
    #final = re.sub(ur'[_]|[^¿%?\w]+', u' ', pre_s)

    nkfd_form = unicodedata.normalize('NFKD', unicode(s))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


def get_file_path_documentos_presentados(instance, filename):
    return path.join(
        gen_path_str_from_key_str(
            str(instance.cedula_titular)
        ),
        str(instance.placa),'documentos_presentados_inspeccion',
        normalize_filename(filename.lower())
    )

def get_file_path_solicitud(instance, filename):
    return path.join(
        gen_path_str_from_key_str(
            str(instance.fk_vehiculo.fk_titular_vehiculo.cedula)
        ),
        str(instance.fk_vehiculo.placa),
        normalize_filename(filename.lower())
    )


def en_revision(x):
    from apps.rcs.models import SolicitudInspeccion
    if SolicitudInspeccion.objects.filter(id= secure_value_decode(str(x))).exists():
        solicitud = SolicitudInspeccion.objects.get(id= secure_value_decode(str(x)))
        vehiculo = solicitud.fk_vehiculo
        peso= vehiculo.peso != None
        color= vehiculo.color != None
        condiciones= vehiculo.condiciones_generales_vehiculo.all().exists()
        mecanica= vehiculo.mecanica_vehiculo.all().exists()
        accesorios= vehiculo.accesorios_vehiculo.all().exists()
        detalles= vehiculo.detalles_datos.all().exists()
        documentos= vehiculo.documentos_presentados.all().exists()

        if peso or color or condiciones or mecanica or accesorios or detalles or documentos:
            return True
        else:  
            return False

    return False