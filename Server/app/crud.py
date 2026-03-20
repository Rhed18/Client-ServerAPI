from .db import get_db
import datetime

RATES = {
    "bw": 2.0,
    "color": 5.0,
    "photo": 20.0,
}


def calculate_total(bw, color, photo):
    return bw * RATES["bw"] + color * RATES["color"] + photo * RATES["photo"]


def create_order(order_dict):
    conn = get_db()
    cur = conn.cursor()
    total = calculate_total(order_dict.get("bw_pages", 0), order_dict.get("color_pages", 0), order_dict.get("photo_pages", 0))
    created_at = datetime.datetime.utcnow().isoformat()
    cur.execute(
        "INSERT INTO orders (customer, bw_pages, color_pages, photo_pages, total, status, created_at) VALUES (?,?,?,?,?,?,?)",
        (
            order_dict.get("customer"),
            order_dict.get("bw_pages", 0),
            order_dict.get("color_pages", 0),
            order_dict.get("photo_pages", 0),
            total,
            "pending",
            created_at,
        ),
    )
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return {
        "id": last_id,
        "customer": order_dict.get("customer"),
        "bw_pages": order_dict.get("bw_pages", 0),
        "color_pages": order_dict.get("color_pages", 0),
        "photo_pages": order_dict.get("photo_pages", 0),
        "total": total,
        "status": "pending",
        "created_at": created_at,
    }


def get_order(order_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)


def list_orders():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_order_completed(order_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status='completed' WHERE id=?", (order_id,))
    conn.commit()
    changed = cur.rowcount
    conn.close()
    return changed > 0