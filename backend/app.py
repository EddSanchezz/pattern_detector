from flask import Flask, request, jsonify
from flask_cors import CORS
from automata import PatternMatcher

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

matcher = PatternMatcher()

PATTERN_DESCRIPTIONS = {
    "email": "Correo electrónico",
    "phone": "Número telefónico móvil colombiano",
    "date": "Fecha (día/mes/año)",
    "url": "Dirección URL web",
    "plate": "Placa de vehículo colombiano",
    "document_id": "Tipo de documento colombiano (CC, NIT, TI, RC, PEP)",
    "password": "Contraseña segura (min 8 caracteres, mayúscula, minúscula, número, carácter especial)"
}


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


@app.route('/api/patterns', methods=['GET'])
def patterns():
    patterns_list = []
    for name in matcher.get_available_patterns():
        patterns_list.append({
            "name": name,
            "description": PATTERN_DESCRIPTIONS.get(name, "")
        })
    return jsonify({"patterns": patterns_list})


@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    text = data.get('text', '')
    patterns = data.get('patterns', [])
    if not text:
        return jsonify({"error": "Text is required"}), 400
    if not patterns:
        return jsonify({"error": "At least one pattern must be specified"}), 400

    results = matcher.search(text, patterns)
    total_matches = sum(len(r) for r in results.values())
    return jsonify({"matches": results, "total_matches": total_matches})


@app.route('/api/validate', methods=['POST'])
def validate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    pattern = data.get('pattern')
    value = data.get('value', '')
    if not pattern:
        return jsonify({"error": "Pattern name is required"}), 400

    valid, pattern_name, val, error = matcher.validate(pattern, value)
    return jsonify({
        "valid": valid,
        "pattern": pattern_name,
        "value": val,
        "error": error
    })


@app.route('/api/validate-form', methods=['POST'])
def validate_form():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    fields = data.get('fields', {})
    if not fields:
        return jsonify({"error": "Fields object is required"}), 400

    errors = {}
    all_valid = True
    for field_name, field_data in fields.items():
        pattern = field_data.get('pattern')
        value = field_data.get('value', '')
        if not pattern:
            errors[field_name] = f"Pattern not specified for field '{field_name}'"
            all_valid = False
            continue

        valid, _, _, error = matcher.validate(pattern, value)
        if not valid:
            errors[field_name] = error
            all_valid = False

    return jsonify({
        "valid": all_valid,
        "errors": errors
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)