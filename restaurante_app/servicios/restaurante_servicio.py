import json
from pathlib import Path

from restaurante_app.modelos.producto import Producto
from restaurante_app.modelos.usuario import Usuario
from restaurante_app.modelos.venta import Venta
from restaurante_app.servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    ROLES = ["Administrador", "Empleado", "Cliente"]

    def __init__(self, datos_dir=None):
        base_dir = Path(datos_dir) if datos_dir else Path(__file__).resolve().parents[1] / "datos"
        self.datos_dir = base_dir if base_dir.suffix == "" else base_dir.parent
        self.usuarios_path = self.datos_dir / "usuarios.json"
        self.productos_path = self.datos_dir / "productos.json"
        self.ventas_path = self.datos_dir / "ventas.json"
        self._inicializar_archivos()
        self._usuarios = self._cargar_usuarios()
        self._productos = self._cargar_productos()
        self._ventas = self._cargar_ventas()

    def _inicializar_archivos(self):
        self.datos_dir.mkdir(parents=True, exist_ok=True)

        if not self.usuarios_path.exists():
            usuarios_iniciales = [
                Usuario(1, "Administrador", "admin", "admin123", "Administrador").to_dict(),
                Usuario(2, "Empleado Demo", "empleado", "empleado123", "Empleado").to_dict(),
                Usuario(3, "Cliente Demo", "cliente", "cliente123", "Cliente").to_dict(),
            ]
            ArchivoServicio(self.usuarios_path).guardar(usuarios_iniciales)

        if not self.productos_path.exists():
            productos_iniciales = [
                Producto(1, "Ceviche", "Plato fuerte", 25.5, 12).to_dict(),
                Producto(2, "Lomo saltado", "Plato fuerte", 29.0, 8).to_dict(),
                Producto(3, "Jugo de naranja", "Bebida", 6.5, 25).to_dict(),
            ]
            ArchivoServicio(self.productos_path).guardar(productos_iniciales)

        if not self.ventas_path.exists():
            ventas_iniciales = [
                Venta(1, "2026-10-04", "Ceviche", 2, 51.0, "Cliente Demo").to_dict(),
                Venta(2, "2026-10-04", "Lomo saltado", 1, 29.0, "Cliente Demo").to_dict(),
            ]
            ArchivoServicio(self.ventas_path).guardar(ventas_iniciales)

    def _cargar_usuarios(self):
        datos = ArchivoServicio(self.usuarios_path).leer()
        return [Usuario.from_dict(item) for item in datos]

    def _cargar_productos(self):
        datos = ArchivoServicio(self.productos_path).leer()
        return [Producto.from_dict(item) for item in datos]

    def _cargar_ventas(self):
        datos = ArchivoServicio(self.ventas_path).leer()
        return [Venta.from_dict(item) for item in datos]

    def _guardar_usuarios(self):
        ArchivoServicio(self.usuarios_path).guardar([usuario.to_dict() for usuario in self._usuarios])

    def _guardar_productos(self):
        ArchivoServicio(self.productos_path).guardar([producto.to_dict() for producto in self._productos])

    def _guardar_ventas(self):
        ArchivoServicio(self.ventas_path).guardar([venta.to_dict() for venta in self._ventas])

    def listar_usuarios(self):
        return [usuario.to_dict() for usuario in self._usuarios]

    def listar_productos(self):
        return [producto.to_dict() for producto in self._productos]

    def listar_ventas(self):
        return [venta.to_dict() for venta in self._ventas]

    def autenticar_usuario(self, usuario: str, password: str):
        for usuario_obj in self._usuarios:
            if usuario_obj.usuario.lower() == usuario.lower() and usuario_obj.password == password:
                return usuario_obj
        return None

    def obtener_usuario_por_id(self, usuario_id):
        for usuario in self._usuarios:
            if usuario.id == int(usuario_id):
                return usuario
        return None

    def _validar_rol(self, rol):
        if rol not in self.ROLES:
            raise ValueError(f"El rol debe ser uno de: {', '.join(self.ROLES)}")

    def _validar_usuario_unico(self, nombre_usuario, usuario_id=None):
        for usuario in self._usuarios:
            if usuario.usuario.lower() == nombre_usuario.lower() and usuario.id != (usuario_id or -1):
                raise ValueError("El nombre de usuario ya existe. Elija otro.")

    def registrar_usuario(self, nombre, usuario, password, rol="Cliente"):
        nombre = (nombre or "").strip()
        usuario = (usuario or "").strip()
        password = (password or "").strip()
        rol = (rol or "Cliente").strip()

        if not nombre or not usuario or not password:
            raise ValueError("Nombre, usuario y contraseña son obligatorios.")
        if len(password) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres.")

        self._validar_rol(rol)
        self._validar_usuario_unico(usuario)

        usuario_id = max((usuario_obj.id for usuario_obj in self._usuarios), default=0) + 1
        nuevo_usuario = Usuario(usuario_id, nombre, usuario, password, rol)
        self._usuarios.append(nuevo_usuario)
        self._guardar_usuarios()
        return nuevo_usuario.to_dict()

    def actualizar_usuario(self, usuario_id, nombre=None, usuario=None, password=None, rol=None):
        usuario_actual = self.obtener_usuario_por_id(usuario_id)
        if usuario_actual is None:
            return False

        nuevo_nombre = (nombre if nombre is not None else usuario_actual.nombre).strip()
        nuevo_usuario = (usuario if usuario is not None else usuario_actual.usuario).strip()
        nueva_password = (password if password is not None else usuario_actual.password).strip()
        nuevo_rol = (rol if rol is not None else usuario_actual.rol).strip()

        if not nuevo_nombre or not nuevo_usuario or not nueva_password:
            raise ValueError("Nombre, usuario y contraseña son obligatorios.")
        if len(nueva_password) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres.")

        self._validar_rol(nuevo_rol)
        self._validar_usuario_unico(nuevo_usuario, usuario_actual.id)

        usuario_actual.nombre = nuevo_nombre
        usuario_actual.usuario = nuevo_usuario
        usuario_actual.password = nueva_password
        usuario_actual.rol = nuevo_rol
        self._guardar_usuarios()
        return True

    def eliminar_usuario(self, usuario_id):
        usuario = self.obtener_usuario_por_id(usuario_id)
        if usuario is None:
            return False
        self._usuarios = [item for item in self._usuarios if item.id != int(usuario_id)]
        self._guardar_usuarios()
        return True

    def registrar_producto(self, nombre, categoria, precio, stock):
        nombre = (nombre or "").strip()
        categoria = (categoria or "").strip()
        if not nombre or not categoria:
            raise ValueError("El nombre y la categoría del producto son obligatorios.")

        producto_id = max((producto.id for producto in self._productos), default=0) + 1
        producto = Producto(producto_id, nombre, categoria, float(precio), int(stock))
        self._productos.append(producto)
        self._guardar_productos()
        return producto.to_dict()

    def registrar_venta(self, fecha, producto, cantidad, total, cliente):
        venta_id = max((venta.id for venta in self._ventas), default=0) + 1
        venta = Venta(venta_id, fecha, producto, int(cantidad), float(total), cliente)
        self._ventas.append(venta)
        self._guardar_ventas()
        return venta.to_dict()
