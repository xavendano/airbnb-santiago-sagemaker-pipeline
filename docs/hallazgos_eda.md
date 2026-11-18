# Hallazgos del análisis exploratorio (EDA)

**Datos:** Inside Airbnb, Santiago de Chile, snapshot de septiembre 2026
**Fecha del análisis:** 2026-11-18
**Decisiones asociadas:** ver [decisiones.md](decisiones.md)

## 1. De 18.904 a 17.256 anuncios

| Paso | Anuncios | Columnas |
|------|---------:|---------:|
| Datos originales | 18.904 | 90 |
| Eliminar columnas con > 90 % de nulos | 18.904 | 74 |
| Selección de variables | 18.904 | 19 |
| Eliminar anuncios sin precio | 18.006 | 19 |
| Eliminar outliers sobre el P99 (629.811 CLP) | 17.825 | 19 |
| Transformaciones (baños, binarias, reseñas) | 17.825 | 21 |
| Excluir centros de ski (longitud > -70,48) | **17.256** | **21** |

Se conservó el **91 %** de los anuncios.

## 2. Calidad de los datos

- **14 columnas vienen 100 % vacías** en este snapshot de Santiago, entre ellas `bathrooms`, `host_since` e `instant_bookable`. `bathrooms` se recuperó desde `bathrooms_text`.
- **El precio viene como texto** (`"$59,303.00"`) y en pesos chilenos. El 4,8 % de los anuncios no tiene precio.
- **Hay precios absurdos**: hasta 97,5 millones CLP por noche, probablemente errores de carga o precios usados para bloquear el calendario.
- **El 15 % de los anuncios no tiene reseñas.** No es un error: se marcó con la columna `sin_resenas`.

Evidencia: [distribución de precios](../images/eda/01_distribucion_precios.png)

## 3. El precio

Después de la limpieza (CLP por noche):

| Mínimo | P25 | Mediana | P75 | Máximo |
|-------:|----:|--------:|----:|-------:|
| 8.463 | 39.158 | **54.000** | 77.000 | 618.333 |

- Antes de limpiar, el **promedio (108 mil) era el doble de la mediana** por culpa de los outliers. Después de limpiar, el promedio es de 66 mil.
- La distribución tiene **cola larga hacia la derecha**, con pocos anuncios muy caros. En escala logarítmica se ve casi simétrica, así que **predecir log(precio)** es una opción a evaluar en el modelo.

## 4. La ubicación es clave

- **El oriente es más caro**: Providencia (mediana de 66 mil), Las Condes (88 mil), Vitacura (118 mil) y Lo Barnechea (127 mil).
- **El sur y el poniente son más baratos**: Pedro Aguirre Cerda (22 mil), Lo Espejo (25 mil) y La Granja (26 mil).
- **Santiago Centro concentra el 41 % de la oferta** (7.030 anuncios), con precios bajos.
- **Hallazgo: los centros de ski.** En el mapa aparecía un grupo de anuncios en plena cordillera (Farellones, La Parva, Valle Nevado) con una mediana de unos 357 mil CLP. Es otro mercado, que depende de la temporada de ski, y **se excluyó** para que el modelo se enfoque en el mercado urbano.
- **Efecto en la correlación:** antes de excluirlos, la longitud tenía una correlación de **0,70** con el precio. Después bajó a **0,33**. Gran parte de esa relación venía de la cordillera y no de la ciudad.

Evidencia: [mapa antes](../images/eda/05_mapa_precios_osm.png) / [mapa después](../images/eda/06_mapa_precios_urbano.png)

## 5. Qué variables se relacionan con el precio

Correlación con el precio, sobre los datos finales:

| Variable | Correlación |
|----------|------------:|
| `accommodates` (capacidad) | **0,50** |
| `bedrooms` | 0,38 |
| `beds` | 0,34 |
| `longitude` | 0,33 |
| `latitude` | 0,31 |
| `review_scores_location` | 0,10 |
| `host_listings_count` | 0,10 |
| Reseñas, disponibilidad, noches mínimas | ~0 |

- **El tamaño (capacidad, dormitorios, camas) y la ubicación** son las variables más relacionadas.
- **Las reseñas casi no se relacionan con el precio.** Un anuncio con muchas reseñas no es necesariamente más caro.
- La correlación solo mide relaciones **lineales**. XGBoost puede capturar relaciones más complejas, así que se conservan igual.

## 6. Tipo de habitación

| Tipo | Mediana (CLP) | Anuncios |
|------|-------------:|---------:|
| Departamento o casa completa | 58.759 | 14.087 (82 %) |
| Habitación privada | 32.159 | 3.081 |
| Habitación compartida | 19.990 | 45 |
| Habitación de hotel | 103.861 | 43 |

El mercado está dominado por **departamentos completos**. Una habitación privada cuesta aproximadamente la mitad.

## 7. Advertencias para el modelo

- **Comunas con muy pocos anuncios** dan medianas poco confiables. Por ejemplo, La Pintana y San Ramón tienen **un solo anuncio** cada una. Las coordenadas (lat/lon) ayudan a compensarlo.
- **Data leakage evitado:** se excluyeron `price_quote_*` y `estimated_revenue_l365d` porque se calculan a partir del precio.
- **Pendiente:** convertir `room_type`, `property_type` y `neighbourhood_cleansed` a variables numéricas (one-hot encoding) antes de entrenar.
