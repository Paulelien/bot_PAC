from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import openai
from dotenv import load_dotenv
import PyPDF2
import os

from datetime import datetime
from config import get_config

# Cargar configuración
config = get_config()

app = Flask(__name__)
CORS(app, origins=config.CORS_ORIGINS)

# Configuración de OpenAI
openai.api_key = config.OPENAI_API_KEY

class PACChatbot:
    def __init__(self):
        self.conversation_history = []
        self.pdf_content = ""
        self.load_course_pdfs()
    
    def load_course_pdfs(self):
        """Cargar automáticamente todos los PDFs del curso"""
        pdf_folder = "pdfs_curso"
        if os.path.exists(pdf_folder):
            for filename in os.listdir(pdf_folder):
                if filename.lower().endswith('.pdf'):
                    pdf_path = os.path.join(pdf_folder, filename)
                    try:
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf_reader = PyPDF2.PdfReader(pdf_file)
                            content = ""
                            for page in pdf_reader.pages:
                                content += page.extract_text() + "\n"
                            self.pdf_content += f"\n\n--- CONTENIDO DE {filename} ---\n{content}"
                            print(f"✅ PDF cargado: {filename}")
                    except Exception as e:
                        print(f"❌ Error al cargar {filename}: {e}")
    
    def get_response(self, user_message):
        """Obtener respuesta del chatbot usando OpenAI"""
        try:
            # Construir el prompt con contexto del curso y contenido de PDFs
            system_prompt = config.load_prompt_from_file()
            
            if self.pdf_content:
                system_prompt += f"\n\nCONTENIDO DEL CURSO PAC:\n{self.pdf_content[:config.MAX_PDF_CONTENT_LENGTH]}"
                print(f"🔍 Enviando a OpenAI: {len(system_prompt)} caracteres")
                print(f"📚 Contenido PDF incluido: {len(self.pdf_content)} caracteres")
            else:
                print("⚠️ No hay contenido de PDF disponible")
            
            # Agregar historial de conversación
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Agregar historial reciente (últimas 5 conversaciones)
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            
            # Agregar mensaje actual del usuario
            messages.append({"role": "user", "content": user_message})
            
            # Llamar a OpenAI (sintaxis compatible con openai==0.28.1)
            openai.api_key = config.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model=config.OPENAI_MODEL,
                messages=messages,
                max_tokens=config.OPENAI_MAX_TOKENS,
                temperature=config.OPENAI_TEMPERATURE
            )
            
            bot_response = response.choices[0]['message']['content']
            
            # Actualizar historial
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            
            # Mantener solo las últimas conversaciones según configuración
            if len(self.conversation_history) > config.MAX_CONVERSATION_HISTORY:
                self.conversation_history = self.conversation_history[-config.MAX_CONVERSATION_HISTORY:]
            
            return bot_response
            
        except Exception as e:
            return f"Lo siento, hubo un error al procesar tu consulta: {str(e)}"

# Instancia global del chatbot
chatbot = PACChatbot()

@app.route('/')
def index():
    """Página principal del chatbot"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para el chat"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        # Obtener respuesta del chatbot
        response = chatbot.get_response(user_message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/status')
def status():
    """Endpoint para verificar el estado del sistema"""
    return jsonify({
        'status': 'online',
        'openai_configured': bool(config.OPENAI_API_KEY),
        'pdfs_loaded': bool(chatbot.pdf_content),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Validar configuración
    config_errors = config.validate_config()
    if config_errors:
        print("Errores de configuración:")
        for error in config_errors:
            print(f"  - {error}")
        print("\nPor favor, corrige estos errores antes de continuar.")
        exit(1)
    
    print(f"🚀 Iniciando Chatbot PAC en http://{config.HOST}:{config.PORT}")
    print(f"📚 Modelo OpenAI: {config.OPENAI_MODEL}")
    print(f"🔧 Modo debug: {config.DEBUG}")
    
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
