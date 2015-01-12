#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from django.utils.translation import ugettext_lazy as _

from resources.views import SingleResourceBaseView
from resources.views import get_fs_file_data


class BudgetPrimitifNantes2014(SingleResourceBaseView):

    ##################################
    #### DESCRIPTION
    ##################################

    title = u'Budget primitif (BP) 2014 de la Ville de Nantes'

    description = u"""Le jeu contient le budget primitif 2014 du budget
    principal de la Ville de Nantes.
    <br /><br />
    Le budget primitif, voté annuellement, constitue la prévision des dépenses
    et des recettes pour l'année. Il est nécessairement équilibré et vaut
    autorisation d'exécution.
    <br /><br />
    La nomenclature comptable du budget principal de la commune est
    l'instruction M14 depuis le 1er janvier 1997. Le budget est voté par nature
    comptable au niveau des chapitres. Les chapitres budgétaires (exemple : 012
    « charges de personnel », 73 « impôts et taxes », 23 immobilisations en
    cours », etc.) regroupent un ensemble d'articles comptables sur lesquels
    portent l'affectation des crédits et l'exécution du budget.
    <br /><br />
    Le budget primitif fait l'objet d'une présentation croisée par fonction.
    Chaque sous-fonction précise l'origine d'une recette ou la destination
    d'une dépense (exemple : 413 « piscines », 33 « action culturelle »,
    etc.).
    <br /><br />
    Par ailleurs, il permet :
    <ul>
    <li> la distinction entre les dépenses et les recettes (colonne D_R), </li>
    <li> l'identification de la section (fonctionnement ou investissement) dans
    la colonne I_F : la section de fonctionnement (F) enregistre les opérations
    courantes qui se renouvellent régulièrement et constituent des charges et
    des produits à caractère définitif (charges de personnel, fournitures,
    intérêts de la dette, prestations de services, …) ; la section
    d'investissement (I) retrace les opérations relatives au patrimoine de la
    Ville (acquisitions, ventes, travaux,…). Ces opérations sont souvent
    étalées sur plusieurs années.
    <li> la séparation entre les dépenses (ou recettes) réelles et les
    dépenses (ou recettes) d'ordre (colonne ORDRE_O_N) : les dépenses
    (recettes) budgétaires sont composées des dépenses (recettes) réelles et
    des dépenses (recettes) d'ordre. Les dépenses (recettes) d'ordre
    correspondent à des écritures n'impliquant ni encaissement, ni décaissement
    effectif. Il s'agit, par exemple, des dotations aux amortissements. Au
    contraire des opérations d'ordre, les dépenses (recettes) réelles donnent
    lieu à des mouvements de fonds.
    </ul>
    """

    paternity = u'Ville de Nantes, Open Database License (ODbL)'

    external_link = u'http://data.nantes.fr/donnees/detail/' \
        'budget-primitif-bp-2014-de-la-ville-de-nantes/'

    updated = '18/02/2014'

    territories = ['France', 'Pays de la Loire', 'Loire Atlantique', 'Nantes']

    keywords = ['Budget', 'Budget primitif']

    thematics = ['Citoyenneté / Institution', 'Finance']

    ##################################
    #### DOWNLOAD PARAMETERS
    ##################################

    download_url = 'http://data.nantes.fr/api/publication/' \
        '24440040400129_VDN_VDN_00114/BP_2014_VDN_STBL/content/?format=json'

    download_format = 'json'

    update_frequence = None

    ##################################
    #### VISUALIZATION
    ##################################

    visualizations = [

        {'title': 'Graphiques',
         'description': "Présentation graphique des données.",
         'url_name': 'highcharts',
         'template_name':
            '<local>/visualization_highcharts.html'},

        {'title': 'Table de données riche',
         'description': "Présentation sous la forme d'un tableau de données "
                        "riche.",
         'url_name': 'datatables-net',
         'template_name':
            'resources-generic/visualization_datatables_net.html'},

        {'title': 'Table de données brute',
         'description': "Présentation sous la forme d'un tableau de données "
                        "brutes (faites défiler de haut en bas et de gauche "
                        "à droite).",
         'url_name': 'datatable-raw',
         'template_name':
            'resources-generic/visualization_datatable_raw.html'},

        {'title': _('Python'),
         'url_name': 'python',
         'description': "Présentation sous la forme de code Python. <strong>"
                        "Seules les 20 premières lignes de données sont "
                        "affichées.</strong>",
         'template_name': 'resources-generic/visualization_python.html'}
    ]

    ##################################
    #### IMPLEMENTATION
    ##################################

    # Format data for the 'datatables-net' view
    def format_datatables_net_data(self):
        """ See SingleResourceBaseView """
        # Get and convert JSON data in Python
        js = get_fs_file_data(self)
        py = json.loads(js)

        return {
            'columns': [

                {'id': 'EXERCICE',
                 'name': 'Exercice',
                 'description': 'Exercice budgétaire concerné'},

                {'id': 'CODE_CHAPITRE',
                 'name': 'Code chapitre',
                 'description': 'Code du chapitre budgétaire'},

                {'id': 'LIBELLE_CHAPITRE',
                 'name': 'Chapitre',
                 'description': 'Libellé du chapitre budgétaire'},

                {'id': 'CODE_SS_FONCTION',
                 'name': 'Code sous-fonction',
                 'description': 'Code de la sous-fonction de rattachement de '
                                'la dépense ou de la recette'},

                {'id': 'LIBELLE_SS_FONCTION',
                 'name': 'Sous-fonction',
                 'description': 'Libellé de la sous-fonction de rattachement '
                                'de la dépense ou de la recette'},

                {'id': 'CODE_ARTICLE',
                 'name': 'Code article',
                 'description': 'Code article de la dépense ou de la recette'},

                {'id': 'LIBELLE_ARTICLE',
                 'name': 'Article',
                 'description': 'Libellé article de la dépense ou de la '
                                'recette'},

                {'id': 'MONTANT',
                 'name': 'Montant',
                 'description': ''},

                {'id': 'D_R',
                 'name': 'Dépense ou Recette',
                 'description': "Identification du type d'opérations "
                                "budgétaires : D pour dépense, R pour "
                                "recette"},

                {'id': 'I_F',
                 'name': 'Investissement ou Fonctionnement',
                 'description': "Indication sur l'appartenance de la ligne "
                                "budgétaire à la section d'investissement (I) "
                                "ou de fonctionnement (F)"},

                {'id': 'ORDRE_O_N',
                 'name': "Imputation d'ordre Oui/Non",
                 'description': "Imputation d'ordre : O pour oui (dépense "
                                "ou recette d'ordre), N pour non (dépense "
                                "ou recette réelle)"}
            ],
            'data': [line for line in py['data']
                     if line['EXERCICE'] is not None],
            'container_css_style': 'overflow: scroll; height: 500px'
        }

    # Format data for the 'datatable-raw' view
    def format_datatable_raw_data(self):
        """ See SingleResourceBaseView """
        # Get and convert JSON data in Python
        js = get_fs_file_data(self)
        py = json.loads(js)

        return {
            'columns': [

                {'id': 'EXERCICE',
                 'name': 'Exercice',
                 'description': 'Exercice budgétaire concerné'},

                {'id': 'CODE_CHAPITRE',
                 'name': 'Code chapitre',
                 'description': 'Code du chapitre budgétaire'},

                {'id': 'LIBELLE_CHAPITRE',
                 'name': 'Chapitre',
                 'description': 'Libellé du chapitre budgétaire'},

                {'id': 'CODE_SS_FONCTION',
                 'name': 'Code sous-fonction',
                 'description': 'Code de la sous-fonction de rattachement de '
                                'la dépense ou de la recette'},

                {'id': 'LIBELLE_SS_FONCTION',
                 'name': 'Sous-fonction',
                 'description': 'Libellé de la sous-fonction de rattachement '
                                'de la dépense ou de la recette'},

                {'id': 'CODE_ARTICLE',
                 'name': 'Code article',
                 'description': 'Code article de la dépense ou de la recette'},

                {'id': 'LIBELLE_ARTICLE',
                 'name': 'Article',
                 'description': 'Libellé article de la dépense ou de la '
                                'recette'},

                {'id': 'MONTANT',
                 'name': 'Montant',
                 'description': ''},

                {'id': 'D_R',
                 'name': 'Dépense ou Recette',
                 'description': "Identification du type d'opérations "
                                "budgétaires : D pour dépense, R pour "
                                "recette"},

                {'id': 'I_F',
                 'name': 'Investissement ou Fonctionnement',
                 'description': "Indication sur l'appartenance de la ligne "
                                "budgétaire à la section d'investissement (I) "
                                "ou de fonctionnement (F)"},

                {'id': 'ORDRE_O_N',
                 'name': "Imputation d'ordre Oui/Non",
                 'description': "Imputation d'ordre : O pour oui (dépense "
                                "ou recette d'ordre), N pour non (dépense "
                                "ou recette réelle)"}
            ],
            'data': py['data'],
            'container_css_style': 'overflow: scroll; height: 500px'
        }

    # Hook for the 'python' view
    def json2python2html_hook(self, data):
        """ See SingleResourceBaseView """
        # Truncate data to the first 20 lines because there is
        # two many lines to display in the Python visualization
        data['data'] = data['data'][:20]
        return data
