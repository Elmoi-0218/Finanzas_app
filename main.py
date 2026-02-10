diff --git a/main.py b/main.py
index 8b137891791fe96927ad78e64b0aad7bded08bdc..f9c9b0aaf43267a64079bf27c15723b5a3c4bd90 100644
--- a/main.py
+++ b/main.py
@@ -1 +1,164 @@
+#!/usr/bin/env python3
+"""Aplicación de finanzas personales en consola.
 
+Permite registrar ingresos y gastos en un archivo JSON local y consultar
+resúmenes por categoría.
+"""
+
+from __future__ import annotations
+
+import argparse
+import json
+from dataclasses import asdict, dataclass
+from datetime import date
+from pathlib import Path
+from typing import Dict, List
+
+DEFAULT_DB_PATH = Path("finanzas_db.json")
+
+
+@dataclass
+class Movimiento:
+    tipo: str
+    monto: float
+    categoria: str
+    descripcion: str
+    fecha: str
+
+
+class GestorFinanzas:
+    def __init__(self, db_path: Path = DEFAULT_DB_PATH) -> None:
+        self.db_path = db_path
+        self.movimientos: List[Movimiento] = []
+        self._cargar()
+
+    def _cargar(self) -> None:
+        if not self.db_path.exists():
+            self.movimientos = []
+            return
+
+        with self.db_path.open("r", encoding="utf-8") as archivo:
+            data = json.load(archivo)
+
+        self.movimientos = [Movimiento(**item) for item in data]
+
+    def _guardar(self) -> None:
+        serializable = [asdict(m) for m in self.movimientos]
+        with self.db_path.open("w", encoding="utf-8") as archivo:
+            json.dump(serializable, archivo, ensure_ascii=False, indent=2)
+
+    def agregar_movimiento(
+        self,
+        tipo: str,
+        monto: float,
+        categoria: str,
+        descripcion: str = "",
+        fecha: str | None = None,
+    ) -> Movimiento:
+        if tipo not in {"ingreso", "gasto"}:
+            raise ValueError("El tipo debe ser 'ingreso' o 'gasto'.")
+        if monto <= 0:
+            raise ValueError("El monto debe ser mayor que cero.")
+
+        movimiento = Movimiento(
+            tipo=tipo,
+            monto=monto,
+            categoria=categoria.strip() or "general",
+            descripcion=descripcion.strip(),
+            fecha=fecha or date.today().isoformat(),
+        )
+        self.movimientos.append(movimiento)
+        self._guardar()
+        return movimiento
+
+    def resumen(self) -> Dict[str, float]:
+        ingresos = sum(m.monto for m in self.movimientos if m.tipo == "ingreso")
+        gastos = sum(m.monto for m in self.movimientos if m.tipo == "gasto")
+        return {
+            "ingresos": round(ingresos, 2),
+            "gastos": round(gastos, 2),
+            "balance": round(ingresos - gastos, 2),
+        }
+
+    def resumen_por_categoria(self, tipo: str = "gasto") -> Dict[str, float]:
+        if tipo not in {"ingreso", "gasto"}:
+            raise ValueError("El tipo debe ser 'ingreso' o 'gasto'.")
+
+        totales: Dict[str, float] = {}
+        for mov in self.movimientos:
+            if mov.tipo != tipo:
+                continue
+            totales[mov.categoria] = totales.get(mov.categoria, 0.0) + mov.monto
+
+        return {cat: round(total, 2) for cat, total in sorted(totales.items())}
+
+    def listar(self) -> List[Movimiento]:
+        return list(self.movimientos)
+
+
+def crear_parser() -> argparse.ArgumentParser:
+    parser = argparse.ArgumentParser(description="Gestor simple de finanzas personales")
+    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH, help="Ruta del archivo JSON")
+
+    subparsers = parser.add_subparsers(dest="comando", required=True)
+
+    add_cmd = subparsers.add_parser("agregar", help="Agregar ingreso o gasto")
+    add_cmd.add_argument("tipo", choices=["ingreso", "gasto"])
+    add_cmd.add_argument("monto", type=float)
+    add_cmd.add_argument("categoria")
+    add_cmd.add_argument("--descripcion", default="")
+    add_cmd.add_argument("--fecha", default=None, help="Formato YYYY-MM-DD")
+
+    subparsers.add_parser("resumen", help="Mostrar resumen general")
+
+    cat_cmd = subparsers.add_parser("categorias", help="Mostrar resumen por categoría")
+    cat_cmd.add_argument("tipo", nargs="?", default="gasto", choices=["ingreso", "gasto"])
+
+    subparsers.add_parser("listar", help="Listar movimientos registrados")
+
+    return parser
+
+
+def main() -> None:
+    parser = crear_parser()
+    args = parser.parse_args()
+
+    gestor = GestorFinanzas(db_path=args.db)
+
+    if args.comando == "agregar":
+        mov = gestor.agregar_movimiento(
+            tipo=args.tipo,
+            monto=args.monto,
+            categoria=args.categoria,
+            descripcion=args.descripcion,
+            fecha=args.fecha,
+        )
+        print(f"✅ Movimiento registrado: {mov.tipo} | {mov.categoria} | ${mov.monto:.2f}")
+
+    elif args.comando == "resumen":
+        r = gestor.resumen()
+        print("📊 Resumen general")
+        print(f"Ingresos: ${r['ingresos']:.2f}")
+        print(f"Gastos:   ${r['gastos']:.2f}")
+        print(f"Balance:  ${r['balance']:.2f}")
+
+    elif args.comando == "categorias":
+        resumen = gestor.resumen_por_categoria(args.tipo)
+        print(f"📂 Resumen por categoría ({args.tipo})")
+        if not resumen:
+            print("No hay movimientos para mostrar.")
+        for categoria, total in resumen.items():
+            print(f"- {categoria}: ${total:.2f}")
+
+    elif args.comando == "listar":
+        movimientos = gestor.listar()
+        if not movimientos:
+            print("No hay movimientos registrados todavía.")
+            return
+        print("🧾 Movimientos")
+        for m in movimientos:
+            print(f"{m.fecha} | {m.tipo:<7} | {m.categoria:<15} | ${m.monto:>10.2f} | {m.descripcion}")
+
+
+if __name__ == "__main__":
+    main()

