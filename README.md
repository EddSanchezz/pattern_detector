# PatternGuard

Sistema de búsqueda y validación de patrones en textos mediante expresiones regulares y autómatas (NFA).

## Tabla de Contenidos

- [Descripción](#descripción)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [API Endpoints](#api-endpoints)
- [Estructura del Proyecto](#estructura-del-proyecto)

## Descripción

PatternGuard es una aplicación desarrollada como proyecto académico para la materia de Teoría de Lenguajes Formales. Implementa un motor de expresiones regulares basado en autómatas NFA (Non-deterministic Finite Automaton) utilizando la construcción de Thompson, permitiendo la búsqueda y validación de patrones en textos sin utilizar librerías regex predefinidas de Python.

## Arquitectura

```
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│   React Frontend │ ←───→ │   Python API    │ ←───→ │ Custom Regex    │
│   (Vite + Tail) │ HTTP  │   (Flask)        │       │ Engine (NFA)    │
└─────────────────┘        └─────────────────┘        └─────────────────┘
     localhost:5173            localhost:5000
```

### Componentes del Motor Regex

1. **Tokenizer**: Convierte la cadena regex en tokens (CHAR, STAR, PLUS, ALT, etc.)
2. **Parser**: Construye un AST (Abstract Syntax Tree) a partir de los tokens
3. **NFA**: Representación del autómata con estados y transiciones
4. **Compiler**: Implementa Thompson's Construction para convertir AST → NFA
5. **Executor**: Simula la ejecución del NFA sobre el texto de entrada
6. **Patterns**: Define los patrones predefinidos (email, phone, date, etc.)

## Requisitos

- Python 3.10+
- Node.js 18+
- npm o bun

## Instalación

### Backend

```bash
cd backend
python -m venv venv
# Activar venv:
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Ejecución

### Backend (Puerto 5000)

```bash
cd backend
python app.py
```

El servidor estará disponible en `http://localhost:5000`

### Frontend (Puerto 5173)

```bash
cd frontend
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

## API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/patterns` | Lista de patrones disponibles |
| POST | `/api/search` | Buscar patrones en texto |
| POST | `/api/validate` | Validar string contra patrón |
| POST | `/api/validate-form` | Validar formulario completo |

### Ejemplos

#### Buscar patrones

```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"text": "Mi email es test@example.com", "patterns": ["email"]}'
```

#### Validar campo

```bash
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"pattern": "email", "value": "test@example.com"}'
```

## Estructura del Proyecto

```
proyecto/
├── backend/
│   ├── app.py                  # Flask API
│   ├── requirements.txt
│   ├── regex_engine/
│   │   ├── __init__.py
│   │   ├── tokenizer.py       # Lexer
│   │   ├── parser.py          # AST
│   │   ├── nfa.py            # NFA representation
│   │   ├── compiler.py      # Thompson's Construction
│   │   ├── executor.py      # NFA simulation
│   │   ├── exceptions.py    # Custom exceptions
│   │   └── patterns.py      # Patrones predefinidos
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
└── docs/
```

## Patrones Disponibles

| Nombre | Descripción | Ejemplo válido |
|--------|-------------|----------------|
| email | Correo electrónico | test@example.com |
| phone | Teléfono | +57 300 123 4567 |
| date | Fecha | 25/12/2024 |
| url | URL | https://google.com |
| plate | Placa de vehículo | ABC-1234 |
| document_id | Identificador | ABC123456789 |

## Tecnologías

- **Backend**: Python 3, Flask, Flask-CORS
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React
- **Motor Regex**: Implementación NFA desde cero (Thompson's Construction)