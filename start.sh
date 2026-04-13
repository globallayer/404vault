#\!/bin/sh
exec uvicorn vault404.api.server:app --host 0.0.0.0 --port "${PORT:-8000}"
