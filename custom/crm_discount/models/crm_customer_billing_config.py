# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api


class BillingConfigModel(models.Model):
    _name = 'crm.customer.billing.config'
    _description = 'Crm customer billing config manage'
    _sql_constraints = [
        ('uniq_biz_id', 'unique (biz_id)', 'The bizId of the discount must be unique for per company !')
    ]

    # fields
    biz_id = fields.Char('Biz ID', required=True)
    company_id = fields.Many2one('res.partner', string="Company",
                                 domain="[('is_company', '=', True)]",
                                 required=True)
    account_biz_id = fields.Char('Account Biz ID', required=True)
    month_upper_limit = fields.Long('Month upper limit', default=0)
    state = fields.Selection([('ENABLE', 'ENABLE'), ('DISABLE', 'DISABLE')], 'State', default='DISABLE')

    # methods
    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            bizId = str(uuid.uuid4())
            record['biz_id'] = bizId
        return super(BillingConfigModel, self).create(vals_list)

    def write(self, vals):
        return super(BillingConfigModel, self).write(vals)
