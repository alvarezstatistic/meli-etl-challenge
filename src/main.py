import os
import yaml
from datetime import datetime, timezone
from dotenv import load_dotenv

from src.db import get_conn, bulk_upsert_items, insert_rate
from src.meli_api import search_items, lookup_items, get_conversion_ratio

def envsubst(val: str) -> str:
    if not isinstance(val, str): return val
    out = val
    for k, v in os.environ.items():
        token = "${" + k + "}"
        if token in out:
            out = out.replace(token, v)
    return out

def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    for k in raw.get("api", {}):
        raw["api"][k] = envsubst(raw["api"][k])
    for k in raw.get("database", {}):
        raw["database"][k] = envsubst(raw["database"][k])
    raw["api"]["page_size"] = int(os.getenv("PAGE_SIZE", raw["api"]["page_size"]))
    raw["api"]["max_records"] = int(os.getenv("MAX_RECORDS", raw["api"]["max_records"]))
    return raw

def transform_items(items, site_id, rate_usd, job_run):
    rows = []
    for it in items:
        item_id = it.get("id")
        title = it.get("title")
        seller_id = it.get("seller_id")
        condition = it.get("condition")
        price_local = it.get("price")
        currency_id = it.get("currency_id")
        price_usd = None
        if price_local is not None and rate_usd:
            price_usd = float(price_local) * float(rate_usd)
        sold_q = it.get("sold_quantity")
        avail_q = it.get("available_quantity")
        listing_type_id = it.get("listing_type_id")
        warranty = it.get("warranty")
        shipping = it.get("shipping") or {}
        shipping_mode = shipping.get("mode")
        logistic_type = shipping.get("logistic_type")
        free_shipping = bool(shipping.get("free_shipping"))
        permalink = it.get("permalink")

        rows.append((
            item_id, site_id, title, seller_id, condition,
            price_local, currency_id, price_usd, sold_q, avail_q,
            listing_type_id, warranty, shipping_mode, logistic_type, free_shipping,
            permalink, job_run
        ))
    return rows

def main():
    load_dotenv()
    cfg = load_config(os.getenv("CONFIG_PATH", "config.yaml"))
    site_id = cfg["api"]["site_id"]
    query = cfg["api"]["search_query"]
    condition = cfg["api"]["condition"]
    page_size = cfg["api"]["page_size"]
    max_records = cfg["api"]["max_records"]

    job_run = datetime.now(timezone.utc).replace(microsecond=0)

    rate = get_conversion_ratio("ARS", "USD")
    conn = get_conn()
    insert_rate(conn, "ARS", "USD", rate, job_run)

    all_basic_ids = []
    for page in search_items(site_id, query, condition=condition, limit=page_size, max_records=max_records):
        ids = [str(x.get("id")) for x in page if x.get("id")]
        all_basic_ids.extend(ids)

    detailed = lookup_items(all_basic_ids)
    rows = transform_items(detailed, site_id, rate, job_run)
    bulk_upsert_items(conn, rows)

    print("ETL finished.")
    print(f"JOB_RUN: {job_run.isoformat()}")
    print(f"Items upserted: {len(rows)}")

if __name__ == "__main__":
    main()
