import os
import psycopg2
from psycopg2.extras import execute_values

def get_conn():
    sslmode = os.getenv("DB_SSLMODE", "disable")
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=sslmode
    )
    conn.autocommit = True
    return conn

def bulk_upsert_items(conn, rows):
    if not rows:
        return
    with conn.cursor() as cur:
        execute_values(cur, """            INSERT INTO meli_items (
              item_id, site_id, title, seller_id, condition,
              price_local, currency_id, price_usd, sold_quantity, available_quantity,
              listing_type_id, warranty, shipping_mode, logistic_type, free_shipping,
              permalink, job_run
            )
            VALUES %s
            ON CONFLICT (item_id) DO UPDATE SET
              site_id = EXCLUDED.site_id,
              title = EXCLUDED.title,
              seller_id = EXCLUDED.seller_id,
              condition = EXCLUDED.condition,
              price_local = EXCLUDED.price_local,
              currency_id = EXCLUDED.currency_id,
              price_usd = EXCLUDED.price_usd,
              sold_quantity = EXCLUDED.sold_quantity,
              available_quantity = EXCLUDED.available_quantity,
              listing_type_id = EXCLUDED.listing_type_id,
              warranty = EXCLUDED.warranty,
              shipping_mode = EXCLUDED.shipping_mode,
              logistic_type = EXCLUDED.logistic_type,
              free_shipping = EXCLUDED.free_shipping,
              permalink = EXCLUDED.permalink,
              job_run = EXCLUDED.job_run;
        """, rows, page_size=1000)

def insert_rate(conn, from_code, to_code, ratio, job_run):
    with conn.cursor() as cur:
        cur.execute("""            INSERT INTO stg_currency_rates (from_code, to_code, ratio, job_run)
            VALUES (%s, %s, %s, %s);
        """, (from_code, to_code, ratio, job_run))
