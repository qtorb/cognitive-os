# 📂 Secciones Colapsables - Cognitive OS

## Descripción

Las secciones de **Ideas** y **Conexiones** pueden ahora colapsarse en desktop para maximizar el espacio visual dedicado a **Decisiones** (el output).

---

## Comportamiento

### Desktop (900px+)
- ✅ Botón de collapse/expand visible (⌄)
- ✅ Estado persiste en localStorage
- ✅ Click para contraer/expandir
- ✅ Sección colapsada muestra solo el título

### Móvil (-900px)
- ❌ Botón de collapse oculto
- ❌ Tabs funcionan como siempre
- ✅ Responsive: Las secciones nunca están colapsadas en mobile

---

## Implementación Técnica

### CSS
```css
.main-card.collapsed {
  max-height: 80px;           /* Altura del header */
  overflow: hidden;
}

.collapse-btn {
  display: none;              /* Hidden en mobile */
  cursor: pointer;
  transition: transform 0.3s;
}

.main-card.collapsed .collapse-btn {
  transform: rotate(-90deg);  /* Gira el ícono */
}

@media (max-width: 900px) {
  .collapse-btn {
    display: none;            /* Never visible on mobile */
  }
  .main-card.collapsed {
    max-height: none;         /* Ignora collapsed en mobile */
  }
}
```

### JavaScript
```javascript
function toggleSectionCollapse(section) {
  const sectionElement = document.querySelector(`[data-section="${section}"]`);
  sectionElement.classList.toggle('collapsed');

  // Guardar estado
  const isCollapsed = sectionElement.classList.contains('collapsed');
  localStorage.setItem(`section_collapsed_${section}`, isCollapsed);
}

function loadCollapsedSections() {
  ['ideas', 'connections'].forEach(section => {
    const isCollapsed = localStorage.getItem(`section_collapsed_${section}`) === 'true';
    if (isCollapsed) {
      document.querySelector(`[data-section="${section}"]`).classList.add('collapsed');
    }
  });
}
```

### HTML
```html
<div class="main-card" data-section="ideas">
  <div class="section-header">
    <h2>💡 Tus ideas</h2>
    <div>
      <button onclick="openIdeaModal()" class="btn btn-primary">+ Nueva idea</button>
      <button class="collapse-btn" onclick="toggleSectionCollapse('ideas')">⌄</button>
    </div>
  </div>
  <!-- Contenido -->
</div>
```

---

## Estados Visuales

### Expandido (Defecto)
```
┌─────────────────────────────────────────┐
│ 💡 Tus ideas              [+ Nueva] [⌄] │
├─────────────────────────────────────────┤
│ [Filtros] [Tarjetas de ideas...]        │
└─────────────────────────────────────────┘
```

### Colapsado
```
┌─────────────────────────────────────────┐
│ 💡 Tus ideas              [+ Nueva] [>] │
└─────────────────────────────────────────┘
```

---

## Casos de Uso

1. **Usuario enfocado en decisiones:** Colapsa Ideas y Conexiones para ver solo Decisiones
2. **Usuario revisando flujo:** Expande todo para ver el contexto completo
3. **Persistencia:** El estado se recuerda entre sesiones (localStorage)

---

## Datos Guardados

Cada sección tiene una key en localStorage:
- `section_collapsed_ideas` → "true" | "false"
- `section_collapsed_connections` → "true" | "false"

---

## Próximas Mejoras

- [ ] Animación smooth al colapsar (transition height)
- [ ] Botón para "colapsar todas" / "expandir todas"
- [ ] Indicador visual de que hay contenido oculto
- [ ] Resumen comprimido (ej: "5 ideas, 3 conexiones" cuando está colapsado)
