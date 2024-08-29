import json

# Cargar el archivo JSON original
INPUT_FILENAME = 'api/data/countries.json'  # Ajusta la ruta según tu estructura
OUTPUT_FILENAME = 'api/data/countries_updated.json'

# Leer el JSON
with open(INPUT_FILENAME, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Eliminar la clave 'postalCode' de cada elemento
for item in data:
    if 'postalCode' in item:
        del item['postalCode']

# Guardar el nuevo JSON con las claves ordenadas alfabéticamente
with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False, sort_keys=True)

print(f"Archivo generado: {OUTPUT_FILENAME}")
