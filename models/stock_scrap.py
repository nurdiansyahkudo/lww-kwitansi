from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero

class StockScrap(models.Model):
    _inherit = "stock.scrap"

    lot_ids = fields.Many2many(
        'stock.lot', string='Lots/Serials',
        domain="[('product_id', '=', product_id), ('product_qty', '>', 0)]", 
        check_company=True
    )
    # lot_id = fields.Many2one(
    #     'stock.lot', 'Lot/Serial',
    #     domain="[('product_id', '=', product_id), ('product_qty', '>', 0)]", check_company=True
    # )
    scrap_qty = fields.Float(
        'Quantity', required=True, digits='Product Unit of Measure',
        compute='_compute_scrap_qty', default=1.0, readonly=False, store=True
    )

    @api.depends('lot_ids.product_qty')  # Mendengar perubahan pada lot_ids
    def _compute_scrap_qty(self):
        for scrap in self:
            if scrap.lot_ids:
                # Hitung total quantity berdasarkan lot yang dipilih
                total_qty = sum(lot.product_qty for lot in scrap.lot_ids)
                scrap.scrap_qty = total_qty
            else:
                scrap.scrap_qty = 0

    @api.onchange('lot_ids')  # Menangani perubahan pada lot_ids
    def _onchange_lot_ids(self):
        if self.lot_ids:
            # Hitung total quantity berdasarkan lot yang dipilih
            total_qty = sum(lot.product_qty for lot in self.lot_ids)
            self.scrap_qty = total_qty
        else:
            self.scrap_qty = 0

    def action_validate(self):
        # Remove ensure_one() since we might process multiple scrap records
        total_available_qty = sum(lot.product_qty for lot in self.lot_ids)

        if float_is_zero(self.scrap_qty, precision_rounding=self.product_uom_id.rounding):
            raise UserError(_('You can only enter positive quantities.'))

        if total_available_qty >= self.scrap_qty:
            # If multiple lots exist, create multiple scrap records
            remaining_qty = self.scrap_qty
            scrap_records = self.env['stock.scrap']
            
            for lot in self.lot_ids:
                if remaining_qty <= 0:
                    break

                qty_to_scrap = min(lot.product_qty, remaining_qty)
                remaining_qty -= qty_to_scrap

                scrap_record = self.copy({
                    'scrap_qty': qty_to_scrap,
                    'lot_id': lot.id,
                })
                scrap_records += scrap_record

            # Validate each scrap record separately
            for scrap in scrap_records:
                scrap.action_validate()

            return True  # Return success

        else:
            # Handle insufficient quantity case
            ctx = dict(self.env.context)
            ctx.update({
                'default_product_id': self.product_id.id,
                'default_location_id': self.location_id.id,
                'default_scrap_id': self.id,
                'default_quantity': self.product_uom_id._compute_quantity(self.scrap_qty, self.product_id.uom_id),
                'default_product_uom_name': self.product_id.uom_name
            })
            return {
                'name': _('%(product)s: Insufficient Quantity To Scrap', product=self.product_id.display_name),
                'view_mode': 'form',
                'res_model': 'stock.warn.insufficient.qty.scrap',
                'view_id': self.env.ref('stock.stock_warn_insufficient_qty_scrap_form_view').id,
                'type': 'ir.actions.act_window',
                'context': ctx,
                'target': 'new'
            }