from odoo import models, fields, api
from num2words import num2words

class AccountPayment(models.Model):
    _inherit = "account.payment"

    amount_to_word = fields.Char(string='Amount in Words', compute='_compute_amount_to_word')

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
    
    def get_print_report_name(self):
        return 'Kwitansi - %s' % (self.name)
