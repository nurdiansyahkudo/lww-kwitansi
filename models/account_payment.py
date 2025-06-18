from odoo import models, fields, api
from odoo.exceptions import ValidationError
from num2words import num2words

class AccountPayment(models.Model):
    _inherit = "account.payment"

    amount_to_word = fields.Char(string='Amount in Words', compute='_compute_amount_to_word', store=True)
    no_kwitansi = fields.Char(string='No. Kwitansi', store=True)

    def action_print_report(self):
        company = self.env['res.company'].browse(self.env.company.id)
        
        if company.name == 'PT. BINA SERVICE':
            return self.env.ref('lww_kwitansi.action_report_bs_kwitansi').report_action(self)
        elif company.name == 'PT. SPARTADUA RIBUJAYA':
            return self.env.ref('lww_kwitansi.action_report_spartadua_kwitansi').report_action(self)
        else:
            # Jika perusahaan tidak cocok dengan ketiganya, menggunakan laporan default
            return self.env.ref('lww_kwitansi.action_report_limawira_kwitansi').report_action(self)

    def _get_currency_config(self, currency_code):
        currency_mapping = {
            'IDR': {
                'lang': 'id',
                'currency_name': 'rupiah',
                'currency_plural': 'Rupiah'
            },
            'USD': {
                'lang': 'en',
                'currency_name': 'dollar',
                'currency_plural': 'Dollars'
            },
            'EUR': {
                'lang': 'en',  # num2words doesn't have native EUR support, use English
                'currency_name': 'euro',
                'currency_plural': 'Euros'
            },
            'GBP': {
                'lang': 'en',
                'currency_name': 'pound',
                'currency_plural': 'Pounds'
            },
            'JPY': {
                'lang': 'en',  # Japanese not commonly supported in num2words
                'currency_name': 'yen',
                'currency_plural': 'Yen'
            },
            'SGD': {
                'lang': 'en',
                'currency_name': 'singapore dollar',
                'currency_plural': 'Singapore Dollars'
            },
            'MYR': {
                'lang': 'en',
                'currency_name': 'ringgit',
                'currency_plural': 'Ringgit'
            },
            'CNY': {
                'lang': 'en',
                'currency_name': 'yuan',
                'currency_plural': 'Yuan'
            },
            'AUD': {
                'lang': 'en',
                'currency_name': 'australian dollar',
                'currency_plural': 'Australian Dollars'
            },
            'CAD': {
                'lang': 'en',
                'currency_name': 'canadian dollar',
                'currency_plural': 'Canadian Dollars'
            }
        }
        
        return currency_mapping.get(currency_code, {
            'lang': 'en',
            'currency_name': currency_code.lower(),
            'currency_plural': currency_code.lower()
        })

    @api.depends('amount', 'currency_id')
    def _compute_amount_to_word(self):
        for record in self:
            if record.amount is not None and record.currency_id:
                try:
                    amount_integer = int(round(record.amount, 0))
                    currency_code = record.currency_id.name or 'IDR'
                    
                    currency_config = self._get_currency_config(currency_code)
                
                    words = num2words(amount_integer, lang=currency_config['lang'])
                    
                    if currency_config['lang'] == 'id':
                        words = words.capitalize()
                    else:
                        words = ' '.join(word.capitalize() if word.lower() not in ['and', 'of', 'the'] else word.lower() 
                                       for word in words.split())
                    
                    if amount_integer == 1:
                        currency_name = currency_config['currency_name']
                    else:
                        currency_name = currency_config['currency_plural']
                    
                    if currency_config['lang'] == 'id':
                        record.amount_to_word = f"{words} {currency_name}"
                    else:
                        record.amount_to_word = f"{words} {currency_name.title()}"
                    
                except Exception as e:
                    record.amount_to_word = f"Error: {str(e)}"
                    import logging
                    _logger = logging.getLogger(__name__)
                    _logger.error(f"Error converting amount to words for currency {currency_code}: {str(e)}")
            else:
                record.amount_to_word = "Amount or currency not set"
                import logging
                _logger = logging.getLogger(__name__)
                _logger.warning("Amount or currency not set for record %s", record.id)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'no_kwitansi' in vals and vals['no_kwitansi']:
                existing_record = self.env['account.payment'].search([
                    ('no_kwitansi', '=', vals['no_kwitansi'])
                ], limit=1)
                if existing_record:
                    raise ValidationError('Kwitansi Sudah Ada!')
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
        return 'Kwitansi - %s' % (self.no_kwitansi)