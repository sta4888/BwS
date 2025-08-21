FROM python:3.10
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

# Установка зависимостей Python
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
    && pip install --no-cache-dir pytesseract pillow

# Установка системных пакетов: Chrome + Tesseract OCR
RUN apt-get update && apt-get install -y wget unzip \
    tesseract-ocr libtesseract-dev \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "main.py"]
