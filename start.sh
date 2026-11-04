#!/bin/bash

set -e

echo "Iniciando configuracao do projeto Emporio da Musica..."

source venv/bin/activate

echo "Configurando banco de dados relacional..."
python src/database_setup.py

echo "Configurando base vetorial (RAG)..."
python src/rag_setup.py

echo "Executando testes do agente..."
python src/agent.py

echo "Iniciando interface web..."
streamlit run src/app.py