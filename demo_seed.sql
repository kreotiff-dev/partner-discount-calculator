-- Демонстрационные отгрузки для показа всех уровней скидки в UI.
-- Скрипт можно запускать повторно: номера отгрузок уникальны.

begin;

insert into deliveries (partner_id, delivery_date, shipment_number, status)
select
    p.partner_id,
    date '2026-03-31',
    source.shipment_number,
    'delivered'
from (
    values
        ('7701234567', 'DEMO-DISCOUNT-5'),
        ('5001098765', 'DEMO-DISCOUNT-10'),
        ('7812345678', 'DEMO-DISCOUNT-15')
) as source(inn, shipment_number)
join partners p on p.inn = source.inn
on conflict (shipment_number) do nothing;

insert into delivery_items (delivery_id, product_id, quantity, unit_price)
select
    d.delivery_id,
    (select product_id from products order by product_id limit 1),
    source.quantity,
    1.0000
from (
    values
        ('DEMO-DISCOUNT-5', 9920.000),
        ('DEMO-DISCOUNT-10', 49800.000),
        ('DEMO-DISCOUNT-15', 299850.000)
) as source(shipment_number, quantity)
join deliveries d on d.shipment_number = source.shipment_number
on conflict (delivery_id, product_id) do nothing;

commit;
