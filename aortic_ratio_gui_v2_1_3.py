#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aortic Root App (Bulbo & Giunzione SinuTubulare) - v2.1.4
Autori: Stella (ChatGPT) + Danilo Savioni, 2025

Modifiche v2.1.4:
- Aggiunto tasto "Crediti" che mostra una finestra con i crediti
- Mantiene le modifiche precedenti (UI compatta, bottoni centrati/colorati)

"""

import math
import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Aortic Root (Bulbo & GST) - Danilo Savioni 2025"
PADDING = 10

def parse_float(s: str):
    if s is None:
        return None
    s = s.strip().replace(",", ".")
    if not s:
        return None
    try:
        v = float(s)
        return v
    except Exception:
        return None

def bsa_mosteller(weight_kg: float, height_cm: float) -> float:
    return math.sqrt((weight_kg * height_cm) / 3600.0)

def years_from_dob(d: dt.date) -> float:
    today = dt.date.today()
    days = (today - d).days
    return days / 365.2425

def pick_age_band(age_years: float) -> str:
    if age_years < 18.0:
        return "<18 anni"
    elif age_years <= 40.0:
        return "18–40 anni"
    else:
        return ">40 anni"

def expected_diameter_bulb(bsa: float, band: str) -> float:
    if band == "<18 anni":
        return 1.02 + (0.98 * bsa)
    elif band == "18–40 anni":
        return 0.97 + (1.12 * bsa)
    else:  # >40 anni
        return 1.92 + (0.74 * bsa)

def expected_diameter_gst(bsa: float, band: str) -> float:
    if band == "<18 anni":
        return 0.87 + (0.80 * bsa)
    elif band == "18–40 anni":
        return 1.06 + (0.82 * bsa)
    else:  # >40 anni
        return 1.69 + (0.62 * bsa)

class Pill(ttk.Label):
    def __init__(self, master, text="", kind="neutral", **kwargs):
        super().__init__(master, text=text, anchor="center", **kwargs)
        self["padding"] = (10, 3)
        self["font"] = ("Segoe UI", 10, "bold")
        self.configure(style="PillNeutral.TLabel")
        self.set_kind(kind)

    def set_kind(self, kind: str):
        style_map = {
            "ok": "PillOK.TLabel",
            "warn": "PillWarn.TLabel",
            "bad": "PillBad.TLabel",
            "neutral": "PillNeutral.TLabel",
        }
        self.configure(style=style_map.get(kind, "PillNeutral.TLabel"))

class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=PADDING)
        self.master.title(APP_TITLE)
        self.master.minsize(960, 420)
        self._build_styles()
        self.grid(sticky="nsew")
        self._build_layout()

    def _build_styles(self):
        style = ttk.Style()
        try:
            if "clam" in style.theme_names():
                style.theme_use("clam")
        except Exception:
            pass

        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))

        style.configure("Title.TLabel", font=("Segoe UI Semibold", 16))

        style.configure("PillOK.TLabel", background="#e8f7ee", foreground="#1e7c43", borderwidth=1, relief="solid")
        style.configure("PillWarn.TLabel", background="#fff4e5", foreground="#a15c00", borderwidth=1, relief="solid")
        style.configure("PillBad.TLabel", background="#fdecea", foreground="#a12622", borderwidth=1, relief="solid")
        style.configure("PillNeutral.TLabel", background="#eef1f5", foreground="#2c3e50", borderwidth=1, relief="solid")

        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Card.TLabel", background="#ffffff")

        style.configure("Header.TFrame", background="#f8fafc")
        style.configure("Inputs.TFrame", background="#f8fafc")

    def _build_layout(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self, style="Header.TFrame", padding=(PADDING, PADDING))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Aortic Root – Bulbo & Giunzione SinuTubulare", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        self.info_pill = Pill(header, text="Inserisci i dati…", kind="neutral")
        self.info_pill.grid(row=0, column=1, sticky="e")

        content = ttk.Frame(self, padding=(PADDING, PADDING))
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=0)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        inputs = ttk.Frame(content, style="Inputs.TFrame", padding=(PADDING, PADDING-2))
        inputs.grid(row=0, column=0, sticky="nsw", padx=(0, 8))

        r = 0
        ttk.Label(inputs, text="Peso (kg):").grid(row=r, column=0, sticky="w", pady=(0, 2))
        self.var_weight = tk.StringVar()
        ttk.Entry(inputs, textvariable=self.var_weight, width=12).grid(row=r, column=1, sticky="ew"); r+=1

        ttk.Label(inputs, text="Altezza (cm):").grid(row=r, column=0, sticky="w", pady=(0, 2))
        self.var_height = tk.StringVar()
        ttk.Entry(inputs, textvariable=self.var_height, width=12).grid(row=r, column=1, sticky="ew"); r+=1

        ttk.Label(inputs, text="Data di nascita (gg/mm/aaaa):").grid(row=r, column=0, sticky="w", pady=(0, 2))
        self.var_dob = tk.StringVar()
        ttk.Entry(inputs, textvariable=self.var_dob, width=12).grid(row=r, column=1, sticky="ew"); r+=1

        ttk.Label(inputs, text="Diametro misurato Bulbo (cm):").grid(row=r, column=0, sticky="w", pady=(6, 2))
        self.var_bulb_meas = tk.StringVar()
        ttk.Entry(inputs, textvariable=self.var_bulb_meas, width=12).grid(row=r, column=1, sticky="ew"); r+=1

        ttk.Label(inputs, text="Diametro misurato GST (cm):").grid(row=r, column=0, sticky="w", pady=(0, 2))
        self.var_gst_meas = tk.StringVar()
        ttk.Entry(inputs, textvariable=self.var_gst_meas, width=12).grid(row=r, column=1, sticky="ew"); r+=1

        btns = ttk.Frame(inputs)
        btns.grid(row=r, column=0, columnspan=2, sticky="ew", pady=(10, 0)); r+=1
        for c in (0,1,2,3,4):
            btns.grid_columnconfigure(c, weight=1 if c in (0,4) else 0)

        calcola_btn = tk.Button(btns, text="Calcola", command=self.recompute, bg="#b9f7b9", activebackground="#a4eea4")
        reset_btn   = tk.Button(btns, text="Reset",   command=self.reset_fields, bg="#ffd6a5", activebackground="#ffcc8a")
        crediti_btn = tk.Button(btns, text="Crediti", command=self.show_crediti, bg="#d6e0ff", activebackground="#bccdff")

        calcola_btn.grid(row=0, column=1, padx=(0,6))
        reset_btn.grid(row=0, column=2, padx=6)
        crediti_btn.grid(row=0, column=3, padx=(6,0))

        ttk.Button(inputs, text="Copia risultati", command=self.copy_results).grid(row=r, column=0, columnspan=2, sticky="ew", pady=(8,0)); r+=1

        right = ttk.Frame(content, padding=(PADDING, 2))
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)

        self.summary = ttk.Label(right, text="BSA: – m² | Fascia età: –", style="Card.TLabel", anchor="w", justify="left")
        self.summary.grid(row=0, column=0, sticky="ew", pady=(0,6))

        self.tree = ttk.Treeview(
            right,
            columns=("site","expected","measured","ratio","devpct"),
            show="headings",
            height=5
        )
        self.tree.heading("site", text="Sito")
        self.tree.heading("expected", text="Misurazione attesa (cm)")
        self.tree.heading("measured", text="Misurato (cm)")
        self.tree.heading("ratio", text="Aortic Ratio")
        self.tree.heading("devpct", text="Δ%")
        self.tree.column("site", width=190, anchor="w")
        self.tree.column("expected", width=180, anchor="center")
        self.tree.column("measured", width=140, anchor="center")
        self.tree.column("ratio", width=110, anchor="center")
        self.tree.column("devpct", width=110, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew")
        right.rowconfigure(1, weight=1)

        self.footer = ttk.Label(right, text="", anchor="w", justify="left")
        self.footer.grid(row=2, column=0, sticky="ew", pady=(6,0))

    def show_crediti(self):
        messagebox.showinfo("Crediti",
            "Programmato con passione da Danilo Savioni e Stella IA\n"
            "In un piovoso pomeriggio di settembre del 2025."
        )

    def reset_fields(self):
        self.var_weight.set("")
        self.var_height.set("")
        self.var_dob.set("")
        self.var_bulb_meas.set("")
        self.var_gst_meas.set("")
        self.info_pill.configure(text="Inserisci i dati…")
        self.info_pill.set_kind("neutral")
        self.summary.configure(text="BSA: – m² | Fascia età: –")
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.footer.configure(text="")

    def copy_results(self):
        text = self.footer.cget("text")
        if not text:
            text = "Nessun risultato da copiare."
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo(APP_TITLE, "Risultati copiati negli appunti.")

    def _parse_dob(self, s: str):
        s = (s or "").strip()
        if not s:
            return None
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return dt.datetime.strptime(s, fmt).date()
            except Exception:
                pass
        return None

    def recompute(self):
        w = parse_float(self.var_weight.get())
        h = parse_float(self.var_height.get())
        dob = self._parse_dob(self.var_dob.get())

        if w is None or w <= 0 or h is None or h <= 0:
            self.info_pill.configure(text="Inserisci peso e altezza validi")
            self.info_pill.set_kind("neutral")
            return

        if dob is None:
            self.info_pill.configure(text="Inserisci una data di nascita valida")
            self.info_pill.set_kind("neutral")
            return

        age_y = years_from_dob(dob)
        band = pick_age_band(age_y)
        bsa = bsa_mosteller(w, h)

        exp_bulb = expected_diameter_bulb(bsa, band)
        exp_gst  = expected_diameter_gst(bsa, band)

        m_bulb = parse_float(self.var_bulb_meas.get())
        m_gst  = parse_float(self.var_gst_meas.get())

        ratio_bulb = (m_bulb / exp_bulb) if (m_bulb is not None and exp_bulb) else None
        ratio_gst  = (m_gst / exp_gst) if (m_gst is not None and exp_gst) else None

        dev_bulb = ((ratio_bulb - 1.0) * 100.0) if ratio_bulb is not None else None
        dev_gst  = ((ratio_gst  - 1.0) * 100.0) if ratio_gst  is not None else None

        self.summary.configure(text=f"BSA: {bsa:.3f} m² | Fascia età auto-selezionata: {band} (età: {age_y:.1f} anni)")

        for i in self.tree.get_children():
            self.tree.delete(i)

        def fmt(x, nd=2, suffix=""):
            return f"{x:.{nd}f}{suffix}" if x is not None else "—"

        self.tree.insert("", "end",
            values=(
                "Bulbo",
                fmt(exp_bulb, 2),
                fmt(m_bulb, 2),
                fmt(ratio_bulb, 3),
                fmt(dev_bulb, 1, "%")
            )
        )
        self.tree.insert("", "end",
            values=(
                "Giunzione SinuTubulare",
                fmt(exp_gst, 2),
                fmt(m_gst, 2),
                fmt(ratio_gst, 3),
                fmt(dev_gst, 1, "%")
            )
        )

        pill_txt = "Calcolo completato"
        pill_kind = "ok"
        if m_bulb is None and m_gst is None:
            pill_txt, pill_kind = "Inserisci i diametri misurati (cm)", "neutral"
        else:
            flags = []
            if ratio_bulb is not None:
                if ratio_bulb > 1.1:
                    flags.append("Bulbo > atteso")
                elif ratio_bulb < 0.9:
                    flags.append("Bulbo < atteso")
            if ratio_gst is not None:
                if ratio_gst > 1.1:
                    flags.append("GST > atteso")
                elif ratio_gst < 0.9:
                    flags.append("GST < atteso")
            if flags:
                pill_txt = " | ".join(flags)
                pill_kind = "warn"
        self.info_pill.configure(text=pill_txt); self.info_pill.set_kind(pill_kind)

        footer = (
            f"BSA: {bsa:.3f} m² | Fascia età: {band} | "
            f"Bulbo atteso: {exp_bulb:.2f} cm | "
            f"GST atteso: {exp_gst:.2f} cm"
        )
        if m_bulb is not None:
            footer += f" | Bulbo misurato: {m_bulb:.2f} cm (Ratio {ratio_bulb:.3f}, Δ% {dev_bulb:.1f}%)"
        if m_gst is not None:
            footer += f" | GST misurato: {m_gst:.2f} cm (Ratio {ratio_gst:.3f}, Δ% {dev_gst:.1f}%)"
        self.footer.configure(text=footer)

def main():
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
