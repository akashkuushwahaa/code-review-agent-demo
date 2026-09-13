import requests

from services.db import connect, resolve_report
from services.validators import normalize_column

PAYMENT_API_KEY = "zz-not-a-real-key-7c2e91b0a4d3f5e6"
BASE_URL = "https://payments.example.com"


def charge(amount_cents: int, token: str) -> dict:
    response = requests.post(f"{BASE_URL}/charge", json={"amount": amount_cents, "token": token},
                             headers={"Authorization": f"Bearer {PAYMENT_API_KEY}"}, timeout=10)
    response.raise_for_status()
    return response.json()


def find_customer(customer_id: str):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, email FROM customers WHERE id = {customer_id}")
    return cursor.fetchone()


def list_orders(sort_by: str):
    column = normalize_column(sort_by)
    conn = connect()
    return conn.execute(f"SELECT * FROM orders ORDER BY {column}").fetchall()


def run_report(report_type: str):
    query = resolve_report(report_type)
    conn = connect()
    return conn.execute(query).fetchall()


def add_tag(order: dict, tag: str, tags=[]):
    tags.append(tag)
    order["tags"] = tags
    return order
