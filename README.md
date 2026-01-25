# BRIN Index Modules for Odoo 18

Колекция от модули, които създават BRIN индекси чрез стандартния Odoo механизъм за наследяване на модели.

## Архитектура

Всеки модул:
1. Наследява съответните Odoo модели
2. Override-ва `init()` метода
3. Създава BRIN индекси при инсталация/update

```
brin_index_accounting/    → account_move, account_move_line
brin_index_stock/         → stock_move, stock_quant, stock_valuation_layer  
brin_index_mail/          → mail_message, mail_tracking_value
brin_index_mrp/           → mrp_production, mrp_workorder
brin_index_pos/           → pos_order, pos_order_line
brin_index_hr/            → hr_attendance, hr_payslip
brin_index_sale/          → sale_order, crm_lead
brin_index_purchase/      → purchase_order
brin_index_project/       → project_task
```

## Инсталация

1. Копирайте модулите в addons директорията
2. Update Apps List
3. Модулите се инсталират **автоматично** с `auto_install=True`

При инсталиране на `account` → автоматично се инсталира `brin_index_accounting`

## Как работи

```python
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def init(self):
        super().init()
        # BRIN индексът се създава при инсталация/update
        create_brin_index(self.env.cr, 'account_move_line', 'date', 32)
```

## Създадени индекси

### brin_index_accounting
| Таблица | Колона | pages_per_range |
|---------|--------|-----------------|
| account_move_line | date | 32 |
| account_move_line | create_date | 32 |
| account_move | date | 64 |
| account_move | invoice_date | 64 |
| account_partial_reconcile | create_date | 64 |
| account_bank_statement_line | date | 64 |
| account_payment | date | 64 |

### brin_index_stock
| Таблица | Колона | pages_per_range |
|---------|--------|-----------------|
| stock_move_line | date | 32 |
| stock_move_line | create_date | 32 |
| stock_move | date | 32 |
| stock_quant | in_date | 64 |
| stock_lot | expiration_date | 64 |
| stock_picking | scheduled_date | 64 |
| stock_picking | date_done | 64 |
| stock_valuation_layer | create_date | 32 |

### brin_index_mail
| Таблица | Колона | pages_per_range |
|---------|--------|-----------------|
| mail_message | date | 32 |
| mail_message | create_date | 32 |
| mail_tracking_value | create_date | 32 |
| mail_notification | create_date | 32 |
| bus_bus | create_date | 16 |
| ir_attachment | create_date | 64 |

### brin_index_mrp
| Таблица | Колона | pages_per_range |
|---------|--------|-----------------|
| mrp_production | date_start | 64 |
| mrp_production | date_finished | 64 |
| mrp_workorder | date_start | 64 |
| mrp_workorder | date_finished | 64 |
| mrp_workcenter_productivity | date_start | 32 |
| mrp_workcenter_productivity | date_end | 32 |

### brin_index_pos
| Таблица | Колона | pages_per_range |
|---------|--------|-----------------|
| pos_order | date_order | 64 |
| pos_order_line | create_date | 64 |
| pos_payment | create_date | 64 |
| pos_session | start_at | 128 |

### brin_index_sale
| Таблица | Колона | pages_per_range |
|---------|--------|-----------------|
| sale_order | date_order | 64 |
| sale_order_line | create_date | 64 |
| crm_lead | create_date | 64 |
| crm_lead | date_deadline | 64 |
| crm_lead | date_closed | 64 |

### brin_index_purchase
| Таблица | Колона | pages_per_range |
|---------|--------|-----------------|
| purchase_order | date_order | 64 |
| purchase_order | date_approve | 64 |
| purchase_order_line | date_planned | 64 |

### brin_index_project
| Таблица | Колона | pages_per_range |
|---------|--------|-----------------|
| project_task | date_deadline | 64 |
| project_task | date_end | 64 |
| account_analytic_line | date | 32 |

### brin_index_hr
| Таблица | Колона | pages_per_range |
|---------|--------|-----------------|
| hr_attendance | check_in | 64 |
| hr_attendance | check_out | 64 |
| hr_leave | date_from | 64 |
| hr_payslip | date_from | 64 |
| hr_payslip_line | create_date | 32 |
| hr_work_entry | date_start | 32 |

## Проверка на индекси

```sql
-- Списък на BRIN индекси
SELECT indexname, tablename, indexdef 
FROM pg_indexes 
WHERE indexname LIKE 'brin_%'
ORDER BY tablename;

-- Размер на индексите
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass))
FROM pg_indexes 
WHERE indexname LIKE 'brin_%';
```

## REINDEX

След масови операции с backdated записи:

```sql
REINDEX INDEX CONCURRENTLY brin_account_move_line_date;
```

## Съвместимост

- Odoo: 17.0, 18.0
- PostgreSQL: 9.5+

## Лиценз

LGPL-3
