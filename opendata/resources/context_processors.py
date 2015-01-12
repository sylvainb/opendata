#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from resources.utils import get_resources_classes


def get_resources(request):

    resources = []

    for klass in get_resources_classes():

        resource_urls = []

        for item in klass.visualizations:
            view_url = klass.get_view_url_part(klass, item)
            real_url = reverse(view_url)
            resource_urls.append(real_url)

        resources.append({
            'url_main': resource_urls[0],
            'url_others': resource_urls[1:],
            'class': klass
        })

    return {
        'resources': resources
    }
