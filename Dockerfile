FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 APP_INTERNAL_PORT=8787

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

EXPOSE 8787
CMD ["sh", "-c", "python manage.py migrate && gunicorn clublectura.wsgi:application --chdir app --bind 0.0.0.0:${APP_INTERNAL_PORT}"]
