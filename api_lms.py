"""
API para integración del Chatbot PAC con LMS
Endpoints RESTful para comunicación con sistemas externos
VERSION CORREGIDA: Compatible con openai==0.28.1
SISTEMA DE CHUNKS: Integrado búsqueda semántica para respuestas precisas
FORZANDO REDESPLIEGUE: Sistema de chunks implementado
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from datetime import datetime
import json
from dotenv import load_dotenv
from semantic_search import SemanticSearch

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

class PACChatbotAPI:
    def __init__(self):
        self.conversation_history = {}
        self.semantic_search = SemanticSearch()
        print("✅ Sistema de búsqueda semántica inicializado")
        
    def get_relevant_chunks(self, user_message):
        """Obtener chunks relevantes para la pregunta del usuario"""
        try:
            # Buscar chunks más relevantes usando búsqueda semántica
            relevant_chunks = self.semantic_search.search(user_message, top_k=3)
            
            if relevant_chunks:
                # Combinar contenido de chunks relevantes
                combined_content = ""
                for i, chunk in enumerate(relevant_chunks, 1):
                    combined_content += f"\n\n--- CHUNK {i} (Unidad {chunk['metadata']['unidad']} - {chunk['metadata']['tema']}) ---\n"
                    combined_content += f"Relevancia: {chunk['similarity_percentage']}%\n"
                    combined_content += chunk['content']
                
                print(f"✅ Encontrados {len(relevant_chunks)} chunks relevantes para: '{user_message}'")
                return combined_content, len(relevant_chunks)
            else:
                print(f"⚠️ No se encontraron chunks relevantes para: '{user_message}'")
                return "", 0
                
        except Exception as e:
            print(f"❌ Error en búsqueda semántica: {str(e)}")
            return "", 0
    
    def get_response(self, user_message, session_id=None):
        """Obtener respuesta del chatbot usando OpenAI"""
        try:
            # Cargar prompt del sistema
            system_prompt = self.load_system_prompt()
            
            # Obtener chunks relevantes para la pregunta
            relevant_content, chunks_found = self.get_relevant_chunks(user_message)
            
            if relevant_content and chunks_found > 0:
                system_prompt += f"\n\nCONTENIDO RELEVANTE DEL CURSO PAC (basado en {chunks_found} chunks):\n{relevant_content}"
                print(f"✅ Enviando {chunks_found} chunks relevantes a OpenAI")
            else:
                system_prompt += "\n\nNO SE ENCONTRÓ INFORMACIÓN RELEVANTE EN LOS MANUALES DEL CURSO PAC."
                print("⚠️ No se encontraron chunks relevantes")
            
            # Obtener historial de la sesión
            session_history = self.conversation_history.get(session_id, [])
            
            # Construir mensajes para OpenAI
            messages = [{"role": "system", "content": system_prompt}]
            
            # Agregar historial reciente (últimas 5 conversaciones)
            for msg in session_history[-10:]:
                messages.append(msg)
            
            # Agregar mensaje actual del usuario
            messages.append({"role": "user", "content": user_message})
            
            # Llamar a OpenAI
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.ChatCompletion.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
                messages=messages,
                max_tokens=int(os.getenv('OPENAI_MAX_TOKENS', '500')),
                temperature=float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
            )
            
            bot_response = response.choices[0]['message']['content']
            
            # Actualizar historial de la sesión
            if session_id:
                if session_id not in self.conversation_history:
                    self.conversation_history[session_id] = []
                
                self.conversation_history[session_id].append({"role": "user", "content": user_message})
                self.conversation_history[session_id].append({"role": "assistant", "content": bot_response})
                
                # Mantener solo las últimas 20 conversaciones
                if len(self.conversation_history[session_id]) > 20:
                    self.conversation_history[session_id] = self.conversation_history[session_id][-20:]
            
            return bot_response
            
        except Exception as e:
            return f"Error al procesar la consulta: {str(e)}"
    
    def load_system_prompt(self):
        """Cargar el prompt del sistema desde archivo"""
        try:
            with open('prompt_sistema.txt', 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return """
            Eres un asistente educativo especializado en el Plan de Aseguramiento de la Calidad en Construcción (PAC).
            Responde basándote SOLO en el contenido de los PDFs del curso.
            Cita definiciones textuales cuando sea posible.
            Menciona siempre la unidad específica del curso.
            Mantén las respuestas concisas y específicas.
            """

# Instancia global del chatbot
chatbot = PACChatbotAPI()

# ============================================================================
# ENDPOINTS DE LA API
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar estado de salud de la API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'PAC Chatbot API',
        'version': '1.0.0'
    })

@app.route('/api/status', methods=['GET'])
def system_status():
    """Verificar estado del sistema"""
    return jsonify({
        'status': 'online',
        'openai_configured': bool(os.getenv('OPENAI_API_KEY')),
        'pdfs_loaded': bool(chatbot.pdf_content),
        'active_sessions': len(chatbot.conversation_history),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal para el chat"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Datos requeridos'}), 400
        
        user_message = data.get('message', '')
        session_id = data.get('session_id')
        user_id = data.get('user_id')
        course_id = data.get('course_id')
        
        if not user_message:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        # Obtener respuesta del chatbot
        response = chatbot.get_response(user_message, session_id)
        
        return jsonify({
            'response': response,
            'session_id': session_id,
            'user_id': user_id,
            'course_id': course_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/session/<session_id>', methods=['GET'])
def get_session_history(session_id):
    """Obtener historial de una sesión específica"""
    try:
        session_history = chatbot.conversation_history.get(session_id, [])
        
        return jsonify({
            'session_id': session_id,
            'history': session_history,
            'message_count': len(session_history),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/session/<session_id>', methods=['DELETE'])
def clear_session_history(session_id):
    """Limpiar historial de una sesión específica"""
    try:
        if session_id in chatbot.conversation_history:
            del chatbot.conversation_history[session_id]
        
        return jsonify({
            'message': f'Sesión {session_id} limpiada exitosamente',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/course/info', methods=['GET'])
def get_course_info():
    """Obtener información del curso disponible"""
    return jsonify({
        'course_name': 'Plan de Aseguramiento de la Calidad en Construcción (PAC)',
        'units': [
            {
                'id': 1,
                'name': 'Definiciones y conceptos básicos del PAC',
                'description': 'Conceptos fundamentales del sistema de calidad'
            },
            {
                'id': 2,
                'name': 'Auditorías y certificación ISO 9001',
                'description': 'Procesos de auditoría y certificación'
            },
            {
                'id': 3,
                'name': 'RES 258:2020 y planes de calidad',
                'description': 'Normativas y planes de calidad'
            }
        ],
        'pdfs_loaded': bool(chatbot.pdf_content),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/course/search', methods=['POST'])
def search_course_content():
    """Buscar contenido específico en el curso"""
    try:
        data = request.get_json()
        search_term = data.get('search_term', '')
        
        if not search_term:
            return jsonify({'error': 'Término de búsqueda requerido'}), 400
        
        # Buscar en el contenido de los PDFs
        if chatbot.pdf_content:
            content_lower = chatbot.pdf_content.lower()
            search_lower = search_term.lower()
            
            if search_lower in content_lower:
                # Encontrar contexto alrededor del término
                start_pos = content_lower.find(search_lower)
                context_start = max(0, start_pos - 200)
                context_end = min(len(chatbot.pdf_content), start_pos + len(search_term) + 200)
                context = chatbot.pdf_content[context_start:context_end]
                
                return jsonify({
                    'search_term': search_term,
                    'found': True,
                    'context': context,
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({
                    'search_term': search_term,
                    'found': False,
                    'message': 'Término no encontrado en el contenido del curso',
                    'timestamp': datetime.now().isoformat()
                })
        else:
            return jsonify({
                'error': 'No hay contenido de PDF disponible',
                'timestamp': datetime.now().isoformat()
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/sessions', methods=['GET'])
def get_session_analytics():
    """Obtener estadísticas de sesiones"""
    try:
        total_sessions = len(chatbot.conversation_history)
        total_messages = sum(len(history) for history in chatbot.conversation_history.values())
        
        return jsonify({
            'total_sessions': total_sessions,
            'total_messages': total_messages,
            'average_messages_per_session': total_messages / total_sessions if total_sessions > 0 else 0,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Método no permitido'}), 405

# ============================================================================
# INICIO DE LA APLICACIÓN
# ============================================================================

if __name__ == '__main__':
    # Validar configuración
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ ERROR: OPENAI_API_KEY no está configurada")
        print("Por favor, configura tu archivo .env")
        exit(1)
    
    print("🚀 Iniciando API del Chatbot PAC para LMS")
    print(f"📚 Modelo OpenAI: {os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')}")
    print(f"🔧 Modo debug: {os.getenv('FLASK_DEBUG', 'True')}")
    print("=" * 60)
    
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true',
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', '5001'))
    )
