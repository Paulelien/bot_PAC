"""
Archivo principal para Render
Importa y ejecuta la API del Chatbot PAC
"""

import os
from api_lms import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5001'))
    app.run(host='0.0.0.0', port=port)
