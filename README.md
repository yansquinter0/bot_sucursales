# Análisis de ventas por sucursal

Este proyecto consolida los informes de las sucursales de Cali, Medellín, Barranquilla y Bogotá.

## Preguntas de análisis

### ¿Qué categoría vende más? ¿Por cuánto?

La categoría que genera más ventas es **Electrónica**, con un total de **$12.640.700**.

La categoría **Ropa** registra **$10.216.200**. En total, las ventas analizadas suman **$22.856.900**.

Los valores se calcularon multiplicando la cantidad vendida por el precio unitario de cada registro:

```text
venta_total = cantidad * precio_unitario
```

### ¿Qué vendedor tiene más ventas totales?

La vendedora con mayor valor de ventas es **Camila Ruiz**, con **$7.152.600**.

### ¿Cuál es el producto más vendido?

Usando `value_counts()`, los productos que aparecen más veces en los registros de ventas son:

- **Jean clasico**: **10 apariciones**.
- **Cargador USB-C**: **10 apariciones**.

Existe un empate por cantidad de registros. Si se mide por unidades vendidas, **Jean clasico** ocupa el primer lugar con **54 unidades**, seguido de **Cargador USB-C** con **46 unidades**.

### ¿Qué decisión tomaría el dueño del negocio?

El dueño debería priorizar la categoría **Electrónica**, porque es la que produce mayores ingresos. También debería:

- Mantener suficiente inventario de **Jean clasico** y **Cargador USB-C**, que son los productos con mayor rotación.
- Reconocer las buenas ventas de **Camila Ruiz** y revisar sus prácticas para compartirlas con el resto del equipo.
- Promocionar productos de Ropa para reducir la diferencia entre categorías.
- Revisar los registros incompletos antes de tomar decisiones definitivas: hay **3 precios unitarios** y **2 vendedores** sin dato.

## Datos analizados

- Archivos: 4 informes de sucursales.
- Registros originales: 66.
- Registros después de eliminar duplicados: 63.
- Categorías: Electrónica y Ropa.
- Período de datos: junio de 2026.

## Sistema de automatización

El proyecto ahora incluye un sistema de automatización que **vigila la carpeta `Datos/`** en busca de nuevos informes de sucursales. La idea es que ya no tengas que borrar ni mover nada: basta con soltar el archivo nuevo en la carpeta y el programa hace todo por sí solo.

### ¿Qué hace el sistema?

Cada vez que se detecta un archivo nuevo, el programa:

1. **Relee todos los informes** de la carpeta `Datos/` (tanto `.csv` como `.xlsx`).
2. **Estandariza las columnas**, para que todos los reportes tengan el mismo formato (fecha, producto, categoria, cantidad, precio_unitario, vendedor, metodo_pago).
3. **Consolida y limpia** los datos (une todo y elimina duplicados).
4. **Actualiza el archivo** `Resultados/consolidado_limpio.xlsx`.
5. **Regenera los gráficos** `grafico_categoria.png` y `grafico_ventas_vendedor.png`.
6. **Agrega una entrada al log** `Resultados/log_automatizacion.txt` registrando la fecha, el archivo detectado y el total de registros procesados.

### ¿Cómo detecta los archivos nuevos?

El programa lleva un registro de los archivos que ya vio (`archivos_vistos`). En un bucle, compara esa lista con lo que hay actualmente en `Datos/`. Cuando aparecen archivos que no estaban antes, se dispara la automatización y se actualiza la lista de archivos conocidos. El bucle repite la revisión cada **5 segundos**.

### ¿Qué pasa cuando encuentra uno?

Se imprime en consola un mensaje tipo:

```text
Nuevo archivo detectado: {'sucursal_medellin_reporte2.csv'}
Proceso completado - log y gráficos actualizados en Resultados/
```

Y de forma inmediata se actualizan el consolidado, los gráficos y el log.

## Ejecución

Instala las dependencias:

```powershell
python -m pip install pandas openpyxl matplotlib
```

Ejecuta el programa desde la carpeta principal del proyecto:

```powershell
python bot.py
```

El programa queda **vigilando** la carpeta `Datos/`. Para probarlo, arrastra y suelta un informe nuevo (por ejemplo `sucursal_cali_reporte2.csv`) dentro de `Datos/` y observa cómo se actualizan los resultados por sí solos. Se detiene con `Ctrl+C`.

Los resultados se guardan en la carpeta `Resultados/`.
