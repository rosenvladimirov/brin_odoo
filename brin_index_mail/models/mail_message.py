# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Mail (BRIN) през sql.create_index.

mail_message is often the largest table in Odoo databases!
"""
from odoo import models
from odoo.tools import sql


class MailMessage(models.Model):
    """BRIN indexes for mail_message - often the LARGEST table in Odoo!"""
    _inherit = 'mail.message'

    def init(self):
        # CRITICAL: Can grow to 10-200M+ rows in production
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


class MailTrackingValue(models.Model):
    """BRIN index for mail_tracking_value - grows fast with tracked fields."""
    _inherit = 'mail.tracking.value'

    def init(self):
        # Every tracked field change creates a record here
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


class MailNotification(models.Model):
    """BRIN index for mail_notification."""
    _inherit = 'mail.notification'

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


class BusBus(models.Model):
    """BRIN index for bus_bus - high write volume."""
    _inherit = 'bus.bus'

    def init(self):
        # High write volume, should be cleaned regularly
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


class IrAttachment(models.Model):
    """BRIN index for ir_attachment."""
    _inherit = 'ir.attachment'

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
