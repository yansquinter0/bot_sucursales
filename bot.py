import time
import os
import sys
import pandas as pd
import glob
import matplotlib.pyplot as plt
from pathlib import Path

# Identificacion UTF-8 para la consola (banner y resumen con tildes)
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Configuración de carpetas
carpeta_datos = Path('Datos')
carpeta_resultados = Path('Resultados')
carpeta_resultados.mkdir(exist_ok=True)
carpeta_datos.mkdir(exist_ok=True)

# Registro de archivos iniciales
archivos_vistos = set(os.listdir(carpeta_datos))


def mostrar_banner():
    """Banner de presentación del sistema de automatización."""
    print("=" * 60)
    print("   SISTEMA AUTOMATICO DE ANALISIS DE VENTAS")
    print("   Consolida sucursales, limpia datos y genera")
    print("   metricas de negocio + resumen ejecutivo")
    print("=" * 60)
    print()


def resumen_ejecutivo(df):
    """
    Calcula las 4 metricas de negocio sobre el consolidado,
    las imprime en consola y las guarda en Resultados/.
    """
    df = df.copy()
    df['venta_total'] = df['cantidad'] * df['precio_unitario']

    # Metrica 1: categoría que más vende
    ventas_categoria = df.groupby('categoria')['venta_total'].sum().sort_values(ascending=False)
    categoria_top = ventas_categoria.idxmax()
    categoria_monto = ventas_categoria.max()

    # Metrica 2: vendedor con más ventas
    ventas_vendedor = df.groupby('vendedor')['venta_total'].sum().sort_values(ascending=False)
    vendedor_top = ventas_vendedor.idxmax()
    vendedor_monto = ventas_vendedor.max()

    # Metrica 3: producto más vendido (value_counts)
    conteo_productos = df['producto'].value_counts()
    producto_top = conteo_productos.idxmax()
    producto_apariciones = int(conteo_productos.max())

    # Metrica 4: promedio de venta por transacción (mean)
    promedio_venta = df['venta_total'].mean()

    lineas = [
        "=" * 60,
        "RESUMEN EJECUTIVO",
        "=" * 60,
        "",
        "1. Categoria que mas vende:",
        f"   - {categoria_top} con $ {categoria_monto:,.0f}",
        "",
        "2. Vendedor con mas ventas:",
        f"   - {vendedor_top} con $ {vendedor_monto:,.0f}",
        "",
        "3. Producto mas vendido (value_counts):",
        f"   - {producto_top} con {producto_apariciones} transacciones",
        "",
        "4. Promedio de venta por transaccion (mean):",
        f"   - $ {promedio_venta:,.0f}",
        "",
        f"Registros procesados: {len(df)}",
        "",
        "=" * 60,
    ]
    texto = "\n".join(lineas)

    print()
    print(texto)

    with open(carpeta_resultados / "resumen_ejecutivo.txt", "w", encoding="utf-8") as f:
        f.write(texto)


def procesar_todo(archivo_nuevo):
    """
    Lee archivos, estandariza columnas, consolida, genera gráficos,
    resumen ejecutivo y guarda un log del proceso automatizado.
    """
    archivos_csv = glob.glob(str(carpeta_datos / "sucursal_*.csv"))
    archivos_xlsx = glob.glob(str(carpeta_datos / "sucursal_*.xlsx"))
    lista_informes = []

    for archivo in archivos_csv:
        lista_informes.append(pd.read_csv(archivo))
    for archivo in archivos_xlsx:
        lista_informes.append(pd.read_excel(archivo, engine='openpyxl'))

    # Estandarización de columnas (Tu código integrado)
    for i, df in enumerate(lista_informes):
        if 'Fecha_Venta' in df.columns:
            lista_informes[i] = df.rename(columns={
                'Fecha_Venta': 'fecha',
                'Producto': 'producto',
                'Categoria': 'categoria',
                'Cant': 'cantidad',
                'Valor_Unitario': 'precio_unitario',
                'Vendedor': 'vendedor',
                'Pago': 'metodo_pago',
            })

    # Consolidación y limpieza
    df_consolidado = pd.concat(lista_informes, ignore_index=True)
    df_consolidado = df_consolidado.drop_duplicates()
    df_consolidado['venta_total'] = df_consolidado['cantidad'] * df_consolidado['precio_unitario']
    df_consolidado.to_excel(carpeta_resultados / "consolidado_limpio.xlsx", index=False)

    # Gráfico 1: Ventas por categoría
    ventas_categoria = df_consolidado.groupby('categoria')['venta_total'].sum()
    ventas_categoria.plot(kind='bar', title='Ventas por Categoría')
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Ventas totales ($)')
    plt.tight_layout()
    plt.savefig(carpeta_resultados / "grafico_categoria.png")
    plt.close()

    # Gráfico 2: Participación por vendedor
    ventas_vendedor = df_consolidado.groupby('vendedor')['venta_total'].sum()
    ventas_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Ventas por Vendedor')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(carpeta_resultados / "grafico_ventas_vendedor.png")
    plt.close()

    # Registro del Log
    with open(carpeta_resultados / "log_automatizacion.txt", "a", encoding="utf-8") as f:
        f.write(f"Proceso ejecutado: {pd.Timestamp.now()}\n")
        f.write(f"Archivo(s) detectado(s): {', '.join(sorted(archivo_nuevo))}\n")
        f.write(f"Total de registros procesados: {len(df_consolidado)}\n")
        f.write("---\n")

    # Resumen ejecutivo con las metricas de negocio
    resumen_ejecutivo(df_consolidado)

    print(f"Proceso completado - log, graficos y resumen actualizados en {carpeta_resultados}/")


mostrar_banner()
print("Monitoreando carpeta de datos... (Ctrl+C para detener)")
while True:
    archivos_actuales = set(os.listdir(carpeta_datos))
    archivos_nuevos = archivos_actuales - archivos_vistos

    if archivos_nuevos:
        print(f"\nNuevo archivo detectado: {archivos_nuevos}")
        procesar_todo(archivos_nuevos)
        archivos_vistos = archivos_actuales

    time.sleep(5)