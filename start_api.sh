#!/bin/bash

echo "========================================"
echo "    API del Chatbot PAC para LMS"
echo "========================================"
echo

echo "🔍 Verificando configuración..."
if [ ! -f ".env" ]; then
    echo "❌ ERROR: Archivo .env no encontrado"
    echo "Por favor, crea el archivo .env con tu configuración"
    echo
    exit 1
fi

echo "✅ Archivo .env encontrado"
echo

echo "🚀 Iniciando API del Chatbot PAC..."
echo "📍 Puerto: 5001"
echo "🌐 URL: http://localhost:5001"
echo "📚 API Docs: http://localhost:5001/api/health"
echo

echo "⏳ Iniciando servidor..."
python3 api_lms.py

echo
echo "❌ El servidor se ha detenido"
