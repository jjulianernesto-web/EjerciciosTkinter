# ⏱️ Reloj Digital y Cronómetro — Python + Tkinter

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![Sin dependencias](https://img.shields.io/badge/Dependencias-Ninguna-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Aplicación de reloj, cronómetro y temporizador desarrollada con **Python + Tkinter** que demuestra cómo actualizar la interfaz gráfica en **tiempo real** sin bloquear el programa, usando el método `.after()` en lugar de `time.sleep()`.

---

## 🎯 Concepto central: `.after()` vs `time.sleep()`

| ❌ `time.sleep()` | ✅ `.after(ms, funcion)` |
|---|---|
| **Congela** el hilo principal | **No bloquea** el hilo principal |
| La UI deja de responder | La UI sigue respondiendo |
| No se puede usar en Tkinter | Diseñado para loops de Tkinter |
| Bloqueante | No bloqueante |

---

## 🔄 Patrón recursivo con `.after()`

```python
def actualizar_reloj(self):
    # 1. Leer la hora del sistema
    ahora = datetime.now()

    # 2. Actualizar el Label grande
    self.lbl_hora.config(text=ahora.strftime("%H:%M:%S"))

    # 3. Reagendar la propia función en 1000 ms
    self.after(1000, self.actualizar_reloj)
    # ↑ Esta línea es la clave: llama a sí misma
    #   sin bloquear el hilo principal de Tkinter
```

---

## 🗂️ Pestañas de la aplicación

### 🕐 Reloj Digital
- Label con fuente `("Consolas", 72, "bold")` para la hora
- Actualización cada **1000 ms** con `.after(1000, fn)`
- Efecto de **dos puntos parpadeantes** cada 500 ms
- Formato **24h / 12h** intercambiable
- Muestra **fecha completa** y día de la semana
- Panel explicativo del patrón `.after()` con código

### ⏱️ Cronómetro
- Actualización cada **10 ms** con `.after(10, fn)` para centésimas
- Botones: ▶ Iniciar · ⏸ Pausar · ⚑ Vuelta · ↺ Reiniciar
- **Historial de vueltas** en Listbox con tiempo de lap y tiempo total
- Tiempo de vuelta actual en tiempo real

### ⏳ Temporizador
- Configuración con `Spinbox` (hh : mm : ss)
- **Presets rápidos**: 1, 5, 10, 25 min · 1 hora
- Barra de progreso `ttk.Progressbar`
- Cambia a **rojo** cuando quedan ≤ 10 segundos
- Alerta con `messagebox` al llegar a cero

---

## 🔍 Widgets y técnicas usadas

| Elemento | Descripción |
|---|---|
| `Label` con fuente grande | `("Consolas", 72, "bold")` — reloj principal |
| `.after(1000, fn)` | Actualiza el reloj sin bloquear |
| `.after(10, fn)` | Cronómetro en centésimas de segundo |
| `.after_cancel(job)` | Cancela un `.after()` activo |
| `datetime.now()` | Lee la hora del sistema |
| `time.perf_counter()` | Medición precisa para cronómetro |
| `Spinbox` | Entrada de horas, minutos, segundos |
| `ttk.Progressbar` | Barra de progreso del temporizador |
| `Listbox` | Historial de vueltas del cronómetro |

---

## 🚀 Ejecución

```bash
git clone https://github.com/tu-usuario/reloj_cronometro.git
cd reloj_cronometro
python main.py
```

> ✅ Sin dependencias externas. Solo Python estándar.

---

## 📂 Estructura

```
reloj_cronometro/
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
