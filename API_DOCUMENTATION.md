# 🚀 API del Chatbot PAC para LMS

## 📋 Descripción General

API RESTful para integrar el Chatbot PAC (Plan de Aseguramiento de la Calidad en Construcción) con sistemas LMS (Learning Management System).

## 🔗 Base URL

```
http://localhost:5001/api
```

## 🔑 Autenticación

Actualmente la API no requiere autenticación, pero se recomienda implementar un sistema de API keys para producción.

## 📚 Endpoints Disponibles

### 1. 🏥 Health Check

**GET** `/api/health`

Verificar el estado de salud de la API.

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-30T20:00:00.000000",
  "service": "PAC Chatbot API",
  "version": "1.0.0"
}
```

### 2. 📊 Estado del Sistema

**GET** `/api/status`

Verificar el estado del sistema y configuración.

**Respuesta:**
```json
{
  "status": "online",
  "openai_configured": true,
  "pdfs_loaded": true,
  "active_sessions": 5,
  "timestamp": "2025-08-30T20:00:00.000000"
}
```

### 3. 💬 Chat Principal

**POST** `/api/chat`

Enviar mensaje al chatbot y recibir respuesta.

**Body:**
```json
{
  "message": "¿Qué es el PAC?",
  "session_id": "user123_session456",
  "user_id": "user123",
  "course_id": "pac_course_001"
}
```

**Respuesta:**
```json
{
  "response": "📚 INFORMACIÓN ENCONTRADA: El PAC es el Plan de Aseguramiento de la Calidad...",
  "session_id": "user123_session456",
  "user_id": "user123",
  "course_id": "pac_course_001",
  "timestamp": "2025-08-30T20:00:00.000000",
  "status": "success"
}
```

### 4. 📖 Historial de Sesión

**GET** `/api/chat/session/{session_id}`

Obtener el historial completo de una sesión.

**Respuesta:**
```json
{
  "session_id": "user123_session456",
  "history": [
    {
      "role": "user",
      "content": "¿Qué es el PAC?"
    },
    {
      "role": "assistant",
      "content": "📚 INFORMACIÓN ENCONTRADA: El PAC es..."
    }
  ],
  "message_count": 2,
  "timestamp": "2025-08-30T20:00:00.000000"
}
```

### 5. 🗑️ Limpiar Sesión

**DELETE** `/api/chat/session/{session_id}`

Eliminar el historial de una sesión específica.

**Respuesta:**
```json
{
  "message": "Sesión user123_session456 limpiada exitosamente",
  "timestamp": "2025-08-30T20:00:00.000000"
}
```

### 6. 📚 Información del Curso

**GET** `/api/course/info`

Obtener información general del curso PAC.

**Respuesta:**
```json
{
  "course_name": "Plan de Aseguramiento de la Calidad en Construcción (PAC)",
  "units": [
    {
      "id": 1,
      "name": "Definiciones y conceptos básicos del PAC",
      "description": "Conceptos fundamentales del sistema de calidad"
    },
    {
      "id": 2,
      "name": "Auditorías y certificación ISO 9001",
      "description": "Procesos de auditoría y certificación"
    },
    {
      "id": 3,
      "name": "RES 258:2020 y planes de calidad",
      "description": "Normativas y planes de calidad"
    }
  ],
  "pdfs_loaded": true,
  "timestamp": "2025-08-30T20:00:00.000000"
}
```

### 7. 🔍 Búsqueda en el Curso

**POST** `/api/course/search`

Buscar contenido específico en el curso.

**Body:**
```json
{
  "search_term": "PCdC"
}
```

**Respuesta:**
```json
{
  "search_term": "PCdC",
  "found": true,
  "context": "...Plan de Calidad del contrato (PCdC)...",
  "timestamp": "2025-08-30T20:00:00.000000"
}
```

### 8. 📈 Estadísticas de Sesiones

**GET** `/api/analytics/sessions`

Obtener estadísticas generales de uso.

**Respuesta:**
```json
{
  "total_sessions": 25,
  "total_messages": 150,
  "average_messages_per_session": 6.0,
  "timestamp": "2025-08-30T20:00:00.000000"
}
```

## 🛠️ Implementación en LMS

### Ejemplo de integración con JavaScript:

```javascript
// Configuración base
const API_BASE_URL = 'http://localhost:5001/api';

// Función para enviar mensaje al chatbot
async function sendMessage(message, sessionId, userId, courseId) {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        session_id: sessionId,
        user_id: userId,
        course_id: courseId
      })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error al enviar mensaje:', error);
    throw error;
  }
}

// Función para obtener historial de sesión
async function getSessionHistory(sessionId) {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/session/${sessionId}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error al obtener historial:', error);
    throw error;
  }
}

// Función para limpiar sesión
async function clearSession(sessionId) {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/session/${sessionId}`, {
      method: 'DELETE'
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error al limpiar sesión:', error);
    throw error;
  }
}

// Ejemplo de uso
const sessionId = `user_${userId}_${Date.now()}`;

sendMessage('¿Qué es el PAC?', sessionId, userId, courseId)
  .then(response => {
    console.log('Respuesta del chatbot:', response.response);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

### Ejemplo de integración con PHP:

```php
<?php
class PACChatbotAPI {
    private $baseUrl = 'http://localhost:5001/api';
    
    public function sendMessage($message, $sessionId, $userId, $courseId) {
        $data = [
            'message' => $message,
            'session_id' => $sessionId,
            'user_id' => $userId,
            'course_id' => $courseId
        ];
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->baseUrl . '/chat');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json'
        ]);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
    
    public function getSessionHistory($sessionId) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->baseUrl . '/chat/session/' . $sessionId);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
}

// Ejemplo de uso
$api = new PACChatbotAPI();
$sessionId = 'user_' . $userId . '_' . time();

$response = $api->sendMessage('¿Qué es el PAC?', $sessionId, $userId, $courseId);
echo $response['response'];
?>
```

## ⚙️ Configuración

### Variables de entorno (.env):

```env
# Configuración del servidor
API_HOST=0.0.0.0
API_PORT=5001
API_DEBUG=True
API_ENV=development

# Configuración de OpenAI
OPENAI_API_KEY=tu_api_key_aqui
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.7

# Configuración del chatbot
MAX_PDF_CONTENT_LENGTH=15000
MAX_SESSION_HISTORY=20

# Configuración de seguridad
CORS_ORIGINS=*
API_KEY_REQUIRED=False
API_KEY_HEADER=X-API-Key

# Configuración de rate limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Configuración de sesiones
SESSION_TIMEOUT=3600
MAX_SESSIONS_PER_USER=5
```

## 🚀 Iniciar la API

```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar la API
python api_lms.py
```

## 📝 Notas Importantes

1. **Sesiones**: Cada usuario puede tener múltiples sesiones activas
2. **Historial**: Se mantiene el historial de las últimas 20 conversaciones por sesión
3. **PDFs**: Los PDFs del curso se cargan automáticamente al iniciar la API
4. **Rate Limiting**: Por defecto 100 requests por hora por IP
5. **CORS**: Configurado para permitir peticiones desde cualquier origen (configurable)

## 🔒 Seguridad

- Implementar autenticación con API keys en producción
- Configurar CORS apropiadamente para tu dominio
- Habilitar rate limiting para prevenir abuso
- Validar y sanitizar todas las entradas del usuario

## 📞 Soporte

Para soporte técnico o preguntas sobre la implementación, contactar al equipo de desarrollo.
