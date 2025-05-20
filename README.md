# Assignment Flask API

A Flask-based API for managing a donut menu with simple add, get, and delete endpoints.

## Run locally
```bash
pip install flask
python app.py

GET /items

POST /items
## Example of post body
## A simple validation is done to the type is alphabet only.
## A response "Type field must contain only alphabets." will be shown if the type is not alphabet
{
  "type": "Cake",
  "name": "New Donut",
  "ppu": 0.65,
  "batters": {
    "batter": [{"id": "1010", "type": "Vanilla"}]
  },
  "topping": [
    {"id": "5010", "type": "Sprinkles"}
  ]
}

DELETE /items?id=0001&type=donut
## Delete only if both match.
## A response "error": "Item not found or type mismatch." will be shown if either one mismatch.
## A response "error": "Missing id or type" if id or type is missing.

##Uses a class (ValidationService) with dependency injection-style passing.

## Run on cloud

https://nativeduck.pythonanywhere.com/items
