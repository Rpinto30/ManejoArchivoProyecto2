"""Validaciones compartidas por las vistas."""
import re

EMAIL_RE = re.compile(r"^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,6}$")
PHONE_RE = re.compile(r"^\d{4}-\d{4}$")


def validate_contact(data: dict) -> list[str]:
    errors = []
    labels = {"name": "Nombre", "phone": "Teléfono", "email": "Correo", "city": "Ciudad"}
    empty = [label for key, label in labels.items() if not data.get(key, "").strip()]
    if empty:
        errors.append("Campos vacíos: " + ", ".join(empty) + ".")
    phone = data.get("phone", "").strip()
    if phone and not PHONE_RE.match(phone):
        errors.append("El teléfono debe tener el formato XXXX-XXXX.")
    email = data.get("email", "").strip()
    if email and not EMAIL_RE.match(email):
        errors.append("El correo no tiene un formato válido.")
    return errors
