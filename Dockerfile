# Dockerfile para Chatbot PAC
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para templates si no existe
RUN mkdir -p templates

# Exponer puerto
EXPOSE 5000

# Variables de entorno por defecto
ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
