# -*- coding: utf-8 -*-
{
    'name': "Limawira PDF",
    'summary': '',
    'author': '',
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': ['base', 'purchase', 'sale', 'account', 'stock'],
    'data': [
        # KWITANSI
        'report/lww_kwitansi_report.xml',
        'views/lww_kwitansi_template.xml',
        'views/bs_kwitansi_template.xml',
        'views/spartadua_kwitansi_template.xml',
        # PURCHASE ORDER
        'report/lww_po_report.xml',
        'views/lww_po_template.xml',
        'views/bs_po_template.xml',
        'views/spartadua_po_template.xml',
        # RECEIPT GOODS
        'report/lww_receipt_report.xml',
        'views/lww_receipt_template.xml',
        # 'views/bs_receipt_template.xml',
        # 'views/spartadua_receipt_template.xml',
        # DELIVERY ORDER
        'report/lww_do_report.xml',
        'views/lww_do_template.xml',
        'views/bs_do_template.xml',
        # 'views/spartadua_do_template.xml',
        # FORM VIEW
        'views/account_payment_view.xml',
        'views/purchase_order_view.xml',
        'views/stock_picking_view.xml',
        'views/stock_scrap_views.xml',
        # 'views/header_template.xml',
    ],
    'installable': True,
    'application': False,
}

