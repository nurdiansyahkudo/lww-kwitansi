from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = "stock.scrap"

    lot_id = fields.Many2one(
        'stock.lot', 'Lot/Serial',
        domain="[('product_id', '=', product_id), ('product_qty', '>', 0)]", 
        check_company=True
    )