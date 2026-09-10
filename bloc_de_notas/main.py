"""
╔══════════════════════════════════════════════════════════╗
║   📝  Bloc de Notas Basico                               ║
║   Widgets: Text · Menu · filedialog · messagebox         ║
║   Logica : open() / read() / write() con Python puro     ║
╚══════════════════════════════════════════════════════════╝

Demuestra:
  - Widget Text  multilinea con scrollbar
  - Menu  barra superior (Archivo, Editar, Ver, Ayuda)
  - filedialog  ventanas nativas del SO para abrir/guardar
  - messagebox  dialogos de confirmacion y error
  - open() / read() / write()  manejo de archivos con Python puro
  - Atajos de teclado  Ctrl+S, Ctrl+O, Ctrl+N, etc.
  - Barra de estado  linea, columna, conteo de palabras
  - Buscar y Reemplazar  ventana secundaria Toplevel
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
import os


# ──────────────────────────────────────────────────────
#  PALETA DE COLORES  (tema oscuro por defecto)
# ──────────────────────────────────────────────────────

TEMA_OSCURO = {
    "bg":        "#0d0f14",
    "surface":   "#161b26",
    "text_bg":   "#1a1f2e",
    "text_fg":   "#e6eaf4",
    "cursor":    "#7c6fff",
    "sel_bg":    "#7c6fff",
    "menu_bg":   "#161b26",
    "menu_fg":   "#e6eaf4",
    "menu_act":  "#2a3147",
    "status_bg": "#0d0f14",
    "status_fg": "#7a8399",
    "accent":    "#7c6fff",
    "green":     "#43d9ad",
    "border":    "#2a3147",
    "lnum_bg":   "#161b26",
    "lnum_fg":   "#3d4a66",
}

TEMA_CLARO = {
    "bg":        "#f5f5f5",
    "surface":   "#ffffff",
    "text_bg":   "#ffffff",
    "text_fg":   "#1a1a2e",
    "cursor":    "#5a4fcf",
    "sel_bg":    "#7c6fff",
    "menu_bg":   "#f0f0f0",
    "menu_fg":   "#1a1a2e",
    "menu_act":  "#dde3f0",
    "status_bg": "#e8e8e8",
    "status_fg": "#555555",
    "accent":    "#5a4fcf",
    "green":     "#2a9d7a",
    "border":    "#cccccc",
    "lnum_bg":   "#f0f0f0",
    "lnum_fg":   "#aaaaaa",
}

FONT_TEXTO   = ("Consolas", 13)
FONT_STATUS  = ("Segoe UI", 9)
FONT_TITULO  = ("Segoe UI", 12, "bold")
FONT_HEADING = ("Segoe UI", 10, "bold")
FONT_SMALL   = ("Segoe UI", 9)

NOMBRE_APP = "Bloc de Notas"
EXTENSIONES = [
    ("Archivos de texto", "*.txt"),
    ("Python",            "*.py"),
    ("Markdown",          "*.md"),
    ("HTML",              "*.html"),
    ("JSON",              "*.json"),
    ("Todos los archivos","*.*"),
]


# ──────────────────────────────────────────────────────
#  APLICACION PRINCIPAL
# ──────────────────────────────────────────────────────

class BlocDeNotas(tk.Tk):
    """Bloc de notas basico con Python + Tkinter."""

    def __init__(self):
        super().__init__()

        # Estado
        self.ruta_actual: str | None = None   # ruta del archivo abierto
        self.modificado:  bool       = False   # hay cambios sin guardar
        self.tema_actual: str        = "oscuro"
        self.T = TEMA_OSCURO                   # colores activos

        self.geometry("900x680")
        self.minsize(600, 400)

        # ── Configurar interfaz ──
        self._build_menu()
        self._build_editor()
        self._build_statusbar()
        self._apply_theme()
        self._update_title()

        # ── Atajos de teclado ──
        self._bind_shortcuts()

        # ── Polling para cursor/palabras ──
        self._poll_status()

    # ──────────────────────────────────────────────────
    #  MENÚ
    # ──────────────────────────────────────────────────

    def _build_menu(self):
        """Crea la barra de menú principal con Menu."""
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # ── Archivo ──
        m_archivo = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Archivo", menu=m_archivo)

        m_archivo.add_command(
            label="Nuevo          Ctrl+N", command=self.nuevo_archivo)
        m_archivo.add_command(
            label="Abrir...       Ctrl+O", command=self.abrir_archivo)
        m_archivo.add_separator()
        m_archivo.add_command(
            label="Guardar        Ctrl+S", command=self.guardar)
        m_archivo.add_command(
            label="Guardar como...Ctrl+Shift+S", command=self.guardar_como)
        m_archivo.add_separator()
        m_archivo.add_command(
            label="Salir          Alt+F4", command=self.salir)

        self.m_archivo = m_archivo   # guardar referencia para re-estilizar

        # ── Editar ──
        m_editar = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Editar", menu=m_editar)

        m_editar.add_command(
            label="Deshacer       Ctrl+Z", command=self._deshacer)
        m_editar.add_command(
            label="Rehacer        Ctrl+Y", command=self._rehacer)
        m_editar.add_separator()
        m_editar.add_command(
            label="Cortar         Ctrl+X", command=self._cortar)
        m_editar.add_command(
            label="Copiar         Ctrl+C", command=self._copiar)
        m_editar.add_command(
            label="Pegar          Ctrl+V", command=self._pegar)
        m_editar.add_separator()
        m_editar.add_command(
            label="Seleccionar todo Ctrl+A", command=self._seleccionar_todo)
        m_editar.add_separator()
        m_editar.add_command(
            label="Buscar y reemplazar  Ctrl+H",
            command=self._abrir_buscar_reemplazar)

        self.m_editar = m_editar

        # ── Ver ──
        m_ver = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ver", menu=m_ver)

        m_ver.add_command(
            label="Aumentar fuente   Ctrl++", command=self._zoom_in)
        m_ver.add_command(
            label="Reducir fuente    Ctrl+-", command=self._zoom_out)
        m_ver.add_command(
            label="Restablecer fuente Ctrl+0", command=self._zoom_reset)
        m_ver.add_separator()

        self.var_word_wrap = tk.BooleanVar(value=True)
        m_ver.add_checkbutton(
            label="Ajuste de linea",
            variable=self.var_word_wrap,
            command=self._toggle_word_wrap)
        m_ver.add_separator()
        m_ver.add_command(
            label="Cambiar tema (oscuro/claro)", command=self._toggle_tema)

        self.m_ver = m_ver

        # ── Ayuda ──
        m_ayuda = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ayuda", menu=m_ayuda)
        m_ayuda.add_command(
            label="Atajos de teclado", command=self._mostrar_atajos)
        m_ayuda.add_separator()
        m_ayuda.add_command(
            label="Acerca de...", command=self._acerca_de)

        self.m_ayuda = m_ayuda
        self._menus = [m_archivo, m_editar, m_ver, m_ayuda]

    # ──────────────────────────────────────────────────
    #  EDITOR
    # ──────────────────────────────────────────────────

    def _build_editor(self):
        """Crea el area de edicion: widget Text + scrollbars."""
        self.editor_frame = tk.Frame(self)
        self.editor_frame.pack(fill="both", expand=True)

        # Scrollbar vertical
        self.scroll_y = tk.Scrollbar(self.editor_frame, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")

        # Scrollbar horizontal
        self.scroll_x = tk.Scrollbar(self.editor_frame, orient="horizontal")
        self.scroll_x.pack(side="bottom", fill="x")

        # Widget Text principal — multilinea
        self.texto = tk.Text(
            self.editor_frame,
            font=FONT_TEXTO,
            wrap="word",                     # ajuste de linea activado
            undo=True,                       # habilitar deshacer/rehacer
            maxundo=-1,                      # historial ilimitado
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set,
            padx=16,
            pady=12,
            relief="flat",
            bd=0,
            insertwidth=2,
            spacing3=2,
        )
        self.texto.pack(side="left", fill="both", expand=True)

        # Conectar scrollbars con el Text
        self.scroll_y.config(command=self.texto.yview)
        self.scroll_x.config(command=self.texto.xview)

        # Detectar cambios para marcar como "modificado"
        self.texto.bind("<<Modified>>", self._on_text_modified)
        self.texto.bind("<KeyRelease>", self._on_key_release)

        # Tamaño de fuente inicial
        self.font_size = 13

    # ──────────────────────────────────────────────────
    #  BARRA DE ESTADO
    # ──────────────────────────────────────────────────

    def _build_statusbar(self):
        """Barra inferior con info de cursor y conteo de palabras."""
        self.status_bar = tk.Frame(self, height=24)
        self.status_bar.pack(side="bottom", fill="x")

        self.lbl_pos = tk.Label(
            self.status_bar,
            text="Ln 1, Col 1",
            font=FONT_STATUS,
            anchor="w",
            padx=12,
        )
        self.lbl_pos.pack(side="left")

        tk.Frame(self.status_bar, width=1).pack(side="left", fill="y", pady=4)

        self.lbl_palabras = tk.Label(
            self.status_bar,
            text="0 palabras · 0 caracteres",
            font=FONT_STATUS,
            anchor="w",
            padx=12,
        )
        self.lbl_palabras.pack(side="left")

        self.lbl_ruta = tk.Label(
            self.status_bar,
            text="Sin guardar",
            font=FONT_STATUS,
            anchor="e",
            padx=12,
        )
        self.lbl_ruta.pack(side="right")

        self.lbl_encoding = tk.Label(
            self.status_bar,
            text="UTF-8",
            font=FONT_STATUS,
            anchor="e",
            padx=12,
        )
        self.lbl_encoding.pack(side="right")

    # ──────────────────────────────────────────────────
    #  TEMA
    # ──────────────────────────────────────────────────

    def _apply_theme(self):
        """Aplica los colores del tema actual a todos los widgets."""
        T = self.T

        self.configure(bg=T["bg"])
        self.editor_frame.configure(bg=T["bg"])

        # Text
        self.texto.configure(
            bg=T["text_bg"],
            fg=T["text_fg"],
            insertbackground=T["cursor"],
            selectbackground=T["sel_bg"],
            selectforeground=T["text_fg"],
        )

        # Scrollbars
        self.scroll_y.configure(
            bg=T["surface"], troughcolor=T["bg"],
            activebackground=T["accent"])
        self.scroll_x.configure(
            bg=T["surface"], troughcolor=T["bg"],
            activebackground=T["accent"])

        # Status bar
        self.status_bar.configure(bg=T["status_bg"])
        for w in (self.lbl_pos, self.lbl_palabras,
                  self.lbl_ruta, self.lbl_encoding):
            w.configure(bg=T["status_bg"], fg=T["status_fg"])

        # Menus
        self.menubar.configure(
            bg=T["menu_bg"], fg=T["menu_fg"],
            activebackground=T["menu_act"],
            activeforeground=T["menu_fg"])
        for m in self._menus:
            m.configure(
                bg=T["menu_bg"], fg=T["menu_fg"],
                activebackground=T["accent"],
                activeforeground="#ffffff",
                selectcolor=T["accent"])

    # ──────────────────────────────────────────────────
    #  ATAJOS DE TECLADO
    # ──────────────────────────────────────────────────

    def _bind_shortcuts(self):
        self.bind("<Control-n>", lambda _: self.nuevo_archivo())
        self.bind("<Control-N>", lambda _: self.nuevo_archivo())
        self.bind("<Control-o>", lambda _: self.abrir_archivo())
        self.bind("<Control-O>", lambda _: self.abrir_archivo())
        self.bind("<Control-s>", lambda _: self.guardar())
        self.bind("<Control-S>", lambda _: self.guardar())
        self.bind("<Control-Shift-s>", lambda _: self.guardar_como())
        self.bind("<Control-Shift-S>", lambda _: self.guardar_como())
        self.bind("<Control-h>",
                  lambda _: self._abrir_buscar_reemplazar())
        self.bind("<Control-H>",
                  lambda _: self._abrir_buscar_reemplazar())
        self.bind("<Control-equal>", lambda _: self._zoom_in())
        self.bind("<Control-plus>",  lambda _: self._zoom_in())
        self.bind("<Control-minus>", lambda _: self._zoom_out())
        self.bind("<Control-0>",     lambda _: self._zoom_reset())
        self.protocol("WM_DELETE_WINDOW", self.salir)

    # ──────────────────────────────────────────────────
    #  LÓGICA: ARCHIVO  (open / read / write)
    # ──────────────────────────────────────────────────

    def nuevo_archivo(self):
        """Crea un documento nuevo. Confirma si hay cambios sin guardar."""
        if not self._confirmar_descarte():
            return
        self.texto.delete("1.0", "end")   # borra todo el contenido del Text
        self.ruta_actual = None
        self.modificado  = False
        self.texto.edit_reset()           # limpia el historial de deshacer
        self._update_title()
        self._update_statusbar()

    def abrir_archivo(self):
        """
        Abre un archivo del sistema usando filedialog.askopenfilename().
        Luego lee su contenido con open() y lo inserta en el Text.
        """
        if not self._confirmar_descarte():
            return

        # filedialog muestra la ventana nativa del SO
        ruta = filedialog.askopenfilename(
            title="Abrir archivo",
            filetypes=EXTENSIONES,
        )
        if not ruta:
            return   # el usuario canceló

        try:
            # Leer archivo con Python puro: open() + read()
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            self.texto.delete("1.0", "end")
            self.texto.insert("1.0", contenido)
            self.texto.edit_reset()
            self.ruta_actual = ruta
            self.modificado  = False
            self._update_title()
            self._update_statusbar()

        except UnicodeDecodeError:
            # Intentar con latin-1 si UTF-8 falla
            try:
                with open(ruta, "r", encoding="latin-1") as f:
                    contenido = f.read()
                self.texto.delete("1.0", "end")
                self.texto.insert("1.0", contenido)
                self.texto.edit_reset()
                self.ruta_actual = ruta
                self.modificado  = False
                self._update_title()
                self._update_statusbar()
                messagebox.showwarning(
                    "Aviso de codificacion",
                    "El archivo se abrio con codificacion latin-1\n"
                    "porque no es compatible con UTF-8.")
            except Exception as e:
                messagebox.showerror("Error al abrir", str(e))

        except PermissionError:
            messagebox.showerror(
                "Sin permisos",
                f"No tienes permiso para leer:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al abrir", str(e))

    def guardar(self):
        """
        Guarda en la ruta actual. Si no hay ruta, llama a guardar_como().
        Usa open() + write() para escribir el archivo.
        """
        if self.ruta_actual:
            self._escribir_archivo(self.ruta_actual)
        else:
            self.guardar_como()

    def guardar_como(self):
        """
        Muestra filedialog.asksaveasfilename() para elegir ruta y nombre,
        luego escribe el archivo con open() + write().
        """
        ruta = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".txt",
            filetypes=EXTENSIONES,
        )
        if not ruta:
            return   # usuario canceló
        self._escribir_archivo(ruta)

    def _escribir_archivo(self, ruta: str):
        """
        Escribe el contenido del Text en disco usando open() y write().
        Esta es la operacion central de E/S del proyecto.
        """
        try:
            contenido = self.texto.get("1.0", "end-1c")  # leer todo el Text

            # Escribir archivo con Python puro: open() + write()
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)

            self.ruta_actual = ruta
            self.modificado  = False
            self._update_title()
            self._update_statusbar()

        except PermissionError:
            messagebox.showerror(
                "Sin permisos",
                f"No tienes permiso para guardar en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    def salir(self):
        """Cierra la aplicacion. Confirma si hay cambios sin guardar."""
        if self._confirmar_descarte():
            self.destroy()

    def _confirmar_descarte(self) -> bool:
        """
        Si hay cambios sin guardar, muestra messagebox.askyesnocancel().
        Devuelve True si se puede continuar, False si el usuario cancela.
        """
        if not self.modificado:
            return True

        nombre = os.path.basename(self.ruta_actual) if self.ruta_actual \
            else "Sin titulo"

        # messagebox muestra un dialogo nativo del SO
        respuesta = messagebox.askyesnocancel(
            "Cambios sin guardar",
            f"'{nombre}' tiene cambios sin guardar.\n\n"
            "¿Deseas guardar antes de continuar?",
        )
        if respuesta is True:     # Si
            self.guardar()
            return not self.modificado  # True si se guardo bien
        elif respuesta is False:  # No
            return True
        else:                     # Cancelar / cerrar dialogo
            return False

    # ──────────────────────────────────────────────────
    #  LÓGICA: EDITAR
    # ──────────────────────────────────────────────────

    def _deshacer(self):
        try:
            self.texto.edit_undo()
        except tk.TclError:
            pass   # no hay nada que deshacer

    def _rehacer(self):
        try:
            self.texto.edit_redo()
        except tk.TclError:
            pass

    def _cortar(self):
        self.texto.event_generate("<<Cut>>")

    def _copiar(self):
        self.texto.event_generate("<<Copy>>")

    def _pegar(self):
        self.texto.event_generate("<<Paste>>")

    def _seleccionar_todo(self):
        self.texto.tag_add("sel", "1.0", "end")

    # ──────────────────────────────────────────────────
    #  LÓGICA: VER
    # ──────────────────────────────────────────────────

    def _zoom_in(self):
        self.font_size = min(self.font_size + 1, 40)
        self.texto.configure(font=(FONT_TEXTO[0], self.font_size))

    def _zoom_out(self):
        self.font_size = max(self.font_size - 1, 7)
        self.texto.configure(font=(FONT_TEXTO[0], self.font_size))

    def _zoom_reset(self):
        self.font_size = 13
        self.texto.configure(font=FONT_TEXTO)

    def _toggle_word_wrap(self):
        wrap = "word" if self.var_word_wrap.get() else "none"
        self.texto.configure(wrap=wrap)

    def _toggle_tema(self):
        if self.tema_actual == "oscuro":
            self.tema_actual = "claro"
            self.T = TEMA_CLARO
        else:
            self.tema_actual = "oscuro"
            self.T = TEMA_OSCURO
        self._apply_theme()

    # ──────────────────────────────────────────────────
    #  BUSCAR Y REEMPLAZAR
    # ──────────────────────────────────────────────────

    def _abrir_buscar_reemplazar(self):
        """Abre una ventana secundaria (Toplevel) de buscar/reemplazar."""
        if hasattr(self, "_ventana_buscar") and \
                self._ventana_buscar.winfo_exists():
            self._ventana_buscar.lift()
            return

        T = self.T
        win = tk.Toplevel(self)
        win.title("Buscar y reemplazar")
        win.geometry("420x220")
        win.resizable(False, False)
        win.configure(bg=T["bg"])
        win.transient(self)      # siempre encima de la ventana principal
        self._ventana_buscar = win

        pad = {"padx": 16, "pady": 6, "fill": "x"}

        def lbl(text):
            tk.Label(win, text=text, font=FONT_SMALL,
                     bg=T["bg"], fg=T["status_fg"],
                     anchor="w").pack(**pad)

        def entrada():
            f = tk.Frame(win, bg=T["entry_bg"] if "entry_bg" in T
                         else T["text_bg"], padx=8, pady=4)
            f.pack(padx=16, pady=(0, 4), fill="x")
            e = tk.Entry(f, font=FONT_TEXTO,
                         bg=T["text_bg"], fg=T["text_fg"],
                         insertbackground=T["cursor"],
                         relief="flat", bd=0)
            e.pack(fill="x")
            return e

        lbl("Buscar:")
        self.entry_buscar = entrada()

        lbl("Reemplazar con:")
        self.entry_reemplazar = entrada()

        # Contador de resultados
        self.lbl_resultados = tk.Label(
            win, text="", font=FONT_SMALL,
            bg=T["bg"], fg=T["accent"])
        self.lbl_resultados.pack(padx=16, anchor="w")

        # Botones
        btn_frame = tk.Frame(win, bg=T["bg"])
        btn_frame.pack(padx=16, pady=(4, 12), fill="x")

        def btn(text, cmd, color=None):
            color = color or T["surface"]
            tk.Button(
                btn_frame, text=text, font=FONT_SMALL,
                bg=color, fg=T["text_fg"],
                activebackground=T["menu_act"],
                activeforeground=T["text_fg"],
                relief="flat", cursor="hand2",
                padx=10, pady=5,
                command=cmd,
            ).pack(side="left", padx=(0, 6))

        btn("Buscar siguiente", self._buscar_siguiente)
        btn("Reemplazar",       self._reemplazar_uno)
        btn("Reemplazar todo",  self._reemplazar_todo,
            color=T["accent"])

        win.bind("<Return>", lambda _: self._buscar_siguiente())
        win.bind("<Escape>", lambda _: win.destroy())
        self.entry_buscar.focus_set()

    def _buscar_siguiente(self):
        """Resalta la siguiente ocurrencia del termino buscado."""
        termino = self.entry_buscar.get()
        if not termino:
            return

        # Quitar marcas anteriores
        self.texto.tag_remove("busqueda", "1.0", "end")

        start = "1.0"
        count = 0
        while True:
            pos = self.texto.search(termino, start, stopindex="end",
                                    nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(termino)}c"
            self.texto.tag_add("busqueda", pos, end)
            self.texto.tag_config(
                "busqueda",
                background=self.T["accent"],
                foreground="#ffffff")
            start = end
            count += 1

        if count:
            # Mover vista a la primera ocurrencia
            first = self.texto.tag_ranges("busqueda")
            if first:
                self.texto.see(first[0])
            self.lbl_resultados.config(
                text=f"  {count} resultado(s) encontrado(s)")
        else:
            self.lbl_resultados.config(
                text="  No se encontraron resultados")

    def _reemplazar_uno(self):
        """Reemplaza la primera ocurrencia seleccionada."""
        termino    = self.entry_buscar.get()
        reemplazo  = self.entry_reemplazar.get()
        if not termino:
            return
        pos = self.texto.search(termino, "1.0", stopindex="end", nocase=True)
        if pos:
            end = f"{pos}+{len(termino)}c"
            self.texto.delete(pos, end)
            self.texto.insert(pos, reemplazo)
            self._buscar_siguiente()

    def _reemplazar_todo(self):
        """Reemplaza todas las ocurrencias del termino."""
        termino   = self.entry_buscar.get()
        reemplazo = self.entry_reemplazar.get()
        if not termino:
            return
        contenido = self.texto.get("1.0", "end-1c")
        nuevo     = contenido.replace(termino, reemplazo)
        count     = contenido.count(termino)
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", nuevo)
        self.lbl_resultados.config(
            text=f"  {count} reemplazo(s) realizados")

    # ──────────────────────────────────────────────────
    #  EVENTOS Y ESTADO
    # ──────────────────────────────────────────────────

    def _on_text_modified(self, _event=None):
        """Se llama cuando el Text registra un cambio (<<Modified>>)."""
        if self.texto.edit_modified():
            self.modificado = True
            self._update_title()
            self.texto.edit_modified(False)  # reset interno de Tkinter

    def _on_key_release(self, _event=None):
        self._update_statusbar()

    def _poll_status(self):
        """Actualiza la barra de estado cada 300ms."""
        self._update_statusbar()
        self.after(300, self._poll_status)

    def _update_title(self):
        """Actualiza el titulo de la ventana."""
        nombre = (os.path.basename(self.ruta_actual)
                  if self.ruta_actual else "Sin titulo")
        marca = " •" if self.modificado else ""
        self.title(f"{nombre}{marca}  —  {NOMBRE_APP}")

    def _update_statusbar(self):
        """Actualiza la posicion del cursor y el conteo de palabras."""
        try:
            pos     = self.texto.index("insert")        # "linea.columna"
            linea, col = pos.split(".")
            contenido = self.texto.get("1.0", "end-1c")
            palabras  = len(contenido.split()) if contenido.strip() else 0
            chars     = len(contenido)

            self.lbl_pos.config(
                text=f"Ln {linea}, Col {int(col)+1}")
            self.lbl_palabras.config(
                text=f"{palabras:,} palabras · {chars:,} caracteres")
            self.lbl_ruta.config(
                text=self.ruta_actual if self.ruta_actual else "Sin guardar")
        except Exception:
            pass

    # ──────────────────────────────────────────────────
    #  AYUDA
    # ──────────────────────────────────────────────────

    def _mostrar_atajos(self):
        atajos = (
            "Atajos de teclado\n"
            "══════════════════════════════\n"
            "Ctrl+N     Nuevo archivo\n"
            "Ctrl+O     Abrir archivo\n"
            "Ctrl+S     Guardar\n"
            "Ctrl+Shift+S  Guardar como\n"
            "Ctrl+Z     Deshacer\n"
            "Ctrl+Y     Rehacer\n"
            "Ctrl+X     Cortar\n"
            "Ctrl+C     Copiar\n"
            "Ctrl+V     Pegar\n"
            "Ctrl+A     Seleccionar todo\n"
            "Ctrl+H     Buscar y reemplazar\n"
            "Ctrl++     Aumentar fuente\n"
            "Ctrl+-     Reducir fuente\n"
            "Ctrl+0     Restablecer fuente\n"
        )
        messagebox.showinfo("Atajos de teclado", atajos)

    def _acerca_de(self):
        messagebox.showinfo(
            "Acerca de",
            f"{NOMBRE_APP}\n\n"
            "Ejercicio de Tkinter:\n"
            "  - Widget Text (multilinea)\n"
            "  - Menu (barra de navegacion)\n"
            "  - filedialog (ventanas nativas del SO)\n"
            "  - messagebox (dialogos emergentes)\n"
            "  - open() / read() / write() (Python puro)\n\n"
            "Python + Tkinter  |  MIT License"
        )


# ──────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    app = BlocDeNotas()
    app.mainloop()
