import json

from restaurante_app.servicios.restaurante_servicio import RestauranteServicio


def test_crear_usuario_y_autenticar_admin(tmp_path):
    datos_path = tmp_path / 'datos'
    servicio = RestauranteServicio(datos_path)

    servicio.registrar_usuario('Ana', 'ana', 'ana123', 'Cliente')
    usuario = servicio.autenticar_usuario('ana', 'ana123')

    assert usuario is not None
    assert usuario.rol == 'Cliente'

    admin = servicio.autenticar_usuario('admin', 'admin123')
    assert admin is not None and admin.rol == 'Administrador'


def test_actualizar_y_eliminar_usuario(tmp_path):
    datos_path = tmp_path / 'datos'
    servicio = RestauranteServicio(datos_path)

    nuevo = servicio.registrar_usuario('Luis', 'luis', 'luis123', 'Empleado')
    servicio.actualizar_usuario(nuevo['id'], nombre='Luis R.', rol='Cliente')
    usuario = servicio.obtener_usuario_por_id(nuevo['id'])

    assert usuario is not None
    assert usuario.nombre == 'Luis R.'
    assert usuario.rol == 'Cliente'

    servicio.eliminar_usuario(nuevo['id'])
    assert servicio.obtener_usuario_por_id(nuevo['id']) is None


def test_json_de_usuarios_incluye_rol(tmp_path):
    datos_path = tmp_path / 'datos'
    servicio = RestauranteServicio(datos_path)
    servicio.registrar_usuario('Pedro', 'pedro', 'pedro123', 'Cliente')

    with open(datos_path / 'usuarios.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    assert any(usuario.get('rol') for usuario in data)
