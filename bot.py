import pandas as pd
import glob
import matplotlib.pyplot as plt
from pathlib import Path

carpeta_datos = Path('Datos')
carpeta_resultados = Path('Resultados')
carpeta_resultados.mkdir(exist_ok=True)

# --------------------------------------------
# PARTE 1: Buscar y leer los archivos (YA VISTO)
# --------------------------------------------
archivos_csv = glob.glob(str(carpeta_datos / "sucursal_*.csv"))
archivos_xlsx = glob.glob(str(carpeta_datos / "sucursal_*.xlsx"))
lista_informes = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_informes.append(df)
    print(f"Leído: {archivo} - {len(df)} filas")

for archivo in archivos_xlsx:
    df = pd.read_excel(archivo, engine='openpyxl')
    lista_informes.append(df)
    print(f"Leído: {archivo} - {len(df)} filas")

# --------------------------------------------
# PARTE 2: Consolidar (YA VISTO - primer intento)
# Aquí van a ver el problema de columnas distintas
# --------------------------------------------
df_consolidado = pd.concat(lista_informes, ignore_index=True)
print(df_consolidado.columns)
# En este punto probablemente veas más de 7 columnas

# --------------------------------------------
# PARTE 3: Renombrar columnas (COMPLETEN USTEDES)
# Identifiquen cuál archivo tiene columnas distintas
# --------------------------------------------
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

df_consolidado = pd.concat(lista_informes, ignore_index=True)
print(df_consolidado.columns)  # debería mostrar exactamente 7

# --------------------------------------------
# PARTE 4: Limpieza de datos
# --------------------------------------------
filas_antes = len(df_consolidado)
df_consolidado = df_consolidado.drop_duplicates()
print(f"Filas antes: {filas_antes} - después: {len(df_consolidado)}")

print(df_consolidado.isnull().sum())
# completar: decidan qué valor tiene sentido para cada columna con nulos

# --------------------------------------------
# PARTE 5: Guardar el resultado
# --------------------------------------------
df_consolidado.to_excel(carpeta_resultados / "consolidado_limpio.xlsx", index=False)
print("Archivo guardado")

# --------------------------------------------
# PARTE 6: Análisis y visualización (NUEVO - hoy)
# --------------------------------------------

# 6a. EJEMPLO RESUELTO: ventas por categoría (gráfico de barras)
ventas_por_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()  # Agrupa y suma por categoría
ventas_por_categoria.plot(kind='bar', title='Ventas por Categoria')  # Crea el gráfico de barras
plt.ticklabel_format(style='plain', axis='y')  # Evita notación científica (1e6)
plt.ylabel('Ventas totales ($)')
plt.xlabel('Categoría')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(carpeta_resultados / "grafico_ventas_categoria.png")
plt.show()

# 6b. EJEMPLO RESUELTO: participación por vendedor (gráfico de torta)
ventas_por_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()  # Agrupa y suma por vendedor
ventas_por_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Participacion de Ventas por Vendedor')  # Grafico de torta con porcentajes
plt.ylabel('')  # No aplica en gráficos de torta
plt.tight_layout()
plt.savefig(carpeta_resultados / "grafico_ventas_vendedor.png")
plt.show()

# 6c. AHORA USTEDES: ¿cuál es el producto que aparece más veces 
# en las ventas? Investiguen la función value_counts() y 
# apliquenla a la columna 'producto'
productos_mas_vendidos = df_consolidado['producto'].value_counts()
print('\nProductos con más apariciones en las ventas:')
print(productos_mas_vendidos.head())