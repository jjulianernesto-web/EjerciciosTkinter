"""
╔══════════════════════════════════════════════════════════╗
║   📊  Monitor de Sensores (Simulado)                     ║
║   Widgets: Scale · Progressbar (ttk) · Canvas            ║
║   Tecnica: DoubleVar + command + .after() para simulacion ║
╚══════════════════════════════════════════════════════════╝

Demuestra:
  - Scale          deslizador que vincula movimiento a una variable
  - DoubleVar      variable de control que conecta Scale y Progressbar
  - Progressbar    barra de estado que refleja el valor del Scale
  - command=fn     callback que se ejecuta al mover el Scale
  - Indicador      texto que cambia (Normal / Advertencia / Critico)
  - .after()       simulacion automatica de lecturas de sensor
  - Canvas         mini-grafico historico de cada sensor
  - Escala de color dinamica (verde → amarillo → rojo)
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random
import math


# ──────────────────────────────────────────────────────
#  COLORES
# ──────────────────────────────────────────────────────
C = {
    "bg":       "#0d0f14",
    "surface":  "#161b26",
    "card":     "#1e2535",
    "border":   "#2a3147",
    "accent":   "#7c6fff",
    "green":    "#43d9ad",
    "yellow":   "#ffd166",
    "orange":   "#ff8c42",
    "red":      "#ff4d4d",
    "text":     "#e6eaf4",
    "muted":    "#7a8399",
    "dim":      "#3d4a66",
    "white":    "#ffffff",
    "entry":    "#252d3d",
    "hover":    "#2e3a52",
}

F_TITULO  = ("Segoe UI", 15, "bold")
F_SENSOR  = ("Segoe UI", 11, "bold")
F_VALOR   = ("Consolas", 22, "bold")
F_ESTADO  = ("Segoe UI", 10, "bold")
F_LABEL   = ("Segoe UI", 9)
F_SMALL   = ("Segoe UI", 8)
F_BTN     = ("Segoe UI", 9, "bold")
F_LOG     = ("Consolas", 9)

# ──────────────────────────────────────────────────────
#  DEFINICION DE SENSORES
# ──────────────────────────────────────────────────────
#
# Cada sensor tiene:
#   nombre, unidad, minimo, maximo,
#   umbral_warn (% del rango), umbral_crit (% del rango),
#   valor_inicial, color_acento, emoji
#
SENSORES_DEF = [
    {
        "id":           "temp",
        "nombre":       "Temperatura",
        "unidad":       "°C",
        "min":          0.0,
        "max":          120.0,
        "warn_pct":     60,       # amarillo a partir del 60%
        "crit_pct":     85,       # rojo a partir del 85%
        "valor_init":   42.0,
        "emoji":        "🌡️",
        "color":        C["orange"],
        "sim_base":     45.0,     # valor base para la simulacion
        "sim_ruido":    5.0,      # amplitud del ruido simulado
    },
    {
        "id":           "hum",
        "nombre":       "Humedad",
        "unidad":       "%",
        "min":          0.0,
        "max":          100.0,
        "warn_pct":     75,
        "crit_pct":     90,
        "valor_init":   55.0,
        "emoji":        "💧",
        "color":        C["accent"],
        "sim_base":     55.0,
        "sim_ruido":    8.0,
    },
    {
        "id":           "cpu",
        "nombre":       "CPU",
        "unidad":       "%",
        "min":          0.0,
        "max":          100.0,
        "warn_pct":     70,
        "crit_pct":     90,
        "valor_init":   30.0,
        "emoji":        "💻",
        "color":        C["accent"],
        "sim_base":     40.0,
        "sim_ruido":    25.0,
    },
    {
        "id":           "pres",
        "nombre":       "Presion",
        "unidad":       "PSI",
        "min":          0.0,
        "max":          200.0,
        "warn_pct":     65,
        "crit_pct":     85,
        "valor_init":   80.0,
        "emoji":        "🔧",
        "color":        C["yellow"],
        "sim_base":     90.0,
        "sim_ruido":    15.0,
    },
    {
        "id":           "volt",
        "nombre":       "Voltaje",
        "unidad":       "V",
        "min":          0.0,
        "max":          15.0,
        "warn_pct":     80,
        "crit_pct":     93,
        "valor_init":   12.0,
        "emoji":        "⚡",
        "color":        C["yellow"],
        "sim_base":     12.0,
        "sim_ruido":    1.5,
    },
    {
        "id":           "rpm",
        "nombre":       "RPM Motor",
        "unidad":       "rpm",
        "min":          0.0,
        "max":          8000.0,
        "warn_pct":     70,
        "crit_pct":     88,
        "valor_init":   2000.0,
        "emoji":        "⚙️",
        "color":        C["green"],
        "sim_base":     2500.0,
        "sim_ruido":    800.0,
    },
]

MAX_HISTORIAL = 60   # puntos maximos en el grafico


# ──────────────────────────────────────────────────────
#  WIDGET: TARJETA DE UN SENSOR
# ──────────────────────────────────────────────────────

class TarjetaSensor(tk.Frame):
    """
    Frame que representa un sensor individual.
    Contiene:
      - Scale   (deslizador de valor manual)
      - DoubleVar vinculada al Scale y a la Progressbar
      - Progressbar que refleja el valor del Scale
      - Label de valor numerico y estado
      - Canvas mini-grafico historico
    """

    def __init__(self, parent, defn: dict, on_alert_fn, **kwargs):
        super().__init__(parent, bg=C["card"],
                         padx=14, pady=12, **kwargs)
        self.defn       = defn
        self.on_alert   = on_alert_fn
        self._historial: list[float] = []   # historial de porcentajes (0-100)
        self._estado_anterior = "Normal"

        # ── Variable de control central ──────────────
        # DoubleVar es la que conecta el Scale con el resto de la UI
        self.var_valor = tk.DoubleVar(value=defn["valor_init"])

        self._build()
        self._actualizar_ui(defn["valor_init"])

    def _build(self):
        d = self.defn

        # ── Encabezado ──
        head = tk.Frame(self, bg=C["card"])
        head.pack(fill="x")

        tk.Label(
            head,
            text=f"{d['emoji']}  {d['nombre']}",
            font=F_SENSOR,
            bg=C["card"],
            fg=d["color"],
        ).pack(side="left")

        # Indicador de estado (Normal / Advertencia / Critico)
        self.lbl_estado = tk.Label(
            head,
            text="● Normal",
            font=F_ESTADO,
            bg=C["card"],
            fg=C["green"],
        )
        self.lbl_estado.pack(side="right")

        # ── Valor numérico grande ──
        self.lbl_valor = tk.Label(
            self,
            text=f"{d['valor_init']:.1f} {d['unidad']}",
            font=F_VALOR,
            bg=C["card"],
            fg=C["text"],
        )
        self.lbl_valor.pack(anchor="w", pady=(6, 0))

        # ── Progressbar (barra de estado) ──
        # ttk.Progressbar refleja el porcentaje del valor en el rango
        style_name = f"{d['id']}.Horizontal.TProgressbar"
        style = ttk.Style()
        style.configure(
            style_name,
            troughcolor=C["entry"],
            background=C["green"],    # cambia dinamicamente
            bordercolor=C["card"],
            lightcolor=C["green"],
            darkcolor=C["green"],
            thickness=10,
        )
        self.pb_style = style_name

        self.progressbar = ttk.Progressbar(
            self,
            style=style_name,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=self._val_a_pct(d["valor_init"]),
        )
        self.progressbar.pack(fill="x", pady=(4, 2))

        # Etiquetas de rango
        rango = tk.Frame(self, bg=C["card"])
        rango.pack(fill="x")
        tk.Label(rango, text=f"{d['min']:.0f}", font=F_SMALL,
                 bg=C["card"], fg=C["dim"]).pack(side="left")
        tk.Label(rango, text=f"{d['max']:.0f} {d['unidad']}", font=F_SMALL,
                 bg=C["card"], fg=C["dim"]).pack(side="right")

        # ── Scale (deslizador manual) ──
        # El Scale vincula su movimiento a var_valor con command=self._on_scale
        self.scale = tk.Scale(
            self,
            variable=self.var_valor,       # ← DoubleVar compartida
            from_=d["min"],
            to=d["max"],
            orient="horizontal",
            resolution=0.1,
            showvalue=False,
            bg=C["card"],
            fg=C["muted"],
            troughcolor=C["entry"],
            activebackground=d["color"],
            highlightthickness=0,
            sliderrelief="flat",
            # command se ejecuta CADA VEZ que el usuario mueve el deslizador
            command=self._on_scale,
        )
        self.scale.pack(fill="x", pady=(4, 0))

        # ── Mini-grafico Canvas ──
        self.canvas_graph = tk.Canvas(
            self,
            bg=C["entry"],
            height=36,
            highlightthickness=0,
        )
        self.canvas_graph.pack(fill="x", pady=(8, 0))

    # ── Callbacks ────────────────────────────────────

    def _on_scale(self, valor_str):
        """
        Se ejecuta cuando el usuario mueve el Scale.
        Actualiza la Progressbar y el indicador de estado.
        """
        valor = float(valor_str)
        self._actualizar_ui(valor)

    def set_valor(self, valor: float):
        """Establece el valor programaticamente (simulacion auto)."""
        valor = max(self.defn["min"], min(self.defn["max"], valor))
        self.var_valor.set(valor)
        self._actualizar_ui(valor)

    def _actualizar_ui(self, valor: float):
        """
        Actualiza todos los elementos visuales en funcion del valor actual:
          1. Label numerico
          2. Progressbar (porcentaje)
          3. Color dinamico segun umbrales
          4. Indicador de estado (Normal / Advertencia / Critico)
          5. Mini-grafico historico
        """
        d   = self.defn
        pct = self._val_a_pct(valor)

        # 1. Actualizar label numerico
        self.lbl_valor.config(text=f"{valor:.1f} {d['unidad']}")

        # 2. Actualizar Progressbar
        self.progressbar["value"] = pct

        # 3. Determinar estado y color segun umbrales
        if pct >= d["crit_pct"]:
            estado = "Critico"
            color  = C["red"]
        elif pct >= d["warn_pct"]:
            estado = "Advertencia"
            color  = C["yellow"]
        else:
            estado = "Normal"
            color  = C["green"]

        # 4. Actualizar indicador de estado
        simbolos = {"Normal": "●", "Advertencia": "▲", "Critico": "■"}
        self.lbl_estado.config(
            text=f"{simbolos[estado]} {estado}",
            fg=color,
        )

        # Actualizar color de la Progressbar dinamicamente
        style = ttk.Style()
        style.configure(self.pb_style, background=color,
                        lightcolor=color, darkcolor=color)

        # 5. Lanzar alerta si el estado cambia
        if estado != self._estado_anterior:
            if estado in ("Advertencia", "Critico"):
                self.on_alert(
                    f"[{d['nombre']}]  {self._estado_anterior} → {estado}  "
                    f"({valor:.1f} {d['unidad']})",
                    color,
                )
            self._estado_anterior = estado

        # 6. Actualizar mini-grafico
        self._historial.append(pct)
        if len(self._historial) > MAX_HISTORIAL:
            self._historial.pop(0)
        self._dibujar_grafico(color)

    def _val_a_pct(self, valor: float) -> float:
        """Convierte un valor absoluto a porcentaje del rango."""
        d = self.defn
        return ((valor - d["min"]) / (d["max"] - d["min"])) * 100

    def _dibujar_grafico(self, color: str):
        """Dibuja el historial como linea en el Canvas mini-grafico."""
        c  = self.canvas_graph
        c.delete("all")
        w  = c.winfo_width()
        h  = c.winfo_height()
        if w < 2 or not self._historial:
            return

        pts = self._historial
        n   = len(pts)
        dx  = w / max(n - 1, 1)

        # Linea de la grafica
        coords = []
        for i, pct in enumerate(pts):
            x = i * dx
            y = h - (pct / 100) * h
            coords.extend([x, y])

        if len(coords) >= 4:
            c.create_line(*coords, fill=color, width=1.5, smooth=True)

        # Lineas de umbral
        d = self.defn
        for pct_thr, thr_color in [
            (d["warn_pct"], C["yellow"]),
            (d["crit_pct"], C["red"]),
        ]:
            y_thr = h - (pct_thr / 100) * h
            c.create_line(0, y_thr, w, y_thr,
                          fill=thr_color, dash=(3, 4), width=1)


# ──────────────────────────────────────────────────────
#  APLICACION PRINCIPAL
# ──────────────────────────────────────────────────────

class MonitorSensores(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitor de Sensores (Simulado)")
        self.geometry("900x740")
        self.minsize(820, 680)
        self.configure(bg=C["bg"])
        self.resizable(True, True)

        self._simulando = False
        self._sim_job   = None
        self._sim_t     = 0.0       # tiempo de la simulacion (para ondas)
        self.tarjetas: dict[str, TarjetaSensor] = {}

        self._apply_global_styles()
        self._build_ui()

    # ──────────────────────────────────────────────────
    #  ESTILOS
    # ──────────────────────────────────────────────────

    def _apply_global_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Toggle.TButton",
            font=F_BTN,
            padding=(12, 6),
            relief="flat",
        )
        style.configure(
            "Dark.TScrollbar",
            background=C["card"],
            troughcolor=C["surface"],
            arrowcolor=C["muted"],
            bordercolor=C["border"],
        )

    # ──────────────────────────────────────────────────
    #  UI PRINCIPAL
    # ──────────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()

        # Layout: sensores (izquierda) + log (derecha)
        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=12, pady=8)

        self._build_sensors_panel(body)
        self._build_log_panel(body)

        self._build_statusbar()

    # ── Header ────────────────────────────────────────

    def _build_header(self):
        header = tk.Frame(self, bg=C["surface"], pady=12)
        header.pack(fill="x")

        tk.Label(
            header,
            text="📊  Monitor de Sensores (Simulado)",
            font=F_TITULO,
            bg=C["surface"],
            fg=C["accent"],
        ).pack(side="left", padx=16)

        tk.Label(
            header,
            text="Scale + DoubleVar + Progressbar  —  los sliders controlan las barras en tiempo real",
            font=F_SMALL,
            bg=C["surface"],
            fg=C["muted"],
        ).pack(side="left")

        # Botones de control
        btn_row = tk.Frame(header, bg=C["surface"])
        btn_row.pack(side="right", padx=12)

        self.btn_sim = tk.Button(
            btn_row,
            text="▶  Iniciar Simulacion",
            font=F_BTN,
            bg=C["green"],
            fg=C["bg"],
            activebackground=C["hover"],
            activeforeground=C["text"],
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=6,
            command=self._toggle_simulacion,
        )
        self.btn_sim.pack(side="left", padx=(0, 8))

        tk.Button(
            btn_row,
            text="↺  Reiniciar",
            font=F_BTN,
            bg=C["border"],
            fg=C["muted"],
            activebackground=C["hover"],
            activeforeground=C["text"],
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=6,
            command=self._reiniciar,
        ).pack(side="left")

    # ── Panel de sensores ──────────────────────────────

    def _build_sensors_panel(self, parent):
        """Grid de tarjetas de sensores con Scale y Progressbar."""
        left = tk.Frame(parent, bg=C["bg"])
        left.pack(side="left", fill="both", expand=True)

        # Titulo + leyenda de umbrales
        info = tk.Frame(left, bg=C["bg"])
        info.pack(fill="x", pady=(0, 8))

        tk.Label(
            info,
            text="Controles manuales  (mueve los deslizadores Scale → la Progressbar se actualiza)",
            font=("Segoe UI", 9, "italic"),
            bg=C["bg"],
            fg=C["muted"],
        ).pack(side="left")

        for color, label in [
            (C["green"],  "Normal"),
            (C["yellow"], "Advertencia"),
            (C["red"],    "Critico"),
        ]:
            tk.Label(info, text=f"  ● {label}",
                     font=F_SMALL, bg=C["bg"], fg=color).pack(side="right")

        # Grid 2×3
        grid = tk.Frame(left, bg=C["bg"])
        grid.pack(fill="both", expand=True)

        for i, defn in enumerate(SENSORES_DEF):
            row, col = divmod(i, 2)
            card = TarjetaSensor(
                grid,
                defn=defn,
                on_alert_fn=self._registrar_alerta,
            )
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.tarjetas[defn["id"]] = card

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        for r in range(3):
            grid.rowconfigure(r, weight=1)

    # ── Panel de log ───────────────────────────────────

    def _build_log_panel(self, parent):
        right = tk.Frame(parent, bg=C["surface"], padx=10, pady=10)
        right.pack(side="right", fill="y", padx=(8, 0))
        right.configure(width=220)
        right.pack_propagate(False)

        tk.Label(
            right,
            text="📋  Registro de Alertas",
            font=F_BTN,
            bg=C["surface"],
            fg=C["accent"],
        ).pack(anchor="w")

        tk.Label(
            right,
            text="Cambios de estado detectados",
            font=F_SMALL,
            bg=C["surface"],
            fg=C["muted"],
        ).pack(anchor="w", pady=(0, 6))

        log_cont = tk.Frame(right, bg=C["surface"])
        log_cont.pack(fill="both", expand=True)

        scroll = ttk.Scrollbar(log_cont, orient="vertical",
                               style="Dark.TScrollbar")
        scroll.pack(side="right", fill="y")

        self.txt_log = tk.Text(
            log_cont,
            font=F_LOG,
            bg=C["entry"],
            fg=C["text"],
            relief="flat",
            bd=0,
            padx=6,
            pady=6,
            state="disabled",
            wrap="word",
            yscrollcommand=scroll.set,
        )
        self.txt_log.pack(side="left", fill="both", expand=True)
        scroll.config(command=self.txt_log.yview)

        # Tags de color para el log
        self.txt_log.tag_config("warn",  foreground=C["yellow"])
        self.txt_log.tag_config("crit",  foreground=C["red"])
        self.txt_log.tag_config("ok",    foreground=C["green"])
        self.txt_log.tag_config("time",  foreground=C["muted"])
        self.txt_log.tag_config("bold",  font=("Consolas", 9, "bold"))

        # Boton limpiar log
        tk.Button(
            right,
            text="🗑  Limpiar log",
            font=F_SMALL,
            bg=C["border"],
            fg=C["muted"],
            activebackground=C["hover"],
            activeforeground=C["text"],
            relief="flat",
            cursor="hand2",
            pady=4,
            command=self._limpiar_log,
        ).pack(fill="x", pady=(8, 0))

        # ── Resumen de estados ──
        tk.Frame(right, bg=C["border"], height=1).pack(
            fill="x", pady=(12, 8))

        tk.Label(right, text="Estado del sistema",
                 font=F_BTN, bg=C["surface"], fg=C["muted"]).pack(anchor="w")

        self.lbl_resumen = tk.Label(
            right,
            text="✅  Todo Normal",
            font=("Segoe UI", 10, "bold"),
            bg=C["surface"],
            fg=C["green"],
            wraplength=190,
            justify="left",
        )
        self.lbl_resumen.pack(anchor="w", pady=(4, 0))

    # ── Barra de estado ────────────────────────────────

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=C["bg"], pady=4)
        bar.pack(side="bottom", fill="x")

        self.lbl_status = tk.Label(
            bar,
            text="Modo manual — mueve los deslizadores para ver los cambios",
            font=F_SMALL,
            bg=C["bg"],
            fg=C["muted"],
            anchor="w",
            padx=12,
        )
        self.lbl_status.pack(side="left")

        self.lbl_tiempo_sim = tk.Label(
            bar,
            text="",
            font=F_SMALL,
            bg=C["bg"],
            fg=C["dim"],
            anchor="e",
            padx=12,
        )
        self.lbl_tiempo_sim.pack(side="right")

    # ──────────────────────────────────────────────────
    #  SIMULACION AUTOMATICA
    # ──────────────────────────────────────────────────

    def _toggle_simulacion(self):
        """Activa o desactiva la simulacion automatica de sensores."""
        if self._simulando:
            # Detener
            self._simulando = False
            if self._sim_job:
                self.after_cancel(self._sim_job)
                self._sim_job = None
            self.btn_sim.config(
                text="▶  Iniciar Simulacion",
                bg=C["green"], fg=C["bg"])
            self.lbl_status.config(
                text="Simulacion detenida — modo manual activo")
            self.lbl_tiempo_sim.config(text="")
            # Habilitar scales
            for card in self.tarjetas.values():
                card.scale.config(state="normal")
        else:
            # Iniciar
            self._simulando = True
            self._sim_t     = 0.0
            self.btn_sim.config(
                text="⏸  Detener Simulacion",
                bg=C["orange"], fg=C["white"])
            self.lbl_status.config(
                text="Simulacion activa — los valores se actualizan automaticamente con .after()")
            # Deshabilitar scales en modo automatico
            for card in self.tarjetas.values():
                card.scale.config(state="disabled")
            self._simular()

    def _simular(self):
        """
        Actualiza los valores de los sensores usando .after(500).
        Genera valores con ruido sinusoidal para simular lecturas reales.
        """
        if not self._simulando:
            return

        self._sim_t += 0.15  # avanzar tiempo de simulacion

        for card in self.tarjetas.values():
            d      = card.defn
            base   = d["sim_base"]
            ruido  = d["sim_ruido"]

            # Valor simulado = base + onda senoidal + ruido aleatorio
            onda   = math.sin(self._sim_t + hash(d["id"]) % 10) * ruido * 0.6
            aleatorio = random.uniform(-ruido * 0.4, ruido * 0.4)
            nuevo  = base + onda + aleatorio

            card.set_valor(nuevo)

        # Tiempo de simulacion en pantalla
        t = self._sim_t
        self.lbl_tiempo_sim.config(
            text=f"t = {t:.1f} s  |  .after(500, simular)")

        # Actualizar resumen del sistema
        self._actualizar_resumen()

        # .after() — reagendar en 500ms sin bloquear
        self._sim_job = self.after(500, self._simular)

    # ──────────────────────────────────────────────────
    #  LOG DE ALERTAS
    # ──────────────────────────────────────────────────

    def _registrar_alerta(self, mensaje: str, color: str):
        """Escribe una linea en el log de alertas con color y timestamp."""
        ahora = datetime.now().strftime("%H:%M:%S")

        tag = "warn"
        if color == C["red"]:
            tag = "crit"
        elif color == C["green"]:
            tag = "ok"

        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", f"[{ahora}] ", "time")
        self.txt_log.insert("end", f"{mensaje}\n", tag)
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")

        self._actualizar_resumen()

    def _limpiar_log(self):
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.configure(state="disabled")

    def _actualizar_resumen(self):
        """Actualiza el label resumen del estado global del sistema."""
        criticos    = []
        advertencias = []
        for card in self.tarjetas.values():
            estado = card._estado_anterior
            if estado == "Critico":
                criticos.append(card.defn["nombre"])
            elif estado == "Advertencia":
                advertencias.append(card.defn["nombre"])

        if criticos:
            self.lbl_resumen.config(
                text=f"⛔  CRITICO:\n{', '.join(criticos)}",
                fg=C["red"])
        elif advertencias:
            self.lbl_resumen.config(
                text=f"⚠️  Advertencia:\n{', '.join(advertencias)}",
                fg=C["yellow"])
        else:
            self.lbl_resumen.config(
                text="✅  Todo Normal",
                fg=C["green"])

    def _reiniciar(self):
        """Resetea todos los sensores a sus valores iniciales."""
        if self._simulando:
            self._toggle_simulacion()
        for card in self.tarjetas.values():
            card.set_valor(card.defn["valor_init"])
            card._historial.clear()
            card._estado_anterior = "Normal"
        self._limpiar_log()
        self.lbl_resumen.config(text="✅  Todo Normal", fg=C["green"])
        self.lbl_status.config(
            text="Sensores reiniciados — modo manual activo")


# ──────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    app = MonitorSensores()
    app.mainloop()
