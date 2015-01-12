#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
import pycurl
import json
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from datetime import datetime
import pprint

from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


def get_fs_file_data(view):
    """ Wrapper around the class function """
    cls = view.__class__
    return cls.get_fs_file_data(cls)


def get_base_fs_dir_path(view):
    """ Wrapper around the class function """
    cls = view.__class__
    return os.path.dirname(inspect.getfile(cls))


class SingleResourceBaseView(TemplateView):
    """ Base view for all resources based on an uniq file """

    ##################################
    #### DESCRIPTION
    ##################################

    # MUST BE OVERRIDDEN
    # title
    title = _('The resource title')

    # MUST BE OVERRIDDEN
    # description
    description = _('The resource description in HTML format')

    # MUST BE OVERRIDDEN
    # paternity: who is the owner, the licence, ...
    paternity = _('The resource owner, licence, ...')

    # MUST BE OVERRIDDEN
    # external_link: where to consult the original resource
    external_link = 'http://www.example.com/the/resource'

    # MUST BE OVERRIDDEN
    # updated (a date like '2014/01/01', a texte like 'all weeks', ...)
    updated = '2014/01/01'

    # MUST BE OVERRIDDEN
    # territories, like ['France', 'Pays de la Loire',
    #                    'Loire Atlantique', 'Nantes']
    territories = ['territory1', 'territory2', 'territory3']

    # MUST BE OVERRIDDEN
    # keywords
    keywords = ['word1', 'word2', 'word3']

    # MUST BE OVERRIDDEN
    # keywords
    thematics = ['thematic1', 'thematic2', 'thematic3']

    ##################################
    #### DOWNLOAD PARAMETERS
    ##################################

    # MUST BE OVERRIDDEN
    # download_url
    download_url = 'http://www.example.com/the/resource.json'

    # MUST BE OVERRIDDEN
    # download_format: json, csv
    download_format = 'json'

    # MUST BE OVERRIDDEN
    # update_frequence: None (= Never) or a frequence in the crontab syntax
    # crontab syntax: http://fr.wikipedia.org/wiki/Crontab
    update_frequence = None

    ##################################
    #### VISUALIZATION
    ##################################

    # MUST BE OVERRIDDEN
    # visualization: the resource "visualization(s)",
    #
    """
    visualizations = [

        # visualization_datatables_net.html uses datatables.net jquery plugin
        {'title': 'Rich data table',
         'description': 'A description for this visualisation',
         'url_name': 'datatables-net',
         'template_name':
            'resources-generic/visualization_datatables_net.html'},

        {'title': 'Raw data table',
         'description': 'A description for this visualisation',
         'url_name': 'datatable-raw',
         'template_name':
            'resources-generic/visualization_datatable_raw.html'},

        {'title': 'Python',
         'description': 'A description for this visualisation',
         'url_name': 'python',
         'template_name': 'resources-generic/visualization_python.html'},

        {'title': 'Map',
         'description': 'A description for this visualisation',
         'url_name': 'map',
         'template_name': 'resources-generic/visualization_map.html'},

    ]
    # Note: Use _('text') if you want to translate titles and descriptions.
    #
    # Note: If you want to place your visualization template in the same folder
    #       as the class definition, use
    #           'template_name': '<local>/my_template.html'
    """
    visualizations = None
    current_visualization = None  # Filled in urls.py with the asked item

    ##################################
    #### PYTHON VISUALIZATION
    #### Use the template visualization_python.html
    #### No preprocessing is needed.
    #### Available hooks:
    ####     - json2python2html_hook
    ##################################

    def json2python2html(self):
        """ Useful if the data in the resource file is in json format.
            Return an HTML representation using pygments.

            Used in the default template visualization_python.html
        """

        # Get and convert JSON data in Python
        js = get_fs_file_data(self)
        py = json.loads(js)

        # Hooks
        py = self.json2python2html_hook(py)

        # Pretty print the result
        py_str = pprint.pformat(py)

        # Convert to HTML
        return highlight(
            py_str,
            get_lexer_by_name('python'),
            HtmlFormatter()
        )

    def json2python2html_hook(self, data):
        """ Hook used in the json2python2html function.
            Data is a Python structure (from the JSON data).
        """
        return data

    ####################################
    #### RAW DATA TABLE VISUALIZATION
    #### Use the template visualization_datatable_raw.html
    #### If used, you must implement the function format_datatable_raw_data
    ####################################

    def datatable_raw_data(self):
        """ Prepare data for the view """
        data = self.format_datatable_raw_data()

        # convert data.data dictionnaries in lists
        new_data = []
        column_ids = [column['id'] for column in data['columns']]
        for line in data['data']:
            new_data.append(
                [line[c] for c in column_ids]
            )
        data['data_list'] = new_data

        return data

    def format_datatable_raw_data(self):
        """ Format data for the raw data table visualization.
            Must be implemented in subclasses.

            Return a distionnary:  {
                'columns': [
                    {'id': 'code',
                     'name': 'Code',
                     'description': 'Country code',
                    {'id': 'country',
                     'name': 'Country',
                     'description': '',
                     'css_style': 'width: 200px'}},
                    ...
                ],
                'data': [
                    {'code': 'FR',
                     'country': 'France'},
                    {'code': 'IT',
                     'country': 'Italy'},
                    ...
                ],
                # CSS style for the div around the table
                # For example to add an overflow and a fixed height
                # for a big table:
                'container_css_style': 'overflow: scroll; height: 400px'
            }

            Note: use _('text') if you want to translate names
                  and descriptions.
        """

        """ Example if the resource file is a JSON file
        # Get and convert JSON data in Python
        js = get_fs_file_data(self)
        py = json.loads(js)
        <your code to compute data>
        return data
        """
        raise NotImplementedError

    ####################################
    #### RICH DATA TABLE VISUALIZATION
    #### Use the template visualization_datatables_net.html
    #### Use the datatables.net JQuery plugin
    #### If used, you must implement the function format_datatables_net_data
    ####################################

    def datatables_net_data(self):
        """ Prepare data for the view """
        data = self.format_datatables_net_data()

        # convert data.data dictionnaries in lists
        new_data = []
        column_ids = [column['id'] for column in data['columns']]
        for line in data['data']:
            new_data.append(
                [line[c] for c in column_ids]
            )
        data['data_list'] = new_data

        return data

    def format_datatables_net_data(self):
        """ Format data for the rich data table visualization.
            Must be implemented in subclasses.

            Return a distionnary:  {
                'columns': [
                    {'id': 'code',
                     'name': 'Code',
                     'description': 'Country code',
                    {'id': 'country',
                     'name': 'Country',
                     'description': '',
                     'css_style': 'width: 200px'}},
                    ...
                ],
                'data': [
                    {'code': 'FR',
                     'country': 'France'},
                    {'code': 'IT',
                     'country': 'Italy'},
                    ...
                ]
            }

            Note: use _('text') if you want to translate names
                  and descriptions.
        """

        """ Example if the resource file is a JSON file
        # Get and convert JSON data in Python
        js = get_fs_file_data(self)
        py = json.loads(js)
        <your code to compute data>
        return data
        """
        raise NotImplementedError

    ##################################
    #### UNDER THE HOOD
    ##################################

    def get_context_data(self, **kwargs):
        context = super(
            SingleResourceBaseView, self
        ).get_context_data(**kwargs)

        cls = self.__class__

        visualizations = [
            {
                'title': item['title'],
                'description': item['description'],
                'url': reverse(cls.get_view_url_part(cls, item))
            }
            for item in self.visualizations
        ]

        context.update({
            'title': self.title,
            'description': self.description,
            'paternity': self.paternity,
            'external_link': self.external_link,
            'updated': self.updated,
            'territories': self.territories,
            'keywords': self.keywords,
            'thematics': self.thematics,

            'download_url': self.download_url,
            'download_format': self.download_format,
            'filename': cls.get_fs_filename(cls),
            'size': cls.get_fs_file_size(cls),

            'visualizations': visualizations,
            'current_visualization': self.current_visualization
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response, using the `response_class` for this
        view, with a template rendered with the given context.
        If any keyword arguments are provided, they will be
        passed to the constructor of the response class.
        """
        template_name = self.template_name

        if template_name.startswith('<local>'):
            # Get the template from the view folder,
            # not the default templates folders
            # Use resources.loaders.Loader
            template_name = template_name.replace(
                '<local>',
                get_base_fs_dir_path(self)
            )

        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            #template=self.get_template_names(),
            # template_name is passed throught urls.py as_view parameter
            template=template_name,
            context=context,
            **response_kwargs
        )

    # class method
    def get_view_url_part(cls, visualization):
        """ Return the corresponding view url.

        visualization must be an item from self.visualizations

        return for example:
            budgetprimitifnantes2014/datatable
            budgetprimitifnantes2014/python
        """
        return '{}/{}'.format(
            cls.__name__.lower(),
            visualization['url_name']
        )

    # class method
    def get_base_fs_dir_path(cls):
        return os.path.dirname(inspect.getfile(cls))

    # class method
    def get_fs_dir_path(cls):
        return cls.get_base_fs_dir_path(cls) + '/.files'

    # class method
    def get_fs_filename(cls):
        return '{}.{}'.format(cls.__name__.lower(), cls.download_format)

    # class method
    def get_fs_file_path(cls):
        return '{}/{}'.format(
            cls.get_fs_dir_path(cls),
            cls.get_fs_filename(cls)
        )

    # class method
    def get_fs_file_size(cls):
        """ Return file size in Kilobytes """
        return int(os.path.getsize(
            cls.get_fs_file_path(cls)
        ) / 1000)

    # class method
    def get_fs_file_data(cls):
        with open(cls.get_fs_file_path(cls), 'r') as f:
            data = f.read()
        return data

    # class method
    def update_resource(cls):
        """ Download the resource file """

        ### Be sure the .files directory exists
        fs_dir = cls.get_fs_dir_path(cls)
        try:
            os.mkdir(fs_dir)
        except OSError:
            # the directory already exists
            pass

        ### Download the file

        filepath = cls.get_fs_file_path(cls)

        with open(filepath, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(c.URL, cls.download_url)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()

        ### Store the result in the file "result.json"

        filename = cls.get_fs_filename(cls)

        result = {
            'updated': datetime.now().isoformat(),
            'files': [filename]
        }

        with open('{}/result.json'.format(fs_dir), 'w') as f:
            f.write(json.dumps(result))
