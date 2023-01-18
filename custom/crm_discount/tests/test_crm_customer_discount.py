# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestDiscount(TransactionCase):
    def test_create(self):
        print("A simple discount test")
        Discount = self.env['crm.customer.billing.config']
        task = Discount.create(
            {'biz_id': 'test001', 'account_id': 'account_001', 'month_upper_limit': '112', 'state': 'ENABLE'})
        self.assertEqual(task.is_done, False)
