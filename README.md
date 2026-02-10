# Finanzas_app
diff --git a/README.md b/README.md
index a8031104c5e4232cdce37a59194fb6b7b2685270..b51219c9fb5c9c7d75cbf7ffc49e5832b177ef1a 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,30 @@
-# Finanzas_app
\ No newline at end of file
+# Finanzas_app
+
+Aplicación de consola escrita en **Python** para registrar ingresos y gastos.
+
+## Requisitos
+
+- Python 3.10+
+
+## Uso
+
+```bash
+python3 main.py --help
+```
+
+### Registrar movimientos
+
+```bash
+python3 main.py agregar ingreso 2500 salario --descripcion "Sueldo mensual"
+python3 main.py agregar gasto 120 comida --descripcion "Supermercado"
+```
+
+### Ver reportes
+
+```bash
+python3 main.py resumen
+python3 main.py categorias gasto
+python3 main.py listar
+```
+
+Por defecto, los datos se guardan en `finanzas_db.json`. Puedes usar otro archivo con `--db`.
