from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero

class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    lot_id = fields.Many2one(
        'stock.lot', string='Lots/Serials',
        domain="[('product_id', '=', product_id), ('product_qty', '>', 0)]",
        check_company=True
    )

    scrap_qty = fields.Float(
        'Quantity', required=True, digits='Product Unit of Measure',
        compute='_compute_scrap_qty', default=1.0, readonly=False, store=True
    )

    @api.depends('lot_id.product_qty')  
    def _compute_scrap_qty(self):
        for scrap in self:
            if scrap.lot_id:
                scrap.scrap_qty = sum(lot.product_qty for lot in scrap.lot_id)
            else:
                scrap.scrap_qty = 0

    @api.onchange('lot_id')  
    def _onchange_lot_ids(self):
        if self.lot_id:
            self.scrap_qty = sum(lot.product_qty for lot in self.lot_id)
        else:
            self.scrap_qty = 0
