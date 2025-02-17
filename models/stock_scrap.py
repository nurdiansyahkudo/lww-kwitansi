from odoo import models, fields, api

class StockScrap(models.Model):
    _inherit = "stock.scrap"

    lot_ids = fields.Many2many(
        'stock.lot', string='Lots/Serials',
        domain="[('product_id', '=', product_id), ('product_qty', '>', 0)]", 
        check_company=True
    )