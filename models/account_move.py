from odoo import models, fields, api
from num2words import num2words
import logging

class AccountMove(models.Model):
    _inherit = "account.move"

    amount_to_word = fields.Char(string='Amount in Words', compute='_compute_amount_to_word', store=False)

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
                'lang': 'en',
                'currency_name': 'euro',
                'currency_plural': 'Euros'
            },
            'GBP': {
                'lang': 'en',
                'currency_name': 'pound',
                'currency_plural': 'Pounds'
            },
            'JPY': {
                'lang': 'en',
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

    @api.depends('amount_total', 'currency_id')
    def _compute_amount_to_word(self):
        for record in self:
            if record.amount_total is not None and record.currency_id:
                try:
                    amount_integer = int(round(record.amount_total, 0))
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
                    _logger = logging.getLogger(__name__)
                    _logger.error(f"Error converting amount to words for currency {currency_code}: {str(e)}")
            else:
                record.amount_to_word = "Amount or currency not set"
                _logger = logging.getLogger(__name__)
                _logger.warning("Amount or currency not set for record %s", record.id)
