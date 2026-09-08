# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Purchasing (BRIN) през sql.create_index.
"""
from odoo import models
from odoo.tools import sql


class PurchaseOrder(models.Model):
    """BRIN indexes for purchase_order."""
    _inherit = 'purchase.order'

    def init(self):
        # 18.0: `models.Index` е 19-only descriptor (в 18 ядрото няма
        # такъв клас, нито `_sql_indexes`) → индексите се създават в
        # init() през sql.create_index, което е идемпотентно.
        super().init()
        for column in ("date_order", "date_approve", "create_date"):
            # Проверката е срещу РЕАЛНАТА схема, не срещу self._fields:
            # при делегиращо наследяване (_inherits) полето съществува в ORM,
            # но колоната е в таблицата на родителя (напр.
            # account.bank.statement.line.date живее в account_move).
            if not sql.column_exists(self.env.cr, self._table, column):
                continue
            sql.create_index(
                self.env.cr, f"{self._table}__{column}_brin",
                self._table, [column], method="brin")


class PurchaseOrderLine(models.Model):
    """BRIN indexes for purchase_order_line."""
    _inherit = 'purchase.order.line'

    def init(self):
        # 18.0: `models.Index` е 19-only descriptor (в 18 ядрото няма
        # такъв клас, нито `_sql_indexes`) → индексите се създават в
        # init() през sql.create_index, което е идемпотентно.
        super().init()
        for column in ("date_planned", "create_date"):
            # Проверката е срещу РЕАЛНАТА схема, не срещу self._fields:
            # при делегиращо наследяване (_inherits) полето съществува в ORM,
            # но колоната е в таблицата на родителя (напр.
            # account.bank.statement.line.date живее в account_move).
            if not sql.column_exists(self.env.cr, self._table, column):
                continue
            sql.create_index(
                self.env.cr, f"{self._table}__{column}_brin",
                self._table, [column], method="brin")
