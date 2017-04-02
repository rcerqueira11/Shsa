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

from apps.registro.models import *


import unicodedata
import re

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import csv




def elimina_tildes(s):
    """
    Metodo para eliminar las tildes en cadenas de caracteres que se
    reciben por el parametro s.
    """
    #pre_s = ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
    #final = re.sub(ur'[_]|[^¿%?\w]+', u' ', pre_s)

    nkfd_form = unicodedata.normalize('NFKD', unicode(s))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])