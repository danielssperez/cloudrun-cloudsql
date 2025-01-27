# Usa una imagen oficial de Python
FROM python:3.10

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar dependencias y código
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer el puerto para Cloud Run
EXPOSE 8080

# Ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
