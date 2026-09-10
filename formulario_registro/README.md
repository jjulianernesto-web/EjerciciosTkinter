# 📋 Formulario de Registro Multiopción

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![Sin dependencias](https://img.shields.io/badge/Dependencias-Ninguna-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Aplicación de escritorio con **Python + Tkinter** que demuestra el uso de múltiples tipos de widgets y variables de control para construir un formulario de registro completo.

---

## 🎯 Conceptos que demuestra

| Widget | Variable de control | Comportamiento |
|---|---|---|
| `Entry` | `StringVar` | Texto libre ingresado por el usuario |
| `Radiobutton` | `StringVar` | **Selección única** — solo una opción activa |
| `Checkbutton` | `BooleanVar` | **Selección múltiple** — varias opciones activas |
| `Checkbutton` (términos) | `IntVar` | Valor binario: `0` = no / `1` = sí |
| `ttk.Combobox` | `StringVar` | Menú desplegable con lista de opciones |
| `Frame` | — | Agrupación visual de secciones del formulario |

---

## 🗂️ Secciones del formulario

1. **👤 Datos personales** — `Entry` + `StringVar` (nombre, apellido, email)
2. **⚧ Género** — `Radiobutton` horizontal + `StringVar` (selección única)
3. **🌍 Ubicación** — `ttk.Combobox` + `StringVar` (país de residencia)
4. **🎓 Educación y experiencia** — `Combobox` + `Radiobutton` vertical
5. **💡 Áreas de interés** — `Checkbutton` grid + `BooleanVar` (selección múltiple)
6. **✅ Términos** — `Checkbutton` + `IntVar` (0 / 1)
7. **📄 Panel de resultados** — `Text` widget con todos los valores leídos

---

## 🚀 Ejecución

```bash
git clone https://github.com/jjulianernesto-web/formulario_registro.git
cd formulario_registro
python main.py
```

> ✅ No se requieren librerías externas. Tkinter viene incluido con Python.

---

## 🔍 Cómo se leen las variables de control

```python
# StringVar — texto y Radiobutton
nombre  = var_nombre.get()      # "Juan"
genero  = var_genero.get()      # "M" | "F" | "NB" | "ND"

# StringVar — Combobox
pais     = var_pais.get()       # "México"
educacion = var_educacion.get() # "Licenciatura / Ingeniería"

# BooleanVar — Checkbutton múltiple
activo = vars_intereses["web"].get()   # True o False

# IntVar — Checkbutton de términos
acepta = var_terminos.get()     # 0 o 1
```

---

## 📂 Estructura

```
formulario_registro/
├── main.py          # Aplicación completa
├── requirements.txt # Sin dependencias externas
├── .gitignore       # Exclusiones de Git
└── README.md        # Esta documentación
```

---

## 📦 Empaquetar como .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

---

## 📝 Licencia

MIT — libre de usar y modificar.
