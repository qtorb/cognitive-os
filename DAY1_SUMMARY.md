# Día 1: Backend Auth + OAuth (Completado ✓)

## Cambios Realizados

### 1. **Actualizado `models.py`**
- Agregados campos OAuth al modelo `User`:
  - `email` (String, unique, index)
  - `google_id` (String, nullable)
  - `name` (String, nullable)
  - `picture_url` (String, nullable)
  - `onboarded` (Integer, para trackear si completó onboarding)

### 2. **Creado `auth.py` (nuevo archivo)**
Módulo completo de autenticación con:
- **Google OAuth 2.0**:
  - `get_google_token()` - Intercambia código por access token
  - `get_google_user_info()` - Obtiene datos del usuario
  - `process_google_login()` - Flujo completo de login
- **JWT Tokens**:
  - `create_jwt_token()` - Crea tokens JWT
  - `verify_jwt_token()` - Verifica y decodifica tokens
  - `get_current_user()` - Obtiene usuario autenticado

### 3. **Actualizado `main.py`**
- **Importes**: Agregado HTTPBearer y funciones de auth
- **Dependencia JWT**: `get_token_user()` para proteger endpoints
- **Nuevos Pydantic models**:
  - `GoogleAuthCallback` - Para recibir código OAuth
  - `AuthResponse` - Respuesta de autenticación
- **Nuevos endpoints**:
  - `GET /auth/login-url` - Retorna URL de login de Google
  - `POST /auth/callback` - Procesa callback de OAuth (intercambia código por JWT)
  - `GET /auth/me` - Obtiene perfil del usuario actual
- **Endpoints protegidos**: Todos los endpoints de negocio ahora requieren JWT:
  - `POST /onboarding` - Ahora usa usuario autenticado
  - `POST /decisions` - Requiere JWT
  - `GET /decisions` - Requiere JWT
  - `GET /decisions/{id}` - Requiere JWT, valida propiedad
  - `PATCH /decisions/{id}` - Requiere JWT, valida propiedad
  - Todos los endpoints de análisis AI requieren JWT
  - `GET /patterns` - Requiere JWT (cambió ruta de `/users/{id}/patterns`)
- **Helper functions**:
  - `get_user_decision()` - Obtiene decisión y valida propiedad del usuario

### 4. **Actualizado `requirements.txt`**
Agregadas dependencias:
- `python-jose[cryptography]==3.3.0` - Para JWT
- `requests==2.31.0` - Para HTTP calls a Google
- `google-auth-oauthlib==1.1.0` - Para Google OAuth

### 5. **Archivos nuevos**
- `.env.example` - Template de variables de entorno
- `README.md` - Documentación completa del proyecto
- `.gitignore` - Para ignorar archivos en Git

## Flujo de Autenticación

```
1. Frontend hace GET /auth/login-url
2. Retorna URL de Google OAuth
3. Usuario hace click y autoriza en Google
4. Google redirige a frontend con código
5. Frontend hace POST /auth/callback con código
6. Backend intercambia código por datos de usuario
7. Crea/actualiza usuario en DB
8. Retorna JWT token
9. Frontend guarda token (localStorage/sessionStorage)
10. Todos los requests posteriores incluyen: Authorization: Bearer {token}
```

## Seguridad

✅ **Implementado**:
- Google OAuth 2.0 (no manejo de contraseñas)
- JWT tokens con expiración (7 días por defecto)
- Validación de propiedad de recursos (usuario solo accede sus decisiones)
- HTTP Bearer auth en todos los endpoints protegidos

⚠️ **Para producción**:
- Cambiar `JWT_SECRET` a algo seguro
- Usar HTTPS obligatoriamente
- Configurar CORS correctamente (no `*`)
- Usar variables de entorno seguras

## Estado Actual

✅ Backend completamente funcional con:
- [x] Autenticación OAuth
- [x] JWT tokens
- [x] Endpoints protegidos
- [x] Validación de propiedad
- [x] Toda funcionalidad anterior (decisiones, análisis AI) integrada

❌ Siguiente:
- [ ] GitHub repo
- [ ] Cloudflare Tunnel (acceso público)
- [ ] Frontend
- [ ] Testing con usuarios reales

## Cómo Probar

```bash
# 1. Instalar dependencias
cd backend
pip install -r requirements.txt

# 2. Crear .env con Google OAuth credentials
cp .env.example .env
# (agregar GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)

# 3. Correr backend
python main.py

# 4. Ir a http://localhost:8000/docs para ver API interactiva
```

## Notas

- El onboarding ahora es **obligatorio después de login**
- Las decisiones están **aisladas por usuario** (no hay cross-contamination)
- El estado `onboarded` previene crear decisiones sin perfil
- Los endpoints de análisis usan el contexto personalizado del usuario
