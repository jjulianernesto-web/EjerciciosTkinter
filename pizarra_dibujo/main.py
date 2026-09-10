"""
╔══════════════════════════════════════════════════════════╗
║   🎨  Mini Pizarra de Dibujo                             ║
║   Widget: Canvas                                         ║
║   Eventos: ButtonPress · B1-Motion · ButtonRelease       ║
║   Metodos: create_line · create_oval · create_rectangle  ║
╚══════════════════════════════════════════════════════════╝

Demuestra:
  - Canvas  renderizado de graficos 2D en tiempo real
  - Binding de eventos de raton:
      <ButtonPress-1>    clic izquierdo presionado
      <B1-Motion>        mover con clic sostenido
      <ButtonRelease-1>  soltar clic izquierdo
  - create_line()      trazar lineas suaves (lapiz / pincel)
  - create_oval()      dibujar circulos y puntos
  - create_rectangle() dibujar rectangulos
  - event.x / event.y  coordenadas del raton en el Canvas
  - colorchooser       selector de color nativo del SO
  - Scale              control deslizante de grosor
  - Deshacer (Ctrl+Z)  pila de objetos Canvas
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, filedialog
from typing import Optional
import os


# ──────────────────────────────────────────────────────
#  PALETA Y CONSTANTES
# ──────────────────────────────────────────────────────

BG        = "#0d0f14"
SURFACE   = "#161b26"
CARD      = "#1e2535"
BORDER    = "#2a3147"
ACCENT    = "#7c6fff"
TEXT      = "#e6eaf4"
MUTED     = "#7a8399"
HOVER     = "#2e3a52"
WHITE     = "#ffffff"
CANVAS_BG = "#ffffff"   # fondo de la pizarra

FONT_UI    = ("Segoe UI", 9)
FONT_LABEL = ("Segoe UI", 8)
FONT_BOLD  = ("Segoe UI", 9, "bold")
FONT_TITLE = ("Segoe UI", 13, "bold")
FONT_SMALL = ("Segoe UI", 8)

# Paleta de colores rapidos
COLORES_RAPIDOS = [
    "#000000", "#ffffff", "#ff4444", "#ff8800",
    "#ffdd00", "#44cc44", "#00aaff", "#9966ff",
    "#ff44bb", "#00ddaa", "#8855ff", "#ff6644",
    "#334455", "#667788", "#aabbcc", "#ddeeFF",
]

# Herramientas disponibles
HERRAMIENTAS = [
    ("lapiz",      "✏",  "Lapiz (Ctrl+P)"),
    ("pincel",     "🖌",  "Pincel (Ctrl+B)"),
    ("borrador",   "⬜",  "Borrador (Ctrl+E)"),
    ("linea",      "╱",  "Linea (Ctrl+L)"),
    ("rectangulo", "□",  "Rectangulo (Ctrl+R)"),
    ("ovalo",      "○",  "Ovalo (Ctrl+V)"),
    ("rect_relleno","■", "Rect. relleno (Ctrl+F)"),
    ("oval_relleno","●", "Oval relleno (Ctrl+G)"),
]


# ──────────────────────────────────────────────────────
#  CLASE PRINCIPAL
# ──────────────────────────────────────────────────────

class Pizarra(tk.Tk):
    """Mini pizarra de dibujo con Canvas y eventos de raton."""

    def __init__(self):
        super().__init__()
        self.title("Mini Pizarra de Dibujo")
        self.geometry("1050x720")
        self.minsize(800, 550)
        self.configure(bg=BG)
        self.resizable(True, True)

        # ── Estado de dibujo ──────────────────────────
        self.herramienta   = tk.StringVar(value="lapiz")
        self.color_frente  = tk.StringVar(value="#000000")   # color pincel
        self.color_fondo   = tk.StringVar(value="#ffffff")   # color relleno
        self.grosor        = tk.IntVar(value=4)

        # Posicion anterior del raton (para trazado continuo)
        self._x_ant: Optional[int] = None
        self._y_ant: Optional[int] = None

        # Objeto temporal (para herramientas de forma)
        self._obj_temp: Optional[int] = None

        # Pila de deshacer  (lista de IDs de objetos Canvas)
        self._historial: list[list[int]] = []
        self._accion_actual: list[int]   = []

        # Botones de herramientas (para resaltar el activo)
        self._btns_herramienta: dict[str, tk.Button] = {}

        self._build_ui()
        self._bind_shortcuts()

    # ──────────────────────────────────────────────────
    #  CONSTRUCCION DE LA UI
    # ──────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        self._build_header()

        # Layout principal: sidebar izquierda + canvas + sidebar derecha
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True)

        self._build_left_panel(main)
        self._build_canvas(main)
        self._build_right_panel(main)

        # Barra de estado inferior
        self._build_statusbar()

    # ── Header ────────────────────────────────────────

    def _build_header(self):
        header = tk.Frame(self, bg=SURFACE, pady=10)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🎨  Mini Pizarra de Dibujo",
            font=FONT_TITLE,
            bg=SURFACE,
            fg=ACCENT,
        ).pack(side="left", padx=16)

        tk.Label(
            header,
            text="Canvas  ·  <ButtonPress-1>  ·  <B1-Motion>  ·  "
                 "create_line() / create_oval() / create_rectangle()",
            font=FONT_SMALL,
            bg=SURFACE,
            fg=MUTED,
        ).pack(side="left", padx=4)

        # Botones de accion en el header
        for texto, cmd in [
            ("🗑  Limpiar (Supr)", self.limpiar_canvas),
            ("↩  Deshacer (Ctrl+Z)", self.deshacer),
            ("💾  Guardar (Ctrl+S)", self.guardar_imagen),
        ]:
            tk.Button(
                header,
                text=texto,
                font=FONT_LABEL,
                bg=CARD,
                fg=MUTED,
                activebackground=HOVER,
                activeforeground=TEXT,
                relief="flat",
                cursor="hand2",
                padx=10,
                pady=4,
                command=cmd,
            ).pack(side="right", padx=(0, 6))

    # ── Panel izquierdo: herramientas ─────────────────

    def _build_left_panel(self, parent):
        panel = tk.Frame(parent, bg=SURFACE, width=80, pady=12)
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)

        tk.Label(
            panel,
            text="Herramienta",
            font=FONT_LABEL,
            bg=SURFACE,
            fg=MUTED,
        ).pack(pady=(0, 6))

        for clave, emoji, tooltip in HERRAMIENTAS:
            btn = tk.Button(
                panel,
                text=emoji,
                font=("Segoe UI Emoji", 16),
                bg=CARD,
                fg=TEXT,
                activebackground=ACCENT,
                activeforeground=WHITE,
                relief="flat",
                cursor="hand2",
                width=3,
                pady=6,
                command=lambda c=clave: self._seleccionar_herramienta(c),
            )
            btn.pack(pady=2, padx=8, fill="x")
            self._btns_herramienta[clave] = btn

            # Tooltip simple al pasar el raton
            self._add_tooltip(btn, tooltip)

        # Resaltar herramienta inicial
        self._resaltar_herramienta("lapiz")

    # ── Canvas principal ───────────────────────────────

    def _build_canvas(self, parent):
        container = tk.Frame(parent, bg=BORDER, padx=2, pady=2)
        container.pack(side="left", fill="both", expand=True,
                       padx=8, pady=8)

        # Scrollbars del canvas
        scroll_y = tk.Scrollbar(container, orient="vertical")
        scroll_x = tk.Scrollbar(container, orient="horizontal")
        scroll_y.pack(side="right",  fill="y")
        scroll_x.pack(side="bottom", fill="x")

        # El widget Canvas donde se dibuja todo
        self.canvas = tk.Canvas(
            container,
            bg=CANVAS_BG,
            cursor="crosshair",
            scrollregion=(0, 0, 2000, 2000),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)
        scroll_y.config(command=self.canvas.yview)
        scroll_x.config(command=self.canvas.xview)

        # ── Binding de eventos del raton ──
        # <ButtonPress-1>   → usuario presiona el boton izquierdo
        self.canvas.bind("<ButtonPress-1>",   self._on_press)
        # <B1-Motion>       → usuario arrastra con el boton sostenido
        self.canvas.bind("<B1-Motion>",       self._on_drag)
        # <ButtonRelease-1> → usuario suelta el boton
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        # Seguimiento de coordenadas para la barra de estado
        self.canvas.bind("<Motion>",          self._on_motion)

    # ── Panel derecho: colores y opciones ─────────────

    def _build_right_panel(self, parent):
        panel = tk.Frame(parent, bg=SURFACE, width=170, pady=12, padx=10)
        panel.pack(side="right", fill="y")
        panel.pack_propagate(False)

        # ── Color del trazo ──
        self._section_label(panel, "Color del trazo")

        # Muestra del color actual
        self.muestra_frente = tk.Label(
            panel,
            bg=self.color_frente.get(),
            width=16,
            height=2,
            relief="flat",
            cursor="hand2",
        )
        self.muestra_frente.pack(fill="x", pady=(2, 6))
        self.muestra_frente.bind("<Button-1>",
                                 lambda _: self._elegir_color_frente())

        # Paleta rapida
        self._build_paleta(panel,
                           lambda c: self._set_color_frente(c))

        tk.Frame(panel, bg=BORDER, height=1).pack(fill="x", pady=8)

        # ── Color de relleno ──
        self._section_label(panel, "Color de relleno")

        self.muestra_fondo = tk.Label(
            panel,
            bg=self.color_fondo.get(),
            width=16,
            height=2,
            relief="flat",
            cursor="hand2",
        )
        self.muestra_fondo.pack(fill="x", pady=(2, 6))
        self.muestra_fondo.bind("<Button-1>",
                                lambda _: self._elegir_color_fondo())

        self._build_paleta(panel,
                           lambda c: self._set_color_fondo(c))

        tk.Frame(panel, bg=BORDER, height=1).pack(fill="x", pady=8)

        # ── Grosor del trazo ──
        self._section_label(panel, "Grosor del trazo")

        self.lbl_grosor = tk.Label(
            panel,
            text=f"{self.grosor.get()} px",
            font=FONT_BOLD,
            bg=SURFACE,
            fg=ACCENT,
        )
        self.lbl_grosor.pack()

        # Scale (control deslizante) para el grosor
        scale = tk.Scale(
            panel,
            variable=self.grosor,
            from_=1,
            to=60,
            orient="horizontal",
            bg=SURFACE,
            fg=TEXT,
            troughcolor=CARD,
            activebackground=ACCENT,
            highlightthickness=0,
            sliderrelief="flat",
            showvalue=False,
            command=lambda v: self.lbl_grosor.config(text=f"{int(float(v))} px"),
        )
        scale.pack(fill="x", pady=(2, 0))

        tk.Frame(panel, bg=BORDER, height=1).pack(fill="x", pady=8)

        # ── Opcion: suavizado ──
        self._section_label(panel, "Opciones")

        self.var_suavizado = tk.BooleanVar(value=True)
        tk.Checkbutton(
            panel,
            text="Trazo suavizado",
            variable=self.var_suavizado,
            font=FONT_LABEL,
            bg=SURFACE,
            fg=TEXT,
            activebackground=SURFACE,
            activeforeground=ACCENT,
            selectcolor=CARD,
            cursor="hand2",
        ).pack(anchor="w")

        self.var_cap_redondo = tk.BooleanVar(value=True)
        tk.Checkbutton(
            panel,
            text="Cap redondeado",
            variable=self.var_cap_redondo,
            font=FONT_LABEL,
            bg=SURFACE,
            fg=TEXT,
            activebackground=SURFACE,
            activeforeground=ACCENT,
            selectcolor=CARD,
            cursor="hand2",
        ).pack(anchor="w", pady=(2, 0))

    def _build_paleta(self, parent, comando):
        """Grid de botones de colores rapidos."""
        grid = tk.Frame(parent, bg=SURFACE)
        grid.pack(fill="x")
        cols = 4
        for i, color in enumerate(COLORES_RAPIDOS):
            row, col = divmod(i, cols)
            btn = tk.Label(
                grid,
                bg=color,
                width=2,
                height=1,
                relief="flat",
                cursor="hand2",
            )
            btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            btn.bind("<Button-1>", lambda e, c=color: comando(c))
        for c in range(cols):
            grid.columnconfigure(c, weight=1)

    def _section_label(self, parent, text):
        tk.Label(
            parent,
            text=text,
            font=FONT_BOLD,
            bg=SURFACE,
            fg=MUTED,
            anchor="w",
        ).pack(fill="x", pady=(0, 2))

    # ── Barra de estado ───────────────────────────────

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=BG, pady=4)
        bar.pack(side="bottom", fill="x")

        self.lbl_coords = tk.Label(
            bar, text="x: 0,  y: 0",
            font=FONT_SMALL, bg=BG, fg=MUTED, anchor="w", padx=12,
        )
        self.lbl_coords.pack(side="left")

        self.lbl_herramienta = tk.Label(
            bar, text="Herramienta: Lapiz",
            font=FONT_SMALL, bg=BG, fg=MUTED, anchor="w", padx=12,
        )
        self.lbl_herramienta.pack(side="left")

        self.lbl_objetos = tk.Label(
            bar, text="Objetos: 0  |  Acciones: 0",
            font=FONT_SMALL, bg=BG, fg=MUTED, anchor="e", padx=12,
        )
        self.lbl_objetos.pack(side="right")

    # ──────────────────────────────────────────────────
    #  EVENTOS DEL CANVAS  (logica central de dibujo)
    # ──────────────────────────────────────────────────

    def _on_press(self, event):
        """
        <ButtonPress-1> — El usuario presiona el boton izquierdo del raton.
        Guarda las coordenadas iniciales y comienza una nueva accion.
        """
        # Convertir coordenadas del canvas (con scroll)
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        self._x_ant = x
        self._y_ant = y
        self._obj_temp = None
        self._accion_actual = []

        herr = self.herramienta.get()

        # Para herramientas de punto (lapiz/pincel/borrador):
        # dibujar un ovalo en el punto de clic inicial
        if herr in ("lapiz", "pincel", "borrador"):
            self._dibujar_punto(x, y)

    def _on_drag(self, event):
        """
        <B1-Motion> — El usuario mueve el raton con el boton sostenido.
        Aqui ocurre el dibujado continuo basado en event.x y event.y.
        """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        herr  = self.herramienta.get()
        color = self._get_color_trazo()
        g     = self.grosor.get()

        if herr in ("lapiz", "pincel", "borrador"):
            # Dibujo continuo: conectar punto anterior con punto actual
            # usando create_line() con las coordenadas event.x, event.y
            if self._x_ant is not None:
                cap  = "round" if self.var_cap_redondo.get() else "butt"
                join = "round" if self.var_suavizado.get()   else "miter"

                obj = self.canvas.create_line(
                    self._x_ant, self._y_ant, x, y,
                    fill=color,
                    width=g,
                    capstyle=cap,
                    joinstyle=join,
                    smooth=self.var_suavizado.get(),
                )
                self._accion_actual.append(obj)

        elif herr in ("linea", "rectangulo", "ovalo",
                      "rect_relleno", "oval_relleno"):
            # Formas: eliminar objeto temporal anterior y crear nuevo
            if self._obj_temp:
                self.canvas.delete(self._obj_temp)

            x0, y0 = self._x_ant, self._y_ant

            if herr == "linea":
                # create_line() con coordenadas de inicio y fin
                self._obj_temp = self.canvas.create_line(
                    x0, y0, x, y,
                    fill=color, width=g,
                    capstyle="round",
                )

            elif herr == "rectangulo":
                # create_rectangle() — solo borde
                self._obj_temp = self.canvas.create_rectangle(
                    x0, y0, x, y,
                    outline=color, width=g,
                    fill="",
                )

            elif herr == "rect_relleno":
                # create_rectangle() con relleno
                self._obj_temp = self.canvas.create_rectangle(
                    x0, y0, x, y,
                    outline=color, width=g,
                    fill=self.color_fondo.get(),
                )

            elif herr == "ovalo":
                # create_oval() — solo borde
                self._obj_temp = self.canvas.create_oval(
                    x0, y0, x, y,
                    outline=color, width=g,
                    fill="",
                )

            elif herr == "oval_relleno":
                # create_oval() con relleno
                self._obj_temp = self.canvas.create_oval(
                    x0, y0, x, y,
                    outline=color, width=g,
                    fill=self.color_fondo.get(),
                )

        # Actualizar posicion anterior
        self._x_ant = x
        self._y_ant = y
        self._update_statusbar_coords(x, y)

    def _on_release(self, event):
        """
        <ButtonRelease-1> — El usuario suelta el boton del raton.
        Finaliza la accion y la agrega al historial de deshacer.
        """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        herr = self.herramienta.get()

        # Para formas: el objeto temporal se convierte en definitivo
        if herr in ("linea", "rectangulo", "ovalo",
                    "rect_relleno", "oval_relleno"):
            if self._obj_temp:
                self._accion_actual.append(self._obj_temp)
                self._obj_temp = None

        # Guardar accion en el historial
        if self._accion_actual:
            self._historial.append(self._accion_actual[:])
            self._accion_actual = []

        self._x_ant = None
        self._y_ant = None
        self._update_statusbar_objetos()

    def _on_motion(self, event):
        """<Motion> — actualiza coordenadas en la barra de estado."""
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self._update_statusbar_coords(x, y)

    # ──────────────────────────────────────────────────
    #  HERRAMIENTAS AUXILIARES DE DIBUJO
    # ──────────────────────────────────────────────────

    def _dibujar_punto(self, x, y):
        """Dibuja un circulo en el punto (x, y) usando create_oval()."""
        g      = self.grosor.get()
        color  = self._get_color_trazo()
        r      = g / 2
        obj = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill=color, outline=color,
        )
        self._accion_actual.append(obj)

    def _get_color_trazo(self) -> str:
        herr = self.herramienta.get()
        if herr == "borrador":
            return CANVAS_BG
        return self.color_frente.get()

    # ──────────────────────────────────────────────────
    #  ACCIONES GLOBALES
    # ──────────────────────────────────────────────────

    def limpiar_canvas(self):
        """Borra todos los objetos del Canvas y limpia el historial."""
        if not self.canvas.find_all():
            return
        confirmar = messagebox.askyesno(
            "Limpiar pizarra",
            "¿Deseas borrar todo el dibujo?\nEsta accion no se puede deshacer.",
        )
        if confirmar:
            self.canvas.delete("all")
            self._historial.clear()
            self._update_statusbar_objetos()

    def deshacer(self):
        """Elimina la ultima accion del historial (Ctrl+Z)."""
        if not self._historial:
            return
        accion = self._historial.pop()
        for obj_id in accion:
            self.canvas.delete(obj_id)
        self._update_statusbar_objetos()

    def guardar_imagen(self):
        """
        Guarda el canvas como archivo PostScript (.ps).
        Si Pillow esta instalado, tambien permite guardar como PNG.
        """
        try:
            from PIL import ImageGrab
            tiene_pil = True
        except ImportError:
            tiene_pil = False

        tipos = [("PostScript", "*.ps")]
        if tiene_pil:
            tipos.insert(0, ("PNG", "*.png"))

        ruta = filedialog.asksaveasfilename(
            title="Guardar imagen",
            defaultextension=".ps",
            filetypes=tipos,
        )
        if not ruta:
            return

        try:
            if ruta.lower().endswith(".png") and tiene_pil:
                # Capturar la region del canvas con PIL
                x = self.canvas.winfo_rootx()
                y = self.canvas.winfo_rooty()
                w = self.canvas.winfo_width()
                h = self.canvas.winfo_height()
                img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
                img.save(ruta)
            else:
                # Guardar como PostScript (sin dependencias)
                self.canvas.postscript(
                    file=ruta,
                    colormode="color",
                )
            messagebox.showinfo("Guardado", f"Imagen guardada en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    # ──────────────────────────────────────────────────
    #  COLORES
    # ──────────────────────────────────────────────────

    def _elegir_color_frente(self):
        """Abre el selector de color nativo del SO (colorchooser)."""
        color = colorchooser.askcolor(
            color=self.color_frente.get(),
            title="Elige el color del trazo",
        )
        if color and color[1]:
            self._set_color_frente(color[1])

    def _elegir_color_fondo(self):
        color = colorchooser.askcolor(
            color=self.color_fondo.get(),
            title="Elige el color de relleno",
        )
        if color and color[1]:
            self._set_color_fondo(color[1])

    def _set_color_frente(self, color: str):
        self.color_frente.set(color)
        self.muestra_frente.config(bg=color)

    def _set_color_fondo(self, color: str):
        self.color_fondo.set(color)
        self.muestra_fondo.config(bg=color)

    # ──────────────────────────────────────────────────
    #  SELECCION DE HERRAMIENTA
    # ──────────────────────────────────────────────────

    def _seleccionar_herramienta(self, clave: str):
        self.herramienta.set(clave)
        self._resaltar_herramienta(clave)

        # Cambiar cursor del canvas segun la herramienta
        cursores = {
            "lapiz":       "pencil",
            "pincel":      "spraycan",
            "borrador":    "dotbox",
            "linea":       "crosshair",
            "rectangulo":  "crosshair",
            "ovalo":       "crosshair",
            "rect_relleno":"crosshair",
            "oval_relleno":"crosshair",
        }
        self.canvas.configure(cursor=cursores.get(clave, "crosshair"))

        nombre = next(
            (n for c, _, n in HERRAMIENTAS if c == clave), clave)
        self.lbl_herramienta.config(text=f"Herramienta: {nombre}")

    def _resaltar_herramienta(self, clave: str):
        """Resalta visualmente el boton de la herramienta activa."""
        for c, btn in self._btns_herramienta.items():
            if c == clave:
                btn.config(bg=ACCENT, fg=WHITE)
            else:
                btn.config(bg=CARD, fg=TEXT)

    # ──────────────────────────────────────────────────
    #  ATAJOS DE TECLADO
    # ──────────────────────────────────────────────────

    def _bind_shortcuts(self):
        self.bind("<Control-z>", lambda _: self.deshacer())
        self.bind("<Control-Z>", lambda _: self.deshacer())
        self.bind("<Delete>",    lambda _: self.limpiar_canvas())
        self.bind("<Control-s>", lambda _: self.guardar_imagen())
        self.bind("<Control-S>", lambda _: self.guardar_imagen())

        # Herramientas
        for tecla, clave in [
            ("p", "lapiz"),    ("b", "pincel"),
            ("e", "borrador"), ("l", "linea"),
            ("r", "rectangulo"), ("v", "ovalo"),
            ("f", "rect_relleno"), ("g", "oval_relleno"),
        ]:
            self.bind(f"<Control-{tecla}>",
                      lambda _, c=clave: self._seleccionar_herramienta(c))
            self.bind(f"<Control-{tecla.upper()}>",
                      lambda _, c=clave: self._seleccionar_herramienta(c))

        # Grosor rapido con [ y ]
        self.bind("]", lambda _: self.grosor.set(
            min(self.grosor.get() + 2, 60)))
        self.bind("[", lambda _: self.grosor.set(
            max(self.grosor.get() - 2, 1)))

    # ──────────────────────────────────────────────────
    #  BARRA DE ESTADO — ACTUALIZACIONES
    # ──────────────────────────────────────────────────

    def _update_statusbar_coords(self, x, y):
        self.lbl_coords.config(text=f"x: {int(x)},  y: {int(y)}")

    def _update_statusbar_objetos(self):
        n_obj = len(self.canvas.find_all())
        n_acc = len(self._historial)
        self.lbl_objetos.config(
            text=f"Objetos Canvas: {n_obj}  |  Acciones: {n_acc}")

    # ──────────────────────────────────────────────────
    #  TOOLTIP SIMPLE
    # ──────────────────────────────────────────────────

    def _add_tooltip(self, widget, texto):
        tip = None

        def mostrar(event):
            nonlocal tip
            x = event.widget.winfo_rootx() + 60
            y = event.widget.winfo_rooty()
            tip = tk.Toplevel(self)
            tip.wm_overrideredirect(True)
            tip.wm_geometry(f"+{x}+{y}")
            tk.Label(
                tip, text=texto, font=FONT_SMALL,
                bg="#2a3147", fg=TEXT, relief="flat", padx=6, pady=3,
            ).pack()

        def ocultar(_):
            nonlocal tip
            if tip:
                tip.destroy()
                tip = None

        widget.bind("<Enter>", mostrar)
        widget.bind("<Leave>", ocultar)


# ──────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    app = Pizarra()
    app.mainloop()
