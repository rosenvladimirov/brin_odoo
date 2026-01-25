# BRIN Index Modules for Odoo 18

Колекция от модули, които създават BRIN индекси използвайки **стандартната Odoo 18 `_sql_indexes` функционалност**.

## Как работи

В Odoo 18 има нов механизъм за дефиниране на индекси директно в модела чрез атрибута `_sql_indexes`:

```python
from odoo import models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    _sql_indexes = [
        models.Index('date', type='brin'),
        models.Index('create_date', type='brin'),
    ]
```

Odoo автоматично:
1. Генерира уникално име за индекса
2. Създава индекса при инсталация/update
3. Управлява жизнения цикъл на индекса

## Модули

| Модул | Зависимост | Таблици |
|-------|------------|---------|
| `brin_index_accounting` | account | account_move_line, account_move, account_payment |
| `brin_index_stock` | stock | stock_move_line, stock_quant, stock_valuation_layer |
| `brin_index_mail` | mail | mail_message, mail_tracking_value, bus_bus |
| `brin_index_mrp` | mrp | mrp_production, mrp_workorder |
| `brin_index_pos` | point_of_sale | pos_order, pos_order_line |
| `brin_index_sale` | sale | sale_order, sale_order_line |
| `brin_index_crm` | crm | crm_lead |
| `brin_index_purchase` | purchase | purchase_order, purchase_order_line |
| `brin_index_project` | project | project_task |
| `brin_index_timesheet` | hr_timesheet | account_analytic_line |
| `brin_index_hr` | hr | (base module) |
| `brin_index_hr_attendance` | hr_attendance | hr_attendance |
| `brin_index_hr_holidays` | hr_holidays | hr_leave |
| `brin_index_hr_payroll` | hr_payroll | hr_payslip, hr_payslip_line |
| `brin_index_hr_work_entry` | hr_work_entry | hr_work_entry |

## Инсталация

1. Копирайте модулите в addons директорията
2. Update Apps List
3. Модулите се инсталират **автоматично** (`auto_install=True`)

## Създадени индекси

### brin_index_accounting
```python
# account_move_line
models.Index('date', type='brin')
models.Index('create_date', type='brin')

# account_move  
models.Index('date', type='brin')
models.Index('invoice_date', type='brin')
models.Index('create_date', type='brin')

# account_partial_reconcile
models.Index('create_date', type='brin')

# account_bank_statement_line
models.Index('date', type='brin')

# account_payment
models.Index('date', type='brin')
```

### brin_index_stock
```python
# stock_move_line
models.Index('date', type='brin')
models.Index('create_date', type='brin')

# stock_move
models.Index('date', type='brin')

# stock_quant (FIFO/FEFO)
models.Index('in_date', type='brin')

# stock_lot (FEFO)
models.Index('expiration_date', type='brin')

# stock_picking
models.Index('scheduled_date', type='brin')
models.Index('date_done', type='brin')

# stock_valuation_layer
models.Index('create_date', type='brin')
```

### brin_index_mail
```python
# mail_message (often the LARGEST table!)
models.Index('date', type='brin')
models.Index('create_date', type='brin')

# mail_tracking_value
models.Index('create_date', type='brin')

# mail_notification
models.Index('create_date', type='brin')

# bus_bus
models.Index('create_date', type='brin')

# ir_attachment
models.Index('create_date', type='brin')
```

## Проверка на индекси

```sql
-- Списък на BRIN индекси
SELECT indexname, tablename 
FROM pg_indexes 
WHERE indexdef LIKE '%USING brin%'
ORDER BY tablename;

-- Размер на индексите
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass))
FROM pg_indexes 
WHERE indexdef LIKE '%USING brin%';
```

## Предимства на Odoo 18 _sql_indexes

1. **Декларативен подход** - индексите се дефинират в модела
2. **Автоматично управление** - Odoo управлява създаване/изтриване
3. **Merge при наследяване** - индексите се добавят към базовите
4. **Консистентност** - използва стандартния Odoo механизъм

## Съвместимост

- Odoo: **18.0** (изисква новата _sql_indexes функционалност)
- PostgreSQL: 9.5+

## Лиценз

LGPL-3
