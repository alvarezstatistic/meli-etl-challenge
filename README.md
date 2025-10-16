# 🚀 Mercado Libre ETL – Samsung Galaxy (Argentina) + Docker

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-SQL-green.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Desafío Técnico – ETL Automatizado (Python + Docker + PostgreSQL)
Este proyecto implementa un pipeline ETL (Extracción, Transformación y Carga) para recopilar, procesar y almacenar datos de productos de 
**Mercado Libre (Argentina), con especial atención a los dispositivos Samsung Galaxy.
---
## 🧩 Estrutura do Projeto

```bash
meli_etl_docker/
│
├meli_etl_docker/
│
├── src/ # Código fuente principal del pipeline ETL
│ ├── main.py # Script de ejecución principal
│ ├── db.py # Conexión y operaciones con la base de datos
│ ├── meli_api.py # Extracción de datos mediante la API de Mercado Libre
│ └── utils/ # Funciones auxiliares y procesamiento de datos
│
├── config.yaml # Archivo de configuración general
├── queries.sql # Consultas SQL para manipulación de datos
├── models.sql # Estructura de tablas y modelado de datos
├── requirements.txt # Dependencias de Python
├── Dockerfile # Imagen base de Docker y Instrucciones
├── docker-compose.yml # Orquestación de contenedores
├── .env.example # Variables de entorno de ejemplo
└── README.md # Este documento