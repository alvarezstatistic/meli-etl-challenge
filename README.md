# Mercado Libre ETL – Samsung Galaxy (Argentina) + Docker

## Rodando com Docker
```bash
cp .env.example .env
docker compose up -d postgres
# criar tabelas
psql -h 127.0.0.1 -U meli_user -d meli -f models.sql
# executar ETL
docker compose up --build etl
```

## Consultas (queries.sql)
Contém as SQLs para responder: sellers com múltiplas publicações, média de vendas por seller, preço médio USD, % com garantia, e métodos de shipping.

## Estrutura
src/ (db.py, meli_api.py, main.py), models.sql, queries.sql, config.yaml, .env.example, Dockerfile, docker-compose.yml, requirements.txt.
