# 🤖 Chatbot PAC - API para LMS

## 📋 Descripción

API RESTful para integrar el Chatbot PAC (Plan de Aseguramiento de la Calidad en Construcción) con sistemas LMS (Learning Management System).

## 🚀 Características

- **API RESTful** completa para integración con LMS
- **Chat inteligente** basado en OpenAI GPT-3.5-turbo
- **Gestión de sesiones** para múltiples usuarios
- **Búsqueda en contenido** del curso PAC
- **Estadísticas y analytics** de uso
- **CORS configurado** para integración web
- **Rate limiting** configurable

## 🌐 Endpoints Disponibles

- `GET /api/health` - Estado de salud de la API
- `GET /api/status` - Estado del sistema
- `POST /api/chat` - Chat principal
- `GET /api/chat/session/{id}` - Historial de sesión
- `DELETE /api/chat/session/{id}` - Limpiar sesión
- `GET /api/course/info` - Información del curso
- `POST /api/course/search` - Búsqueda en contenido
- `GET /api/analytics/sessions` - Estadísticas

## 🛠️ Instalación Local

### Prerrequisitos
- Python 3.9+
- OpenAI API Key

### Pasos
1. **Clonar el repositorio:**
```bash
git clone <tu-repositorio>
cd Chat_bot_PAC
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno:**
```bash
# Crear archivo .env
OPENAI_API_KEY=tu_api_key_aqui
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.7
```

4. **Ejecutar la API:**
```bash
python api_lms.py
```

## 🚀 Despliegue en Render

1. **Subir a Git:**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Conectar con Render:**
- Crear cuenta en [render.com](https://render.com)
- Conectar tu repositorio de Git
- Configurar como servicio web Python
- Agregar variable de entorno `OPENAI_API_KEY`

## 📚 Uso

### Ejemplo de integración con JavaScript:
```javascript
const API_URL = 'https://tu-api.onrender.com/api';

fetch(`${API_URL}/chat`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: "¿Qué es el PAC?",
    session_id: "user123_session001",
    user_id: "user123",
    course_id: "pac_course"
  })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

## 🔧 Configuración

### Variables de Entorno:
- `OPENAI_API_KEY` - Tu clave de API de OpenAI
- `OPENAI_MODEL` - Modelo de OpenAI (default: gpt-3.5-turbo)
- `OPENAI_MAX_TOKENS` - Máximo de tokens por respuesta
- `OPENAI_TEMPERATURE` - Temperatura para respuestas
- `MAX_PDF_CONTENT_LENGTH` - Longitud máxima del contenido PDF

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

## 📞 Soporte

Para soporte técnico, contacta al equipo de desarrollo.
