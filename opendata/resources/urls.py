#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .utils import get_resources_classes

from .resources.france.nantes.budget.budget_primitif import BudgetPrimitifNantes2014

urlpatterns = patterns(
    '',
)

for klass in get_resources_classes():

    for item in klass.visualizations:

        view_url = klass.get_view_url_part(klass, item)

        """ Example:
        ^resources/ ^budgetprimitifnantes2014/datatable$ [name='budgetprimitifnantes2014/datatable']
        ^resources/ ^budgetprimitifnantes2014/json$ [name='budgetprimitifnantes2014/json']
        """

        urlpatterns += patterns(
            '',

            url(regex=r'^{}$'.format(view_url),
                view=klass.as_view(
                    template_name=item['template_name'],
                    current_visualization=item
                ),
                name=view_url
                ),

        )
