"""Keep account_move_line.date populated so the partition key is never NULL.

When account_move_line is RANGE-partitioned by ``date``, that column becomes
part of the composite primary key ``(id, date)`` and is therefore NOT NULL.
Odoo, however, leaves ``date`` empty on the lines of a *draft* move (the
accounting date is only assigned on posting), so the very first INSERT of a
draft invoice/journal-entry line hits the partitioned table with ``date = NULL``
and fails::

    null value in column "date" of relation "account_move_line_default"
    violates not-null constraint

This is pure runtime business logic (it runs while records are written, not
during schema init), so it is a normal model override — NOT a server-wide
monkeypatch like ``fk_partition_patch``.

The fallback mirrors what core already uses elsewhere for a move's effective
date: ``move.date`` → ``move.invoice_date`` → today. On posting, core assigns
the real ``move.date`` and the line's date is realigned. Draft lines carry a
provisional date, which is harmless: reports filter drafts out via
``parent_state``.

Scope: only fills a date that would otherwise be NULL — never overrides a date
that is already provided.
"""
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _partition_fallback_date(self, move):
        """Effective date for a line whose move has no accounting date yet."""
        return (move.date or move.invoice_date
                or fields.Date.context_today(self))

    @api.model_create_multi
    def create(self, vals_list):
        # Resolve the fallback per referenced move in one batch read.
        move_ids = {v['move_id'] for v in vals_list if v.get('move_id')}
        moves = self.env['account.move'].browse(move_ids)
        move_date = {m.id: (m.date or m.invoice_date) for m in moves}
        today = fields.Date.context_today(self)
        for vals in vals_list:
            if not vals.get('date'):
                vals['date'] = move_date.get(vals.get('move_id')) or today
        return super().create(vals_list)

    def write(self, vals):
        # The partition key can never be NULL; if something tries to clear the
        # date, substitute the per-record fallback instead.
        if 'date' in vals and not vals['date']:
            vals = {k: v for k, v in vals.items() if k != 'date'}
            res = super().write(vals) if vals else True
            for line in self:
                super(AccountMoveLine, line).write(
                    {'date': line._partition_fallback_date(line.move_id)})
            return res
        return super().write(vals)
