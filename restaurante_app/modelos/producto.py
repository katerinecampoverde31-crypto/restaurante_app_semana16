from dataclasses import asdict, dataclass


@dataclass
class Producto:
    id: int
    nombre: str
    categoria: str
    precio: float
    stock: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", 0),
            nombre=data.get("nombre", ""),
            categoria=data.get("categoria", ""),
            precio=float(data.get("precio", 0)),
            stock=int(data.get("stock", 0)),
        )
