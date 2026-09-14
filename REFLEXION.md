# Reflexión

Respuestas personales sobre el sistema de automatización de ventas.

## 1. ¿Qué hace `os.listdir(ruta_datos)`?

Devuelve una lista con los nombres de todos los archivos y carpetas que hay dentro de `ruta_datos`. En mi código lo uso como `os.listdir(carpeta_datos)`: al inicio del programa tomo una "foto" de los archivos que ya conozco, y dentro del `while` lo vuelvo a llamar para ver qué hay ahora en la carpeta. Comparando ambas fotos sé si llegó un archivo nuevo.

## 2. ¿Qué diferencia hay entre `set` y lista para guardar archivos vistos?

Una **lista** conserva el orden y permite repetidos, pero revisar si un archivo ya fue visto es lento porque tiene que recorrer todos los elementos. Un **set** no tiene repetidos ni orden y la búsqueda es casi instantánea; además permite usar la resta `archivos_actuales - archivos_vistos` para saber exactamente qué archivos son nuevos. Por eso guardo los vistos en un `set`: solo necesito saber si un archivo ya fue visto o no, y ese cálculo se hace al instante.

## 3. ¿Qué hace `drop_duplicates()` y por qué es importante aquí?

Elimina las filas exactamente repetidas y deja una sola copia de cada una. Es importante porque al consolidar varios informes el mismo registro puede aparecer dos veces (por ejemplo, si un archivo llega repetido o duplicado), y eso inflaría las ventas totales y las métricas. Con `drop_duplicates()` cada venta se cuenta una sola vez y el análisis no engaña.

## 4. ¿Cuántos commits tiene tu repo? Menciona 2 de tus mensajes

Mi repositorio tiene **8 commits**. Dos ejemplos de mensajes:
- `agregar sistema de automatización`
- `agregar banner y resumen ejecutivo con 4 metricas`

## 5. ¿Qué mejora le harías a este sistema?

- Completar o marcar los registros incompletos (hoy quedan celdas vacías en precio, vendedor y método de pago).
- Enviar una alerta (correo o mensaje) cada vez que caiga un archivo nuevo o cuando una categoría baje de su promedio histórico.
- Agregar la mediana de venta y filtros por fecha para analizar el negocio por semana o por sucursal.
- Procesar solo el archivo nuevo en lugar de volver a consolidar todo desde cero cada vez.

## 6. ¿Qué fue lo que más te gustó aprender?

Que se puede "contar una historia con datos": con pocas líneas el sistema detecta el archivo, lo limpia, lo consolida y te dice qué categoría vende más, quién es el mejor vendedor y qué promedio hay por transacción, sin abrir nada manualmente. Lo que más me gustó fue el `while` con `set` y `os.listdir()` para detectar archivos nuevos, porque convierte un trabajo repetitivo y manual en algo completamente automático.