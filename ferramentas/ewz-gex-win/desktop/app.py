from __future__ import annotations
import csv
import json
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from barchart_client import BARCHART_URL, BarchartBrowserClient
from gex_core import (
    LEVEL_SPECS,
    contracts_from_records,
    derive_levels,
    extract_market_prices,
    format_export_block,
    level_distance_pct,
)
from edge_profiles import list_edge_profiles

APP_TITLE = "EWZ GEX → WIN Desktop"
APP_VERSION = "0.2.0-alpha.1"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_TITLE} {APP_VERSION}")
        self.geometry("1120x830")
        self.minsize(980, 700)
        self.snapshot = None
        self.level_vars: dict[str, tk.StringVar] = {}
        self.visible_browser = tk.BooleanVar(value=True)
        self.use_edge_extensions = tk.BooleanVar(value=True)
        self.edge_profile_var = tk.StringVar(value="")
        self.edge_profile_map: dict[str, str] = {}
        self.edge_extension_status_var = tk.StringVar(value="Detectando perfis do Edge…")
        self.status_var = tk.StringVar(value="Pronto. Clique em Atualizar Barchart.")
        self.source_var = tk.StringVar(value=BARCHART_URL)
        self.spot_var = tk.StringVar(value="—")
        self.reference_close_var = tk.StringVar(value="—")
        self.exp_var = tk.StringVar(value="—")
        self._build_ui()
        self._reload_edge_profiles()

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
        controls.pack(fill="x", pady=(0, 10))
        self.fetch_btn = ttk.Button(controls, text="Atualizar Barchart", command=self.fetch)
        self.fetch_btn.pack(side="left")
        ttk.Checkbutton(
            controls,
            text="Mostrar Edge durante a coleta",
            variable=self.visible_browser,
        ).pack(side="left", padx=12)
        ttk.Button(controls, text="Importar JSON", command=self.import_json).pack(side="left")
        ttk.Button(controls, text="Exportar CSV", command=self.export_csv).pack(side="left", padx=(8, 0))
        ttk.Button(controls, text="Salvar JSON", command=self.save_snapshot_json).pack(side="left", padx=(8, 0))
        ttk.Button(controls, text="Sobre", command=self.show_about).pack(side="right")

        browser = ttk.LabelFrame(root, text="Edge e extensões", padding=10)
        browser.pack(fill="x", pady=(0, 10))
        ttk.Checkbutton(
            browser,
            text="Usar minhas extensões do Edge (recomendado para Cold Turkey)",
            variable=self.use_edge_extensions,
        ).grid(row=0, column=0, columnspan=3, sticky="w")

        ttk.Label(browser, text="Perfil do Edge:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.edge_profile_combo = ttk.Combobox(
            browser,
            textvariable=self.edge_profile_var,
            state="readonly",
            width=48,
        )
        self.edge_profile_combo.grid(row=1, column=1, sticky="ew", padx=(8, 8), pady=(8, 0))
        ttk.Button(
            browser,
            text="Detectar novamente",
            command=self._reload_edge_profiles,
        ).grid(row=1, column=2, sticky="e", pady=(8, 0))
        ttk.Label(
            browser,
            textvariable=self.edge_extension_status_var,
            foreground="#555",
        ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(6, 0))
        browser.columnconfigure(1, weight=1)

        info = ttk.LabelFrame(root, text="Snapshot", padding=10)
        info.pack(fill="x")
        for col, (label, var) in enumerate(
            (
                ("EWZ atual / pré-mercado", self.spot_var),
                ("Fechamento EWZ D-1 (referência)", self.reference_close_var),
                ("Vencimentos", self.exp_var),
                ("Fonte", self.source_var),
            )
        ):
            ttk.Label(info, text=label, font=("Segoe UI", 9, "bold")).grid(
                row=0, column=col, sticky="w", padx=(0, 18)
            )
            ttk.Label(info, textvariable=var, wraplength=430 if col == 2 else 220).grid(
                row=1, column=col, sticky="w", padx=(0, 18)
            )
        info.columnconfigure(3, weight=1)

        table = ttk.LabelFrame(root, text="Níveis — você pode revisar/editar antes de copiar", padding=10)
        table.pack(fill="both", expand=True, pady=12)
        headers = ["Nível", "EWZ", "Δ vs. fechamento D-1", "Origem", "Confiança", "Observação"]
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
            ttk.Label(table, text="—", name=f"pct_{key}").grid(
                row=r, column=2, sticky="w", padx=4, pady=4
            )
            ttk.Label(table, text="—", name=f"origin_{key}").grid(
                row=r, column=3, sticky="w", padx=4, pady=4
            )
            ttk.Label(table, text="—", name=f"confidence_{key}").grid(
                row=r, column=4, sticky="w", padx=4, pady=4
            )
            ttk.Label(table, text="—", wraplength=360, name=f"note_{key}").grid(
                row=r, column=5, sticky="w", padx=4, pady=4
            )
        table.columnconfigure(5, weight=1)

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
            text="No TradingView: Configurações do indicador → Aplicação desktop → Bloco EWZGEX1. NÃO cole no código Pine.",
        ).pack(side="left", padx=8)

        ttk.Label(root, textvariable=self.status_var, foreground="#555").pack(
            anchor="w", pady=(10, 0)
        )

    def set_busy(self, busy: bool, text: str | None = None):
        self.fetch_btn.configure(state="disabled" if busy else "normal")
        if text:
            self.status_var.set(text)

    def _reload_edge_profiles(self):
        try:
            profiles = list_edge_profiles()
        except Exception as exc:
            self.edge_profile_map = {}
            self.edge_profile_combo["values"] = []
            self.edge_extension_status_var.set(f"Não foi possível detectar perfis do Edge: {exc}")
            return

        self.edge_profile_map = {p.display_name: p.directory for p in profiles}
        labels = list(self.edge_profile_map.keys())
        self.edge_profile_combo["values"] = labels

        preferred = next((p for p in profiles if p.has_cold_turkey), None)
        if preferred is None and profiles:
            preferred = profiles[0]

        if preferred:
            self.edge_profile_var.set(preferred.display_name)
            if preferred.has_cold_turkey:
                self.edge_extension_status_var.set(
                    f"Cold Turkey detectado neste perfil. {preferred.extension_count} extensões serão copiadas para um perfil isolado da aplicação."
                )
            else:
                self.edge_extension_status_var.set(
                    f"{preferred.extension_count} extensões detectadas. Cold Turkey não foi localizado neste perfil; selecione outro perfil se necessário."
                )
        else:
            self.edge_profile_var.set("")
            self.edge_extension_status_var.set("Nenhum perfil do Edge com extensões foi encontrado.")

    def _selected_edge_profile_dir(self) -> str:
        label = self.edge_profile_var.get().strip()
        return self.edge_profile_map.get(label, "Default")


    def fetch(self):
        self.set_busy(True, "Preparando o Edge e capturando dados do Barchart…")
        visible = bool(self.visible_browser.get())
        use_extensions = bool(self.use_edge_extensions.get())
        profile_dir = self._selected_edge_profile_dir()
        threading.Thread(
            target=self._fetch_worker,
            args=(visible, use_extensions, profile_dir),
            daemon=True,
        ).start()

    def _fetch_worker(self, visible: bool, use_extensions: bool, profile_dir: str):
        try:
            client = BarchartBrowserClient(
                visible=visible,
                use_edge_extensions=use_extensions,
                edge_profile_dir=profile_dir,
            )
            records, official, meta = client.fetch()
            current_spot, reference_close = extract_market_prices(records)
            contracts = contracts_from_records(records, prefer_eod=True)
            snap = derive_levels(
                contracts,
                official,
                source_url=meta.get("page_url", BARCHART_URL),
                selection_spot=current_spot,
                reference_close=reference_close,
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
        self.reference_close_var.set(
            "—" if snap.reference_close is None else f"{snap.reference_close:.2f}"
        )
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
            pct = level_distance_pct(lv.value, snap.reference_close)
            levels_frame.nametowidget(f"pct_{lv.key}").configure(
                text="—" if pct is None else f"{pct * 100:+.2f}%"
            )
            levels_frame.nametowidget(f"origin_{lv.key}").configure(text=lv.origin)
            levels_frame.nametowidget(f"confidence_{lv.key}").configure(text=lv.confidence)
            levels_frame.nametowidget(f"note_{lv.key}").configure(text=lv.note)

        self.refresh_output()
        warn = " | ".join(snap.warnings)
        profile_meta = (meta or {}).get("edge_profile") or {}
        profile_note = ""
        if profile_meta:
            cold = "Cold Turkey ✓" if profile_meta.get("cold_turkey") else "Cold Turkey não detectado"
            profile_note = f" Perfil Edge: {profile_meta.get('source_profile', '—')} · {profile_meta.get('extension_count', 0)} extensões · {cold}."
        if warn:
            self.set_busy(False, f"Coleta concluída: {len(snap.exposures)} strikes.{profile_note} {warn}")
        else:
            self.set_busy(False, f"Coleta concluída: {len(snap.exposures)} strikes.{profile_note}")

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
        self.status_var.set("Bloco copiado. No TradingView, cole em Configurações do indicador → Bloco EWZGEX1; não cole no código Pine.")

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
            current_spot, reference_close = extract_market_prices(records)
            contracts = contracts_from_records(records, prefer_eod=True)
            snap = derive_levels(
                contracts,
                {},
                source_url=str(path),
                selection_spot=current_spot,
                reference_close=reference_close,
            )
            self._apply_snapshot(snap, {"api_url": str(path)})
        except Exception as exc:
            self._error(str(exc))


    def save_snapshot_json(self):
        if not self.snapshot:
            messagebox.showinfo(APP_TITLE, "Atualize ou importe dados primeiro.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile="EWZ_GEX_snapshot.json",
        )
        if not path:
            return

        payload = {
            "app_version": APP_VERSION,
            "symbol": self.snapshot.symbol,
            "spot": self.snapshot.spot,
            "reference_close": self.snapshot.reference_close,
            "source_url": self.snapshot.source_url,
            "source_timestamp": self.snapshot.source_timestamp,
            "expirations": self.snapshot.expirations,
            "warnings": self.snapshot.warnings,
            "levels": [
                {
                    "key": lv.key,
                    "label": lv.label,
                    "value": self._overrides().get(lv.key),
                    "origin": lv.origin,
                    "confidence": lv.confidence,
                    "note": lv.note,
                }
                for lv in self.snapshot.levels
            ],
            "exposures": [
                {
                    "strike": row.strike,
                    "call_gex": row.call_gex,
                    "put_gex": row.put_gex,
                    "net_gex": row.net_gex,
                    "call_oi": row.call_oi,
                    "put_oi": row.put_oi,
                }
                for row in self.snapshot.exposures
            ],
            "tradingview_block": format_export_block(self.snapshot, self._overrides()),
        }
        Path(path).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self.status_var.set(f"Snapshot JSON salvo em {path}")

    def show_about(self):
        messagebox.showinfo(
            "Sobre — EWZ GEX → WIN Desktop",
            f"{APP_TITLE}\nVersão {APP_VERSION}\n\n"
            "Aplicação complementar ao indicador EWZ GEX → WIN.\n"
            "Inclui modo de compatibilidade com extensões do Edge, inclusive Cold Turkey.\n"
            "A projeção principal segue a palestra: distância percentual do fechamento EWZ D-1 aplicada 1:1 ao WIN no mesmo instante.\n"
            "Build alpha: os níveis e a coleta ainda estão em validação.",
        )

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
