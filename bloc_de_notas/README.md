# 📝 Bloc de Notas Básico — Python + Tkinter

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![Sin dependencias](https://img.shields.io/badge/Dependencias-Ninguna-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Bloc de notas de escritorio desarrollado con **Python + Tkinter** que demuestra la interacción con el sistema operativo para **leer y guardar archivos**, y la construcción de **barras de navegación** con menús.

---

## 🎯 Conceptos que demuestra

| Herramienta | Descripción |
|---|---|
| `Text` | Caja de texto multilínea con scroll y deshacer/rehacer |
| `Menu` | Barra superior con submenús: Archivo, Editar, Ver, Ayuda |
| `filedialog` | Ventanas nativas del SO para abrir y guardar rutas |
| `messagebox` | Diálogos emergentes de confirmación y error |
| `open()` / `read()` | Lectura de archivos con Python puro |
| `write()` | Escritura de archivos con Python puro |
| `Toplevel` | Ventana secundaria para Buscar y Reemplazar |

---

## 🗂️ Menú completo

### 📁 Archivo
| Opción | Atajo | Función |
|---|---|---|
| Nuevo | `Ctrl+N` | Crea documento vacío (confirma descarte) |
| Abrir... | `Ctrl+O` | `filedialog.askopenfilename()` + `open()` + `read()` |
| Guardar | `Ctrl+S` | `open()` + `write()` en la ruta actual |
| Guardar como... | `Ctrl+Shift+S` | `filedialog.asksaveasfilename()` + `write()` |
| Salir | `Alt+F4` | Confirma con `messagebox.askyesnocancel()` |

### ✏️ Editar
`Deshacer` · `Rehacer` · `Cortar` · `Copiar` · `Pegar` · `Seleccionar todo` · **Buscar y Reemplazar** (`Ctrl+H`)

### 👁️ Ver
`Aumentar fuente` · `Reducir fuente` · `Restablecer` · `Ajuste de línea` · **Cambiar tema oscuro/claro**

---

## ✨ Características

- 📄 Indicador `•` en el título cuando hay cambios sin guardar
- 📊 **Barra de estado**: línea, columna, conteo de palabras y caracteres
- 🔍 **Buscar y Reemplazar** con resaltado de coincidencias
- 🎨 **Dos temas**: oscuro (por defecto) y claro
- 🔤 **Zoom de fuente**: `Ctrl++` / `Ctrl+-` / `Ctrl+0`
- ↩️ **Deshacer / Rehacer** ilimitado
- 🌐 Soporte **UTF-8** (con fallback a latin-1)
- 📁 Abre `.txt`, `.py`, `.md`, `.html`, `.json` y más

---

## 🚀 Ejecución

```bash
git clone https://github.com/tu-usuario/bloc_de_notas.git
cd bloc_de_notas
python main.py
```

> ✅ No se requieren librerías externas.

---

## 🔍 Lógica central de archivos

```python
# LEER un archivo (open + read)
with open(ruta, "r", encoding="utf-8") as f:
    contenido = f.read()
texto_widget.insert("1.0", contenido)

# GUARDAR un archivo (open + write)
contenido = texto_widget.get("1.0", "end-1c")
with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

# VENTANA NATIVA para elegir ruta
ruta = filedialog.askopenfilename(filetypes=[("Texto", "*.txt")])
ruta = filedialog.asksaveasfilename(defaultextension=".txt")

# DIÁLOGO de confirmación
respuesta = messagebox.askyesnocancel("Título", "¿Guardar cambios?")
```

---

## 📂 Estructura

```
bloc_de_notas/
├── main.py          # Aplicación completa
├── requirements.txt # Sin dependencias externas
├── .gitignore
└── README.md
```

---

## 📝 Licencia

MIT — libre de usar y modificar.

## 👤 Autor

**Tu Nombre** — GitHub: [@tu-usuario](https://github.com/tu-usuario)
