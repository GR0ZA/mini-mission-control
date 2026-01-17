FROM python:3.11-slim

WORKDIR /app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared ./shared
COPY tc_uplink ./tc_uplink
COPY api ./api


CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]