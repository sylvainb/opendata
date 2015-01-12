#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

#from foundation import urls as foundation_urls

from resources import urls as resources_urls
from .views import HomeView


urlpatterns = patterns(
    '',

    # TEST FOUNDATION
    #url(r'^foundation/', include(foundation_urls)),

    # Dashboard
    url(regex=r'^$',
        view=HomeView.as_view(),
        name="home"),

    url(r'^resources/', include(resources_urls)),

    url(r'^admin/', include(admin.site.urls)),
)
