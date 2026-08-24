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

El producto más vendido por cantidad de unidades es **Jean clásico**, con **54 unidades**.

El segundo producto es **Cargador USB-C**, con **46 unidades**.

### ¿Qué decisión tomaría el dueño del negocio?

El dueño debería priorizar la categoría **Electrónica**, porque es la que produce mayores ingresos. También debería:

- Mantener suficiente inventario de **Jean clásico** y **Cargador USB-C**, que son los productos con mayor rotación.
- Reconocer las buenas ventas de **Camila Ruiz** y revisar sus prácticas para compartirlas con el resto del equipo.
- Promocionar productos de Ropa para reducir la diferencia entre categorías.
- Revisar los registros incompletos antes de tomar decisiones definitivas: hay **3 precios unitarios** y **2 vendedores** sin dato.

## Datos analizados

- Archivos: 4 informes de sucursales.
- Registros originales: 66.
- Registros después de eliminar duplicados: 63.
- Categorías: Electrónica y Ropa.
- Período de datos: junio de 2026.

## Ejecución

Instala las dependencias:

```powershell
python -m pip install pandas openpyxl matplotlib
```

Ejecuta el programa desde la carpeta principal del proyecto:

```powershell
python bot.py
```

Los resultados se guardan en la carpeta `Resultados/`.
