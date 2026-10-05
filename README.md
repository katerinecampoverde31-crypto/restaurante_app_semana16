# Restaurante App - Semana 16

Este proyecto mantiene la arquitectura modular de semanas anteriores y evoluciona la gestión de usuarios aplicando manejo de eventos en Tkinter.

## Objetivo

- Mantener la persistencia con archivos JSON.
- Conservar un sistema modular con modelos, servicios e interfaz.
- Gestionar usuarios con registro, consulta, actualización y eliminación desde una tabla Treeview.
- Usar eventos de Tkinter como `<<TreeviewSelect>>`, `<Return>`, `<Escape>` y `<<ComboboxSelected>>`.

## Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo.svg
│   └── icon.svg
├── __init__.py
├── main.py
└── README.md
```

## Roles implementados

- Administrador: acceso completo a usuarios.
- Empleado: acceso limitado.
- Cliente: acceso solo al panel principal.

## Eventos trabajados

- `<<TreeviewSelect>>`: carga los datos del usuario seleccionado en el formulario.
- `<Return>`: ejecuta la operación de registro reutilizando el mismo método.
- `<Escape>`: limpia el formulario y la selección actual.
- `<<ComboboxSelected>>`: responde al cambio del rol del usuario.
- `command=`: botones Registrar, Actualizar, Eliminar y Limpiar.

## Ejecución

1. Abrir una terminal en la raíz del proyecto.
2. Ejecutar:
   ```bash
   python main.py
   ```
3. Iniciar sesión con el usuario administrativo:
   - Usuario: `admin`
   - Contraseña: `admin123`

## Persistencia

Los datos se guardan en archivos JSON dentro de `restaurante_app/datos/`.
La lógica de negocio y validaciones están centralizadas en `RestauranteServicio`, evitando que la interfaz acceda directamente a los archivos.
