"""
Configuración para la API del Chatbot PAC para LMS
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class APIConfig:
    """Configuración de la API para LMS"""
    
    # Configuración del servidor
    HOST = os.getenv('API_HOST', '0.0.0.0')
    PORT = int(os.getenv('API_PORT', '5001'))
    DEBUG = os.getenv('API_DEBUG', 'True').lower() == 'true'
    
    # Configuración de OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '500'))
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # Configuración del chatbot
    MAX_PDF_CONTENT_LENGTH = int(os.getenv('MAX_PDF_CONTENT_LENGTH', '15000'))
    MAX_SESSION_HISTORY = int(os.getenv('MAX_SESSION_HISTORY', '20'))
    
    # Configuración de seguridad
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    API_KEY_REQUIRED = os.getenv('API_KEY_REQUIRED', 'False').lower() == 'true'
    API_KEY_HEADER = os.getenv('API_KEY_HEADER', 'X-API-Key')
    
    # Configuración de rate limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '100'))  # requests per hour
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '3600'))    # 1 hour in seconds
    
    # Configuración de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'api_pac.log')
    
    # Configuración de sesiones
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))  # 1 hour in seconds
    MAX_SESSIONS_PER_USER = int(os.getenv('MAX_SESSIONS_PER_USER', '5'))
    
    @classmethod
    def validate_config(cls):
        """Validar que la configuración sea correcta"""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY no está configurada")
        
        if cls.OPENAI_MAX_TOKENS < 100 or cls.OPENAI_MAX_TOKENS > 2000:
            errors.append("OPENAI_MAX_TOKENS debe estar entre 100 y 2000")
        
        if cls.OPENAI_TEMPERATURE < 0 or cls.OPENAI_TEMPERATURE > 1:
            errors.append("OPENAI_TEMPERATURE debe estar entre 0 y 1")
        
        if cls.PORT < 1024 or cls.PORT > 65535:
            errors.append("PORT debe estar entre 1024 y 65535")
        
        if cls.RATE_LIMIT_REQUESTS < 1:
            errors.append("RATE_LIMIT_REQUESTS debe ser mayor a 0")
        
        if cls.SESSION_TIMEOUT < 300:  # 5 minutes minimum
            errors.append("SESSION_TIMEOUT debe ser al menos 300 segundos")
        
        return errors

# Configuración de desarrollo
class DevelopmentAPIConfig(APIConfig):
    """Configuración para desarrollo"""
    DEBUG = True
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000', 'http://localhost:5001', '*']
    LOG_LEVEL = 'DEBUG'

# Configuración de producción
class ProductionAPIConfig(APIConfig):
    """Configuración para producción"""
    DEBUG = False
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')
    API_KEY_REQUIRED = True
    RATE_LIMIT_ENABLED = True
    
    @classmethod
    def validate_config(cls):
        """Validación adicional para producción"""
        errors = super().validate_config()
        
        if cls.CORS_ORIGINS == ['']:
            errors.append("CORS_ORIGINS debe estar configurado en producción")
        
        if not cls.API_KEY_REQUIRED:
            errors.append("API_KEY_REQUIRED debe estar habilitado en producción")
        
        return errors

# Configuración de testing
class TestingAPIConfig(APIConfig):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True
    OPENAI_API_KEY = 'test_key'
    RATE_LIMIT_ENABLED = False

# Diccionario de configuraciones
api_config = {
    'development': DevelopmentAPIConfig,
    'production': ProductionAPIConfig,
    'testing': TestingAPIConfig,
    'default': DevelopmentAPIConfig
}

def get_api_config():
    """Obtener configuración según el entorno"""
    env = os.getenv('API_ENV', 'development')
    return api_config.get(env, api_config['default'])
