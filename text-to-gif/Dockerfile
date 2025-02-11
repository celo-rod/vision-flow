FROM nvidia/cuda:12.8.0-runtime-ubuntu24.04

RUN apt update && apt install -y python3 python3.12-venv && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --upgrade pip setuptools wheel

WORKDIR /app

COPY requirements.txt .

RUN /opt/venv/bin/pip install -r requirements.txt

COPY main.py .

EXPOSE 8001

CMD ["/opt/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
