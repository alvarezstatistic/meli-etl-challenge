# 🚀 Mercado Libre ETL – Samsung Galaxy (Argentina) + Docker

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-SQL-green.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Desafio Técnico – ETL Automatizado (Python + Docker + PostgreSQL)**  
> Este projeto implementa um pipeline ETL (Extract, Transform, Load) para coletar, processar e armazenar dados de produtos da **Mercado Libre (Argentina)** — com foco em dispositivos **Samsung Galaxy**.
---
## 🧩 Estrutura do Projeto

```bash
meli_etl_docker/
│
├── src/                     # Código-fonte principal do pipeline ETL
│   ├── main.py              # Script principal de execução
│   ├── db.py                # Conexão e operações no banco de dados
│   ├── meli_api.py          # Extração de dados via API Mercado Libre
│   └── utils/               # Funções auxiliares e tratamento de dados
│
├── config.yaml              # Arquivo de configuração geral
├── queries.sql              # Consultas SQL para manipulação dos dados
├── models.sql               # Estrutura de tabelas e modelagem de dados
├── requirements.txt         # Dependências Python
├── Dockerfile               # Imagem base e instruções Docker
├── docker-compose.yml       # Orquestração de containers
├── .env.example             # Exemplo de variáveis de ambiente
└── README.md                # Este documento
