"""
╔══════════════════════════════════════════════════════════╗
║   📋  Formulario de Registro Multiopción                 ║
║   Widgets: Frame · Radiobutton · Checkbutton · Combobox  ║
║   Variables: IntVar · StringVar · BooleanVar             ║
╚══════════════════════════════════════════════════════════╝

Demuestra:
  - Agrupación de secciones con Frame
  - Selección única con Radiobutton   → StringVar / IntVar
  - Selección múltiple con Checkbutton → BooleanVar
  - Menú desplegable con ttk.Combobox → StringVar
  - Validación básica de formulario
  - Muestra de resultados en un widget Text
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# ──────────────────────────────────────────────────────
#  PALETA DE COLORES
# ──────────────────────────────────────────────────────
C = {
    "bg":       "#0d0f14",
    "surface":  "#161b26",
    "card":     "#1e2535",
    "border":   "#2a3147",
    "accent":   "#7c6fff",
    "green":    "#43d9ad",
    "pink":     "#ff6b9d",
    "yellow":   "#ffd166",
    "text":     "#e6eaf4",
    "muted":    "#7a8399",
    "entry":    "#252d3d",
    "hover":    "#2e3a52",
    "white":    "#ffffff",
    "error":    "#ff6b6b",
}

# ──────────────────────────────────────────────────────
#  FUENTES
# ──────────────────────────────────────────────────────
F = {
    "title":   ("Segoe UI", 20, "bold"),
    "heading": ("Segoe UI", 12, "bold"),
    "label":   ("Segoe UI", 10),
    "label_b": ("Segoe UI", 10, "bold"),
    "entry":   ("Segoe UI", 11),
    "small":   ("Segoe UI", 9),
    "mono":    ("Consolas", 10),
    "result":  ("Consolas", 10),
}

# ──────────────────────────────────────────────────────
#  DATOS DEL FORMULARIO
# ──────────────────────────────────────────────────────
PAISES = [
    "Mexico", "Argentina", "Colombia", "Espana", "Chile",
    "Peru", "Venezuela", "Ecuador", "Bolivia", "Uruguay",
    "Paraguay", "Guatemala", "Honduras", "El Salvador",
    "Nicaragua", "Costa Rica", "Panama", "Cuba",
    "Republica Dominicana", "Otro",
]

NIVELES_EDUCACION = [
    "Primaria", "Secundaria / Preparatoria",
    "Tecnico / Tecnologo", "Licenciatura / Ingenieria",
    "Maestria", "Doctorado",
]

GENERO_OPCIONES = [
    ("Masculino",        "M"),
    ("Femenino",         "F"),
    ("No binario",       "NB"),
    ("Prefiero no decir","ND"),
]

INTERESES = [
    ("Programacion",           "programacion"),
    ("Diseno grafico",         "diseno"),
    ("Ciencia de datos",       "datos"),
    ("Inteligencia Artificial","ia"),
    ("Desarrollo web",         "web"),
    ("Apps moviles",           "movil"),
    ("Videojuegos",            "juegos"),
    ("Ciberseguridad",         "seguridad"),
    ("Cloud / DevOps",         "cloud"),
    ("Testing / QA",           "testing"),
]

EXPERIENCIA_OPCIONES = [
    ("Sin experiencia (0 anos)",  "0"),
    ("Junior (1 - 2 anos)",       "1-2"),
    ("Mid-level (3 - 5 anos)",    "3-5"),
    ("Senior (6 - 10 anos)",      "6-10"),
    ("Experto (10+ anos)",        "10+"),
]


# ──────────────────────────────────────────────────────
#  CLASE PRINCIPAL
# ──────────────────────────────────────────────────────

class FormularioRegistro(tk.Tk):
    """Ventana principal del formulario de registro multiopcion."""

    def __init__(self):
        super().__init__()
        self.title("Formulario de Registro Multiopcion")
        self.geometry("820x780")
        self.minsize(780, 700)
        self.configure(bg=C["bg"])
        self.resizable(True, True)

        # ── Variables de control ──────────────────────
        self.var_nombre    = tk.StringVar()
        self.var_apellido  = tk.StringVar()
        self.var_email     = tk.StringVar()

        # StringVar — seleccion unica (Radiobutton)
        self.var_genero      = tk.StringVar(value="")
        self.var_experiencia = tk.StringVar(value="0")

        # StringVar — menu desplegable (Combobox)
        self.var_pais      = tk.StringVar()
        self.var_educacion = tk.StringVar()

        # BooleanVar — seleccion multiple (Checkbutton)
        self.vars_intereses = {
            clave: tk.BooleanVar(value=False)
            for _, clave in INTERESES
        }

        # IntVar — aceptar terminos (Checkbutton unico)
        self.var_terminos = tk.IntVar(value=0)

        self._apply_styles()
        self._build_ui()

    # ── Estilos ttk ───────────────────────────────────

    def _apply_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Dark.TCombobox",
            fieldbackground=C["entry"],
            background=C["entry"],
            foreground=C["text"],
            selectbackground=C["accent"],
            selectforeground=C["white"],
            arrowcolor=C["accent"],
            bordercolor=C["border"],
            padding=6,
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", C["entry"])],
            foreground=[("readonly", C["text"])],
        )
        style.configure(
            "Dark.TScrollbar",
            background=C["card"],
            troughcolor=C["surface"],
            bordercolor=C["border"],
            arrowcolor=C["muted"],
        )

    # ── UI principal ──────────────────────────────────

    def _build_ui(self):
        self._make_header()

        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical",
                                  command=canvas.yview,
                                  style="Dark.TScrollbar")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(canvas, bg=C["bg"])
        self.inner_id = canvas.create_window(
            (0, 0), window=self.inner, anchor="nw")

        self.inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(self.inner_id, width=e.width))

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        pad = {"padx": 20, "pady": 8, "fill": "x"}

        self._section_datos_personales().pack(**pad)
        self._section_genero().pack(**pad)
        self._section_ubicacion().pack(**pad)
        self._section_educacion_experiencia().pack(**pad)
        self._section_intereses().pack(**pad)
        self._section_terminos().pack(**pad)
        self._section_botones().pack(padx=20, pady=(4, 16), fill="x")
        self._section_resultados().pack(
            padx=20, pady=(0, 20), fill="both", expand=True)

    # ── Header ────────────────────────────────────────

    def _make_header(self):
        header = tk.Frame(self, bg=C["surface"], pady=18)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Formulario de Registro - Multiopcion",
            font=F["title"],
            bg=C["surface"],
            fg=C["accent"],
        ).pack()
        tk.Label(
            header,
            text="Frame  |  Radiobutton  |  Checkbutton  |  Combobox  |"
                 "  IntVar / StringVar / BooleanVar",
            font=F["small"],
            bg=C["surface"],
            fg=C["muted"],
        ).pack(pady=(3, 0))

    # ── Helpers ───────────────────────────────────────

    def _make_card(self, parent, title, color=None):
        color = color or C["accent"]
        card = tk.Frame(parent, bg=C["card"], padx=18, pady=14)
        tk.Frame(card, bg=color, height=3).pack(fill="x", pady=(0, 10))
        tk.Label(card, text=title, font=F["heading"],
                 bg=C["card"], fg=color).pack(anchor="w")
        return card

    def _make_entry(self, parent, label, textvariable):
        frame = tk.Frame(parent, bg=C["card"])
        tk.Label(frame, text=label, font=F["small"],
                 bg=C["card"], fg=C["muted"]).pack(anchor="w")
        container = tk.Frame(frame, bg=C["entry"], padx=10, pady=4)
        container.pack(fill="x", pady=(2, 0))
        tk.Entry(
            container,
            textvariable=textvariable,
            font=F["entry"],
            bg=C["entry"],
            fg=C["text"],
            insertbackground=C["accent"],
            relief="flat",
            bd=0,
        ).pack(fill="x")
        return frame

    def _hint(self, parent, text):
        tk.Label(parent, text=text, font=F["small"],
                 bg=C["card"], fg=C["muted"]).pack(anchor="w", pady=(8, 6))

    def _small_btn(self, parent, text, command):
        return tk.Button(
            parent, text=text, font=F["small"],
            bg=C["border"], fg=C["muted"],
            activebackground=C["hover"], activeforeground=C["text"],
            relief="flat", cursor="hand2", padx=8, pady=3, command=command,
        )

    # ── Secciones ─────────────────────────────────────

    def _section_datos_personales(self):
        card = self._make_card(self.inner, "Datos personales", C["accent"])

        row1 = tk.Frame(card, bg=C["card"])
        row1.pack(fill="x", pady=(10, 0))
        self._make_entry(row1, "Nombre *", self.var_nombre).pack(
            side="left", fill="x", expand=True, padx=(0, 8))
        self._make_entry(row1, "Apellido *", self.var_apellido).pack(
            side="left", fill="x", expand=True)
        self._make_entry(card, "Correo electronico *", self.var_email).pack(
            fill="x", pady=(8, 0))
        return card

    def _section_genero(self):
        """Radiobutton con StringVar — seleccion unica."""
        card = self._make_card(self.inner, "Genero", C["pink"])
        self._hint(card, "Radiobutton + StringVar  (seleccion unica: solo una opcion activa a la vez)")

        btn_frame = tk.Frame(card, bg=C["card"])
        btn_frame.pack(fill="x")

        for i, (texto, valor) in enumerate(GENERO_OPCIONES):
            tk.Radiobutton(
                btn_frame,
                text=texto,
                variable=self.var_genero,   # StringVar compartida
                value=valor,
                font=F["label"],
                bg=C["card"], fg=C["text"],
                activebackground=C["card"],
                activeforeground=C["pink"],
                selectcolor=C["entry"],
                cursor="hand2",
            ).grid(row=0, column=i, padx=(0, 20), sticky="w")
        return card

    def _section_ubicacion(self):
        """Combobox con StringVar — menu desplegable."""
        card = self._make_card(self.inner, "Ubicacion", C["green"])
        self._hint(card, "ttk.Combobox + StringVar  (menu desplegable, un valor a la vez)")

        tk.Label(card, text="Pais de residencia *",
                 font=F["small"], bg=C["card"], fg=C["muted"]).pack(anchor="w")

        self.combo_pais = ttk.Combobox(
            card,
            textvariable=self.var_pais,     # StringVar
            values=PAISES,
            state="readonly",
            style="Dark.TCombobox",
            font=F["entry"],
        )
        self.combo_pais.pack(fill="x", pady=(2, 0))
        self.combo_pais.set("-- Selecciona tu pais --")
        return card

    def _section_educacion_experiencia(self):
        """Combobox (educacion) + Radiobutton vertical (experiencia)."""
        card = self._make_card(self.inner, "Educacion y experiencia", C["yellow"])

        row = tk.Frame(card, bg=C["card"])
        row.pack(fill="x", pady=(10, 0))

        # Combobox educacion
        left = tk.Frame(row, bg=C["card"])
        left.pack(side="left", fill="x", expand=True, padx=(0, 16))

        tk.Label(left, text="Combobox + StringVar",
                 font=F["small"], bg=C["card"], fg=C["muted"]).pack(anchor="w")
        tk.Label(left, text="Nivel educativo *",
                 font=F["small"], bg=C["card"], fg=C["muted"]).pack(anchor="w")

        self.combo_edu = ttk.Combobox(
            left,
            textvariable=self.var_educacion,  # StringVar
            values=NIVELES_EDUCACION,
            state="readonly",
            style="Dark.TCombobox",
            font=F["entry"],
        )
        self.combo_edu.pack(fill="x", pady=(2, 0))
        self.combo_edu.set("-- Selecciona --")

        # Radiobutton experiencia
        right = tk.Frame(row, bg=C["card"])
        right.pack(side="left", fill="x", expand=True)

        tk.Label(right, text="Radiobutton + StringVar (vertical)",
                 font=F["small"], bg=C["card"], fg=C["muted"]).pack(anchor="w")

        for texto, valor in EXPERIENCIA_OPCIONES:
            tk.Radiobutton(
                right,
                text=texto,
                variable=self.var_experiencia,  # StringVar
                value=valor,
                font=F["small"],
                bg=C["card"], fg=C["text"],
                activebackground=C["card"],
                activeforeground=C["yellow"],
                selectcolor=C["entry"],
                cursor="hand2",
            ).pack(anchor="w")
        return card

    def _section_intereses(self):
        """Checkbutton con BooleanVar — seleccion multiple."""
        card = self._make_card(self.inner, "Areas de interes", C["accent"])
        self._hint(
            card,
            "Checkbutton + BooleanVar  (seleccion multiple: varias opciones activas a la vez)"
        )

        grid = tk.Frame(card, bg=C["card"])
        grid.pack(fill="x")

        cols = 2
        for i, (texto, clave) in enumerate(INTERESES):
            row_idx, col_idx = divmod(i, cols)
            tk.Checkbutton(
                grid,
                text=texto,
                variable=self.vars_intereses[clave],  # BooleanVar individual
                font=F["label"],
                bg=C["card"], fg=C["text"],
                activebackground=C["card"],
                activeforeground=C["accent"],
                selectcolor=C["entry"],
                cursor="hand2",
                onvalue=True, offvalue=False,
            ).grid(row=row_idx, column=col_idx,
                   padx=(0, 24), pady=2, sticky="w")

        for c in range(cols):
            grid.columnconfigure(c, weight=1)

        aux = tk.Frame(card, bg=C["card"])
        aux.pack(anchor="e", pady=(8, 0))
        self._small_btn(aux, "Seleccionar todos",
                        lambda: self._set_all_intereses(True)).pack(
            side="left", padx=(0, 6))
        self._small_btn(aux, "Limpiar seleccion",
                        lambda: self._set_all_intereses(False)).pack(side="left")
        return card

    def _section_terminos(self):
        """Checkbutton con IntVar — valor 0 o 1."""
        card = tk.Frame(self.inner, bg=C["surface"], padx=18, pady=12)
        tk.Checkbutton(
            card,
            text="  Acepto los Terminos y Condiciones  "
                 "(Checkbutton + IntVar:  0 = no aceptado  /  1 = aceptado)",
            variable=self.var_terminos,   # IntVar
            font=F["label"],
            bg=C["surface"], fg=C["text"],
            activebackground=C["surface"],
            activeforeground=C["green"],
            selectcolor=C["entry"],
            cursor="hand2",
            onvalue=1, offvalue=0,
        ).pack(anchor="w")
        return card

    def _section_botones(self):
        frame = tk.Frame(self.inner, bg=C["bg"])
        tk.Button(
            frame,
            text="Registrar",
            font=("Segoe UI", 11, "bold"),
            bg=C["accent"], fg=C["white"],
            activebackground="#6358e0",
            activeforeground=C["white"],
            relief="flat", cursor="hand2",
            padx=22, pady=9,
            command=self._on_registrar,
        ).pack(side="left")
        tk.Button(
            frame,
            text="Limpiar todo",
            font=F["label"],
            bg=C["border"], fg=C["muted"],
            activebackground=C["hover"],
            activeforeground=C["text"],
            relief="flat", cursor="hand2",
            padx=14, pady=9,
            command=self._on_limpiar,
        ).pack(side="left", padx=(10, 0))
        return frame

    def _section_resultados(self):
        """Panel Text para mostrar el resultado del formulario."""
        frame = tk.Frame(self.inner, bg=C["bg"])

        header = tk.Frame(frame, bg=C["surface"], padx=18, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="Resultado del formulario",
                 font=F["heading"], bg=C["surface"], fg=C["green"]).pack(side="left")
        tk.Button(
            header, text="Copiar",
            font=F["small"], bg=C["border"], fg=C["muted"],
            activebackground=C["hover"], activeforeground=C["text"],
            relief="flat", cursor="hand2", padx=8, pady=3,
            command=self._copiar_resultado,
        ).pack(side="right")

        txt_frame = tk.Frame(frame, bg=C["surface"], padx=4, pady=4)
        txt_frame.pack(fill="both", expand=True)

        self.txt_resultado = tk.Text(
            txt_frame,
            font=F["result"],
            bg=C["entry"], fg=C["green"],
            insertbackground=C["green"],
            relief="flat", bd=0,
            padx=14, pady=10,
            state="disabled",
            height=12,
            wrap="word",
        )
        scrolly = ttk.Scrollbar(txt_frame, orient="vertical",
                                command=self.txt_resultado.yview,
                                style="Dark.TScrollbar")
        self.txt_resultado.configure(yscrollcommand=scrolly.set)
        scrolly.pack(side="right", fill="y")
        self.txt_resultado.pack(side="left", fill="both", expand=True)

        self._set_result_text(
            "El resultado aparecera aqui despues de hacer clic en 'Registrar'.\n\n"
            "Variables de control utilizadas:\n"
            "  StringVar.get()   ->  Entry (texto libre) y Radiobutton\n"
            "  BooleanVar.get()  ->  Checkbutton (True / False)\n"
            "  IntVar.get()      ->  Checkbutton de terminos (0 / 1)\n"
            "  StringVar.get()   ->  ttk.Combobox (menu desplegable)\n"
        )
        return frame

    # ── Logica ────────────────────────────────────────

    def _set_result_text(self, text):
        self.txt_resultado.configure(state="normal")
        self.txt_resultado.delete("1.0", "end")
        self.txt_resultado.insert("1.0", text)
        self.txt_resultado.configure(state="disabled")

    def _set_all_intereses(self, value):
        for var in self.vars_intereses.values():
            var.set(value)

    def _validar(self):
        errores = []
        if not self.var_nombre.get().strip():
            errores.append("- El nombre es obligatorio.")
        if not self.var_apellido.get().strip():
            errores.append("- El apellido es obligatorio.")
        email = self.var_email.get().strip()
        if not email:
            errores.append("- El correo electronico es obligatorio.")
        elif "@" not in email or "." not in email.split("@")[-1]:
            errores.append("- El correo no parece valido.")
        if not self.var_genero.get():
            errores.append("- Selecciona una opcion de genero.")
        if self.var_pais.get() in ("", "-- Selecciona tu pais --"):
            errores.append("- Selecciona tu pais.")
        if self.var_educacion.get() in ("", "-- Selecciona --"):
            errores.append("- Selecciona tu nivel educativo.")
        if not self.var_terminos.get():
            errores.append("- Debes aceptar los Terminos y Condiciones.")
        return errores

    def _on_registrar(self):
        errores = self._validar()
        if errores:
            messagebox.showwarning(
                "Campos incompletos",
                "Por favor corrige:\n\n" + "\n".join(errores))
            return

        # ── Leer variables de control ──
        nombre      = self.var_nombre.get().strip()       # StringVar
        apellido    = self.var_apellido.get().strip()     # StringVar
        email       = self.var_email.get().strip()        # StringVar
        genero      = self.var_genero.get()               # StringVar <- Radiobutton
        pais        = self.var_pais.get()                 # StringVar <- Combobox
        educacion   = self.var_educacion.get()            # StringVar <- Combobox
        experiencia = self.var_experiencia.get()          # StringVar <- Radiobutton
        terminos    = self.var_terminos.get()             # IntVar    <- Checkbutton
        intereses   = [                                   # BooleanVar <- Checkbutton[]
            etiqueta
            for etiqueta, clave in INTERESES
            if self.vars_intereses[clave].get()
        ]

        sep = "-" * 52
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        resumen = (
            f"{'='*52}\n"
            f"  REGISTRO COMPLETADO  |  {ahora}\n"
            f"{'='*52}\n\n"
            f"DATOS PERSONALES\n{sep}\n"
            f"  Nombre     : {nombre} {apellido}\n"
            f"  Correo     : {email}\n"
            f"  Genero     : {genero}   <- StringVar (Radiobutton)\n\n"
            f"UBICACION\n{sep}\n"
            f"  Pais       : {pais}   <- StringVar (Combobox)\n\n"
            f"EDUCACION Y EXPERIENCIA\n{sep}\n"
            f"  Educacion  : {educacion}   <- StringVar (Combobox)\n"
            f"  Experiencia: {experiencia} anos   <- StringVar (Radiobutton)\n\n"
            f"AREAS DE INTERES\n{sep}\n"
        )

        if intereses:
            for item in intereses:
                resumen += f"  [x] {item}   <- BooleanVar (Checkbutton)\n"
        else:
            resumen += "  (ninguno seleccionado)\n"

        resumen += (
            f"\nTERMINOS\n{sep}\n"
            f"  Aceptados  : {'Si (IntVar = 1)' if terminos else 'No (IntVar = 0)'}  "
            f"<- IntVar (Checkbutton)\n\n"
            f"{'='*52}\n"
            f"  Registro completado correctamente.\n"
        )

        # Mostrar en el panel Text
        self._set_result_text(resumen)

        # También imprimir en consola
        print("\n" + resumen)

        messagebox.showinfo(
            "Registro exitoso",
            f"Bienvenido/a, {nombre}!\n"
            "Revisa el panel inferior para ver los detalles.")

    def _on_limpiar(self):
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_email.set("")
        self.var_genero.set("")
        self.var_experiencia.set("0")
        self.var_pais.set("")
        self.var_educacion.set("")
        self.combo_pais.set("-- Selecciona tu pais --")
        self.combo_edu.set("-- Selecciona --")
        self.var_terminos.set(0)
        self._set_all_intereses(False)
        self._set_result_text("Formulario limpiado. Completa los campos y presiona Registrar.\n")

    def _copiar_resultado(self):
        contenido = self.txt_resultado.get("1.0", "end").strip()
        if contenido:
            self.clipboard_clear()
            self.clipboard_append(contenido)
            messagebox.showinfo("Copiado", "Resultado copiado al portapapeles.")


# ──────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    app = FormularioRegistro()
    app.mainloop()
