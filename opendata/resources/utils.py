#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

from django.conf import settings

from resources.views import SingleResourceBaseView


def get_resources_classes():
    """ List all resources classes (childs of SingleResourceBaseView) """
    classes = [
        m[1] for m in inspect.getmembers(settings.RESOURCES_MODULE_LIST,
                                         predicate=inspect.isclass)
        if issubclass(m[1], SingleResourceBaseView)
    ]

    return classes
