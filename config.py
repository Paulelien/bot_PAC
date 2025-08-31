"""
Configuración del Chatbot PAC
Plan de Aseguramiento de la Calidad en Construcción
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración principal de la aplicación"""
    
    # Configuración de OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '500'))
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # Configuración del servidor
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configuración del chatbot
    MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', '20'))
    MAX_PDF_CONTENT_LENGTH = int(os.getenv('MAX_PDF_CONTENT_LENGTH', '15000'))
    
    # Contexto del curso PAC
    PAC_CONTEXT = ""
    
    @classmethod
    def load_prompt_from_file(cls):
        """Cargar el prompt del sistema desde archivo"""
        try:
            with open('prompt_sistema.txt', 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            # Prompt de respaldo si no se encuentra el archivo
            return """
            Eres un asistente educativo especializado en el Plan de Aseguramiento de la Calidad en Construcción (PAC).
            Responde basándote SOLO en el contenido de los PDFs del curso.
            Cita definiciones textuales cuando sea posible.
            Menciona siempre la unidad específica del curso.
            Mantén las respuestas concisas y específicas.
            """
    
    # Preguntas frecuentes sugeridas
    SUGGESTED_QUESTIONS = [
        "¿Qué es el PAC?",
        "¿Cuáles son los procedimientos de calidad?",
        "¿Qué normativas vigentes aplican?",
        "¿Cómo se realiza el control de calidad?",
        "¿Qué documentación se requiere?",
        "¿Cuáles son las responsabilidades del supervisor?",
        "¿Cómo se manejan las no conformidades?",
        "¿Qué es un plan de muestreo?",
        "¿Cómo se documentan las inspecciones?",
        "¿Qué son los puntos de control crítico?"
    ]
    
    # Configuración de archivos
    ALLOWED_EXTENSIONS = {'.pdf'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    # Configuración de seguridad
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
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
        
        return errors

# Configuración de desarrollo
class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000', '*']

# Configuración de producción
class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')
    
    @classmethod
    def validate_config(cls):
        """Validación adicional para producción"""
        errors = super().validate_config()
        
        if cls.CORS_ORIGINS == ['']:
            errors.append("CORS_ORIGINS debe estar configurado en producción")
        
        return errors

# Configuración de testing
class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True
    OPENAI_API_KEY = 'test_key'

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtener configuración según el entorno"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
