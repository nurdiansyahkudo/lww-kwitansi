# -*- coding: utf-8 -*-
{
    'name': "Limawira Kwitansi",
    'summary': '',
    'author': '',
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': ['base', 'sale', 'account', 'stock'],
    'data': [
        # KWITANSI
        'report/lww_kwitansi_report.xml',
        'views/lww_kwitansi_template.xml',
        'views/bs_kwitansi_template.xml',
        'views/spartadua_kwitansi_template.xml',
        # FORM VIEW
        'views/account_payment_view.xml',
        # 'views/header_template.xml',
    ],
    'installable': True,
    'application': False,
}

