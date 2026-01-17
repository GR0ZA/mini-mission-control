FROM python:3.11-slim

WORKDIR /app


COPY shared ./shared
COPY sat_simulator ./sat_simulator

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "sat_simulator.sat_simulator"]