# Guía de Usuario - PatternGuard

## 1. Introducción

PatternGuard es una herramienta de búsqueda y validación de patrones diseñada para identificar y verificar formatos específicos en textos y formularios. Utiliza tecnología de autómatas para ofrecer validación precisa sin dependencias de librerías externas.

## 2. Requisitos del Sistema

### 2.1 Requisitos de Software

- **Python**: Versión 3.10 o superior
- **Node.js**: Versión 18 o superior
- **Navegador web**: Chrome, Firefox, Edge o Safari (versión reciente)

### 2.2 Requisitos de Hardware

- Mínimo 4GB de RAM
- 500MB de espacio en disco

## 3. Instalación

### 3.1 Instalar Backend

1. Abrir una terminal
2. Navegar a la carpeta `backend`:
   ```bash
   cd backend
   ```
3. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
4. Activar el entorno virtual:
   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`
5. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### 3.2 Instalar Frontend

1. Abrir una nueva terminal
2. Navegar a la carpeta `frontend`:
   ```bash
   cd frontend
   ```
3. Instalar dependencias:
   ```bash
   npm install
   ```

## 4. Ejecución

### 4.1 Iniciar Backend

1. Asegurarse de que el entorno virtual está activado
2. Ejecutar:
   ```bash
   python app.py
   ```
3. El backend estará disponible en `http://localhost:5000`

### 4.2 Iniciar Frontend

1. En otra terminal (mantener el backend activo)
2. Ejecutar:
   ```bash
   npm run dev
   ```
3. La aplicación estará disponible en `http://localhost:5173`

## 5. Uso de la Aplicación

### 5.1 Vista de Búsqueda de Patrones

Esta vista permite buscar patrones específicos dentro de un texto.

**Pasos:**

1. Acceder a la pestaña "Búsqueda de Patrones"
2. Ingresar o pegar el texto donde buscar patrones
3. Seleccionar los tipos de patrones a buscar (email, teléfono, etc.)
4. Hacer clic en el botón "Buscar Patrones"
5. Revisar los resultados en la tabla inferior

**Interpretación de resultados:**

| Campo | Descripción |
|-------|-------------|
| Tipo | Categoría del patrón encontrado |
| Valor | Texto exacto que hizo match |
| Posición | Índice inicial y final en el texto |

### 5.2 Vista de Validación de Formularios

Esta vista permite validar campos de formulario en tiempo real.

**Campos disponibles:**

| Campo | Descripción | Ejemplo válido |
|-------|-------------|----------------|
| Correo electrónico | Direcciones de email válidas | usuario@ejemplo.com |
| Teléfono | Números de teléfono | +57 300 123 4567 |
| Fecha | Fechas en múltiples formatos | 25/12/2024, 2024-12-25 |
| URL | Direcciones web | https://google.com |
| Placa de vehículo | Matrículas de vehículos | ABC-1234 |
| Documento ID | Identificadores alfanuméricos | ABC123456789 |

**Indicadores de estado:**

| Indicador | Significado |
|-----------|-------------|
| ✓ (verde) | El valor ingresada es válido |
| ✗ (rojo) | El valor ingresado no cumple el formato |
| Spinner | Validando... |

**Flujo de validación:**

1. Escribir en cada campo
2. La validación es automática tras 300ms de inactividad
3. El botón "Enviar" se habilita cuando todos los campos son válidos

## 6. Patrones Soportados

### 6.1 Correo Electrónico

Acepta formatos estándar de email como `usuario@dominio.com`

### 6.2 Teléfono

Acepta formatos:
- Internacional: `+57 300 123 4567`
- Con paréntesis: `(300) 123-4567`
- Sin formato: `3001234567`

### 6.3 Fecha

Acepta múltiples formatos:
- `DD/MM/YYYY`: `25/12/2024`
- `YYYY-MM-DD`: `2024-12-25`
- `MM/DD/YYYY`: `12/25/2024`

### 6.4 URL

Acepta direcciones con http y https:
- `https://google.com`
- `http://test.org/path`

### 6.5 Placa de Vehículo

Acepta formatos latinoamericanos:
- `ABC-1234`
- `AB 12345`
- `ABCD123456`

### 6.6 Documento ID

Acepta identificadores alfanuméricos de 5 a 15 caracteres.

## 7. Casos de Uso Comunes

### 7.1 Extraer emails de un texto

1. Copiar el texto que contiene emails
2. Ir a "Búsqueda de Patrones"
3. Seleccionar solo "Correo electrónico"
4. Buscar y extraer los resultados

### 7.2 Validar datos de registro

1. Ir a "Validación de Formularios"
2. Completar cada campo con los datos del usuario
3. Asegurarse de que todos muestren ✓ verde
4. Enviar el formulario

### 7.3 Buscar múltiples tipos de información

1. Pegar un texto con diferentes tipos de datos
2. Seleccionar todos los patrones relevantes
3. Buscar para ver todos los elementos encontrados

## 8. Solución de Problemas

### 8.1 El backend no inicia

**Problema:** Error al ejecutar `python app.py`

**Solución:**
1. Verificar que el entorno virtual está activado
2. Verificar que `pip install -r requirements.txt` se ejecutó correctamente
3. Verificar que el puerto 5000 no está en uso

### 8.2 El frontend no conecta al backend

**Problema:** Errores de conexión en la consola del navegador

**Solución:**
1. Verificar que el backend está corriendo en `http://localhost:5000`
2. Verificar que no hay firewall bloqueando las conexiones
3. Reiniciar ambos servicios

### 8.3 La búsqueda no encuentra patrones

**Problema:** No hay resultados aunque debería haberlos

**Solución:**
1. Verificar que se seleccionó al menos un patrón
2. Verificar que el texto contiene el tipo de dato esperado
3. Probar con un ejemplo conocido (ej: email estándar)

## 9. Créditos y Licencia

Desarrollado como proyecto académico para la materia de Teoría de Lenguajes Formales.

**Autores:** Proyecto grupal - Universidad de Quillindio

**Versión:** 1.0.0