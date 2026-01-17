FROM python:3.11-slim

WORKDIR /app

COPY shared ./shared
COPY procedures ./procedures
COPY tc_uplink ./tc_uplink
COPY tm_ingestor ./tm_ingestor

EXPOSE 5005/udp

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "tm_ingestor.tm_ingestor"]