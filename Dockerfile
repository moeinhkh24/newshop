FROM python:3.13.1

# جلوگیری از ساخت فایل‌های .pyc و نمایش خروجی بلادرنگ
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# نصب PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Set environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=config.settings

# Expose port
EXPOSE 8000

# Command will be overridden by docker-compose.yaml
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
