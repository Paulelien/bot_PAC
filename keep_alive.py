#!/usr/bin/env python3
"""
Script para mantener la API del Chatbot PAC activa
Consulta la API cada minuto para evitar el "cold start"
"""

import requests
import time
import schedule
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
API_URL = os.getenv('API_URL', 'http://localhost:5001/api/health')
CHECK_INTERVAL = 1  # minutos

def check_api_health():
    """Verificar el estado de salud de la API"""
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] API activa - Status: {response.status_code}")
        else:
            print(f"⚠️  [{datetime.now().strftime('%H:%M:%S')}] API respondió con status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Error conectando a la API: {str(e)}")

def keep_alive():
    """Función principal para mantener la API activa"""
    print(f"🚀 Iniciando keep-alive para API del Chatbot PAC")
    print(f"📡 URL: {API_URL}")
    print(f"⏰ Intervalo: {CHECK_INTERVAL} minuto(s)")
    print("=" * 60)
    
    # Programar tarea cada minuto
    schedule.every(CHECK_INTERVAL).minutes.do(check_api_health)
    
    # Ejecutar inmediatamente la primera vez
    check_api_health()
    
    # Bucle principal
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo keep-alive...")
        print("✅ Script terminado")

if __name__ == "__main__":
    keep_alive()
