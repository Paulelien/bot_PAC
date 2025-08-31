#!/bin/bash

echo "========================================"
echo "   Chatbot PAC - Iniciando Sistema"
echo "========================================"
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Por favor, instala Python 3.8 o superior"
    exit 1
fi

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo crear el entorno virtual"
        exit 1
    fi
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Verificar si las dependencias están instaladas
if [ ! -d "venv/lib/python*/site-packages/flask" ]; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudieron instalar las dependencias"
        exit 1
    fi
fi

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo
    echo "ADVERTENCIA: No se encontró el archivo .env"
    echo "Por favor, crea un archivo .env con tu API key de OpenAI"
    echo "Ejemplo:"
    echo "OPENAI_API_KEY=tu_api_key_aqui"
    echo
    read -p "¿Deseas continuar sin configurar OpenAI? (s/n): " continue
    if [[ ! $continue =~ ^[Ss]$ ]]; then
        echo "Configuración cancelada"
        exit 1
    fi
fi

echo
echo "Iniciando Chatbot PAC..."
echo
echo "La aplicación estará disponible en: http://localhost:5000"
echo "Presiona Ctrl+C para detener el servidor"
echo

# Iniciar la aplicación
python app.py
