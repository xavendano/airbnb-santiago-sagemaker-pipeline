# Registro de experimentos

Cada entrenamiento del modelo se registra aquí con sus cambios y sus métricas, para comparar versiones y saber qué mejoró el resultado. Las decisiones que justifican cada cambio están en [decisiones.md](decisiones.md).

## Configuración común

Salvo que la tabla diga otra cosa, todas las versiones usan:

| Parámetro          | Valor                                                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Entorno            | Google Colab                                                                                                                |
| Modelo             | XGBoost (`XGBRegressor`)                                                                                                    |
| Variable objetivo  | `log1p(price)`; las métricas se calculan en CLP tras `expm1`                                                                |
| Split              | 80/20 entrenamiento/prueba, `random_state=42`                                                                               |
| Hiperparámetros    | `n_estimators=500`, `learning_rate=0.05`, `max_depth=6`, `subsample=0.8`, `colsample_bytree=0.8`                            |
| Categóricas        | One-hot de `room_type`, `property_type` (< 50 anuncios → "Otro") y `neighbourhood_cleansed` (< 30 anuncios → "Otra comuna") |
| Referencia ingenua | Predecir siempre la mediana del precio de entrenamiento (columna "MAE mediana")                                             |

## Resultados

| Versión | Fecha      | Cambios respecto a la anterior                                                                                                                                                                                                                                |  Filas | Columnas |  MAE (CLP) | RMSE (CLP) |        R² | MAE mediana (CLP) | Notas                                                                                                                                                                                                                       |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -----: | -------: | ---------: | ---------: | --------: | ----------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| v1      | 2026-11-21 | Modelo base: 18 variables + one-hot (umbrales 50/30), sin filtro de precios sospechosos                                                                                                                                                                       | 17.256 |       60 |     14.533 |     30.201 |     0,595 |            27.794 | El error se concentra en el quintil más caro (~36 mil de MAE vs 7–12 mil en el resto). Los peores casos: habitaciones privadas a 320–416 mil y unidades completas de Las Condes/Vitacura a 450–500 mil predichas en ~90 mil |
| v2      | 2026-11-21 | + Filtro de precios sospechosos (78 anuncios: habitaciones > 150 mil, completas > 150 mil por huésped) + 11 variables premium (`n_amenities`, 7 indicadores de amenities, `dist_el_golf_km`, `titulo_premium`, `calculated_host_listings_count_entire_homes`) | 17.178 |       71 | **13.109** | **25.915** | **0,673** |            27.215 | MAE −9,8 % y R² +0,078 vs v1. En una prueba aparte (validación cruzada de 5 folds), la mayor parte de la mejora viene del filtro; las variables premium aportan ~3 % de MAE adicional                                       |
| v3      | 2026-11-21 | Ajuste de hiperparámetros, uno a la vez con validación cruzada de 5 folds sobre el train: `max_depth=8`, `colsample_bytree=0.6`, `reg_lambda=10` (el resto igual a v2)                                                                                        | 17.178 |       71 | **13.017** | **25.842** | **0,675** |            27.215 | Mejora pequeña frente a v2 (MAE −0,7 %). Los datos y las variables pesan más que los hiperparámetros                                                                                                                        |

> **Ojo al comparar:** v2 se evalúa sobre un conjunto de prueba sin los 78 precios sospechosos, así que parte de la mejora viene de quitar casos imposibles de predecir, no solo de un mejor modelo.

## Próximos experimentos

| Versión | Idea                                                                           | Estado    |
| ------- | ------------------------------------------------------------------------------ | --------- |
| —       | Mismo modelo entrenado en SageMaker (training job), para comparar contra Colab | Pendiente |

## Cómo agregar un experimento

1. Agregar una fila a **Resultados** con la siguiente versión (v3, v4…), la fecha y solo lo que cambió respecto a la anterior.
2. Si cambian los hiperparámetros o el split, anotarlos en la columna "Cambios" (la configuración común queda como está).
3. Si el cambio implica una decisión nueva (datos, variables, modelo), registrarla también en [decisiones.md](decisiones.md).
