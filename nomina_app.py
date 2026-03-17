"""
Aplicación de Gestión de Nómina - Constructora Mejor
Autor: Alexander Sinisterra
Curso: Abstracción y Codificación
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


# ──────────────────────────────────────────────────────────────────────────────
# Clase pública GestionEmpleados
# ──────────────────────────────────────────────────────────────────────────────

class GestionEmpleados:
    """Almacena los datos de un empleado y calcula su pago de nómina."""

    VALOR_DIA = {
        "Servicios Generales": 40000,
        "Administrativo": 50000,
        "Electricista": 60000,
        "Mecánico": 80000,
        "Soldador": 90000,
    }

    def __init__(self, identificacion: str, nombre: str, genero: str,
                 cargo: str, dias_laborados: int, fecha_registro: str):
        self.identificacion = identificacion
        self.nombre = nombre
        self.genero = genero
        self.cargo = cargo
        self.dias_laborados = dias_laborados
        self.fecha_registro = fecha_registro

    def calcular_pago(self) -> float:
        """Calcula el costo total del pago según cargo y días laborados."""
        valor_dia = self.VALOR_DIA.get(self.cargo, 0)
        return valor_dia * self.dias_laborados


# ──────────────────────────────────────────────────────────────────────────────
# Ventana de Reporte
# ──────────────────────────────────────────────────────────────────────────────

class VentanaReporte(tk.Toplevel):
    """Muestra el reporte de nómina del empleado registrado."""

    def __init__(self, parent, empleado: GestionEmpleados):
        super().__init__(parent)
        self.title("Reporte de Nómina")
        self.resizable(False, False)
        self.configure(bg="#f0f4f8")
        self._build(empleado)
        self.grab_set()

    def _build(self, emp: GestionEmpleados):
        pad = {"padx": 20, "pady": 6}

        tk.Label(self, text="REPORTE DE NÓMINA", font=("Arial", 14, "bold"),
                 bg="#2c3e50", fg="white", width=38).pack(fill="x")

        frame = tk.Frame(self, bg="#f0f4f8", padx=20, pady=10)
        frame.pack(fill="both", expand=True)

        campos = [
            ("Nombre:", emp.nombre),
            ("ID:", emp.identificacion),
            ("Género:", emp.genero),
            ("Cargo:", emp.cargo),
            ("Días Laborados:", str(emp.dias_laborados)),
            ("Fecha de Registro:", emp.fecha_registro),
            ("Valor Día:", f"$ {GestionEmpleados.VALOR_DIA.get(emp.cargo, 0):,.0f}"),
            ("VALOR A PAGAR:", f"$ {emp.calcular_pago():,.0f}"),
        ]

        for i, (label, valor) in enumerate(campos):
            bold = "bold" if label == "VALOR A PAGAR:" else "normal"
            tk.Label(frame, text=label, font=("Arial", 11, bold),
                     bg="#f0f4f8", anchor="w", width=18).grid(row=i, column=0, sticky="w", pady=3)
            tk.Label(frame, text=valor, font=("Arial", 11),
                     bg="#f0f4f8", anchor="w").grid(row=i, column=1, sticky="w", pady=3)

        tk.Button(self, text="Cerrar", command=self.destroy,
                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=6).pack(pady=10)


# ──────────────────────────────────────────────────────────────────────────────
# Ventana de Registro de Datos
# ──────────────────────────────────────────────────────────────────────────────

class VentanaRegistro(tk.Toplevel):
    """Interfaz para registrar los datos del empleado."""

    CARGOS = list(GestionEmpleados.VALOR_DIA.keys())

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Nómina - Constructora Mejor")
        self.resizable(False, False)
        self.configure(bg="#f0f4f8")
        self._empleado: GestionEmpleados | None = None
        self._build()
        self.grab_set()

    # ── construcción de la UI ──────────────────────────────────────────────

    def _build(self):
        # Encabezado
        tk.Label(self, text="REGISTRO DE EMPLEADO",
                 font=("Arial", 14, "bold"), bg="#2c3e50", fg="white",
                 width=42).pack(fill="x")

        form = tk.Frame(self, bg="#f0f4f8", padx=24, pady=14)
        form.pack(fill="both", expand=True)

        # Identificación
        self._add_label(form, "Identificación:", 0)
        self._id_var = tk.StringVar()
        tk.Entry(form, textvariable=self._id_var, width=28,
                 font=("Arial", 10)).grid(row=0, column=1, sticky="w", pady=4)

        # Nombre completo
        self._add_label(form, "Nombre Completo:", 1)
        self._nombre_var = tk.StringVar()
        tk.Entry(form, textvariable=self._nombre_var, width=28,
                 font=("Arial", 10)).grid(row=1, column=1, sticky="w", pady=4)

        # Género
        self._add_label(form, "Género:", 2)
        self._genero_var = tk.StringVar(value="Masculino")
        genero_frame = tk.Frame(form, bg="#f0f4f8")
        genero_frame.grid(row=2, column=1, sticky="w", pady=4)
        tk.Radiobutton(genero_frame, text="Masculino", variable=self._genero_var,
                       value="Masculino", bg="#f0f4f8",
                       font=("Arial", 10)).pack(side="left")
        tk.Radiobutton(genero_frame, text="Femenino", variable=self._genero_var,
                       value="Femenino", bg="#f0f4f8",
                       font=("Arial", 10)).pack(side="left", padx=8)

        # Cargo laboral
        self._add_label(form, "Cargo Laboral:", 3)
        self._cargo_var = tk.StringVar()
        cargo_combo = ttk.Combobox(form, textvariable=self._cargo_var,
                                   values=self.CARGOS, state="readonly",
                                   width=25, font=("Arial", 10))
        cargo_combo.grid(row=3, column=1, sticky="w", pady=4)
        cargo_combo.bind("<<ComboboxSelected>>", self._on_cargo_change)

        # Valor día (deshabilitado)
        self._add_label(form, "Valor Día de Trabajo:", 4)
        self._valor_dia_var = tk.StringVar(value="")
        self._valor_dia_entry = tk.Entry(form, textvariable=self._valor_dia_var,
                                         width=20, font=("Arial", 10),
                                         state="disabled", disabledforeground="#555")
        self._valor_dia_entry.grid(row=4, column=1, sticky="w", pady=4)

        # Días laborados
        self._add_label(form, "Días Laborados:", 5)
        self._dias_var = tk.StringVar()
        tk.Entry(form, textvariable=self._dias_var, width=10,
                 font=("Arial", 10)).grid(row=5, column=1, sticky="w", pady=4)

        # Fecha de registro (automática)
        self._add_label(form, "Fecha de Registro:", 6)
        self._fecha_var = tk.StringVar(value=str(date.today()))
        tk.Entry(form, textvariable=self._fecha_var, width=16,
                 font=("Arial", 10), state="disabled",
                 disabledforeground="#555").grid(row=6, column=1, sticky="w", pady=4)

        # Botones
        btn_frame = tk.Frame(self, bg="#f0f4f8", pady=10)
        btn_frame.pack()

        tk.Button(btn_frame, text="Guardar Registro",
                  command=self._guardar, bg="#27ae60", fg="white",
                  font=("Arial", 10, "bold"), padx=12, pady=6).pack(side="left", padx=6)

        tk.Button(btn_frame, text="Calcular Nómina / Mostrar Reporte",
                  command=self._mostrar_reporte, bg="#2980b9", fg="white",
                  font=("Arial", 10, "bold"), padx=12, pady=6).pack(side="left", padx=6)

        tk.Button(btn_frame, text="Salir",
                  command=self._salir, bg="#e74c3c", fg="white",
                  font=("Arial", 10, "bold"), padx=12, pady=6).pack(side="left", padx=6)

    @staticmethod
    def _add_label(parent, text: str, row: int):
        tk.Label(parent, text=text, font=("Arial", 10, "bold"),
                 bg="#f0f4f8", anchor="w", width=22).grid(
            row=row, column=0, sticky="w", pady=4)

    # ── lógica de eventos ──────────────────────────────────────────────────

    def _on_cargo_change(self, _event=None):
        cargo = self._cargo_var.get()
        valor = GestionEmpleados.VALOR_DIA.get(cargo, 0)
        self._valor_dia_var.set(f"$ {valor:,.0f}")

    def _guardar(self):
        if not self._validar():
            return
        self._empleado = GestionEmpleados(
            identificacion=self._id_var.get().strip(),
            nombre=self._nombre_var.get().strip(),
            genero=self._genero_var.get(),
            cargo=self._cargo_var.get(),
            dias_laborados=int(self._dias_var.get().strip()),
            fecha_registro=self._fecha_var.get(),
        )
        messagebox.showinfo("Éxito", "Registro guardado correctamente.")

    def _mostrar_reporte(self):
        if self._empleado is None:
            messagebox.showwarning("Advertencia",
                                   "Primero guarde un registro de empleado.")
            return
        VentanaReporte(self, self._empleado)

    def _salir(self):
        if messagebox.askyesno("Salir", "¿Desea salir de la aplicación?"):
            self.master.destroy()

    def _validar(self) -> bool:
        if not self._id_var.get().strip():
            messagebox.showerror("Error", "Ingrese la identificación.")
            return False
        if not self._nombre_var.get().strip():
            messagebox.showerror("Error", "Ingrese el nombre completo.")
            return False
        if not self._cargo_var.get():
            messagebox.showerror("Error", "Seleccione un cargo.")
            return False
        dias = self._dias_var.get().strip()
        if not dias or not dias.isdigit() or int(dias) <= 0 or int(dias) > 31:
            messagebox.showerror("Error", "Ingrese un número válido de días laborados (1-31).")
            return False
        return True


# ──────────────────────────────────────────────────────────────────────────────
# Ventana de Login
# ──────────────────────────────────────────────────────────────────────────────

class VentanaLogin(tk.Tk):
    """Interfaz de acceso con contraseña enmascarada."""

    PASSWORD = "4682"

    def __init__(self):
        super().__init__()
        self.title("Acceso - Gestión de Nómina")
        self.resizable(False, False)
        self.configure(bg="#2c3e50")
        self._build()

    def _build(self):
        tk.Label(self, text="CONSTRUCTORA MEJOR",
                 font=("Arial", 16, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=(24, 4))
        tk.Label(self, text="Sistema de Gestión de Nómina",
                 font=("Arial", 12), bg="#2c3e50", fg="#bdc3c7").pack()
        tk.Label(self, text="Autor: Alkexander Sinisterra",
                 font=("Arial", 10, "italic"), bg="#2c3e50", fg="#95a5a6").pack(pady=(4, 20))

        card = tk.Frame(self, bg="#ecf0f1", padx=30, pady=20,
                        relief="groove", bd=2)
        card.pack(padx=40, pady=10)

        tk.Label(card, text="Contraseña:", font=("Arial", 11, "bold"),
                 bg="#ecf0f1").pack(anchor="w")
        self._pwd_var = tk.StringVar()
        tk.Entry(card, textvariable=self._pwd_var, show="*",
                 font=("Arial", 12), width=20).pack(pady=6)

        tk.Button(card, text="Ingresar", command=self._ingresar,
                  bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                  padx=16, pady=6).pack(pady=4)

        self.bind("<Return>", lambda _: self._ingresar())

    def _ingresar(self):
        if self._pwd_var.get() == self.PASSWORD:
            self.withdraw()
            reg = VentanaRegistro(self)
            reg.protocol("WM_DELETE_WINDOW", lambda: (reg.destroy(), self.destroy()))
        else:
            messagebox.showerror("Acceso denegado",
                                 "Contraseña incorrecta. Inténtelo de nuevo.")
            self._pwd_var.set("")


# ──────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()