# -*- coding: utf-8 -*-
import datetime
import time
import uuid

import pytz

from odoo import models, fields, api


class ContractModel(models.Model):
    # Header
    _name = "crm.customer.contract"
    _description = "Crm customer contract manage"
    _sql_constraints = [
        ('uniq_biz_id', 'unique (biz_id)', 'The bizId of the contract must be unique per company!')
    ]

    # Fields
    biz_id = fields.Char('Biz ID', required=True)
    company_id = fields.Many2one('res.partner', string="Company",
                                 domain="[('is_company', '=', True)]",
                                 required=True)
    account_id = fields.Char('Account ID', required=True, index=True)
    expire_date = fields.Date('Expire date', store=False, default=lambda s: fields.Date.context_today(s),
                              compute="_compute_expire_date")
    expire_at = fields.Long('Expire at', required=True, invisible=True)
    state = fields.Selection([('ENABLE', 'ENABLE'), ('DISABLE', 'DISABLE')], 'State')

    # Method
    @api.depends('expire_at')
    def _compute_expire_date(self):
        for record in self:
            if record.expire_at:
                date = datetime.datetime.fromtimestamp(record.expire_at)
                record.expire_date = date

    @api.onchange('company_id')
    def _on_user_id_change(self):
        for record in self:
            record.account_id = str(record.company_id.id)

    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            bizId = str(uuid.uuid4())
            record['biz_id'] = bizId
            timeStr = record['expire_date']
            record['expire_at'] = int(time.mktime(time.strptime(timeStr, "%Y-%m-%d")))
        return super(ContractModel, self).create(vals_list)

    def write(self, vals):
        if 'expire_date' in vals:
            timeStr = vals['expire_date']
            vals['expire_at'] = int(time.mktime(time.strptime(timeStr, "%Y-%m-%d")))
        return super(ContractModel, self).write(vals)
