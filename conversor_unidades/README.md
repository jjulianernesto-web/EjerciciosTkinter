# 🔄 Conversor de Unidades

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Sin dependencias](https://img.shields.io/badge/Dependencias-Ninguna-brightgreen)

Aplicación de escritorio para convertir unidades, desarrollada con **Python + Tkinter**.  
Incluye **8 categorías** de conversión con diseño oscuro moderno y conversión en tiempo real.

---

## 📸 Características

| Categoría | Unidades incluidas |
|---|---|
| 🌡️ Temperatura | Celsius, Fahrenheit, Kelvin, Rankine |
| 📏 Longitud | Metro, Km, cm, mm, Pulgada, Pie, Yarda, Milla… |
| ⚖️ Masa | Kg, g, mg, Tonelada, Libra, Onza, Piedra |
| 🧴 Volumen | Litro, mL, Galón, Cuarto, Pinta, Taza… |
| 💨 Velocidad | m/s, km/h, mph, Nudo, Mach |
| ⏱️ Tiempo | Segundos, Minutos, Horas, Días, Semanas, Años… |
| 📐 Área | m², km², Hectárea, Acre, Pie², Milla²… |
| ⚡ Energía | Julio, kJ, Caloría, kcal, kWh, BTU… |

### ✨ Funciones destacadas
- ⚡ **Conversión en tiempo real** mientras escribes
- 🔄 **Botón de intercambio** (⇄) entre unidades
- 📊 **Tabla de referencia rápida** por categoría
- 🎨 **Diseño oscuro moderno** con colores personalizados
- 🚫 **Sin dependencias externas** — solo Python estándar

---

## 🚀 Instalación y uso

### Requisitos
- Python 3.8 o superior
- Tkinter (incluido por defecto en todas las instalaciones de Python)

### Clonar y ejecutar

```bash
git clone https://github.com/tu-usuario/conversor_unidades.git
cd conversor_unidades
python main.py
```

> ✅ No necesitas instalar nada más. Tkinter viene incluido con Python.

---

## 📂 Estructura del proyecto

```
conversor_unidades/
│
├── main.py            # Aplicación completa (UI + lógica de conversión)
├── requirements.txt   # Nota sobre dependencias (ninguna)
├── .gitignore         # Archivos ignorados por Git
└── README.md          # Esta documentación
```

---

## 🧩 Uso como módulo (solo lógica)

Puedes importar las funciones de conversión en otros scripts:

```python
from main import convert, format_result

# Celsius a Fahrenheit
resultado = convert("🌡️  Temperatura", 100, "Celsius", "Fahrenheit")
print(format_result(resultado))  # → "212"

# Kilómetros a Millas
resultado = convert("📏  Longitud", 10, "Kilómetro", "Milla")
print(format_result(resultado))  # → "6.21371"

# Kilogramos a Libras
resultado = convert("⚖️  Masa", 75, "Kilogramo", "Libra")
print(format_result(resultado))  # → "165.347"
```

---

## 📦 Empaquetar como ejecutable (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# El ejecutable se genera en dist/main.exe
```

---

## 🤝 Contribuir

1. Haz un **fork** del repositorio
2. Crea tu rama: `git checkout -b feature/nueva-categoria`
3. Añade tus cambios en `CATEGORIES` dentro de `main.py`
4. Commit: `git commit -m "feat: agregar conversión de Presión"`
5. Push y abre un **Pull Request**

---

## 📝 Licencia

MIT License — libre de usar, modificar y distribuir.

---

## 👤 Autor

**Tu Nombre**  
GitHub: [@tu-usuario](https://github.com/tu-usuario)
