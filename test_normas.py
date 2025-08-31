import requests
import json

def test_chatbot_normas():
    """Probar que el chatbot esté usando el prompt especializado en normas"""
    
    url = "http://127.0.0.1:5000/api/chat"
    
    # Preguntas específicas sobre normas y definiciones
    test_questions = [
        "¿Qué es el Sistema de Gestión de Calidad según el curso?",
        "¿Cómo define el curso una auditoría?",
        "¿Qué establece la RES 258:2020?",
        "¿Cuáles son los criterios de auditoría según el manual?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Pregunta {i}: {question}")
        print("=" * 60)
        
        try:
            response = requests.post(
                url,
                headers={'Content-Type': 'application/json'},
                json={'message': question}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Respuesta del chatbot:")
                print(data['response'])
                
                # Verificar características del prompt de normas
                response_text = data['response'].lower()
                
                print("\n🔍 Análisis del prompt de normas:")
                print("-" * 40)
                
                # Verificar si menciona unidades del curso
                if any(unit in response_text for unit in ['unidad 1', 'unidad 2', 'unidad 3']):
                    print("✅ Menciona unidades específicas del curso")
                else:
                    print("❌ No menciona unidades específicas")
                
                # Verificar si cita definiciones textuales
                if any(phrase in response_text for phrase in ['se define como', 'se define', 'define como']):
                    print("✅ Cita definiciones textuales")
                else:
                    print("❌ No cita definiciones textuales")
                
                # Verificar si menciona fuentes específicas
                if any(source in response_text for source in ['iso', 'res', 'norma']):
                    print("✅ Menciona fuentes específicas (ISO, RES, etc.)")
                else:
                    print("❌ No menciona fuentes específicas")
                
                # Verificar si es específico vs genérico
                if any(phrase in response_text for phrase in ['en general', 'típicamente', 'usualmente']):
                    print("❌ Usa lenguaje genérico")
                else:
                    print("✅ Usa lenguaje específico")
                    
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except requests.exceptions.ConnectionError:
            print("❌ No se puede conectar al chatbot")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    test_chatbot_normas()
