from odoo import models, fields, api
from odoo.exceptions import ValidationError
from num2words import num2words

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    name = fields.Char('Order Reference', 
        required=True, 
        index='trigram', 
        copy=False, 
        default=lambda self: self._get_next_sequence()
    )
    no_po = fields.Char(string='Order Number', store=True, required=True)

    @api.model
    def _get_next_sequence(self):
        """ Generate the next Sequence when click New """
        return self.env['ir.sequence'].next_by_code('purchase.order') or 'New'

    def action_print_report(self):
        company = self.env['res.company'].browse(self.env.company.id)
        
        if company.name == 'PT. BINA SERVICE':
            return self.env.ref('lww_kwitansi.action_report_bs_po').report_action(self)
        elif company.name == 'PT. SPARTADUA RIBUJAYA':
            return self.env.ref('lww_kwitansi.action_report_spartadua_po').report_action(self)
        else:
            # Jika perusahaan tidak cocok dengan ketiganya, menggunakan laporan default
            return self.env.ref('lww_kwitansi.action_report_limawira_po').report_action(self)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'no_po' in vals and vals['no_po']:
                existing_record = self.env['purchase.order'].search([
                    ('no_po', '=', vals['no_po'])
                ], limit=1)
                if existing_record:
                    raise ValidationError('PO Sudah Ada!')
        return super().create(vals_list)

    def write(self, vals):
        if 'no_po' in vals and vals['no_po']:
            for record in self:
                existing_record = self.env['purchase.order'].search([
                    ('no_po', '=', vals['no_po']),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing_record:
                    raise ValidationError('Kwitansi already exist!')
        return super().write(vals)
    
    def get_print_report_name(self):
        return 'Purchase Order - %s' % (self.no_po)
