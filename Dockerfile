FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

#RUN chmod +x /app/entrypoint.sh
#ENTRYPOINT ["/app/entrypoint.sh"]


