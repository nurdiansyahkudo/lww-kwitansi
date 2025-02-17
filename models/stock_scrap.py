from odoo import models, fields, api

class StockScrapLot(models.Model):
    _name = "stock.scrap.lot"
    _description = "Stock Scrap Lot"

    scrap_id = fields.Many2one('stock.scrap',
                                string="Scrap Reference",
                                required=True,
                                ondelete="cascade"
                               )
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial', required=True, 
                             domain="[('product_id', '=', product_id), ('product_qty', '>', 0)]")
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    scrap_lot_ids = fields.One2many('stock.scrap.lot', 'scrap_id', string='Lot/Serial Numbers')