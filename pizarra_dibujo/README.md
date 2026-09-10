# 🎨 Mini Pizarra de Dibujo — Python + Tkinter

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![Sin dependencias](https://img.shields.io/badge/Dependencias-Ninguna-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Aplicación de dibujo 2D desarrollada con **Python + Tkinter** que demuestra cómo el widget **Canvas** renderiza gráficos y cómo el **sistema de binding de eventos** responde al ratón en tiempo real.

---

## 🎯 Conceptos que demuestra

| Concepto | Descripción |
|---|---|
| `Canvas` | Widget de dibujo 2D — superficie de renderizado |
| `<ButtonPress-1>` | Evento: usuario presiona el botón izquierdo |
| `<B1-Motion>` | Evento: usuario arrastra con el botón sostenido |
| `<ButtonRelease-1>` | Evento: usuario suelta el botón |
| `create_line()` | Traza líneas usando `event.x` / `event.y` |
| `create_oval()` | Dibuja círculos y puntos en el canvas |
| `create_rectangle()` | Dibuja rectángulos (borde o relleno) |
| `colorchooser` | Selector de color nativo del SO |
| `canvas.delete()` | Borra objetos por ID (base del deshacer) |

---

## 🖌️ Herramientas de dibujo

| Herramienta | Atajo | Método Canvas |
|---|---|---|
| ✏ Lápiz | `Ctrl+P` | `create_line()` continuo |
| 🖌 Pincel | `Ctrl+B` | `create_line()` grueso |
| ⬜ Borrador | `Ctrl+E` | `create_line()` con color fondo |
| ╱ Línea | `Ctrl+L` | `create_line()` de extremo a extremo |
| □ Rectángulo | `Ctrl+R` | `create_rectangle()` solo borde |
| ■ Rect. relleno | `Ctrl+F` | `create_rectangle()` + `fill` |
| ○ Óvalo | `Ctrl+V` | `create_oval()` solo borde |
| ● Oval relleno | `Ctrl+G` | `create_oval()` + `fill` |

---

## ⌨️ Atajos de teclado

| Atajo | Acción |
|---|---|
| `Ctrl+Z` | Deshacer última acción |
| `Ctrl+S` | Guardar imagen |
| `Supr` | Limpiar toda la pizarra |
| `]` | Aumentar grosor del trazo |
| `[` | Reducir grosor del trazo |

---

## 🔍 Lógica central del dibujo

```python
# Binding de eventos en el Canvas
canvas.bind("<ButtonPress-1>",   on_press)    # inicio del trazo
canvas.bind("<B1-Motion>",       on_drag)     # dibujo continuo
canvas.bind("<ButtonRelease-1>", on_release)  # fin del trazo

# Leer coordenadas del ratón
def on_drag(event):
    x = canvas.canvasx(event.x)  # coordenada X en el canvas
    y = canvas.canvasy(event.y)  # coordenada Y en el canvas

    # Trazar línea del punto anterior al actual
    canvas.create_line(x_ant, y_ant, x, y,
                       fill="black", width=4,
                       capstyle="round", smooth=True)

# Dibujar formas con coordenadas del ratón
canvas.create_oval(x0, y0, x1, y1, fill="red", outline="red")
canvas.create_rectangle(x0, y0, x1, y1, outline="blue", width=2)
canvas.create_line(x0, y0, x1, y1, fill="green", width=3)
```

---

## ✨ Características

- 🎨 **8 herramientas**: lápiz, pincel, borrador, línea, rectángulo, óvalo (con y sin relleno)
- 🎨 **Paleta de 16 colores** rápidos + selector nativo del SO
- 📏 **Control de grosor** 1–60 px con slider + atajos `[` `]`
- ↩️ **Deshacer** acción por acción (pila de objetos Canvas)
- 💾 **Guardar** como PostScript (o PNG si Pillow está instalado)
- 📊 Barra de estado: coordenadas X/Y, objetos en canvas, acciones
- 🖱️ Cursor cambia según la herramienta activa
- 💡 Tooltips en los botones de herramientas

---

## 🚀 Ejecución

```bash
git clone https://github.com/tu-usuario/pizarra_dibujo.git
cd pizarra_dibujo
python main.py
```

> ✅ Sin dependencias externas. Tkinter incluido con Python.
> 
> 💡 Instala `Pillow` para guardar como PNG: `pip install Pillow`

---

## 📂 Estructura

```
pizarra_dibujo/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📝 Licencia

MIT — libre de usar y modificar.

## 👤 Autor

**Tu Nombre** — GitHub: [@tu-usuario](https://github.com/tu-usuario)
