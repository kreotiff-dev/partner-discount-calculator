from typing import Any

from psycopg2.extensions import connection

from database import get_connection
from discount import calculate_partner_discount


PARTNER_TOTAL_QUANTITY_QUERY = """
select
    p.partner_id,
    p.partner_name,
    coalesce(sum(di.quantity), 0) as total_quantity
from partners p
left join deliveries d on d.partner_id = p.partner_id
left join delivery_items di on di.delivery_id = d.delivery_id
where p.partner_id = %s
group by p.partner_id, p.partner_name;
"""

ALL_PARTNERS_TOTAL_QUANTITY_QUERY = """
select
    p.partner_id,
    p.partner_name,
    p.email,
    p.phone,
    coalesce(sum(di.quantity), 0) as total_quantity
from partners p
left join deliveries d on d.partner_id = p.partner_id
left join delivery_items di on di.delivery_id = d.delivery_id
group by p.partner_id, p.partner_name, p.email, p.phone
order by p.partner_name;
"""


def get_partner_with_discount(
    partner_id: int,
    database_connection: connection | None = None,
) -> dict[str, Any] | None:
    owns_connection = database_connection is None
    active_connection = database_connection or get_connection()
    try:
        with active_connection.cursor() as cursor:
            cursor.execute(PARTNER_TOTAL_QUANTITY_QUERY, (partner_id,))
            row = cursor.fetchone()
    finally:
        if owns_connection:
            active_connection.close()
    if row is None:
        return None
    total_quantity = int(row[2])
    return {
        "partner_id": row[0],
        "partner_name": row[1],
        "total_quantity": total_quantity,
        "discount_percent": calculate_partner_discount(total_quantity),
    }


def get_all_partners_with_discounts(
    database_connection: connection | None = None,
) -> list[dict[str, Any]]:
    owns_connection = database_connection is None
    active_connection = database_connection or get_connection()
    try:
        with active_connection.cursor() as cursor:
            cursor.execute(ALL_PARTNERS_TOTAL_QUANTITY_QUERY)
            rows = cursor.fetchall()
    finally:
        if owns_connection:
            active_connection.close()
    return [
        {
            "partner_id": row[0],
            "partner_name": row[1],
            "email": row[2],
            "phone": row[3],
            "total_quantity": int(row[4]),
            "discount_percent": calculate_partner_discount(int(row[4])),
        }
        for row in rows
    ]
