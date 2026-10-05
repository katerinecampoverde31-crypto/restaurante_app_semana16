import tkinter as tk
from tkinter import messagebox, ttk

from restaurante_app.servicios.restaurante_servicio import RestauranteServicio


class MainView:
    def __init__(self, root, usuario_actual):
        self.root = root
        self.usuario_actual = usuario_actual
        self.servicio = RestauranteServicio()
        self.root.title(f"Panel principal - {usuario_actual.nombre} ({usuario_actual.rol})")
        self.root.geometry("1100x700")
        self.root.configure(bg="#eef3f8")

        self._crear_encabezado()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tab_productos = ttk.Frame(self.notebook)
        self.tab_ventas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_productos, text="Productos")
        self.notebook.add(self.tab_ventas, text="Ventas")

        self._cargar_tab_productos()
        self._cargar_tab_ventas()

        if usuario_actual.rol == "Administrador":
            self.tab_usuarios = ttk.Frame(self.notebook)
            self.notebook.add(self.tab_usuarios, text="Usuarios")
            self._cargar_tab_usuarios()
        else:
            self.tab_usuarios = None
            self.notebook.add(ttk.Frame(self.notebook), text="Usuarios")
            ttk.Label(self.notebook.tabs()[-1], text="No tienes permisos para gestionar usuarios.", font=("Arial", 11)).pack(pady=50)

    def _crear_encabezado(self):
        frame = ttk.Frame(self.root, padding=(12, 12, 12, 6))
        frame.pack(fill="x")

        ttk.Label(frame, text="Sistema de restaurante", font=("Arial", 15, "bold")).pack(anchor="w")
        ttk.Label(frame, text=f"Usuario activo: {self.usuario_actual.nombre} | Rol: {self.usuario_actual.rol}", font=("Arial", 10)).pack(anchor="w")

    def _cargar_tab_productos(self):
        ttk.Label(self.tab_productos, text="Productos del restaurante", font=("Arial", 12, "bold")).pack(anchor="w", padx=12, pady=(16, 8))
        tree = ttk.Treeview(self.tab_productos, columns=("id", "nombre", "categoria", "precio", "stock"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nombre", text="Nombre")
        tree.heading("categoria", text="Categoría")
        tree.heading("precio", text="Precio")
        tree.heading("stock", text="Stock")
        tree.column("id", width=60, anchor="center")
        tree.column("nombre", width=220)
        tree.column("categoria", width=180)
        tree.column("precio", width=100, anchor="center")
        tree.column("stock", width=100, anchor="center")
        tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        for producto in self.servicio.listar_productos():
            tree.insert("", "end", values=(producto["id"], producto["nombre"], producto["categoria"], producto["precio"], producto["stock"]))

    def _cargar_tab_ventas(self):
        ttk.Label(self.tab_ventas, text="Ventas recientes", font=("Arial", 12, "bold")).pack(anchor="w", padx=12, pady=(16, 8))
        tree = ttk.Treeview(self.tab_ventas, columns=("id", "fecha", "producto", "cantidad", "total"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("fecha", text="Fecha")
        tree.heading("producto", text="Producto")
        tree.heading("cantidad", text="Cantidad")
        tree.heading("total", text="Total")
        tree.column("id", width=60, anchor="center")
        tree.column("fecha", width=140)
        tree.column("producto", width=200)
        tree.column("cantidad", width=100, anchor="center")
        tree.column("total", width=110, anchor="center")
        tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        for venta in self.servicio.listar_ventas():
            tree.insert("", "end", values=(venta["id"], venta["fecha"], venta["producto"], venta["cantidad"], venta["total"]))

    def _cargar_tab_usuarios(self):
        self.frame_form = ttk.Frame(self.tab_usuarios, padding=12)
        self.frame_form.pack(fill="x")

        self.var_id = tk.StringVar(value="")
        self.var_nombre = tk.StringVar()
        self.var_usuario = tk.StringVar()
        self.var_password = tk.StringVar()
        self.var_rol = tk.StringVar(value="Cliente")

        campos = [
            ("ID", self.var_id, False),
            ("Nombre", self.var_nombre, True),
            ("Usuario", self.var_usuario, True),
            ("Contraseña", self.var_password, True),
            ("Rol", self.var_rol, True),
        ]

        for idx, (label_text, variable, requerido) in enumerate(campos):
            fila = ttk.Frame(self.frame_form)
            fila.grid(row=idx // 2, column=idx % 2, padx=10, pady=8, sticky="ew")
            ttk.Label(fila, text=f"{label_text}:", width=16, anchor="w").pack(side="left")
            if label_text == "Rol":
                combo = ttk.Combobox(fila, textvariable=variable, values=["Administrador", "Empleado", "Cliente"], state="readonly", width=22)
                combo.bind("<<ComboboxSelected>>", self.on_rol_cambiado)
                combo.pack(side="left")
                self.combo_rol = combo
            else:
                if label_text == "Contraseña":
                    entry = ttk.Entry(fila, textvariable=variable, show="*", width=25)
                elif label_text == "ID":
                    entry = ttk.Entry(fila, textvariable=variable, state="readonly", width=25)
                else:
                    entry = ttk.Entry(fila, textvariable=variable, width=25)
                entry.pack(side="left")
                if label_text == "ID":
                    self.entry_id = entry
                elif label_text == "Nombre":
                    self.entry_nombre = entry
                elif label_text == "Usuario":
                    self.entry_usuario = entry
                elif label_text == "Contraseña":
                    self.entry_password = entry

        self.btn_registrar = ttk.Button(self.frame_form, text="Registrar", command=self.registrar_usuario)
        self.btn_registrar.grid(row=2, column=0, padx=10, pady=12, sticky="ew")
        self.btn_actualizar = ttk.Button(self.frame_form, text="Actualizar", command=self.actualizar_usuario)
        self.btn_actualizar.grid(row=2, column=1, padx=10, pady=12, sticky="ew")
        self.btn_eliminar = ttk.Button(self.frame_form, text="Eliminar", command=self.eliminar_usuario)
        self.btn_eliminar.grid(row=3, column=0, padx=10, pady=12, sticky="ew")
        self.btn_limpiar = ttk.Button(self.frame_form, text="Limpiar", command=self.limpiar_formulario)
        self.btn_limpiar.grid(row=3, column=1, padx=10, pady=12, sticky="ew")

        self.frame_form.columnconfigure(0, weight=1)
        self.frame_form.columnconfigure(1, weight=1)

        self.tree_usuarios = ttk.Treeview(self.tab_usuarios, columns=("id", "nombre", "usuario", "rol"), show="headings")
        self.tree_usuarios.heading("id", text="ID")
        self.tree_usuarios.heading("nombre", text="Nombre")
        self.tree_usuarios.heading("usuario", text="Usuario")
        self.tree_usuarios.heading("rol", text="Rol")
        self.tree_usuarios.column("id", width=60, anchor="center")
        self.tree_usuarios.column("nombre", width=180)
        self.tree_usuarios.column("usuario", width=150)
        self.tree_usuarios.column("rol", width=130)
        self.tree_usuarios.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.tree_usuarios.bind("<<TreeviewSelect>>", self.on_usuario_seleccionado)

        self.root.bind("<Return>", self.on_enter_registro)
        self.root.bind("<Escape>", self.on_escape_limpiar)

        self._recargar_usuarios_tree()

    def on_rol_cambiado(self, event=None):
        rol = self.var_rol.get()
        if rol:
            self.root.title(f"Panel principal - {self.usuario_actual.nombre} ({self.usuario_actual.rol}) - Rol seleccionado: {rol}")

    def on_enter_registro(self, event=None):
        self.registrar_usuario()

    def on_escape_limpiar(self, event=None):
        self.limpiar_formulario()

    def _recargar_usuarios_tree(self):
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        for usuario in self.servicio.listar_usuarios():
            self.tree_usuarios.insert("", "end", values=(usuario["id"], usuario["nombre"], usuario["usuario"], usuario["rol"]))

    def on_usuario_seleccionado(self, event=None):
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            return

        item = self.tree_usuarios.item(seleccion[0], "values")
        if not item:
            return

        usuario_id = int(item[0])
        usuario = self.servicio.obtener_usuario_por_id(usuario_id)
        if usuario is None:
            return

        self.var_id.set(str(usuario.id))
        self.var_nombre.set(usuario.nombre)
        self.var_usuario.set(usuario.usuario)
        self.var_password.set(usuario.password)
        self.var_rol.set(usuario.rol)

    def limpiar_formulario(self):
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_usuario.set("")
        self.var_password.set("")
        self.var_rol.set("Cliente")
        self.tree_usuarios.selection_remove(self.tree_usuarios.selection())

    def registrar_usuario(self):
        if self.var_id.get():
            self.actualizar_usuario()
            return

        nombre = self.var_nombre.get().strip()
        usuario = self.var_usuario.get().strip()
        password = self.var_password.get().strip()
        rol = self.var_rol.get().strip()

        if not nombre or not usuario or not password:
            messagebox.showwarning("Datos incompletos", "Debe completar nombre, usuario y contraseña.")
            return

        try:
            self.servicio.registrar_usuario(nombre, usuario, password, rol)
            self._recargar_usuarios_tree()
            self.limpiar_formulario()
            messagebox.showinfo("Registro correcto", "Usuario registrado con éxito.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def actualizar_usuario(self):
        usuario_id = self.var_id.get().strip()
        if not usuario_id:
            messagebox.showwarning("Selección requerida", "Seleccione un usuario para actualizar.")
            return

        nombre = self.var_nombre.get().strip()
        usuario = self.var_usuario.get().strip()
        password = self.var_password.get().strip()
        rol = self.var_rol.get().strip()

        try:
            actualizado = self.servicio.actualizar_usuario(
                int(usuario_id),
                nombre=nombre,
                usuario=usuario,
                password=password,
                rol=rol,
            )
            if actualizado:
                self._recargar_usuarios_tree()
                self.limpiar_formulario()
                messagebox.showinfo("Actualización", "Usuario actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el usuario.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def eliminar_usuario(self):
        usuario_id = self.var_id.get().strip()
        if not usuario_id:
            messagebox.showwarning("Selección requerida", "Seleccione un usuario para eliminar.")
            return

        if int(usuario_id) == self.usuario_actual.id:
            messagebox.showerror("Acción no permitida", "No puedes eliminar tu propia cuenta administrativa.")
            return

        confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Desea eliminar el usuario seleccionado?")
        if not confirmacion:
            return

        eliminado = self.servicio.eliminar_usuario(int(usuario_id))
        if eliminado:
            self._recargar_usuarios_tree()
            self.limpiar_formulario()
            messagebox.showinfo("Eliminado", "Usuario eliminado correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró el usuario para eliminar.")
