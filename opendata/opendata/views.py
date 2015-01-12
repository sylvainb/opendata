#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _


class HomeView(TemplateView):
    """ Render the Home Page """
    title = _('Home')
    template_name = 'opendata/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context
