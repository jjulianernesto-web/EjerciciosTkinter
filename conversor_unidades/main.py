"""
╔══════════════════════════════════════════════════════╗
║   🔄  Conversor de Unidades — Python + Tkinter       ║
║   Categorías: Temperatura, Longitud, Masa,           ║
║               Volumen, Velocidad, Tiempo, Área       ║
╚══════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable


# ──────────────────────────────────────────────────────
#  PALETA DE COLORES
# ──────────────────────────────────────────────────────
COLORS = {
    "bg":        "#0d0f14",
    "surface":   "#161b26",
    "card":      "#1e2535",
    "border":    "#2a3147",
    "accent":    "#7c6fff",
    "accent2":   "#43d9ad",
    "accent3":   "#ff6b9d",
    "text":      "#e6eaf4",
    "muted":     "#7a8399",
    "white":     "#ffffff",
    "entry_bg":  "#252d3d",
    "hover":     "#2e3a52",
}

FONT_TITLE   = ("Segoe UI", 22, "bold")
FONT_HEADING = ("Segoe UI", 13, "bold")
FONT_LABEL   = ("Segoe UI", 10)
FONT_ENTRY   = ("Segoe UI", 18, "bold")
FONT_UNIT    = ("Segoe UI", 10, "bold")
FONT_SMALL   = ("Segoe UI", 9)
FONT_RESULT  = ("Segoe UI", 13)


# ──────────────────────────────────────────────────────
#  DATOS DE CONVERSIÓN
#  Todas las conversiones tienen una unidad BASE.
#  factor = cuántas unidades_base hay en 1 unidad.
# ──────────────────────────────────────────────────────
CATEGORIES = {
    "🌡️  Temperatura": {
        "base": "Celsius",
        "units": ["Celsius", "Fahrenheit", "Kelvin", "Rankine"],
        # Temperatura no es lineal → manejada aparte
    },
    "📏  Longitud": {
        "base": "Metro",
        "units": ["Metro", "Kilómetro", "Centímetro", "Milímetro",
                  "Pulgada", "Pie", "Yarda", "Milla", "Milla náutica"],
        "factors": {
            "Metro":          1.0,
            "Kilómetro":      1_000.0,
            "Centímetro":     0.01,
            "Milímetro":      0.001,
            "Pulgada":        0.0254,
            "Pie":            0.3048,
            "Yarda":          0.9144,
            "Milla":          1_609.344,
            "Milla náutica":  1_852.0,
        },
    },
    "⚖️  Masa": {
        "base": "Kilogramo",
        "units": ["Kilogramo", "Gramo", "Miligramo", "Tonelada",
                  "Libra", "Onza", "Piedra"],
        "factors": {
            "Kilogramo":  1.0,
            "Gramo":      0.001,
            "Miligramo":  1e-6,
            "Tonelada":   1_000.0,
            "Libra":      0.453592,
            "Onza":       0.0283495,
            "Piedra":     6.35029,
        },
    },
    "🧴  Volumen": {
        "base": "Litro",
        "units": ["Litro", "Mililitro", "Centilitro", "Decilitro",
                  "Metro cúbico", "Galón (US)", "Cuarto (US)",
                  "Pinta (US)", "Taza (US)", "Onza líquida (US)"],
        "factors": {
            "Litro":              1.0,
            "Mililitro":          0.001,
            "Centilitro":         0.01,
            "Decilitro":          0.1,
            "Metro cúbico":       1_000.0,
            "Galón (US)":         3.78541,
            "Cuarto (US)":        0.946353,
            "Pinta (US)":         0.473176,
            "Taza (US)":          0.236588,
            "Onza líquida (US)":  0.0295735,
        },
    },
    "💨  Velocidad": {
        "base": "m/s",
        "units": ["m/s", "km/h", "mph", "Nudo", "pie/s", "Mach"],
        "factors": {
            "m/s":    1.0,
            "km/h":   1 / 3.6,
            "mph":    0.44704,
            "Nudo":   0.514444,
            "pie/s":  0.3048,
            "Mach":   340.29,
        },
    },
    "⏱️  Tiempo": {
        "base": "Segundo",
        "units": ["Segundo", "Minuto", "Hora", "Día", "Semana",
                  "Mes (30d)", "Año (365d)", "Milisegundo", "Microsegundo"],
        "factors": {
            "Segundo":     1.0,
            "Minuto":      60.0,
            "Hora":        3_600.0,
            "Día":         86_400.0,
            "Semana":      604_800.0,
            "Mes (30d)":   2_592_000.0,
            "Año (365d)":  31_536_000.0,
            "Milisegundo": 0.001,
            "Microsegundo":1e-6,
        },
    },
    "📐  Área": {
        "base": "Metro²",
        "units": ["Metro²", "Kilómetro²", "Centímetro²", "Milímetro²",
                  "Hectárea", "Acre", "Pie²", "Pulgada²", "Yarda²", "Milla²"],
        "factors": {
            "Metro²":       1.0,
            "Kilómetro²":   1e6,
            "Centímetro²":  1e-4,
            "Milímetro²":   1e-6,
            "Hectárea":     10_000.0,
            "Acre":         4_046.86,
            "Pie²":         0.092903,
            "Pulgada²":     0.00064516,
            "Yarda²":       0.836127,
            "Milla²":       2_589_988.11,
        },
    },
    "⚡  Energía": {
        "base": "Julio",
        "units": ["Julio", "Kilojulio", "Caloría", "Kilocaloría",
                  "Watt·hora", "kWh", "BTU", "Electrón·volt"],
        "factors": {
            "Julio":        1.0,
            "Kilojulio":    1_000.0,
            "Caloría":      4.184,
            "Kilocaloría":  4_184.0,
            "Watt·hora":    3_600.0,
            "kWh":          3_600_000.0,
            "BTU":          1_055.06,
            "Electrón·volt":1.60218e-19,
        },
    },
}


# ──────────────────────────────────────────────────────
#  LÓGICA DE CONVERSIÓN
# ──────────────────────────────────────────────────────

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convierte temperatura (no lineal, requiere manejo especial)."""
    # Primero convertir a Celsius
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    elif from_unit == "Rankine":
        celsius = (value - 491.67) * 5 / 9
    else:
        raise ValueError(f"Unidad desconocida: {from_unit}")

    # Luego convertir de Celsius a la unidad destino
    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return celsius * 9 / 5 + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    elif to_unit == "Rankine":
        return (celsius + 273.15) * 9 / 5
    else:
        raise ValueError(f"Unidad desconocida: {to_unit}")


def convert_linear(value: float, from_unit: str, to_unit: str, factors: dict) -> float:
    """Conversión lineal mediante unidad base."""
    base_value = value * factors[from_unit]
    return base_value / factors[to_unit]


def convert(category: str, value: float, from_unit: str, to_unit: str) -> float:
    """Función principal de conversión."""
    if from_unit == to_unit:
        return value
    if "Temperatura" in category:
        return convert_temperature(value, from_unit, to_unit)
    factors = CATEGORIES[category]["factors"]
    return convert_linear(value, from_unit, to_unit, factors)


def format_result(value: float) -> str:
    """Formatea el resultado eliminando ceros innecesarios."""
    if abs(value) >= 1e12 or (abs(value) < 1e-6 and value != 0):
        return f"{value:.6e}"
    if value == int(value) and abs(value) < 1e9:
        return f"{int(value):,}"
    return f"{value:,.8f}".rstrip("0").rstrip(".")


# ──────────────────────────────────────────────────────
#  APLICACIÓN PRINCIPAL
# ──────────────────────────────────────────────────────

class ConversorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversor de Unidades")
        self.geometry("680x620")
        self.minsize(600, 560)
        self.configure(bg=COLORS["bg"])
        self.resizable(True, True)

        # Estado
        self.current_category = tk.StringVar(value=list(CATEGORIES.keys())[0])
        self.from_unit = tk.StringVar()
        self.to_unit   = tk.StringVar()
        self.input_var = tk.StringVar()
        self.result_var = tk.StringVar(value="—")
        self.formula_var = tk.StringVar()

        self._build_ui()
        self._on_category_change()

        # Escuchar cambios en el campo de entrada
        self.input_var.trace_add("write", self._on_value_change)
        self.from_unit.trace_add("write", self._on_value_change)
        self.to_unit.trace_add("write",   self._on_value_change)

    # ── Construcción de la UI ──────────────────────────

    def _build_ui(self):
        # ── Header ──
        header = tk.Frame(self, bg=COLORS["surface"], pady=16)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🔄 Conversor de Unidades",
            font=FONT_TITLE,
            bg=COLORS["surface"],
            fg=COLORS["accent"],
        ).pack()
        tk.Label(
            header,
            text="Temperatura · Longitud · Masa · Volumen · Velocidad · Tiempo · Área · Energía",
            font=FONT_SMALL,
            bg=COLORS["surface"],
            fg=COLORS["muted"],
        ).pack(pady=(2, 0))

        # ── Selector de categoría ──
        cat_frame = tk.Frame(self, bg=COLORS["bg"], pady=14)
        cat_frame.pack(fill="x", padx=24)

        tk.Label(
            cat_frame,
            text="Categoría",
            font=FONT_LABEL,
            bg=COLORS["bg"],
            fg=COLORS["muted"],
        ).pack(anchor="w")

        self._style_combobox()
        self.cat_combo = ttk.Combobox(
            cat_frame,
            textvariable=self.current_category,
            values=list(CATEGORIES.keys()),
            state="readonly",
            style="Custom.TCombobox",
            font=FONT_HEADING,
        )
        self.cat_combo.pack(fill="x", pady=(4, 0))
        self.cat_combo.bind("<<ComboboxSelected>>", lambda _: self._on_category_change())

        # ── Tarjeta de conversión ──
        card = tk.Frame(self, bg=COLORS["card"], padx=24, pady=22,
                        relief="flat", bd=0)
        card.pack(fill="x", padx=24, pady=(0, 8))
        self._build_conversion_card(card)

        # ── Resultado ──
        self._build_result_section()

        # ── Tabla de referencia rápida ──
        self._build_quick_table()

        # ── Footer ──
        tk.Label(
            self,
            text="Python + Tkinter  ·  Conversor de Unidades  ·  MIT License",
            font=FONT_SMALL,
            bg=COLORS["bg"],
            fg=COLORS["muted"],
        ).pack(side="bottom", pady=8)

    def _build_conversion_card(self, parent):
        # Fila superior: unidades
        units_row = tk.Frame(parent, bg=COLORS["card"])
        units_row.pack(fill="x")

        # ── FROM ──
        left = tk.Frame(units_row, bg=COLORS["card"])
        left.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="De", font=FONT_LABEL,
                 bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w")
        self.from_combo = ttk.Combobox(
            left, textvariable=self.from_unit,
            state="readonly", style="Custom.TCombobox", font=FONT_UNIT,
        )
        self.from_combo.pack(fill="x", pady=(4, 0))

        # ── SWAP button ──
        mid = tk.Frame(units_row, bg=COLORS["card"], padx=10)
        mid.pack(side="left")
        tk.Button(
            mid,
            text="⇄",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS["accent"],
            fg=COLORS["white"],
            activebackground=COLORS["hover"],
            activeforeground=COLORS["white"],
            relief="flat",
            cursor="hand2",
            width=3,
            command=self._swap_units,
        ).pack(pady=(18, 0))

        # ── TO ──
        right = tk.Frame(units_row, bg=COLORS["card"])
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="A", font=FONT_LABEL,
                 bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w")
        self.to_combo = ttk.Combobox(
            right, textvariable=self.to_unit,
            state="readonly", style="Custom.TCombobox", font=FONT_UNIT,
        )
        self.to_combo.pack(fill="x", pady=(4, 0))

        # ── Entry de valor ──
        entry_frame = tk.Frame(parent, bg=COLORS["card"], pady=16)
        entry_frame.pack(fill="x")

        tk.Label(entry_frame, text="Valor a convertir",
                 font=FONT_LABEL, bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w")

        entry_container = tk.Frame(entry_frame, bg=COLORS["entry_bg"],
                                   padx=14, pady=6)
        entry_container.pack(fill="x", pady=(4, 0))

        self.entry = tk.Entry(
            entry_container,
            textvariable=self.input_var,
            font=FONT_ENTRY,
            bg=COLORS["entry_bg"],
            fg=COLORS["white"],
            insertbackground=COLORS["accent"],
            relief="flat",
            bd=0,
        )
        self.entry.pack(fill="x")
        self.entry.focus_set()

        # Botón limpiar
        btn_row = tk.Frame(parent, bg=COLORS["card"])
        btn_row.pack(fill="x")
        tk.Button(
            btn_row,
            text="🗑  Limpiar",
            font=FONT_SMALL,
            bg=COLORS["border"],
            fg=COLORS["muted"],
            activebackground=COLORS["hover"],
            activeforeground=COLORS["text"],
            relief="flat",
            cursor="hand2",
            pady=4,
            command=self._clear,
        ).pack(side="right")

    def _build_result_section(self):
        res_frame = tk.Frame(self, bg=COLORS["surface"], padx=24, pady=16)
        res_frame.pack(fill="x", padx=24, pady=(0, 8))

        tk.Label(
            res_frame,
            text="Resultado",
            font=FONT_LABEL,
            bg=COLORS["surface"],
            fg=COLORS["muted"],
        ).pack(anchor="w")

        self.result_label = tk.Label(
            res_frame,
            textvariable=self.result_var,
            font=("Segoe UI", 28, "bold"),
            bg=COLORS["surface"],
            fg=COLORS["accent2"],
        )
        self.result_label.pack(anchor="w", pady=(4, 0))

        self.formula_label = tk.Label(
            res_frame,
            textvariable=self.formula_var,
            font=FONT_RESULT,
            bg=COLORS["surface"],
            fg=COLORS["muted"],
        )
        self.formula_label.pack(anchor="w")

    def _build_quick_table(self):
        """Tabla con conversiones comunes de la categoría activa."""
        outer = tk.Frame(self, bg=COLORS["bg"], padx=24)
        outer.pack(fill="both", expand=True)

        tk.Label(
            outer,
            text="Referencias rápidas",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["muted"],
        ).pack(anchor="w", pady=(0, 6))

        self.table_frame = tk.Frame(outer, bg=COLORS["bg"])
        self.table_frame.pack(fill="both", expand=True)

    def _style_combobox(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Custom.TCombobox",
            fieldbackground=COLORS["entry_bg"],
            background=COLORS["entry_bg"],
            foreground=COLORS["text"],
            selectbackground=COLORS["accent"],
            selectforeground=COLORS["white"],
            arrowcolor=COLORS["accent"],
            bordercolor=COLORS["border"],
            darkcolor=COLORS["border"],
            lightcolor=COLORS["border"],
            padding=6,
        )
        style.map(
            "Custom.TCombobox",
            fieldbackground=[("readonly", COLORS["entry_bg"])],
            foreground=[("readonly", COLORS["text"])],
        )

    # ── Lógica de eventos ──────────────────────────────

    def _on_category_change(self):
        cat = self.current_category.get()
        units = CATEGORIES[cat]["units"]

        self.from_combo["values"] = units
        self.to_combo["values"]   = units

        self.from_unit.set(units[0])
        self.to_unit.set(units[1] if len(units) > 1 else units[0])

        self._update_result()
        self._update_quick_table()

    def _on_value_change(self, *_):
        self._update_result()

    def _update_result(self):
        raw = self.input_var.get().strip().replace(",", ".")
        from_u = self.from_unit.get()
        to_u   = self.to_unit.get()
        cat    = self.current_category.get()

        if not raw:
            self.result_var.set("—")
            self.formula_var.set("")
            return

        try:
            value = float(raw)
        except ValueError:
            self.result_var.set("⚠ Valor inválido")
            self.formula_var.set("")
            self.result_label.config(fg=COLORS["accent3"])
            return

        try:
            result = convert(cat, value, from_u, to_u)
            formatted = format_result(result)
            self.result_var.set(f"{formatted} {to_u}")
            self.formula_var.set(f"{format_result(value)} {from_u}  =  {formatted} {to_u}")
            self.result_label.config(fg=COLORS["accent2"])
        except Exception as e:
            self.result_var.set("⚠ Error")
            self.formula_var.set(str(e))
            self.result_label.config(fg=COLORS["accent3"])

    def _update_quick_table(self):
        """Actualiza la tabla de referencia rápida."""
        for w in self.table_frame.winfo_children():
            w.destroy()

        cat  = self.current_category.get()
        data = CATEGORIES[cat]
        units = data["units"]

        # Mostrar 6 conversiones de referencia (1 unidad base → otras)
        base_unit = units[0]
        refs = [(1, base_unit, u) for u in units[1:7]]

        cols = 3
        for i, (val, from_u, to_u) in enumerate(refs):
            try:
                result = convert(cat, val, from_u, to_u)
                text = f"1 {from_u} = {format_result(result)} {to_u}"
            except Exception:
                continue

            row, col = divmod(i, cols)
            cell = tk.Label(
                self.table_frame,
                text=text,
                font=FONT_SMALL,
                bg=COLORS["card"],
                fg=COLORS["muted"],
                padx=8,
                pady=4,
                anchor="w",
                relief="flat",
            )
            cell.grid(row=row, column=col, padx=3, pady=2, sticky="ew")

        for c in range(cols):
            self.table_frame.columnconfigure(c, weight=1)

    def _swap_units(self):
        a = self.from_unit.get()
        b = self.to_unit.get()
        self.from_unit.set(b)
        self.to_unit.set(a)
        self._update_result()

    def _clear(self):
        self.input_var.set("")
        self.result_var.set("—")
        self.formula_var.set("")
        self.entry.focus_set()


# ──────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    app = ConversorApp()
    app.mainloop()
