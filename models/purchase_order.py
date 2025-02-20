from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    name = fields.Char(
        'Order Reference',
        required=True,
        index='trigram',
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('purchase.order') or '/'
    )
    no_po = fields.Char(string='Order Number', store=True, required=True)

    def action_print_report(self):
        company = self.env['res.company'].browse(self.env.company.id)
        
        if company.name == 'PT. BINA SERVICE':
            return self.env.ref('lww_kwitansi.action_report_bs_po').report_action(self)
        elif company.name == 'PT. SPARTADUA RIBUJAYA':
            return self.env.ref('lww_kwitansi.action_report_spartadua_po').report_action(self)
        else:
            return self.env.ref('lww_kwitansi.action_report_limawira_po').report_action(self)

    @api.model_create_multi
    def create(self, vals_list):
        orders = self.browse()
        partner_vals_list = []
        for vals in vals_list:
            company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
            self_comp = self.with_company(company_id)

            # **Perbaikan utama di sini**
            # Cek jika 'name' sudah berupa sequence, jika belum maka buat baru
            if not vals.get('name') or vals.get('name') == 'New':
                seq_date = vals.get('date_order')
                if seq_date:
                    seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(seq_date))
                vals['name'] = self_comp.env['ir.sequence'].next_by_code('purchase.order', sequence_date=seq_date) or '/'

            # Cek apakah 'no_po' sudah ada sebelumnya
            if 'no_po' in vals and vals['no_po']:
                existing_record = self.env['purchase.order'].search([
                    ('no_po', '=', vals['no_po'])
                ], limit=1)
                if existing_record:
                    raise ValidationError('PO Sudah Ada!')

            vals, partner_vals = self._write_partner_values(vals)
            partner_vals_list.append(partner_vals)
            orders |= super(PurchaseOrder, self_comp).create(vals)

        for order, partner_vals in zip(orders, partner_vals_list):
            if partner_vals:
                order.sudo().write(partner_vals)

        return orders

    def write(self, vals):
        if 'no_po' in vals and vals['no_po']:
            for record in self:
                existing_record = self.env['purchase.order'].search([
                    ('no_po', '=', vals['no_po']),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing_record:
                    raise ValidationError('PO already exist!')
        return super().write(vals)
    
    def get_print_report_name(self):
        return 'Purchase Order - %s' % (self.no_po)
