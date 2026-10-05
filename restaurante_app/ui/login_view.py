import tkinter as tk
from tkinter import messagebox, ttk

from restaurante_app.servicios.restaurante_servicio import RestauranteServicio
from restaurante_app.ui.main_view import MainView


class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurante App - Acceso")
        self.root.geometry("420x360")
        self.root.minsize(380, 320)
        self.root.configure(bg="#f2f6fb")

        self.servicio = RestauranteServicio()
        self._crear_interfaz()
        self.root.bind("<Return>", self.verificar_login)

    def _crear_interfaz(self):
        container = ttk.Frame(self.root, padding=26)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, width=200, height=80, bg="#f2f6fb", highlightthickness=0)
        canvas.pack(pady=(0, 14))
        canvas.create_rectangle(20, 20, 180, 60, fill="#2c7be5", outline="")
        canvas.create_text(100, 40, text="Restaurante", fill="white", font=("Arial", 14, "bold"))

        ttk.Label(container, text="Usuario", font=("Arial", 11)).pack(anchor="w", pady=(0, 5))
        self.entry_usuario = ttk.Entry(container, width=30)
        self.entry_usuario.pack(fill="x", pady=(0, 10))

        ttk.Label(container, text="Contraseña", font=("Arial", 11)).pack(anchor="w", pady=(0, 5))
        self.entry_password = ttk.Entry(container, width=30, show="*")
        self.entry_password.pack(fill="x", pady=(0, 15))

        self.btn_login = ttk.Button(container, text="Iniciar sesión", command=self.verificar_login)
        self.btn_login.pack(fill="x")

    def verificar_login(self, event=None):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Datos incompletos", "Debe ingresar usuario y contraseña.")
            return

        usuario_encontrado = self.servicio.autenticar_usuario(usuario, password)
        if usuario_encontrado is None:
            messagebox.showerror("Credenciales inválidas", "Usuario o contraseña incorrectos.")
            return

        self.root.withdraw()
        ventana_principal = tk.Toplevel(self.root)
        MainView(ventana_principal, usuario_encontrado)
        ventana_principal.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())
