# -*- coding: utf-8 -*-
import datetime
import logging
import time
import uuid

import grpc

from odoo.exceptions import ValidationError, UserError
from rpc import contract_service_pb2
from rpc import contract_service_pb2_grpc

from odoo import models, fields, api

logger = logging.getLogger(__name__)


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
    account_biz_id = fields.Char('Account Biz ID', required=True, index=True)
    expire_date = fields.Date('Expire date', store=False, default=lambda s: fields.Date.context_today(s),
                              compute="_compute_expire_date")
    expire_at = fields.Long('Expire at', required=True, invisible=True)
    state = fields.Selection([('ENABLE', 'ENABLE'), ('DISABLE', 'DISABLE')], 'State')

    @api.onchange("company_id")
    def _on_change_company(self):
        for record in self:
            self.account_biz_id = None
            if record.company_id.account_biz_id:
                self.account_biz_id = record.company_id.account_biz_id

    # Method
    @api.depends('expire_at')
    def _compute_expire_date(self):
        for record in self:
            if record.expire_at:
                date = datetime.datetime.fromtimestamp(record.expire_at)
                record.expire_date = date

    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            count = self.search_count(domain=[('account_biz_id', '=', record['account_biz_id'])])
            if count > 0:
                raise ValidationError("Account data is already exist : %s" % record['account_biz_id'])

            bizId = str(uuid.uuid4())
            record['biz_id'] = bizId
            timeStr = record['expire_date']
            record['expire_at'] = int(time.mktime(time.strptime(timeStr, "%Y-%m-%d")))
        records = super(ContractModel, self).create(vals_list)

        for record in vals_list:
            dto = {
                'biz_id': record['biz_id'],
                'account_id': record['account_biz_id'],
                'expired_time': record['expire_at'],
                'state': 'ENABLE'
            }
            self.create_approval(dto)
        return records

    def write(self, vals):
        if 'expire_date' in vals:
            timeStr = vals['expire_date']
            vals['expire_at'] = int(time.mktime(time.strptime(timeStr, "%Y-%m-%d")))
        dto = {
            'biz_id': self.biz_id,
            'account_id': self.account_biz_id,
            'expired_time': vals['expire_at'] if 'expire_at' in vals.keys() else self.expire_at,
            'state': vals['state'] if 'state' in vals.keys() else self.state
        }
        self.create_approval(dto)

    def do_write(self, vals):
        return super(ContractModel, self).write(vals)

    def create_approval(self, dto):
        result = False
        try:
            req = contract_service_pb2.CreateContractApprovalReq()
            req.biz_id = dto['biz_id']
            req.account_id = dto['account_id']
            req.expired_time = dto['expired_time']
            req.state = dto['state'];
            req.email = self.env.user['email']

            channel = grpc.insecure_channel("{0}:{1}".format('localhost', '31082'))
            client = contract_service_pb2_grpc.ContractServiceStub(channel=channel)

            rsp = client.CreateContractApproval(req)
            logger.info('Create contract config approval,rsp:%s result:%s', rsp, result)
            result = True
        except Exception as e:
            logger.error('Contract config submit approval failed, e:', e)
            raise UserError("Contract config submit approval failed")
        return result
