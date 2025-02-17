from odoo import models, fields, api

class StockScrapLot(models.Model):
    _name = "stock.scrap.lot"
    _description = "Stock Scrap Lot"

    scrap_id = fields.Many2one(
        'stock.scrap',
        string="Scrap Reference",
        required=True,
        ondelete="cascade"
    )
    product_id = fields.Many2one(
        'product.product', string='Product',
        related="scrap_id.product_id", store=True, readonly=True
    )
    lot_id = fields.Many2one(
        'stock.lot', string='Lot/Serial', required=True,
        domain="[('product_id', '=', product_id), ('product_qty', '>', 0)]"
    )
    quantity = fields.Float(string='Quantity', required=True, default=1.0)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Set domain for lot_id based on selected product"""
        if self.product_id:
            return {
                'domain': {'lot_id': [('product_id', '=', self.product_id.id), ('product_qty', '>', 0)]}
            }
        return {'domain': {'lot_id': []}}

class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    scrap_lot_ids = fields.One2many(
        'stock.scrap.lot', 'scrap_id', string='Lot/Serial Numbers'
    )
    quantity = fields.Float(
        string="Quantity", compute="_compute_total_quantity", store=True
    )

    @api.depends('scrap_lot_ids.quantity')
    def _compute_total_quantity(self):
        for scrap in self:
            scrap.quantity = sum(scrap.scrap_lot_ids.mapped('quantity'))
