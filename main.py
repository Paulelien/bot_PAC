"""
Archivo principal para Render
Importa y ejecuta la API del Chatbot PAC
"""

from api_lms import app
import os

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', '5001'))
    )
