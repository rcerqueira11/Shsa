# -*- coding: utf-8 -*-

"""

"""

# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from os import path
from re import compile as re_compile
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
EXT_CONTENT_TYPE = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'pdf': 'application/pdf',
    'png': 'image/png',
}

FILE_REGEX = re_compile(r'^(?:\w{4}-){10}.*$')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - Lista contiene content_types permitidos. Ejemplo: ['application/pdf', 'image/jpeg']
        * max_upload_size - un número que indica el tamaño máximo de archivo permitido para la carga.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        if "content_types" in kwargs.keys():
            self.content_types = kwargs.pop("content_types")

        if "max_upload_size" in kwargs.keys():
            self.max_upload_size = kwargs.pop("max_upload_size")

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        # Django es un framework de lo más retardado (aka estúpido)
        if FILE_REGEX.match(unicode(data)):
            return data

        fobj = data.file
        content_type = get_content_type(fobj)

        if content_type in self.content_types:
            if fobj.size > self.max_upload_size:
                msg = (
                    u'Por favor, mantenga tamaño de archivo bajo {0}. '
                    u'el tamaño del archivo es: {1}'
                ).format(
                    filesizeformat(self.max_upload_size),
                    filesizeformat(fobj.size)
                )

                raise forms.ValidationError(msg)
        else:
            raise forms.ValidationError(u'El tipo de archivo no es soportado.')

        return data

# from south.modelsinspector import add_introspection_rules
# add_introspection_rules([], ["^utils\.validate_files\.ContentTypeRestrictedFileField"])


# Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_content_type(fobj):
    if not hasattr(fobj, 'content_type'):
        ext = path.splitext(fobj.name)[1][1:].lower()
        return EXT_CONTENT_TYPE.get(ext, 'text/plain')
    return getattr(fobj, 'content_type')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
