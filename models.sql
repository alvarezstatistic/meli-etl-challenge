CREATE TABLE IF NOT EXISTS stg_currency_rates (
  from_code TEXT NOT NULL,
  to_code   TEXT NOT NULL,
  ratio     NUMERIC(18,8) NOT NULL,
  fetched_at TIMESTAMP NOT NULL DEFAULT NOW(),
  job_run   TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS meli_items (
  item_id        TEXT PRIMARY KEY,
  site_id        TEXT NOT NULL,
  title          TEXT NOT NULL,
  seller_id      BIGINT NOT NULL,
  condition      TEXT,
  price_local    NUMERIC(18,2),
  currency_id    TEXT,
  price_usd      NUMERIC(18,2),
  sold_quantity  BIGINT,
  available_quantity BIGINT,
  listing_type_id TEXT,
  warranty       TEXT,
  shipping_mode  TEXT,
  logistic_type  TEXT,
  free_shipping  BOOLEAN,
  permalink      TEXT,
  job_run        TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS meli_sellers (
  seller_id   BIGINT PRIMARY KEY,
  nickname    TEXT,
  registration_date TIMESTAMP,
  job_run     TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_items_seller ON meli_items (seller_id);
CREATE INDEX IF NOT EXISTS idx_items_jobrun ON meli_items (job_run);
CREATE INDEX IF NOT EXISTS idx_items_condition ON meli_items (condition);
