# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Stock (BRIN) през sql.create_index.
"""
from odoo import models
from odoo.tools import sql


class StockMoveLine(models.Model):
    """BRIN indexes for stock_move_line - high volume table."""
    _inherit = 'stock.move.line'

    def init(self):
        # 18.0: `models.Index` е 19-only descriptor (в 18 ядрото няма
        # такъв клас, нито `_sql_indexes`) → индексите се създават в
        # init() през sql.create_index, което е идемпотентно.
        super().init()
        for column in ("date", "create_date"):
            # Проверката е срещу РЕАЛНАТА схема, не срещу self._fields:
            # при делегиращо наследяване (_inherits) полето съществува в ORM,
            # но колоната е в таблицата на родителя (напр.
            # account.bank.statement.line.date живее в account_move).
            if not sql.column_exists(self.env.cr, self._table, column):
                continue
            sql.create_index(
                self.env.cr, f"{self._table}__{column}_brin",
                self._table, [column], method="brin")


class StockMove(models.Model):
    """BRIN indexes for stock_move."""
    _inherit = 'stock.move'

    def init(self):
        # 18.0: `models.Index` е 19-only descriptor (в 18 ядрото няма
        # такъв клас, нито `_sql_indexes`) → индексите се създават в
        # init() през sql.create_index, което е идемпотентно.
        super().init()
        for column in ("date", "create_date"):
            # Проверката е срещу РЕАЛНАТА схема, не срещу self._fields:
            # при делегиращо наследяване (_inherits) полето съществува в ORM,
            # но колоната е в таблицата на родителя (напр.
            # account.bank.statement.line.date живее в account_move).
            if not sql.column_exists(self.env.cr, self._table, column):
                continue
            sql.create_index(
                self.env.cr, f"{self._table}__{column}_brin",
                self._table, [column], method="brin")


class StockQuant(models.Model):
    """BRIN index for stock_quant - Critical for FIFO/FEFO costing."""
    _inherit = 'stock.quant'

    def init(self):
        # Critical for FIFO/FEFO
        # 18.0: `models.Index` е 19-only descriptor (в 18 ядрото няма
        # такъв клас, нито `_sql_indexes`) → индексите се създават в
        # init() през sql.create_index, което е идемпотентно.
        super().init()
        for column in ("in_date", "create_date"):
            # Проверката е срещу РЕАЛНАТА схема, не срещу self._fields:
            # при делегиращо наследяване (_inherits) полето съществува в ORM,
            # но колоната е в таблицата на родителя (напр.
            # account.bank.statement.line.date живее в account_move).
            if not sql.column_exists(self.env.cr, self._table, column):
                continue
            sql.create_index(
                self.env.cr, f"{self._table}__{column}_brin",
                self._table, [column], method="brin")


class StockLot(models.Model):
    """BRIN indexes for stock_lot - important for FEFO."""
    _inherit = 'stock.lot'

    def init(self):
        # Critical for FEFO expiration management
        # 18.0: `models.Index` е 19-only descriptor (в 18 ядрото няма
        # такъв клас, нито `_sql_indexes`) → индексите се създават в
        # init() през sql.create_index, което е идемпотентно.
        super().init()
        for column in ("create_date", "expiration_date"):
            # Проверката е срещу РЕАЛНАТА схема, не срещу self._fields:
            # при делегиращо наследяване (_inherits) полето съществува в ORM,
            # но колоната е в таблицата на родителя (напр.
            # account.bank.statement.line.date живее в account_move).
            if not sql.column_exists(self.env.cr, self._table, column):
                continue
            sql.create_index(
                self.env.cr, f"{self._table}__{column}_brin",
                self._table, [column], method="brin")


class StockPicking(models.Model):
    """BRIN indexes for stock_picking."""
    _inherit = 'stock.picking'

    def init(self):
        # 18.0: `models.Index` е 19-only descriptor (в 18 ядрото няма
        # такъв клас, нито `_sql_indexes`) → индексите се създават в
        # init() през sql.create_index, което е идемпотентно.
        super().init()
        for column in ("scheduled_date", "date_done"):
            # Проверката е срещу РЕАЛНАТА схема, не срещу self._fields:
            # при делегиращо наследяване (_inherits) полето съществува в ORM,
            # но колоната е в таблицата на родителя (напр.
            # account.bank.statement.line.date живее в account_move).
            if not sql.column_exists(self.env.cr, self._table, column):
                continue
            sql.create_index(
                self.env.cr, f"{self._table}__{column}_brin",
                self._table, [column], method="brin")


class StockValuationLayer(models.Model):
    """BRIN index for stock_valuation_layer - grows fast with AVCO/FIFO."""
    _inherit = 'stock.valuation.layer'

    def init(self):
        # 18.0: `models.Index` е 19-only descriptor (в 18 ядрото няма
        # такъв клас, нито `_sql_indexes`) → индексите се създават в
        # init() през sql.create_index, което е идемпотентно.
        super().init()
        for column in ("create_date",):
            # Проверката е срещу РЕАЛНАТА схема, не срещу self._fields:
            # при делегиращо наследяване (_inherits) полето съществува в ORM,
            # но колоната е в таблицата на родителя (напр.
            # account.bank.statement.line.date живее в account_move).
            if not sql.column_exists(self.env.cr, self._table, column):
                continue
            sql.create_index(
                self.env.cr, f"{self._table}__{column}_brin",
                self._table, [column], method="brin")
