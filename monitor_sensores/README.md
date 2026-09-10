# 📊 Monitor de Sensores (Simulado) — Python + Tkinter

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![Sin dependencias](https://img.shields.io/badge/Dependencias-Ninguna-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Dashboard de monitoreo de sensores simulado con **Python + Tkinter** que demuestra cómo vincular **`Scale`** (deslizadores) con **`ttk.Progressbar`** mediante **`DoubleVar`**, cambiando indicadores de estado según umbrales numéricos.

---

## 🎯 Conceptos que demuestra

| Elemento | Descripción |
|---|---|
| `Scale` | Deslizador numérico que el usuario controla |
| `DoubleVar` | Variable de control que conecta `Scale` ↔ `Progressbar` |
| `ttk.Progressbar` | Barra de estado que refleja el valor del `Scale` |
| `command=fn` | Callback del `Scale`: se ejecuta en cada movimiento |
| Indicador de estado | Label que cambia entre **Normal / Advertencia / Crítico** |
| Color dinámico | Progressbar cambia de 🟢 verde → 🟡 amarillo → 🔴 rojo |
| `.after(500, fn)` | Simulación automática sin bloquear la UI |
| `Canvas` | Mini-gráfico histórico de cada sensor |

---

## 🔍 Lógica central

```python
# DoubleVar conecta el Scale con la Progressbar
self.var_valor = tk.DoubleVar(value=42.0)

# Scale lee/escribe la DoubleVar y llama al callback
Scale(parent,
      variable=self.var_valor,    # ← DoubleVar compartida
      from_=0, to=120,
      command=self._on_scale)     # ← se ejecuta en cada movimiento

# Callback: actualiza Progressbar e indicador de estado
def _on_scale(self, valor_str):
    valor = float(valor_str)
    pct   = ((valor - MIN) / (MAX - MIN)) * 100

    self.progressbar["value"] = pct          # Progressbar

    if pct >= UMBRAL_CRITICO:
        self.lbl_estado.config(text="■ Critico",     fg="red")
    elif pct >= UMBRAL_ADVERTENCIA:
        self.lbl_estado.config(text="▲ Advertencia", fg="yellow")
    else:
        self.lbl_estado.config(text="● Normal",      fg="green")
```

---

## 🌡️ Sensores incluidos

| Sensor | Rango | Advertencia | Crítico |
|---|---|---|---|
| 🌡️ Temperatura | 0 – 120 °C | 60% (72°C) | 85% (102°C) |
| 💧 Humedad | 0 – 100 % | 75% | 90% |
| 💻 CPU | 0 – 100 % | 70% | 90% |
| 🔧 Presión | 0 – 200 PSI | 65% | 85% |
| ⚡ Voltaje | 0 – 15 V | 80% | 93% |
| ⚙️ RPM Motor | 0 – 8000 rpm | 70% | 88% |

---

## ✨ Características

- 🎛️ **6 sensores** con `Scale` manual individual
- 📊 **Progressbar** que refleja el valor del slider en tiempo real
- 🟢🟡🔴 **Color dinámico** que cambia según umbrales configurados
- 📈 **Mini-gráfico Canvas** con historial de 60 puntos por sensor
- ▶️ **Simulación automática** con `.after(500)` y ondas sinusoidales + ruido
- 📋 **Log de alertas** con timestamp y colores por nivel de severidad
- ✅ **Resumen global** del estado del sistema
- 🔒 Sliders se deshabilitan durante la simulación automática

---

## 🚀 Ejecución

```bash
git clone https://github.com/jjulianernesto-web/monitor_sensores.git
cd monitor_sensores
python main.py
```

---

## 📂 Estructura

```
monitor_sensores/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📝 Licencia

MIT — libre de usar y modificar.
