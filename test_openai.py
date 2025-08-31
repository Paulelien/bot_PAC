#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con OpenAI
"""

import os
from dotenv import load_dotenv
import openai

# Cargar variables de entorno
load_dotenv()

def test_openai_connection():
    """Probar la conexión con OpenAI"""
    print("🔍 Probando conexión con OpenAI...")
    print("=" * 50)
    
    # Obtener API key
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"📋 API Key encontrada: {'Sí' if api_key else 'No'}")
    
    if not api_key:
        print("❌ ERROR: No se encontró OPENAI_API_KEY en el archivo .env")
        return False
    
    # Verificar formato de la API key
    if not api_key.startswith('sk-'):
        print("❌ ERROR: La API key no tiene el formato correcto (debe empezar con 'sk-')")
        return False
    
    print(f"✅ Formato de API key correcto")
    print(f"🔑 API Key: {api_key[:20]}...{api_key[-4:]}")
    
    try:
        # Configurar OpenAI
        openai.api_key = api_key
        
        # Hacer una prueba simple
        print("\n🧪 Haciendo prueba de conexión...")
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hola, responde solo 'OK' si puedes leer este mensaje."}
            ],
            max_tokens=10,
            temperature=0
        )
        
        print("✅ Conexión exitosa con OpenAI!")
        print(f"🤖 Respuesta: {response.choices[0].message.content}")
        return True
        
    except openai.AuthenticationError:
        print("❌ ERROR: API key inválida o expirada")
        print("💡 Verifica que tu API key sea correcta en https://platform.openai.com/")
        return False
        
    except openai.RateLimitError:
        print("❌ ERROR: Límite de uso excedido")
        print("💡 Verifica tu saldo en https://platform.openai.com/")
        return False
        
    except openai.APIConnectionError:
        print("❌ ERROR: Problema de conexión con OpenAI")
        print("💡 Verifica tu conexión a internet")
        return False
        
    except Exception as e:
        print(f"❌ ERROR inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    print("🏗️ Test de Conexión OpenAI - Chatbot PAC")
    print("=" * 50)
    
    success = test_openai_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡Todo está funcionando correctamente!")
        print("💡 El chatbot debería funcionar con IA")
    else:
        print("⚠️ Hay problemas con la configuración de OpenAI")
        print("💡 Revisa los errores anteriores")
    
    input("\nPresiona Enter para continuar...")
