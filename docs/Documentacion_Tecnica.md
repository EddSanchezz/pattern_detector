# Documentación Técnica - PatternGuard

## 1. Introducción

### 1.1 Propósito

Este documento describe la arquitectura técnica, diseño e implementación del sistema PatternGuard, desarrollado como proyecto académico para la materia de Teoría de Lenguajes Formales. El sistema implementa un motor de expresiones regulares basado en autómatas NFA (Non-deterministic Finite Automaton).

### 1.2 Alcance

- Motor de regex personalizado (sin uso de librerías predefinidas)
- Búsqueda de patrones en textos
- Validación de formularios interactivos
- API REST para comunicación frontend-backend

---

## 2. Teoría de Autómatas

### 2.1 Conceptos Fundamentales

#### Autómata Finito No Determinista (NFA)

Un NFA consiste en:
- Un conjunto de estados `Q`
- Un alfabeto de entrada `Σ`
- Una función de transición `δ: Q × Σ → P(Q)`
- Un estado inicial `q₀`
- Un conjunto de estados de aceptación `F ⊆ Q`

#### Construcción de Thompson

La construcción de Thompson es un algoritmo que convierte una expresión regular directamente a un NFA. Fue propuesta por Ken Thompson en 1968 y tiene las siguientes propiedades:

- Cada subexpresión crea nuevos estados
- Se utilizan ε-transiciones (transiciones vacías) para conectar componentes
- El NFA resultante tiene un único estado inicial y un único estado de aceptación

### 2.2 Algoritmos del Motor Regex

#### Tokenizer (Lexer)

El tokenizer analiza la cadena de la expresión regular y la convierte en una secuencia de tokens.

**Tokens soportados:**

| Token | Símbolo | Descripción |
|-------|---------|-------------|
| CHAR | `a`, `z` | Carácter literal |
| DOT | `.` | Cualquier carácter |
| STAR | `*` | Cero o más repeticiones (Kleene star) |
| PLUS | `+` | Una o más repeticiones |
| QMARK | `?` | Cero o una vez (opcional) |
| ALT | `\|` | Alternación (OR) |
| LPAREN | `(` | Inicio de grupo |
| RPAREN | `)` | Fin de grupo |
| LBRACKET | `[` | Inicio de clase de caracteres |
| RBRACKET | `]` | Fin de clase de caracteres |
| DASH | `-` | Rango en clase de caracteres |
| CARET | `^` | Negación en clase de caracteres |
| BACKSLASH | `\` | Secuencia de escape |

#### Parser (AST)

El parser construye un Árbol de Sintaxis Abstracta (AST) a partir de los tokens.

**Tipos de nodos AST:**

```
ASTNode (abstract)
├── CharNode         # a
├── DotNode          # .
├── ConcatNode       # abc
├── AltNode          # a|b
├── StarNode         # a*
├── PlusNode         # a+
├── OptionalNode     # a?
├── CharClassNode    # [a-zA-Z]
├── EscapeNode       # \d, \w, \s
└── GroupNode        # (abc)
```

#### Compiler (Thompson's Construction)

El compiler convierte el AST a NFA aplicando las siguientes reglas:

| Operación | NFA Result |
|-----------|------------|
| Carácter `a` | `s0 --a--> s1` |
| Concatenación `AB` | `A` conectado a `B` via ε |
| Alternación `A\|B` | Nuevo estado inicial con ε a `A` y `B` |
| Kleene star `A*` | Nuevo estado inicial con bypass y loop |
| Plus `A+` | Como star pero sin bypass a aceptación |
| Opcional `A?` | Como star pero solo bypass (sin loop) |

#### Executor (NFA Simulation)

La ejecución simula el NFA sobre el texto de entrada usando:

1. **ε-closure(s)**: Todos los estados alcanzables via ε-transiciones
2. **move(S, c)**: Todos los estados alcanzables desde `S` con carácter `c`
3. **Simulación**: Iterar sobre cada carácter del input

---

## 3. Arquitectura del Sistema

### 3.1 Diagrama de Componentes

```
┌──────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ PatternSearch│  │FormValidation│  │     ResultsTable    │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         └────────────────┼───────────────────┘              │
│                          │ fetch()                         │
└──────────────────────────┼──────────────────────────────────┘
                           │ HTTP
┌──────────────────────────┼──────────────────────────────────┐
│                    BACKEND API                               │
│  ┌─────────────┐  ┌───────┴───────┐  ┌─────────────────────┐  │
│  │  /search    │  │  /validate   │  │   /validate-form    │  │
│  └──────┬──────┘  └──────┬───────┘  └──────────┬──────────┘  │
│         └────────────────┴──────────────────────┘            │
│                          │                                   │
│  ┌──────────────────────┴──────────────────────────────────┐│
│  │                    RegexEngine                          ││
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        ││
│  │  │Tokenizer│→│ Parser │→│Compiler│→│Executor│        ││
│  │  └────────┘  └────────┘  └────────┘  └────────┘        ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Estructura de Datos del NFA

```python
class State:
    id: int                          # Identificador único
    transitions: Dict[str, List[State]]  # Transiciones por carácter
    is_accept: bool                  # Estado de aceptación

class NFA:
    start_state: State               # Estado inicial
    accept_states: Set[State]        # Estados de aceptación
    states: Set[State]               # Todos los estados
```

### 3.3 Formato de Datos

#### MatchResult

```python
@dataclass
class MatchResult:
    value: str       # Texto que hizo match
    start: int      # Índice inicial
    end: int        # Índice final
    matched: bool   # Siempre True para matches
```

#### API Response - Search

```json
{
  "matches": {
    "email": [{"value": "test@example.com", "start": 12, "end": 28}],
    "phone": [{"value": "+57 300 123 4567", "start": 42, "end": 59}]
  },
  "total_matches": 2
}
```

---

## 4. Implementación Detallada

### 4.1 Tokenizer

**Archivo:** `backend/regex_engine/tokenizer.py`

El tokenizer recorre la cadena de entrada carácter por carácter y emite tokens según las reglas léxicas definidas.

```python
def tokenize(pattern: str) -> List[Token]:
    tokenizer = Tokenizer(pattern)
    return tokenizer.tokenize()
```

### 4.2 Parser

**Archivo:** `backend/regex_engine/parser.py`

El parser utiliza recursión descendente con lookahead de un token para construir el AST.

**Precedencia de operadores:**

1. `*`, `+`, `?` (unarios, mayor precedencia)
2. Concatenación
3. `|` (alternación, menor precedencia)

### 4.3 Compiler

**Archivo:** `backend/regex_engine/compiler.py`

Implementa Thompson's Construction con las siguientes operaciones:

```python
def _char_to_nfa(self, char: str) -> NFA:
    s1 = NFA.new_state()
    s2 = NFA.new_state(is_accept=True)
    s1.add_transition(char, s2)
    return NFA(start=s1, accept_states={s2})
```

### 4.4 Executor

**Archivo:** `backend/regex_engine/executor.py`

Utiliza el algoritmo de simulación de NFA:

```python
def simulate(nfa: NFA, input_str: str) -> bool:
    current = epsilon_closure({nfa.start_state})
    for char in input_str:
        current = epsilon_closure(move(current, char))
    return any(s.is_accept for s in current)
```

---

## 5. API REST

### 5.1 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Verifica que el servicio esté activo |
| GET | `/api/patterns` | Retorna lista de patrones predefinidos |
| POST | `/api/search` | Busca patrones en texto |
| POST | `/api/validate` | Valida un valor contra un patrón |
| POST | `/api/validate-form` | Valida múltiples campos |

### 5.2 Códigos de Respuesta

| Código | Significado |
|--------|-------------|
| 200 | Solicitud exitosa |
| 400 | Solicitud mal formada |
| 404 | Patrón no encontrado |
| 422 | Error en validación del motor |
| 500 | Error interno del servidor |

---

## 6. Decisiones de Diseño

### 6.1 Sin uso de librerías regex predefinidas

El proyecto cumple con el requisito de implementar el procesamiento de expresiones regulares sin utilizar las librerías `re` de Python. Esto obliga a construir desde cero el tokenizer, parser, y executor.

### 6.2 Construcción de Thompson

Se eligió la construcción de Thompson por:
- Simplicidad de implementación
- Garantía de un único estado inicial y final
- Comportamiento bien definido para todas las operaciones

### 6.3 API RESTful

La separación en API REST permite que el frontend y backend evolucionen independientemente y facilita las pruebas.

---

## 7. Pruebas

### 7.1 Suite de Pruebas

El proyecto incluye una suite de pruebas unitarias en `backend/tests/`:

- `test_tokenizer.py`: Tests del lexer
- `test_parser.py`: Tests del parser AST
- `test_compiler.py`: Tests del compiler NFA
- `test_executor.py`: Tests del executor
- `test_patterns.py`: Tests de patrones predefinidos

### 7.2 Ejecución de Pruebas

```bash
cd backend
python -m pytest tests/ -v
```

---

## 8. Limitaciones y Trabajo Futuro

### 8.1 Limitaciones Actuales

- No soporta clases de caracteres negadas (`[^a-z]`)
- No soporta escapes completos (`\n`, `\t`, etc.)
- El matching es greedy (maximal) pero la implementación de search puede no encontrar todos los overlaps

### 8.2 Posibles Mejoras

- Implementar classes de caracteres negadas
- Soportar más secuencias de escape
- Mejorar el algoritmo de search para encontrar overlapping matches
- Implementar grouping y backreferences
- Optimizar el NFA para reducir número de estados

---

## 9. Glosario

| Término | Definición |
|---------|-----------|
| NFA | Non-deterministic Finite Automaton (Autómata Finito No Determinista) |
| AST | Abstract Syntax Tree (Árbol de Sintaxis Abstracta) |
| Thompson's Construction | Algoritmo para convertir regex a NFA |
| Token | Unidad léxica reconocida por el lexer |
| ε-transición | Transición que no consume caracteres de entrada |
| ε-closure | Conjunto de estados alcanzables via ε-transiciones |