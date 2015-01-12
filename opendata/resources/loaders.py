#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader


class Loader(BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        """
        Custom Loader: load a template from an absolute path inside the
        resources/resources directory.

        Useful when we want to place a visualization template near the
        resource class declaration (i.e in the same directory).
        In this case, the template is declared in the class with
        'template_name': '<local>/template.html'
        """

        # Security
        template_name = template_name.replace('/..', '')
        template_name = template_name.replace('../', '')
        template_name = template_name.replace('..', '')

        if template_name.startswith(
            '{}/resources/resources/'.format(settings.BASE_DIR)
        ):
            try:
                with open(template_name, 'rb') as fp:
                    return (fp.read().decode(settings.FILE_CHARSET),
                            template_name)
            except IOError:
                pass

        raise TemplateDoesNotExist(template_name)
