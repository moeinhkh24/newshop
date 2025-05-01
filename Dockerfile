FROM python:3.13.1

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Collect static
# RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
