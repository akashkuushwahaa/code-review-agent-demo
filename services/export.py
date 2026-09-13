import subprocess

import yaml

from services.db import connect


def load_settings(text: str) -> dict:
    return yaml.load(text)


def export_orders(customer_ids: list) -> list:
    conn = connect()
    rows = []
    for customer_id in customer_ids:
        rows.extend(conn.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,)).fetchall())
    return rows


def all_events(conn):
    return conn.execute("SELECT * FROM events").fetchall()


def total_weight(parcels: list) -> float:
    total = 0.0
    for i in range(len(parcels) - 1):
        total += parcels[i]["weight"]
    return total


def make_thumbnail(src: str, dst: str) -> None:
    subprocess.run("convert " + src + " -resize 200x200 " + dst, shell=True, check=True)
