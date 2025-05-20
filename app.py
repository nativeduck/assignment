import json
import re
import logging
from flask import Flask, request, jsonify

# === Logging Setup ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# === Load data from file ===
DATA_FILE = "obj.json"
with open(DATA_FILE, "r") as f:
    items = json.load(f)

# === Flask App ===
app = Flask(__name__)

# === Validation Service ===
class ValidationService:
    def validate_type(self, type_value):
        if not re.fullmatch(r"[A-Za-z]+", type_value):
            raise ValueError("Type field must contain only alphabets.")

validator = ValidationService()

# === Routes ===
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items), 200

@app.route("/items", methods=["POST"])
def add_item():
    try:
        new_item = request.get_json()
        validator.validate_type(new_item.get("type", ""))
        
        # Generate new ID
        existing_ids = [int(i["id"]) for i in items]
        next_id = f"{max(existing_ids) + 1:04d}"
        new_item["id"] = next_id
        items.append(new_item)

        # Save to file
        with open(DATA_FILE, "w") as f:
            json.dump(items, f, indent=4)

        return jsonify({"message": "Item added", "id": next_id}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/items", methods=["DELETE"])
def delete_item():
    item_id = request.args.get("id")
    item_type = request.args.get("type")

    if not item_id or not item_type:
        return jsonify({"error": "Missing 'id' or 'type' parameter"}), 400

    global items
    for i, item in enumerate(items):
        if item["id"] == item_id and item["type"] == item_type:
            del items[i]
            with open(DATA_FILE, "w") as f:
                json.dump(items, f, indent=4)
            return jsonify({"message": "Item deleted"}), 200

    return jsonify({"error": "Item not found or type mismatch"}), 404

if __name__ == '__main__':
    app.run(debug=True)