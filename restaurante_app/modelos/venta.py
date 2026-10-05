from dataclasses import asdict, dataclass


@dataclass
class Venta:
    id: int
    fecha: str
    producto: str
    cantidad: int
    total: float
    cliente: str = "Cliente"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", 0),
            fecha=data.get("fecha", ""),
            producto=data.get("producto", ""),
            cantidad=int(data.get("cantidad", 0)),
            total=float(data.get("total", 0)),
            cliente=data.get("cliente", "Cliente"),
        )
