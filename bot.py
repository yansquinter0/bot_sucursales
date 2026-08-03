import pandas as pd
import glob
#1. buscar datos y leer archivos

df_medellin = pd.read_csv('sucursal_medellin.csv')
# print(df_medellin)

df_bogota = pd.read_excel('sucursal_bogota.xlsx')
# print(df_bogota.head(3))

# print(df_bogota.columns)

# print(df_medellin.columns)

#2. guardar en una lista

archivos_csv = glob.glob('*.csv')
print(f'archivos_csv {archivos_csv}')

archivos_xlsx = glob.glob('*.xlsx')
print(f'archivos_xlsx {archivos_xlsx}')

lista_df = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_df.append(df)
    print(f'leido: {archivo} - {len(df)} filas')

for archivos in archivos_xlsx:
    df = pd.read_excel(archivos)
    lista_df.append(df)
    print(f'leido: {archivos} - {len(df)} filas')

df_consolidado = pd.concat(lista_df, ignore_index=True)
df_consolidado.to_excel("consolidado_desordenado.xlsx", index=False)

for i, df in enumerate(lista_df):
    if 'Fecha_Venta' in df.columns:
        lista_df[i] = df.rename(columns={'Fecha_Venta':'fecha', 'Producto':'producto', 'Categoria':'categoria', 'Cant':'cantidad', 'Valor_Unitario':'precio_unitario', 'Vendedor':'vendedor', 'Pago':'metodo_pago'})

df_consolidado = pd.concat(lista_df, ignore_index=True)
df_consolidado.to_excel("consolidado_ordenado.xlsx", index=False)