[README.md](https://github.com/user-attachments/files/32036779/README.md)
# 🖥️ Ejercicios Tkinter — Colección de Apps de Escritorio con Python

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?logo=python)
![Proyectos](https://img.shields.io/badge/Proyectos-6-blueviolet)
![Sin dependencias](https://img.shields.io/badge/Dependencias_externas-Ninguna-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Colección de **6 aplicaciones de escritorio** desarrolladas con **Python puro + Tkinter**, organizadas de menor a mayor complejidad. Cada proyecto demuestra un conjunto de widgets, variables de control y técnicas específicas de Tkinter, ideales para aprender desarrollo de interfaces gráficas sin frameworks externos.

> **Sin instalaciones adicionales** — Tkinter viene incluido con todas las distribuciones oficiales de Python.

---

## 📁 Estructura del repositorio

```
EjerciciosTkinter/
│
├── 📂 conversor_unidades/      # 01 — Conversor de unidades
├── 📂 formulario_registro/     # 02 — Formulario multiopción
├── 📂 bloc_de_notas/           # 03 — Bloc de notas con menú
├── 📂 pizarra_dibujo/          # 04 — Pizarra de dibujo (Canvas)
├── 📂 reloj_cronometro/        # 05 — Reloj digital y cronómetro
├── 📂 monitor_sensores/        # 06 — Monitor de sensores simulado
│
└── README.md                   # Este archivo
```

Cada subcarpeta contiene su propio `main.py`, `README.md`, `requirements.txt` y `.gitignore`.

---

## 🗂️ Proyectos

---

### 01 — 🔄 Conversor de Unidades

> **Carpeta:** `conversor_unidades/`

Aplicación para convertir entre unidades de medida con **8 categorías** y conversión en tiempo real.

**Widgets y técnicas:**
- `ttk.Combobox` — menú desplegable para seleccionar unidades
- `Entry` + `StringVar` — campo de entrada con variable de control
- Tabla de referencia rápida generada dinámicamente

**Categorías incluidas:**

| | | | |
|---|---|---|---|
| 🌡️ Temperatura | 📏 Longitud | ⚖️ Masa | 🧴 Volumen |
| 💨 Velocidad | ⏱️ Tiempo | 📐 Área | ⚡ Energía |

```bash
cd conversor_unidades
python main.py
```

---

### 02 — 📋 Formulario de Registro Multiopción

> **Carpeta:** `formulario_registro/`

Formulario completo que demuestra el **manejo de variables de control** de Tkinter y la **agrupación de elementos** en contenedores `Frame`.

**Widgets y variables de control:**

| Widget | Variable | Comportamiento |
|---|---|---|
| `Entry` | `StringVar` | Texto libre |
| `Radiobutton` | `StringVar` | Selección única |
| `ttk.Combobox` | `StringVar` | Menú desplegable |
| `Checkbutton` × 10 | `BooleanVar` | Selección múltiple |
| `Checkbutton` (términos) | `IntVar` | Valor `0` / `1` |
| `Frame` | — | Agrupación visual de secciones |

```bash
cd formulario_registro
python main.py
```

---

### 03 — 📝 Bloc de Notas Básico

> **Carpeta:** `bloc_de_notas/`

Editor de texto funcional que demuestra la **interacción con el sistema de archivos** y la creación de **barras de navegación** con menús.

**Widgets y herramientas:**
- `Text` — caja de texto multilínea con historial de deshacer
- `Menu` — barra superior con 4 submenús (Archivo, Editar, Ver, Ayuda)
- `filedialog` — ventanas nativas del SO para abrir y guardar rutas
- `messagebox` — diálogos emergentes de confirmación y error
- `open()` / `read()` / `write()` — E/S de archivos con Python puro

**Extras:** Buscar y Reemplazar · Tema oscuro/claro · Zoom de fuente · Barra de estado

```bash
cd bloc_de_notas
python main.py
```

---

### 04 — 🎨 Mini Pizarra de Dibujo

> **Carpeta:** `pizarra_dibujo/`

Aplicación de dibujo 2D que demuestra la **capacidad del Canvas** para renderizar gráficos y **escuchar eventos de hardware** (ratón) en tiempo real.

**Widgets y eventos:**

```python
canvas.bind("<ButtonPress-1>",   on_press)    # presionar botón
canvas.bind("<B1-Motion>",       on_drag)     # arrastrar
canvas.bind("<ButtonRelease-1>", on_release)  # soltar

# Métodos de dibujo con coordenadas event.x / event.y
canvas.create_line(x0, y0, x1, y1, ...)
canvas.create_oval(x0, y0, x1, y1, ...)
canvas.create_rectangle(x0, y0, x1, y1, ...)
```

**Herramientas:** ✏ Lápiz · 🖌 Pincel · ⬜ Borrador · ╱ Línea · □ Rectángulo · ○ Óvalo · ■ Rect. relleno · ● Oval relleno

```bash
cd pizarra_dibujo
python main.py
```

---

### 05 — ⏱️ Reloj Digital y Cronómetro

> **Carpeta:** `reloj_cronometro/`

Aplicación en tiempo real que demuestra cómo **actualizar la UI continuamente** sin congelar el programa, usando `.after()` en lugar de `time.sleep()`.

**Técnica central — patrón recursivo con `.after()`:**

```python
def actualizar_reloj(self):
    ahora = datetime.now()                           # leer sistema
    self.lbl_hora.config(text=ahora.strftime(...))   # actualizar Label
    self.after(1000, self.actualizar_reloj)          # ← reagendar
    # ↑ Se llama a sí misma cada 1 s SIN bloquear el hilo principal
```

| ❌ `time.sleep(1)` | ✅ `.after(1000, fn)` |
|---|---|
| Congela el hilo principal | No bloquea la UI |
| La ventana deja de responder | La ventana sigue respondiendo |

**Pestañas:** 🕐 Reloj (fuente 72pt) · ⏱️ Cronómetro con vueltas · ⏳ Temporizador con presets

```bash
cd reloj_cronometro
python main.py
```

---

### 06 — 📊 Monitor de Sensores (Simulado)

> **Carpeta:** `monitor_sensores/`

Dashboard de monitoreo que demuestra la **visualización de datos numéricos** y **controles deslizantes**, con indicadores de estado dinámicos según umbrales.

**Widgets y lógica:**

```python
# DoubleVar conecta Scale y Progressbar
var = tk.DoubleVar(value=42.0)

Scale(parent, variable=var, from_=0, to=120,
      command=lambda v: actualizar(float(v)))  # callback en cada movimiento

def actualizar(valor):
    pct = ((valor - MIN) / (MAX - MIN)) * 100
    progressbar["value"] = pct

    if pct >= CRITICO:     lbl.config(text="■ Crítico",     fg="red")
    elif pct >= ADVERTENCIA: lbl.config(text="▲ Advertencia", fg="yellow")
    else:                    lbl.config(text="● Normal",      fg="green")
```

**Sensores:** 🌡️ Temperatura · 💧 Humedad · 💻 CPU · 🔧 Presión · ⚡ Voltaje · ⚙️ RPM

**Extras:** Simulación automática con `.after()` · Mini-gráficos Canvas · Log de alertas

```bash
cd monitor_sensores
python main.py
```

---

## 📚 Tabla resumen de widgets cubiertos

| Widget / Técnica | Proj. 01 | Proj. 02 | Proj. 03 | Proj. 04 | Proj. 05 | Proj. 06 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `Label` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `Entry` + `StringVar` | ✅ | ✅ | — | — | — | — |
| `Button` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `Frame` (agrupación) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ttk.Combobox` | ✅ | ✅ | — | — | — | — |
| `Radiobutton` + `StringVar` | — | ✅ | — | — | — | — |
| `Checkbutton` + `BooleanVar`/`IntVar` | — | ✅ | — | — | — | — |
| `Text` (multilínea) | — | — | ✅ | — | — | ✅ |
| `Menu` + `filedialog` + `messagebox` | — | — | ✅ | — | — | — |
| `Canvas` + eventos ratón | — | — | — | ✅ | — | ✅ |
| `create_line/oval/rectangle` | — | — | — | ✅ | — | — |
| `.after()` (loop no bloqueante) | — | — | — | — | ✅ | ✅ |
| `Scale` + `DoubleVar` | — | — | — | — | — | ✅ |
| `ttk.Progressbar` | — | — | — | — | ✅ | ✅ |
| `Listbox` + `Scrollbar` | — | — | — | — | ✅ | ✅ |
| `Spinbox` | — | — | — | — | ✅ | — |
| `colorchooser` | — | — | — | ✅ | — | — |

---

## 🚀 Cómo ejecutar cualquier proyecto

```bash
# 1. Clona el repositorio
git clone https://github.com/jjulianernesto-web/EjerciciosTkinter.git
cd EjerciciosTkinter

# 2. Entra a la carpeta del proyecto que quieras probar
cd conversor_unidades   # o cualquiera de los 6

# 3. Ejecuta
python main.py
```

> ✅ **No se requiere instalar nada.** Tkinter, `datetime`, `math` y `random` vienen con Python.

---

## 🐍 Requisitos

- **Python 3.8** o superior
- **Tkinter** (incluido en todas las instalaciones oficiales de Python para Windows, macOS y Linux)

Para verificar que Tkinter está disponible:

```bash
python -c "import tkinter; print('Tkinter OK -', tkinter.TkVersion)"
```

---

## 📦 Empaquetar como ejecutable `.exe`

Cualquier proyecto puede convertirse en un ejecutable independiente con **PyInstaller**:

```bash
pip install pyinstaller
cd nombre_del_proyecto
pyinstaller --onefile --windowed main.py
# El .exe se genera en dist/
```

---

## 🤝 Contribuir

1. Haz un **fork** del repositorio
2. Crea tu rama: `git checkout -b feature/nuevo-ejercicio`
3. Agrega tu proyecto en una nueva carpeta con su propio `main.py` y `README.md`
4. Commit: `git commit -m "feat: agregar ejercicio de X"`
5. Abre un **Pull Request**

---

## 📝 Licencia

Distribuido bajo la licencia **MIT** — libre de usar, modificar y distribuir con fines educativos y comerciales.

---

<div align="center">

Hecho con 🐍 Python y ❤️ como material de aprendizaje de Tkinter

</div>
