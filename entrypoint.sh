#!/bin/sh

# Aguarda o banco de dados estar pronto
echo "Aguardando o banco de dados iniciar..."
until nc -z db 3306; do
  echo "Banco de dados ainda não está disponível. Tentando novamente em 2 segundos..."
  sleep 2
done

echo "Banco de dados iniciado!"

# Executa a aplicação
exec gunicorn --bind 0.0.0.0:5000 src.main:app