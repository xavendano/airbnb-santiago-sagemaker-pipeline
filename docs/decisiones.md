# Registro de decisiones

Cada decisión relevante del proyecto (datos, modelo, arquitectura, costos) se registra aquí con su fecha y su porqué.

| Fecha | Decisión | Por qué |
|-------|----------|---------|
| 2026-11-18 | Se eligió SageMaker (no Bedrock) como base | El objetivo es mostrar el ciclo completo datos → entrenamiento → despliegue; Bedrock es para modelos fundacionales ya entrenados |
| 2026-11-18 | Se trabajó solo con datos de Santiago de Chile | Una sola versión mantiene el alcance acotado; datos locales le dan un ángulo propio al proyecto |
| 2026-11-18 | Se definió explorar en Colab y llevar a SageMaker solo la producción | Colab es gratis para experimentar; AWS solo para lo que se muestra |
| 2026-11-18 | Se definió Hugging Face Spaces para la demo | Demo pública sin costo mensual en AWS |
| 2026-11-18 | Se adoptó el bajo costo como principio rector | La prioridad es pilotear y entender AWS con gasto mínimo: todo se prueba en Colab y solo lo testeado pasa a AWS |
| 2026-11-18 | Se eliminaron las columnas con más de 90 % de nulos (16 columnas: 14 vacías al 100 %, más `license` y `source`) | No aportan información al modelo. Inside Airbnb no publica esos campos para Santiago en este snapshot (p. ej. `bathrooms`, `host_since`, `instant_bookable`) |
| 2026-11-18 | Se seleccionaron 18 variables + `price` como objetivo, con tres criterios (ver detalle abajo) | Quedarse solo con lo que puede explicar el precio y evitar data leakage |
| 2026-11-18 | Se eliminaron los anuncios sin precio (898) | No se puede entrenar con filas sin el valor a predecir |
| 2026-11-18 | Se eliminaron los outliers de precio sobre el percentil 99 (corte: 629.811 CLP/noche, ~180 anuncios) | Hay precios de hasta 97 millones CLP/noche, claramente errores o bloqueos de calendario. El P99 es un criterio objetivo que conserva las propiedades caras reales. Evidencia: [distribución de precios](../images/eda/01_distribucion_precios.png) |
| 2026-11-18 | Se convirtió `bathrooms_text` en `banos` (número; half-bath = 0,5) y `bano_compartido` (1/0) | El modelo necesita números; además, si el baño es compartido puede influir en el precio |
| 2026-11-18 | Se convirtieron `host_is_superhost` y `host_identity_verified` de `t`/`f` a 1/0 | Formato numérico para el modelo |
| 2026-11-18 | En los anuncios sin reseñas (2.530) se asignó 0 a `reviews_per_month`, se rellenaron los puntajes con la mediana y se creó la columna `sin_resenas` (1/0) | Los nulos significan "sin reseñas", no un error; la columna indicadora evita que el modelo tome el puntaje imputado como real |
| 2026-11-18 | Se rellenaron con la mediana los pocos nulos de `bedrooms` (4), `beds` (186), `minimum_nights` (5) y `bathrooms_text` (13) | Son muy pocos casos; la mediana es robusta a valores extremos |
| 2026-11-18 | En `property_type` se conservaron las 10 categorías más frecuentes y el resto (de 69) se agrupó como "Otro" | Muchas categorías tienen muy pocos anuncios y solo agregarían ruido |
| 2026-11-18 | Se excluyeron los anuncios de los centros de ski (longitud > -70,48; 569 anuncios, todos de Lo Barnechea) | El alcance del modelo es el mercado urbano de Santiago. Farellones, La Parva y Valle Nevado son otro mercado (precio mediano ~357 mil CLP/noche, dependiente de la temporada de ski). Evidencia: [antes](../images/eda/05_mapa_precios_osm.png) / [después](../images/eda/06_mapa_precios_urbano.png) |

---

## Detalle: selección de variables (2026-11-18)

A partir de las 74 columnas que quedaron tras eliminar las de más de 90 % de nulos, se aplicaron tres criterios:

### 1. Se descartaron identificadores, URLs y texto libre
No aportan información para predecir el precio.

- Identificadores: `id`, `scrape_id`, `host_id`, `host_profile_id`
- URLs: `listing_url`, `picture_url`, `host_url`, `host_profile_url`, `host_picture_url`
- Texto libre: `name`, `description`, `host_name`, `host_about`, `host_location`
- Fechas de scraping: `last_scraped`, `calendar_last_scraped`

### 2. Se descartaron las columnas que filtran el precio (data leakage)
Se calculan a partir del precio. Si se usaran, el modelo "haría trampa": obtendría métricas excelentes en entrenamiento pero no serviría para anuncios nuevos.

- `price_quote_checkin_date`, `price_quote_checkout_date`, `price_quote_total_price`, `price_quote_price_per_night`, `price_quote_raw`
- `estimated_revenue_l365d`

### 3. Se conservaron las variables con poder explicativo

| Grupo | Variables |
|-------|-----------|
| Propiedad | `room_type`, `property_type`, `accommodates`, `bedrooms`, `beds`, `bathrooms_text` |
| Ubicación | `neighbourhood_cleansed`, `latitude`, `longitude` |
| Anfitrión | `host_is_superhost`, `host_listings_count`, `host_identity_verified` |
| Reseñas | `number_of_reviews`, `review_scores_rating`, `review_scores_location`, `reviews_per_month` |
| Disponibilidad | `minimum_nights`, `availability_365` |
| **Objetivo** | `price` |

Notas:
- `bathrooms_text` reemplazó a `bathrooms` (100 % vacía); el número se extrajo desde el texto (p. ej. "1.5 baths" → 1.5).
- El resto de columnas no listadas (variantes de noches mínimas/máximas, disponibilidad a 30/60/90 días, subpuntajes de reseñas, conteos de anuncios por tipo) se dejaron fuera por redundantes en esta primera versión.
