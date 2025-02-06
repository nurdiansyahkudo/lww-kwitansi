from odoo import models, fields, api
from odoo.exceptions import ValidationError
from num2words import num2words

class StockPicking(models.Model):
    _inherit = "stock.picking"

    no_do = fields.Char(string='DO Number', store=True, required=True)

    def action_print_report(self):
        company = self.env['res.company'].browse(self.env.company.id)
        
        if company.name == 'PT. BINA SERVICE':
            return self.env.ref('lww_kwitansi.action_report_bs_do').report_action(self)
        elif company.name == 'PT. SPARTADUA RIBUJAYA':
            return self.env.ref('lww_kwitansi.action_report_spartadua_do').report_action(self)
        else:
            # Jika perusahaan tidak cocok dengan ketiganya, menggunakan laporan default
            return self.env.ref('lww_kwitansi.action_report_limawira_do').report_action(self)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'no_do' in vals and vals['no_do']:
                existing_record = self.env['stock_picking'].search([
                    ('no_do', '=', vals['no_do'])
                ], limit=1)
                if existing_record:
                    raise ValidationError('DO Sudah Ada!')
        return super().create(vals_list)

    def write(self, vals):
        if 'no_do' in vals and vals['no_do']:
            for record in self:
                existing_record = self.env['stock_picking'].search([
                    ('no_do', '=', vals['no_do']),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing_record:
                    raise ValidationError('DO Sudah Ada!')
        return super().write(vals)
    
    def get_print_report_name(self):
        return 'Purchase Order - %s' % (self.no_do)
