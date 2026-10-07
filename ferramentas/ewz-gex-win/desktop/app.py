from __future__ import annotations
import csv
import json
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from barchart_client import BARCHART_URL, BarchartBrowserClient
from gex_core import LEVEL_SPECS, contracts_from_records, derive_levels, format_export_block

APP_TITLE = "EWZ GEX → WIN Desktop"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("980x720")
        self.minsize(860, 620)
        self.snapshot = None
        self.level_vars: dict[str, tk.StringVar] = {}
        self.visible_browser = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Pronto. Clique em Atualizar Barchart.")
        self.source_var = tk.StringVar(value=BARCHART_URL)
        self.spot_var = tk.StringVar(value="—")
        self.exp_var = tk.StringVar(value="—")
        self._build_ui()

    def _build_ui(self):
        style = ttk.Style(self)
        try:
            style.theme_use("vista")
        except tk.TclError:
            pass

        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)
        ttk.Label(root, text=APP_TITLE, font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            root,
            text="Extrai a estrutura de opções do EWZ, organiza níveis GEX e gera um bloco para o indicador do TradingView.",
            wraplength=900,
        ).pack(anchor="w", pady=(2, 12))

        controls = ttk.Frame(root)
        controls.pack(fill="x", pady=(0, 12))
        self.fetch_btn = ttk.Button(controls, text="Atualizar Barchart", command=self.fetch)
        self.fetch_btn.pack(side="left")
        ttk.Checkbutton(
            controls,
            text="Mostrar Edge durante a coleta",
            variable=self.visible_browser,
        ).pack(side="left", padx=12)
        ttk.Button(controls, text="Importar JSON", command=self.import_json).pack(side="left")
        ttk.Button(controls, text="Exportar CSV", command=self.export_csv).pack(side="left", padx=(8, 0))

        info = ttk.LabelFrame(root, text="Snapshot", padding=10)
        info.pack(fill="x")
        for col, (label, var) in enumerate(
            (("Spot EWZ", self.spot_var), ("Vencimentos", self.exp_var), ("Fonte", self.source_var))
        ):
            ttk.Label(info, text=label, font=("Segoe UI", 9, "bold")).grid(
                row=0, column=col, sticky="w", padx=(0, 18)
            )
            ttk.Label(info, textvariable=var, wraplength=430 if col == 2 else 220).grid(
                row=1, column=col, sticky="w", padx=(0, 18)
            )
        info.columnconfigure(2, weight=1)

        table = ttk.LabelFrame(root, text="Níveis — você pode revisar/editar antes de copiar", padding=10)
        table.pack(fill="both", expand=True, pady=12)
        headers = ["Nível", "EWZ", "Origem", "Confiança", "Observação"]
        for c, h in enumerate(headers):
            ttk.Label(table, text=h, font=("Segoe UI", 9, "bold")).grid(
                row=0, column=c, sticky="w", padx=4, pady=4
            )

        for r, (key, label) in enumerate(LEVEL_SPECS, start=1):
            ttk.Label(table, text=label).grid(row=r, column=0, sticky="w", padx=4, pady=4)
            var = tk.StringVar(value="")
            self.level_vars[key] = var
            ttk.Entry(table, textvariable=var, width=12).grid(
                row=r, column=1, sticky="w", padx=4, pady=4
            )
            ttk.Label(table, text="—", name=f"origin_{key}").grid(
                row=r, column=2, sticky="w", padx=4, pady=4
            )
            ttk.Label(table, text="—", name=f"confidence_{key}").grid(
                row=r, column=3, sticky="w", padx=4, pady=4
            )
            ttk.Label(table, text="—", wraplength=390, name=f"note_{key}").grid(
                row=r, column=4, sticky="w", padx=4, pady=4
            )
        table.columnconfigure(4, weight=1)

        out = ttk.LabelFrame(root, text="Bloco para TradingView", padding=10)
        out.pack(fill="x")
        self.output = tk.Text(out, height=3, wrap="word", font=("Consolas", 9))
        self.output.pack(fill="x")
        actions = ttk.Frame(out)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Gerar bloco", command=self.refresh_output).pack(side="left")
        ttk.Button(actions, text="Copiar bloco", command=self.copy_output).pack(side="left", padx=8)
        ttk.Label(
            actions,
            text="Cole o bloco em 'Bloco do aplicativo' no indicador Pine.",
        ).pack(side="left", padx=8)

        ttk.Label(root, textvariable=self.status_var, foreground="#555").pack(
            anchor="w", pady=(10, 0)
        )

    def set_busy(self, busy: bool, text: str | None = None):
        self.fetch_btn.configure(state="disabled" if busy else "normal")
        if text:
            self.status_var.set(text)

    def fetch(self):
        self.set_busy(True, "Abrindo o Barchart e capturando dados…")
        visible = bool(self.visible_browser.get())
        threading.Thread(
            target=self._fetch_worker,
            args=(visible,),
            daemon=True,
        ).start()

    def _fetch_worker(self, visible: bool):
        try:
            client = BarchartBrowserClient(visible=visible)
            records, official, meta = client.fetch()
            contracts = contracts_from_records(records, prefer_eod=True)
            snap = derive_levels(
                contracts,
                official,
                source_url=meta.get("page_url", BARCHART_URL),
            )
            self.after(0, lambda: self._apply_snapshot(snap, meta))
        except Exception as exc:
            self.after(0, lambda: self._error(str(exc)))

    def _error(self, msg):
        self.set_busy(False, "Falha na coleta.")
        messagebox.showerror(APP_TITLE, msg)

    def _levels_frame(self):
        root = self.winfo_children()[0]
        frames = [w for w in root.winfo_children() if isinstance(w, ttk.LabelFrame)]
        return next(f for f in frames if str(f.cget("text")).startswith("Níveis"))

    def _apply_snapshot(self, snap, meta=None):
        self.snapshot = snap
        self.spot_var.set(f"{snap.spot:.2f}")
        self.exp_var.set(
            ", ".join(snap.expirations[:5])
            + ("…" if len(snap.expirations) > 5 else "")
            or "—"
        )
        self.source_var.set((meta or {}).get("api_url") or snap.source_url)

        levels_frame = self._levels_frame()
        for lv in snap.levels:
            self.level_vars[lv.key].set(
                "" if lv.value is None else f"{lv.value:.4f}".rstrip("0").rstrip(".")
            )
            levels_frame.nametowidget(f"origin_{lv.key}").configure(text=lv.origin)
            levels_frame.nametowidget(f"confidence_{lv.key}").configure(text=lv.confidence)
            levels_frame.nametowidget(f"note_{lv.key}").configure(text=lv.note)

        self.refresh_output()
        warn = " | ".join(snap.warnings)
        if warn:
            self.set_busy(False, f"Coleta concluída: {len(snap.exposures)} strikes. {warn}")
        else:
            self.set_busy(False, f"Coleta concluída: {len(snap.exposures)} strikes.")

    def _overrides(self):
        vals = {}
        for key, var in self.level_vars.items():
            text = var.get().strip().replace(",", ".")
            if not text:
                vals[key] = None
            else:
                try:
                    vals[key] = float(text)
                except ValueError:
                    raise ValueError(f"Valor inválido em {key}: {text}")
        return vals

    def refresh_output(self):
        if not self.snapshot:
            self.output.delete("1.0", "end")
            self.output.insert("1.0", "Atualize ou importe dados primeiro.")
            return

        try:
            block = format_export_block(self.snapshot, self._overrides())
        except ValueError as exc:
            messagebox.showerror(APP_TITLE, str(exc))
            return

        self.output.delete("1.0", "end")
        self.output.insert("1.0", block)

    def copy_output(self):
        self.refresh_output()
        text = self.output.get("1.0", "end").strip()
        if not text or text.startswith("Atualize"):
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        self.status_var.set("Bloco copiado para a área de transferência.")

    def import_json(self):
        path = filedialog.askopenfilename(
            title="Importar resposta JSON",
            filetypes=[("JSON", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if not path:
            return

        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
            from barchart_client import _flatten_records

            records = _flatten_records(
                payload.get("data", payload) if isinstance(payload, dict) else payload
            )
            contracts = contracts_from_records(records, prefer_eod=True)
            snap = derive_levels(contracts, {}, source_url=str(path))
            self._apply_snapshot(snap, {"api_url": str(path)})
        except Exception as exc:
            self._error(str(exc))

    def export_csv(self):
        if not self.snapshot:
            messagebox.showinfo(APP_TITLE, "Atualize ou importe dados primeiro.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile="EWZ_GEX_snapshot.csv",
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(
                ["strike", "call_gex", "put_gex", "net_gex", "call_oi", "put_oi"]
            )
            for row in self.snapshot.exposures:
                writer.writerow(
                    [
                        row.strike,
                        row.call_gex,
                        row.put_gex,
                        row.net_gex,
                        row.call_oi,
                        row.put_oi,
                    ]
                )
        self.status_var.set(f"CSV salvo em {path}")

if __name__ == "__main__":
    App().mainloop()
