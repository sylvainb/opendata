#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand

from resources.utils import get_resources_classes


class Command(BaseCommand):
    """ Update Open Data resources files. """
    args = ''
    help = ('Update Open Data resources files.')

    def handle(self, *args, **kwargs):

        for klass in get_resources_classes():
            self.stdout.write('Process "{}"'.format(klass.title))
            klass.update_resource(klass)

        self.stdout.write("Resources updated")
