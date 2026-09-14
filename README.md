# Análisis de ventas por sucursal

Este proyecto consolida los informes de las sucursales de Cali, Medellín, Barranquilla y Bogotá. Incluye un **sistema de automatización** que vigila la carpeta `Datos/`, procesa cada informe nuevo y genera **gráficos + resumen ejecutivo** con métricas de negocio.

## Sistema de automatización

El proyecto incluye un sistema de automatización que **vigila la carpeta `Datos/`** en busca de nuevos informes de sucursales. No tienes que borrar ni mover nada: basta con soltar el archivo nuevo en la carpeta y el programa hace todo por sí solo.

### ¿Qué hace el sistema?

Cada vez que se detecta un archivo nuevo, el programa:

1. **Relee todos los informes** de la carpeta `Datos/` (tanto `.csv` como `.xlsx`).
2. **Estandariza las columnas**, para que todos los reportes tengan el mismo formato (fecha, producto, categoria, cantidad, precio_unitario, vendedor, metodo_pago).
3. **Consolida y limpia** los datos (une todo y elimina duplicados).
4. **Actualiza el archivo** `Resultados/consolidado_limpio.xlsx`.
5. **Regenera los gráficos** `grafico_categoria.png` y `grafico_ventas_vendedor.png`.
6. **Genera el resumen ejecutivo** `Resultados/resumen_ejecutivo.txt` con las 4 métricas de negocio.
7. **Agrega una entrada al log** `Resultados/log_automatizacion.txt` registrando la fecha, el archivo detectado y el total de registros procesados.

Al iniciar, el programa muestra un **banner** de presentación y al final de cada proceso imprime el **resumen ejecutivo** en consola.

### Métricas del resumen ejecutivo

Las 4 métricas de negocio que calcula el sistema:

1. **Categoría que más vende** (suma de `cantidad * precio_unitario` por categoría).
2. **Vendedor con más ventas** (suma de `cantidad * precio_unitario` por vendedor).
3. **Producto más vendido** (`value_counts()` sobre la columna producto).
4. **Promedio de venta por transacción** (`mean()` sobre el valor total de cada transacción).

### ¿Cómo detecta los archivos nuevos?

El programa lleva un registro de los archivos que ya vio (`archivos_vistos`). En un bucle, compara esa lista con lo que hay actualmente en `Datos/`. Cuando aparecen archivos que no estaban antes, se dispara la automatización y se actualiza la lista de archivos conocidos. El bucle repite la revisión cada **5 segundos**.

### ¿Qué pasa cuando encuentra uno?

Se imprime en consola un mensaje tipo:

```text
Nuevo archivo detectado: {'sucursal_medellin_reporte2.csv'}
...
RESUMEN EJECUTIVO
...
Proceso completado - log, graficos y resumen actualizados en Resultados/
```

Y de forma inmediata se actualizan el consolidado, los gráficos, el resumen ejecutivo y el log.

## Preguntas de negocio (con las 4 métricas)

### 1. ¿Qué categoría vende más? ¿Por cuánto?

La categoría que genera más ventas es **Electrónica**, con un total de **$19.374.700**. La categoría **Ropa** registra **$11.107.200**. En total, las ventas analizadas suman **$30.481.900**.

Los valores se calcularon multiplicando la cantidad vendida por el precio unitario de cada registro:

```text
venta_total = cantidad * precio_unitario
```

### 2. ¿Qué vendedor tiene más ventas totales?

La vendedora con mayor valor de ventas es **Camila Ruiz**, con **$7.152.600**, seguida de **Andrés Gómez** con **$5.320.000** y **Sofía Mena** con **$4.604.400**.

### 3. ¿Cuál es el producto más vendido? (métrica con `value_counts()`)

Usando `value_counts()` sobre la columna **producto**, los productos que aparecen más veces son:

- **Jean clasico**: **10 apariciones** (primer lugar en el resumen ejecutivo).
- **Cargador USB-C**: **10 apariciones**.

Existe un **empate** por número de transacciones. Midiendo por unidades vendidas, **Jean clasico** ocupa el primer lugar con **54 unidades**, seguido de **Cargador USB-C** con **46 unidades**.

### 4. ¿Cuál es el promedio de venta por transacción? (métrica con `mean()`)

El promedio de venta por transacción es **$423.360**. Se obtiene con el promedio (`mean()`) del valor de cada venta (`cantidad * precio_unitario`) a lo largo de las 75 transacciones analizadas.

Este valor sirve como referencia para evaluar el rendimiento diario: una jornada con muchas transacciones por debajo de ese promedio indica ventas de bajo ticket, mientras que transacciones que lo superan ampliamente (por ejemplo una Laptop de $2.500.000) impulsan el total.

## Conclusión

Con las 4 métricas se ve un negocio con una **fuerte dependencia de Electrónica** (cerca del 64 % de los ingresos) y de una **vendedora estrella** (Camila Ruiz). El producto de mayor rotación es **Jean clasico**, empatado con **Cargador USB-C**, y una transacción promedio ronda los **$423.360**.

El dueño debería:

- Mantener **inventario suficiente de Electrónica** y de los productos con mayor rotación (**Jean clasico** y **Cargador USB-C**).
- **Replicar las prácticas de Camila Ruiz** en el resto del equipo.
- **Impulsar Ropa** con promociones para reducir la brecha contra Electrónica.
- Usar el **promedio de venta por transacción** como meta diaria por vendedor.
- Completar los registros incompletos: hay **3 precios unitarios**, **2 vendedores** y **14 métodos de pago** sin dato.

## Reflexión final

> ¿Confiaría en un sistema automático como este para tomar decisiones?

**Sí, con supervisión.** Un sistema automático como este reduce errores humanos, procesa los informes en segundos y siempre aplica la misma regla de cálculo, lo cual es muy valioso para que las decisiones se basen en números comparables entre sucursales. Las 4 métricas que entrega (categoría, vendedor, producto y promedio por transacción) cubren las preguntas centrales de un negocio de retail: qué vendo, quién vende, qué rota y cuánto vale cada venta.

Sin embargo, no confiaría ciegamente por tres razones:

1. **Calidad de los datos**: el propio proceso encontró registros con datos vacíos (precio, vendedor, método de pago). Un sistema automático no puede tomar bien una decisión si los datos de entrada están mal.
2. **Los promedios ocultan extremos**: el promedio de $423.360 se distorsiona con ventas grandes poco frecuentes (como una Laptop), por lo que conviene mirar también la mediana o revisar días atípicos.
3. **Falta contexto humano**: el sistema dice cuánto se vendió, pero no explica el "por qué" (descuentos, temporadas, devoluciones). Esas explicaciones siguen siendo trabajo del dueño.

En resumen: es una herramienta **excelente para vigilar y alertar**, y la usaría como base para decidir, pero siempre con una revisión humana de los datos y del contexto antes de comprometer dinero o inventario.

## Datos analizados

- Archivos: 7 informes de sucursales (4 originales + 3 de prueba `_reporte2`).
- Registros después de eliminar duplicados: **75**.
- Categorías: Electrónica y Ropa.
- Productos distintos: 22.
- Vendedores: 12.
- Período de datos: junio a agosto de 2026.

## Archivos de prueba

Para probar el sistema se usaron tres informes `_reporte2` en `Datos/`:

- `sucursal_medellin_reporte2.csv`
- `sucursal_cali_reporte2.csv`
- `sucursal_bogota_reporte2.csv` (creado copiando uno de los anteriores, cambiando el nombre de la sucursal y modificando algunos valores).

Se agregaron **uno a la vez** y el registro en `Resultados/log_automatizacion.txt` muestra cómo el total de registros pasó de 67 → 71 → 75.

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