import json
from pathlib import Path


class ArchivoServicio:
    def __init__(self, archivo: str | Path):
        self.archivo = Path(archivo)

    def leer(self):
        if not self.archivo.exists():
            return []

        try:
            with open(self.archivo, "r", encoding="utf-8") as file:
                datos = json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

        return datos if isinstance(datos, list) else []

    def guardar(self, datos):
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        with open(self.archivo, "w", encoding="utf-8") as file:
            json.dump(datos, file, ensure_ascii=False, indent=2)
