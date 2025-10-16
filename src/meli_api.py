import os
import time
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

BASE = os.getenv("API_BASE_URL", "https://api.mercadolibre.com")

class ApiError(Exception):
    pass

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=16),
       retry=retry_if_exception_type(ApiError))
def get(url, params=None):
    resp = requests.get(url, params=params, timeout=20)
    if resp.status_code >= 400:
        raise ApiError(f"GET {url} failed: {resp.status_code} {resp.text[:200]}")
    return resp.json()

def get_conversion_ratio(from_code="ARS", to_code="USD"):
    url = f"{BASE}/currency_conversions/search"
    data = get(url, params={"from": from_code, "to": to_code})
    ratio = float(data.get("ratio") or data.get("conversion_rate") or 0.0)
    if ratio == 0.0:
        logging.warning("Currency conversion ratio not found; defaulting to 0.0")
    return ratio

def search_items(site_id, query, condition="new", limit=200, max_records=1000):
    url = f"{BASE}/sites/{site_id}/search"
    total_collected = 0
    offset = 0
    while total_collected < max_records:
        page_size = min(limit, max_records - total_collected)
        params = {"q": query, "condition": condition, "limit": page_size, "offset": offset}
        data = get(url, params=params)
        results = data.get("results", [])
        if not results:
            break
        yield results
        got = len(results)
        total_collected += got
        offset += got
        time.sleep(0.2)

def lookup_items(ids):
    url = f"{BASE}/items"
    CHUNK = 50
    out = []
    for i in range(0, len(ids), CHUNK):
        chunk = ids[i:i+CHUNK]
        data = requests.get(url, params={"ids": ",".join(chunk)}, timeout=20)
        if data.status_code >= 400:
            raise ApiError(f"/items batch failed: {data.status_code} {data.text[:200]}")
        payload = data.json()
        for el in payload:
            body = el.get("body", {})
            if body and body.get("id"):
                out.append(body)
        time.sleep(0.2)
    return out
