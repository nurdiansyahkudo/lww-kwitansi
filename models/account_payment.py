from odoo import models, fields, api
from odoo.exceptions import ValidationError
from num2words import num2words

class AccountPayment(models.Model):
    _inherit = "account.payment"

    amount_to_word = fields.Char(string='Amount in Words', compute='_compute_amount_to_word')
    no_kwitansi = fields.Char(string='No. Kwitansi')

    def action_print_report(self):
      company = self.env['res.company'].browse(self.env.company.id)
      if company.name == 'PT. LIMAWIRA WISESA':
          return self.env.ref('lww_kwitansi.action_report_limawira_kwitansi').report_action(self)
      return self.env.ref('lww_kwitansi.action_report_bs_kwitansi').report_action(self)

    @api.depends('amount', 'currency_id')
    def _compute_amount_to_word(self):
        for record in self:
            if record.amount:
                try:
                    amount_integer = int(record.amount)
                    words = num2words(amount_integer, lang='id').capitalize()
                    record.amount_to_word = f"{words} rupiah"
                except Exception as e:
                    record.amount_to_word = 'Error: %s' % e

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'no_kwitansi' in vals and vals['no_kwitansi']:
                existing_record = self.env['account.payment'].search([
                    ('no_kwitansi', '=', vals['no_kwitansi'])
                ], limit=1)
                if existing_record:
                    raise ValidationError('Kwitansi already exist!')
        return super().create(vals_list)

    def write(self, vals):
        if 'no_kwitansi' in vals and vals['no_kwitansi']:
            for record in self:
                existing_record = self.env['account.payment'].search([
                    ('no_kwitansi', '=', vals['no_kwitansi']),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing_record:
                    raise ValidationError('Kwitansi already exist!')
        return super().write(vals)
    
    def get_print_report_name(self):
        return 'Kwitansi - %s' % (self.name)
