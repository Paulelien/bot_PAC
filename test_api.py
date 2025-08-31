"""
Script de testing para la API del Chatbot PAC para LMS
Prueba todos los endpoints disponibles
"""

import requests
import json
import time
from datetime import datetime

# Configuración
API_BASE_URL = "http://localhost:5001/api"
TEST_SESSION_ID = f"test_session_{int(time.time())}"
TEST_USER_ID = "test_user_123"
TEST_COURSE_ID = "pac_course_test"

def print_test_result(test_name, success, response=None, error=None):
    """Imprimir resultado del test"""
    if success:
        print(f"✅ {test_name}: EXITOSO")
        if response:
            print(f"   📊 Status: {response.status_code}")
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    data = response.json()
                    print(f"   📝 Respuesta: {json.dumps(data, indent=2, ensure_ascii=False)}")
                except:
                    print(f"   📝 Respuesta: {response.text}")
    else:
        print(f"❌ {test_name}: FALLÓ")
        if error:
            print(f"   🚨 Error: {error}")
        if response:
            print(f"   📊 Status: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")

def test_health_check():
    """Probar endpoint de health check"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        success = response.status_code == 200
        print_test_result("Health Check", success, response)
        return success
    except Exception as e:
        print_test_result("Health Check", False, error=str(e))
        return False

def test_system_status():
    """Probar endpoint de estado del sistema"""
    try:
        response = requests.get(f"{API_BASE_URL}/status")
        success = response.status_code == 200
        print_test_result("System Status", success, response)
        return success
    except Exception as e:
        print_test_result("System Status", False, error=str(e))
        return False

def test_course_info():
    """Probar endpoint de información del curso"""
    try:
        response = requests.get(f"{API_BASE_URL}/course/info")
        success = response.status_code == 200
        print_test_result("Course Info", success, response)
        return success
    except Exception as e:
        print_test_result("Course Info", False, error=str(e))
        return False

def test_chat_message():
    """Probar endpoint de chat"""
    try:
        data = {
            "message": "¿Qué es el PAC?",
            "session_id": TEST_SESSION_ID,
            "user_id": TEST_USER_ID,
            "course_id": TEST_COURSE_ID
        }
        response = requests.post(f"{API_BASE_URL}/chat", json=data)
        success = response.status_code == 200
        print_test_result("Chat Message", success, response)
        return success
    except Exception as e:
        print_test_result("Chat Message", False, error=str(e))
        return False

def test_session_history():
    """Probar endpoint de historial de sesión"""
    try:
        response = requests.get(f"{API_BASE_URL}/chat/session/{TEST_SESSION_ID}")
        success = response.status_code == 200
        print_test_result("Session History", success, response)
        return success
    except Exception as e:
        print_test_result("Session History", False, error=str(e))
        return False

def test_course_search():
    """Probar endpoint de búsqueda en el curso"""
    try:
        data = {"search_term": "PAC"}
        response = requests.post(f"{API_BASE_URL}/course/search", json=data)
        success = response.status_code == 200
        print_test_result("Course Search", success, response)
        return success
    except Exception as e:
        print_test_result("Course Search", False, error=str(e))
        return False

def test_session_analytics():
    """Probar endpoint de estadísticas de sesiones"""
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/sessions")
        success = response.status_code == 200
        print_test_result("Session Analytics", success, response)
        return success
    except Exception as e:
        print_test_result("Session Analytics", False, error=str(e))
        return False

def test_clear_session():
    """Probar endpoint de limpiar sesión"""
    try:
        response = requests.delete(f"{API_BASE_URL}/chat/session/{TEST_SESSION_ID}")
        success = response.status_code == 200
        print_test_result("Clear Session", success, response)
        return success
    except Exception as e:
        print_test_result("Clear Session", False, error=str(e))
        return False

def test_invalid_endpoint():
    """Probar endpoint inexistente (debe devolver 404)"""
    try:
        response = requests.get(f"{API_BASE_URL}/invalid_endpoint")
        success = response.status_code == 404
        print_test_result("Invalid Endpoint (404)", success, response)
        return success
    except Exception as e:
        print_test_result("Invalid Endpoint (404)", False, error=str(e))
        return False

def test_invalid_chat_data():
    """Probar chat con datos inválidos (debe devolver 400)"""
    try:
        data = {"invalid_field": "test"}
        response = requests.post(f"{API_BASE_URL}/chat", json=data)
        success = response.status_code == 400
        print_test_result("Invalid Chat Data (400)", success, response)
        return success
    except Exception as e:
        print_test_result("Invalid Chat Data (400)", False, error=str(e))
        return False

def run_all_tests():
    """Ejecutar todos los tests"""
    print("🧪 INICIANDO TESTS DE LA API DEL CHATBOT PAC")
    print("=" * 60)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API Base URL: {API_BASE_URL}")
    print(f"🆔 Test Session ID: {TEST_SESSION_ID}")
    print("=" * 60)
    print()
    
    tests = [
        ("Health Check", test_health_check),
        ("System Status", test_system_status),
        ("Course Info", test_course_info),
        ("Chat Message", test_chat_message),
        ("Session History", test_session_history),
        ("Course Search", test_course_search),
        ("Session Analytics", test_session_analytics),
        ("Clear Session", test_clear_session),
        ("Invalid Endpoint (404)", test_invalid_endpoint),
        ("Invalid Chat Data (400)", test_invalid_chat_data)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🔍 Ejecutando: {test_name}")
        result = test_func()
        results.append((test_name, result))
        print()
        time.sleep(0.5)  # Pequeña pausa entre tests
    
    # Resumen de resultados
    print("=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} - {test_name}")
    
    print()
    print(f"📈 RESULTADOS: {passed}/{total} tests exitosos")
    
    if passed == total:
        print("🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
    else:
        print(f"⚠️  {total - passed} test(s) fallaron")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrumpidos por el usuario")
        exit(1)
    except Exception as e:
        print(f"\n\n💥 Error inesperado: {e}")
        exit(1)
