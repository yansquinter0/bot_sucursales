import time
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
from pathlib import Path

# Configuración de carpetas
carpeta_datos = Path('Datos')
carpeta_resultados = Path('Resultados')
carpeta_resultados.mkdir(exist_ok=True)
carpeta_datos.mkdir(exist_ok=True)

# Registro de archivos iniciales
archivos_vistos = set(os.listdir(carpeta_datos))

def procesar_todo(archivo_nuevo):
    """
    Lee archivos, estandariza columnas, consolida, genera gráficos
    y guarda un log del proceso automatizado.
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
    df_consolidado.to_excel(carpeta_resultados / "consolidado_limpio.xlsx", index=False)
    
    # Gráfico 1: Ventas por categoría
    ventas_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
    ventas_categoria.plot(kind='bar', title='Ventas por Categoría')
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Ventas totales ($)')
    plt.tight_layout()
    plt.savefig(carpeta_resultados / "grafico_categoria.png")
    plt.close()
    
    # Gráfico 2: Participación por vendedor
    ventas_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
    ventas_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Ventas por Vendedor')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(carpeta_resultados / "grafico_ventas_vendedor.png")
    plt.close()
    
    # Registro del Log
    with open(carpeta_resultados / "log_automatizacion.txt", "a") as f:
        f.write(f"Proceso ejecutado: {pd.Timestamp.now()}\n")
        f.write(f"Archivo(s) detectado(s): {archivo_nuevo}\n")
        f.write(f"Total de registros procesados: {len(df_consolidado)}\n")
        f.write("---\n")
    
    print(f"Proceso completado - log y gráficos actualizados en {carpeta_resultados}/")

print("Monitoreando carpeta de datos... (Ctrl+C para detener)")
while True:
    archivos_actuales = set(os.listdir(carpeta_datos))
    archivos_nuevos = archivos_actuales - archivos_vistos
    
    if archivos_nuevos:
        print(f"\nNuevo archivo detectado: {archivos_nuevos}")
        procesar_todo(archivos_nuevos)
        archivos_vistos = archivos_actuales
    
    time.sleep(5)