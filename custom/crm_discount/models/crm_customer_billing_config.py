# -*- coding: utf-8 -*-
import uuid
import grpc
import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from rpc import billing_config_service_pb2
from rpc import billing_config_service_pb2_grpc

logger = logging.getLogger(__name__)


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

    @api.onchange("company_id")
    def _on_change_company(self):
        for record in self:
            self.account_biz_id = None
            if record.company_id.account_biz_id:
                self.account_biz_id = record.company_id.account_biz_id

    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            count = self.search_count(domain=[('account_biz_id', '=', record['account_biz_id'])])
            if count > 0:
                raise ValidationError("Account data is already exist : %s" % record['account_biz_id'])
            bizId = str(uuid.uuid4())
            record['biz_id'] = bizId
            record['state'] = 'DISABLE'
        records = super(BillingConfigModel, self).create(vals_list)

        for record in vals_list:
            dto = {
                'biz_id': record['biz_id'],
                'account_id': record['account_biz_id'],
                'month_upper_limit': record['month_upper_limit'],
                'state': 'ENABLE'
            }
            self.create_approval(dto)

        return records

    def write(self, vals):
        dto = {
            'biz_id': self.biz_id,
            'account_biz_id': self.account_biz_id,
            'month_upper_limit': vals[
                'month_upper_limit'] if 'month_upper_limit' in vals.keys() else self.month_upper_limit,
            'state': vals['state'] if 'state' in vals.keys() else self.state
        }
        return self.create_approval(dto)

    def do_write(self, vals):
        return super(BillingConfigModel, self).write(vals)

    def create_approval(self, dto):
        result = False
        try:
            req = billing_config_service_pb2.CreateBillingConfigApprovalReq()
            req.biz_id = dto['biz_id']
            req.account_id = dto['account_id']
            req.month_upper_limit = dto['month_upper_limit']
            req.state = dto['state']
            req.email = self.env.user['email']

            channel = grpc.insecure_channel("{0}:{1}".format('localhost', '31082'))
            client = billing_config_service_pb2_grpc.BillingConfigServiceStub(channel=channel)
            rsp = client.CreateBillingConfigApproval(req)
            result = True
            logger.info('Create billing config approval,rsp:%s result:%s', rsp, result)
        except Exception as e:
            logger.error('Billing config submit approval failed, e:', e)
            raise UserError("Billing config submit approval failed")
        return result
