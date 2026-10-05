from dataclasses import asdict, dataclass


@dataclass
class Usuario:
    id: int
    nombre: str
    usuario: str
    password: str
    rol: str = "Cliente"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", 0),
            nombre=data.get("nombre", ""),
            usuario=data.get("usuario", ""),
            password=data.get("password", ""),
            rol=data.get("rol", "Cliente"),
        )
