"""
╔══════════════════════════════════════════════════════════╗
║   ⏱️  Reloj Digital y Cronometro                         ║
║   Widgets: Label (fuente grande) · Frame · Button        ║
║   Tecnica clave: .after(ms, funcion)  —  sin sleep()     ║
╚══════════════════════════════════════════════════════════╝

Demuestra:
  - .after(1000, fn)   actualiza la UI cada 1 s SIN bloquear el hilo
  - Patron recursivo   la funcion se llama a si misma via .after()
  - datetime.now()     leer hora del sistema
  - Label con fuente   configuracion avanzada de fuentes grandes
  - Cronometro         .after(10, fn)  resolucion de centesimas
  - Temporizador       cuenta regresiva con .after()
  - Vueltas            historial de laps en un Listbox

Diagrama del patron .after():
    actualizar_reloj()
        ↓ lee datetime.now()
        ↓ actualiza label.config(text=hora)
        ↓ self.after(1000, actualizar_reloj)  ← se agenda a si misma
        ↑___________________________________|
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from datetime import datetime, timedelta
import time


# ──────────────────────────────────────────────────────
#  COLORES
# ──────────────────────────────────────────────────────

C = {
    "bg":        "#0d0f14",
    "surface":   "#161b26",
    "card":      "#1e2535",
    "border":    "#2a3147",
    "accent":    "#7c6fff",
    "green":     "#43d9ad",
    "pink":      "#ff6b9d",
    "yellow":    "#ffd166",
    "red":       "#ff6b6b",
    "text":      "#e6eaf4",
    "muted":     "#7a8399",
    "white":     "#ffffff",
    "entry":     "#252d3d",
    "hover":     "#2e3a52",
    "dim":       "#3d4a66",
}

# Fuentes
F_RELOJ_GRANDE  = ("Consolas", 72, "bold")   # hora principal
F_RELOJ_MEDIANO = ("Consolas", 36, "bold")   # cronometro
F_RELOJ_CHICO   = ("Consolas", 22, "bold")   # centesimas / temporizador
F_FECHA         = ("Segoe UI", 14)
F_TITULO        = ("Segoe UI", 18, "bold")
F_LABEL         = ("Segoe UI", 10)
F_BTN           = ("Segoe UI", 10, "bold")
F_SMALL         = ("Segoe UI", 9)
F_LAP           = ("Consolas", 10)

NOMBRE_DIAS = ["Lunes", "Martes", "Miércoles", "Jueves",
               "Viernes", "Sábado", "Domingo"]
NOMBRE_MESES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo",
                "Junio", "Julio", "Agosto", "Septiembre",
                "Octubre", "Noviembre", "Diciembre"]


# ──────────────────────────────────────────────────────
#  APLICACION PRINCIPAL
# ──────────────────────────────────────────────────────

class RelojCronometro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reloj Digital y Cronometro")
        self.geometry("700x620")
        self.minsize(660, 580)
        self.configure(bg=C["bg"])
        self.resizable(True, True)

        # ── Estado del cronometro ──────────────────────
        self._crono_corriendo = False
        self._crono_inicio: float | None = None   # time.perf_counter()
        self._crono_acumulado: float = 0.0        # segundos acumulados
        self._crono_job = None                    # ID del .after() activo
        self._laps: list[float] = []              # tiempos de vuelta

        # ── Estado del temporizador ────────────────────
        self._timer_corriendo  = False
        self._timer_restante:  float = 0.0        # segundos restantes
        self._timer_total:     float = 0.0
        self._timer_inicio:    float | None = None
        self._timer_job  = None

        # ── Estado del reloj ──────────────────────────
        self._reloj_job  = None
        self._parpadeo   = True                   # dos puntos parpadeantes

        self._build_ui()
        self._iniciar_reloj()    # arrancar el reloj al abrir

    # ──────────────────────────────────────────────────
    #  UI
    # ──────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=C["surface"], pady=12)
        header.pack(fill="x")
        tk.Label(
            header,
            text="⏱  Reloj Digital y Cronometro",
            font=F_TITULO,
            bg=C["surface"],
            fg=C["accent"],
        ).pack()
        tk.Label(
            header,
            text=".after(ms, funcion)  —  actualizacion continua sin bloquear el hilo principal",
            font=F_SMALL,
            bg=C["surface"],
            fg=C["muted"],
        ).pack(pady=(2, 0))

        # Pestañas
        self._build_tabs()

    def _build_tabs(self):
        """Implementacion de pestanas con Frames + botones de seleccion."""
        tab_bar = tk.Frame(self, bg=C["surface"])
        tab_bar.pack(fill="x")

        self.content = tk.Frame(self, bg=C["bg"])
        self.content.pack(fill="both", expand=True)

        # Frames de cada pestana
        self.frame_reloj   = tk.Frame(self.content, bg=C["bg"])
        self.frame_crono   = tk.Frame(self.content, bg=C["bg"])
        self.frame_timer   = tk.Frame(self.content, bg=C["bg"])

        # Construir contenido
        self._build_tab_reloj(self.frame_reloj)
        self._build_tab_cronometro(self.frame_crono)
        self._build_tab_temporizador(self.frame_timer)

        # Botones de pestana
        self._tab_btns = {}
        for texto, frame in [
            ("🕐  Reloj",        self.frame_reloj),
            ("⏱  Cronometro",   self.frame_crono),
            ("⏳  Temporizador", self.frame_timer),
        ]:
            btn = tk.Button(
                tab_bar,
                text=texto,
                font=F_BTN,
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=8,
                bg=C["surface"],
                fg=C["muted"],
                activebackground=C["hover"],
                activeforeground=C["text"],
                command=lambda f=frame, t=texto: self._switch_tab(f, t),
            )
            btn.pack(side="left")
            self._tab_btns[texto] = btn

        # Mostrar la primera pestana
        self._switch_tab(self.frame_reloj, "🕐  Reloj")

    def _switch_tab(self, frame_activo, nombre):
        """Oculta todos los frames y muestra el seleccionado."""
        for f in (self.frame_reloj, self.frame_crono, self.frame_timer):
            f.pack_forget()
        frame_activo.pack(fill="both", expand=True, padx=20, pady=16)

        for txt, btn in self._tab_btns.items():
            if txt == nombre:
                btn.config(bg=C["accent"], fg=C["white"])
            else:
                btn.config(bg=C["surface"], fg=C["muted"])

    # ──────────────────────────────────────────────────
    #  PESTAÑA 1: RELOJ DIGITAL
    # ──────────────────────────────────────────────────

    def _build_tab_reloj(self, parent):
        parent.columnconfigure(0, weight=1)

        # ── Hora grande ──
        # Label con fuente gigante — configuracion avanzada de fuente
        self.lbl_hora = tk.Label(
            parent,
            text="00:00:00",
            font=F_RELOJ_GRANDE,          # fuente grande tipo consola
            bg=C["bg"],
            fg=C["accent"],
        )
        self.lbl_hora.pack(pady=(30, 0))

        # Centesimas de segundo
        self.lbl_ms_reloj = tk.Label(
            parent,
            text=".000",
            font=("Consolas", 28),
            bg=C["bg"],
            fg=C["dim"],
        )
        self.lbl_ms_reloj.pack()

        # ── Fecha ──
        self.lbl_fecha = tk.Label(
            parent,
            text="",
            font=F_FECHA,
            bg=C["bg"],
            fg=C["muted"],
        )
        self.lbl_fecha.pack(pady=(4, 0))

        # Dia de la semana
        self.lbl_dia = tk.Label(
            parent,
            text="",
            font=("Segoe UI", 12),
            bg=C["bg"],
            fg=C["dim"],
        )
        self.lbl_dia.pack()

        # ── Panel de info ──
        info = tk.Frame(parent, bg=C["card"], padx=20, pady=14)
        info.pack(fill="x", pady=(24, 0))

        tk.Label(
            info,
            text="Patron .after()  —  como funciona el reloj:",
            font=F_BTN,
            bg=C["card"],
            fg=C["accent"],
        ).pack(anchor="w")

        codigo = (
            "  def actualizar_reloj(self):\n"
            "      ahora = datetime.now()                    # leer hora del sistema\n"
            "      self.lbl_hora.config(text=ahora.strftime('%H:%M:%S'))  # actualizar Label\n"
            "      self._reloj_job = self.after(1000, self.actualizar_reloj)  # reagendar\n"
            "                                          ↑___________________________|\n"
            "                              llamada recursiva cada 1000 ms"
        )
        tk.Label(
            info,
            text=codigo,
            font=("Consolas", 9),
            bg=C["card"],
            fg=C["green"],
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        # Opciones de formato
        opt = tk.Frame(parent, bg=C["bg"])
        opt.pack(pady=(16, 0))

        self.var_formato_24h = tk.BooleanVar(value=True)
        tk.Checkbutton(
            opt,
            text="Formato 24h",
            variable=self.var_formato_24h,
            font=F_LABEL,
            bg=C["bg"], fg=C["text"],
            activebackground=C["bg"],
            activeforeground=C["accent"],
            selectcolor=C["entry"],
            cursor="hand2",
        ).pack(side="left", padx=8)

        self.var_parpadeo = tk.BooleanVar(value=True)
        tk.Checkbutton(
            opt,
            text="Dos puntos parpadeantes",
            variable=self.var_parpadeo,
            font=F_LABEL,
            bg=C["bg"], fg=C["text"],
            activebackground=C["bg"],
            activeforeground=C["accent"],
            selectcolor=C["entry"],
            cursor="hand2",
        ).pack(side="left", padx=8)

    # ──────────────────────────────────────────────────
    #  PESTAÑA 2: CRONOMETRO
    # ──────────────────────────────────────────────────

    def _build_tab_cronometro(self, parent):
        # Display del cronometro
        self.lbl_crono = tk.Label(
            parent,
            text="00:00",
            font=F_RELOJ_MEDIANO,
            bg=C["bg"],
            fg=C["green"],
        )
        self.lbl_crono.pack(pady=(20, 0))

        self.lbl_crono_cs = tk.Label(
            parent,
            text=".00",
            font=F_RELOJ_CHICO,
            bg=C["bg"],
            fg=C["dim"],
        )
        self.lbl_crono_cs.pack()

        # Tiempo de vuelta actual
        self.lbl_vuelta_actual = tk.Label(
            parent,
            text="",
            font=("Segoe UI", 10),
            bg=C["bg"],
            fg=C["muted"],
        )
        self.lbl_vuelta_actual.pack()

        # Botones
        btn_row = tk.Frame(parent, bg=C["bg"])
        btn_row.pack(pady=16)

        self.btn_iniciar = self._make_btn(
            btn_row, "▶  Iniciar", C["green"], self._crono_toggle)
        self.btn_iniciar.pack(side="left", padx=6)

        self.btn_vuelta = self._make_btn(
            btn_row, "⚑  Vuelta", C["yellow"], self._crono_vuelta,
            disabled=True)
        self.btn_vuelta.pack(side="left", padx=6)

        self.btn_reset = self._make_btn(
            btn_row, "↺  Reiniciar", C["border"], self._crono_reset,
            disabled=True)
        self.btn_reset.pack(side="left", padx=6)

        # Lista de vueltas
        lap_frame = tk.Frame(parent, bg=C["card"], padx=12, pady=10)
        lap_frame.pack(fill="both", expand=True, pady=(0, 8))

        tk.Label(
            lap_frame,
            text="Historial de vueltas",
            font=F_BTN,
            bg=C["card"],
            fg=C["muted"],
        ).pack(anchor="w")

        list_cont = tk.Frame(lap_frame, bg=C["card"])
        list_cont.pack(fill="both", expand=True, pady=(6, 0))

        scroll_lap = tk.Scrollbar(list_cont, orient="vertical")
        scroll_lap.pack(side="right", fill="y")

        self.listbox_laps = tk.Listbox(
            list_cont,
            font=F_LAP,
            bg=C["entry"],
            fg=C["text"],
            selectbackground=C["accent"],
            selectforeground=C["white"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scroll_lap.set,
            height=6,
        )
        self.listbox_laps.pack(side="left", fill="both", expand=True)
        scroll_lap.config(command=self.listbox_laps.yview)

    # ──────────────────────────────────────────────────
    #  PESTAÑA 3: TEMPORIZADOR
    # ──────────────────────────────────────────────────

    def _build_tab_temporizador(self, parent):
        tk.Label(
            parent,
            text="Configurar tiempo",
            font=F_BTN,
            bg=C["bg"],
            fg=C["muted"],
        ).pack(pady=(16, 6))

        # Inputs hh : mm : ss
        input_row = tk.Frame(parent, bg=C["bg"])
        input_row.pack()

        def spin(parent, label, maximo):
            f = tk.Frame(parent, bg=C["bg"])
            tk.Label(f, text=label, font=F_SMALL,
                     bg=C["bg"], fg=C["muted"]).pack()
            var = tk.StringVar(value="00")
            sb = tk.Spinbox(
                f,
                from_=0, to=maximo,
                textvariable=var,
                font=("Consolas", 22, "bold"),
                width=3,
                bg=C["entry"],
                fg=C["text"],
                buttonbackground=C["hover"],
                relief="flat",
                bd=0,
                highlightthickness=0,
                justify="center",
                format="%02.0f",
                wrap=True,
            )
            sb.pack()
            return var

        self.timer_h  = spin(input_row, "Horas",    23)
        tk.Label(input_row, text=":", font=("Consolas", 28, "bold"),
                 bg=C["bg"], fg=C["dim"]).pack(side="left", padx=4, pady=14)
        self.timer_m  = spin(input_row, "Minutos",  59)
        tk.Label(input_row, text=":", font=("Consolas", 28, "bold"),
                 bg=C["bg"], fg=C["dim"]).pack(side="left", padx=4, pady=14)
        self.timer_s  = spin(input_row, "Segundos", 59)

        # Display del temporizador
        self.lbl_timer = tk.Label(
            parent,
            text="00:00:00",
            font=F_RELOJ_MEDIANO,
            bg=C["bg"],
            fg=C["yellow"],
        )
        self.lbl_timer.pack(pady=(16, 0))

        # Barra de progreso
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Timer.Horizontal.TProgressbar",
            troughcolor=C["card"],
            background=C["yellow"],
            bordercolor=C["bg"],
            lightcolor=C["yellow"],
            darkcolor=C["yellow"],
        )
        self.timer_progress = ttk.Progressbar(
            parent,
            style="Timer.Horizontal.TProgressbar",
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=100,
        )
        self.timer_progress.pack(fill="x", padx=40, pady=(8, 0))

        # Botones
        t_btn_row = tk.Frame(parent, bg=C["bg"])
        t_btn_row.pack(pady=14)

        self.btn_timer_start = self._make_btn(
            t_btn_row, "▶  Iniciar", C["yellow"], self._timer_toggle)
        self.btn_timer_start.pack(side="left", padx=6)

        self._make_btn(
            t_btn_row, "↺  Reiniciar", C["border"], self._timer_reset
        ).pack(side="left", padx=6)

        # Presets rapidos
        preset_row = tk.Frame(parent, bg=C["bg"])
        preset_row.pack()
        tk.Label(preset_row, text="Presets:",
                 font=F_SMALL, bg=C["bg"], fg=C["muted"]).pack(side="left",
                                                                padx=(0, 8))
        for label, h, m, s in [
            ("1 min", 0, 1, 0), ("5 min", 0, 5, 0),
            ("10 min", 0, 10, 0), ("25 min", 0, 25, 0),
            ("1 hora", 1, 0, 0),
        ]:
            tk.Button(
                preset_row,
                text=label,
                font=F_SMALL,
                bg=C["card"],
                fg=C["muted"],
                activebackground=C["hover"],
                activeforeground=C["text"],
                relief="flat",
                cursor="hand2",
                padx=8,
                pady=3,
                command=lambda hh=h, mm=m, ss=s: self._timer_preset(hh, mm, ss),
            ).pack(side="left", padx=2)

    # ──────────────────────────────────────────────────
    #  LOGICA: RELOJ DIGITAL
    # ──────────────────────────────────────────────────

    def _iniciar_reloj(self):
        """Arranca el bucle del reloj. La funcion se llama a si misma con .after()."""
        self._actualizar_reloj()

    def _actualizar_reloj(self):
        """
        Funcion recursiva que actualiza la hora cada 1000 ms usando .after().

        Patron:
            1. Lee datetime.now()
            2. Actualiza el Label con .config(text=...)
            3. Agenda su propia ejecucion: self.after(1000, self._actualizar_reloj)
        """
        # 1. Leer la hora del sistema con datetime
        ahora = datetime.now()

        # 2a. Formatear la hora segun el modo seleccionado
        if self.var_formato_24h.get():
            fmt_hora = "%H:%M:%S"
        else:
            fmt_hora = "%I:%M:%S %p"

        hora_str = ahora.strftime(fmt_hora)

        # 2b. Efecto parpadeo en los dos puntos cada medio segundo
        if self.var_parpadeo.get() and ahora.microsecond < 500_000:
            if not self.var_formato_24h.get():
                hora_str = hora_str.replace(":", " ", 2)
            else:
                hora_str = hora_str.replace(":", " ")

        # 2c. Actualizar el Label grande con la hora
        self.lbl_hora.config(text=hora_str)

        # Milisegundos para el label secundario
        self.lbl_ms_reloj.config(
            text=f".{ahora.microsecond // 1000:03d}")

        # 2d. Actualizar la fecha
        dia_semana  = NOMBRE_DIAS[ahora.weekday()]
        mes_nombre  = NOMBRE_MESES[ahora.month]
        fecha_str   = f"{dia_semana}, {ahora.day} de {mes_nombre} de {ahora.year}"
        self.lbl_fecha.config(text=ahora.strftime("%d / %m / %Y"))
        self.lbl_dia.config(text=fecha_str)

        # 3. Reagendar: .after(1000, funcion) — NO usa sleep()
        #    Esto programa la siguiente llamada en 1000 ms
        #    sin bloquear el hilo principal de Tkinter
        self._reloj_job = self.after(1000, self._actualizar_reloj)
        #                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #                  Esta linea es la clave: llama a si misma
        #                  despues de 1 segundo

    # ──────────────────────────────────────────────────
    #  LOGICA: CRONOMETRO
    # ──────────────────────────────────────────────────

    def _crono_toggle(self):
        """Inicia o pausa el cronometro."""
        if self._crono_corriendo:
            # Pausar: acumular tiempo transcurrido
            self._crono_acumulado += time.perf_counter() - self._crono_inicio
            self._crono_corriendo = False
            if self._crono_job:
                self.after_cancel(self._crono_job)
                self._crono_job = None
            self.btn_iniciar.config(
                text="▶  Continuar", bg=C["green"])
        else:
            # Iniciar / continuar
            self._crono_inicio  = time.perf_counter()
            self._crono_corriendo = True
            self.btn_iniciar.config(
                text="⏸  Pausar", bg=C["pink"])
            self.btn_vuelta.config(state="normal", bg=C["yellow"],
                                   fg=C["bg"])
            self.btn_reset.config(state="normal", bg=C["border"],
                                  fg=C["text"])
            self._actualizar_cronometro()

    def _actualizar_cronometro(self):
        """
        Actualiza el display del cronometro cada 10 ms usando .after(10).
        Misma tecnica que el reloj pero con menor intervalo para mostrar
        centesimas de segundo.
        """
        if not self._crono_corriendo:
            return

        # Calcular tiempo total transcurrido
        transcurrido = self._crono_acumulado + (
            time.perf_counter() - self._crono_inicio)

        # Formatear: MM:SS.cc
        minutos   = int(transcurrido // 60)
        segundos  = int(transcurrido % 60)
        centesimas = int((transcurrido * 100) % 100)
        horas     = int(transcurrido // 3600)

        if horas > 0:
            self.lbl_crono.config(
                text=f"{horas:02d}:{minutos % 60:02d}:{segundos:02d}")
        else:
            self.lbl_crono.config(
                text=f"{minutos:02d}:{segundos:02d}")

        self.lbl_crono_cs.config(text=f".{centesimas:02d}")

        # Mostrar diferencia respecto a la ultima vuelta
        if self._laps:
            t_vuelta = transcurrido - self._laps[-1]
            mv = int(t_vuelta // 60)
            sv = int(t_vuelta % 60)
            cv = int((t_vuelta * 100) % 100)
            self.lbl_vuelta_actual.config(
                text=f"Vuelta actual:  {mv:02d}:{sv:02d}.{cv:02d}")

        # .after(10) — reagendar en 10 ms para centesimas fluidas
        self._crono_job = self.after(10, self._actualizar_cronometro)

    def _crono_vuelta(self):
        """Registra el tiempo de vuelta actual."""
        if not self._crono_corriendo:
            return
        transcurrido = self._crono_acumulado + (
            time.perf_counter() - self._crono_inicio)
        self._laps.append(transcurrido)

        n = len(self._laps)
        # Tiempo de esta vuelta (diferencial)
        if n == 1:
            t_vuelta = transcurrido
        else:
            t_vuelta = transcurrido - self._laps[-2]

        mv = int(t_vuelta // 60)
        sv = int(t_vuelta % 60)
        cv = int((t_vuelta * 100) % 100)
        mt = int(transcurrido // 60)
        st = int(transcurrido % 60)
        ct = int((transcurrido * 100) % 100)

        self.listbox_laps.insert(
            0,
            f"  Vuelta {n:>2}   lap: {mv:02d}:{sv:02d}.{cv:02d}   "
            f"total: {mt:02d}:{st:02d}.{ct:02d}",
        )

    def _crono_reset(self):
        """Reinicia el cronometro al estado inicial."""
        if self._crono_corriendo:
            self._crono_toggle()   # pausar primero

        self._crono_acumulado = 0.0
        self._crono_inicio    = None
        self._laps.clear()

        self.lbl_crono.config(text="00:00")
        self.lbl_crono_cs.config(text=".00")
        self.lbl_vuelta_actual.config(text="")
        self.listbox_laps.delete(0, "end")
        self.btn_iniciar.config(text="▶  Iniciar", bg=C["green"])
        self.btn_vuelta.config(state="disabled",
                               bg=C["border"], fg=C["muted"])
        self.btn_reset.config(state="disabled",
                              bg=C["border"], fg=C["muted"])

    # ──────────────────────────────────────────────────
    #  LOGICA: TEMPORIZADOR
    # ──────────────────────────────────────────────────

    def _timer_preset(self, h, m, s):
        """Carga un tiempo predefinido en los spinboxes."""
        self.timer_h.set(f"{h:02d}")
        self.timer_m.set(f"{m:02d}")
        self.timer_s.set(f"{s:02d}")

    def _timer_toggle(self):
        """Inicia o pausa el temporizador."""
        if self._timer_corriendo:
            # Pausar
            self._timer_restante -= time.perf_counter() - self._timer_inicio
            self._timer_corriendo = False
            if self._timer_job:
                self.after_cancel(self._timer_job)
                self._timer_job = None
            self.btn_timer_start.config(text="▶  Continuar", bg=C["yellow"])
        else:
            # Primera vez: leer los spinboxes
            if self._timer_restante == 0:
                try:
                    h = int(self.timer_h.get())
                    m = int(self.timer_m.get())
                    s = int(self.timer_s.get())
                except ValueError:
                    messagebox.showerror("Error", "Introduce valores numericos.")
                    return

                self._timer_total    = h * 3600 + m * 60 + s
                self._timer_restante = self._timer_total

                if self._timer_total == 0:
                    messagebox.showwarning(
                        "Tiempo cero", "Introduce un tiempo mayor a cero.")
                    return

            self._timer_corriendo = True
            self._timer_inicio    = time.perf_counter()
            self.btn_timer_start.config(text="⏸  Pausar", bg=C["pink"])
            self._actualizar_timer()

    def _actualizar_timer(self):
        """
        Cuenta regresiva usando .after(200) — misma tecnica que el reloj.
        Cuando llega a cero lanza messagebox de alarma.
        """
        if not self._timer_corriendo:
            return

        transcurrido = time.perf_counter() - self._timer_inicio
        restante = max(0.0, self._timer_restante - transcurrido)

        # Actualizar display
        h = int(restante // 3600)
        m = int((restante % 3600) // 60)
        s = int(restante % 60)
        self.lbl_timer.config(text=f"{h:02d}:{m:02d}:{s:02d}")

        # Barra de progreso
        if self._timer_total > 0:
            pct = (restante / self._timer_total) * 100
            self.timer_progress["value"] = pct

        # Cambiar color cuando queden menos de 10 segundos
        if restante <= 10:
            self.lbl_timer.config(fg=C["red"])
        else:
            self.lbl_timer.config(fg=C["yellow"])

        if restante <= 0:
            # ¡Tiempo terminado!
            self._timer_corriendo = False
            self.btn_timer_start.config(text="▶  Iniciar", bg=C["yellow"])
            self.timer_progress["value"] = 0
            self.lbl_timer.config(text="00:00:00", fg=C["red"])
            messagebox.showinfo(
                "¡Tiempo terminado!",
                "El temporizador ha llegado a cero.\n\n"
                "Presiona 'Reiniciar' para configurar uno nuevo.")
            return

        # Reagendar — .after() con 200ms para respuesta rapida
        self._timer_job = self.after(200, self._actualizar_timer)

    def _timer_reset(self):
        """Reinicia el temporizador."""
        if self._timer_corriendo:
            self._timer_corriendo = False
            if self._timer_job:
                self.after_cancel(self._timer_job)
                self._timer_job = None

        self._timer_restante = 0.0
        self._timer_total    = 0.0
        self.lbl_timer.config(text="00:00:00", fg=C["yellow"])
        self.timer_progress["value"] = 100
        self.btn_timer_start.config(text="▶  Iniciar", bg=C["yellow"])

    # ──────────────────────────────────────────────────
    #  HELPER: BOTON ESTILIZADO
    # ──────────────────────────────────────────────────

    def _make_btn(self, parent, text, color, cmd, disabled=False):
        state = "disabled" if disabled else "normal"
        fg    = C["muted"] if disabled else C["bg"] if color != C["border"] \
            else C["text"]
        btn = tk.Button(
            parent,
            text=text,
            font=F_BTN,
            bg=color if not disabled else C["border"],
            fg=fg,
            activebackground=C["hover"],
            activeforeground=C["text"],
            disabledforeground=C["muted"],
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=8,
            state=state,
            command=cmd,
        )
        return btn


# ──────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    app = RelojCronometro()
    app.mainloop()
