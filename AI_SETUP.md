# Configurar Claude API para Cognitive OS

El análisis con IA está integrado, pero necesita tu API key de Claude.

## 1. Obtener API Key

1. Ve a https://console.anthropic.com
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys"
4. Crea una nueva API key
5. **Copia la clave** (solo se muestra una vez)

## 2. Configurar en tu computadora

### Windows (PowerShell)

```powershell
# Establece la variable de entorno
$env:ANTHROPIC_API_KEY="tu-api-key-aqui"

# Verifica que se guardó
$env:ANTHROPIC_API_KEY
```

Para hacerlo permanente, edita variables de entorno del sistema:
1. `Win + X` → "System" (o "Configuración")
2. "Advanced system settings"
3. "Environment Variables"
4. Nueva variable: `ANTHROPIC_API_KEY` = tu clave

### macOS/Linux

```bash
export ANTHROPIC_API_KEY="tu-api-key-aqui"
```

Para hacerlo permanente, agrega a `~/.zshrc` o `~/.bashrc`:
```bash
export ANTHROPIC_API_KEY="tu-api-key-aqui"
```

## 3. Instalar SDK de Claude

En la carpeta backend:

```powershell
python -m pip install anthropic
```

## 4. Reiniciar el servidor

```powershell
python main.py
```

Deberías ver: "Claude SDK available" (o similar)

## 5. Usar análisis en dashboard

En el dashboard, cada decisión tendrá botones:
- **Analizar** - Identifica gaps, sesgos y riesgos
- **Contraargumento** - Cuestiona las premisas
- **Síntesis** - Resume hallazgos
- **Pre-mortem** - "¿Y si falla?"

## Modo Demo

Si no tienes API key, el sistema funciona en modo demo:
- Respuestas de ejemplo
- Útil para testear UI
- Avisa que falta configuración

## ⚠️ Importante

- **No compartas tu API key públicamente**
- No la commits a Git
- La clave se lee desde variables de entorno
- Cuesta dinero según uso (barato para MVP)

## Verificar que funciona

En PowerShell/Terminal:

```powershell
python main.py
```

Si ves "Uvicorn running..." sin errores de "ANTHROPIC_API_KEY", está configurado.

Luego en el dashboard, intenta "Analizar" una decisión. Debería dar respuestas reales (no demo).

---

**¿Dudas?** El sistema funciona perfectamente sin API key en modo demo.
