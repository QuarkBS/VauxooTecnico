# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real Estate',
    'depends': ['base','web'],
    'category': 'Real Estate/Brokerage',
    'data' : [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/estate_data.xml',
        'views/estate_menus.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/inherited_estate_property_users_views.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        ],
}
