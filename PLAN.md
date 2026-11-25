# Plan de trabajo

El plan está ordenado por fases, según lo que hay que hacer, y no tiene fechas. Cada fase depende de la anterior.

> **Principio rector:** Bajo costo. Todo se prueba primero en Colab; a AWS solo pasa lo testeado.
>
> **Regla de cada sesión:** Antes de cerrar, registrar decisiones en `docs/decisiones.md` y hacer commit en GitHub.

> **Alcance de este repositorio:** Cubre las Fases 1 a 3 (análisis, limpieza y entrenamiento en Colab) y está cerrado. La Fase 4 se explicará en otra plataforma, todavía por definir.

## Fase 1 - Exploración en Colab ✅

- [x] Descargar `listings.csv.gz` de Santiago (Inside Airbnb) en `data/raw/`
- [x] Anotar fecha del snapshot en `data/README.md` (septiembre 2026)
- [x] EDA: Forma, nulos, distribución de `price`, outliers → [hallazgos](docs/hallazgos_eda.md)
- [x] Crear repo en GitHub con `.gitignore` y README → [xavendano/airbnb-santiago-sagemaker-pipeline](https://github.com/xavendano/airbnb-santiago-sagemaker-pipeline) (privado)

## Fase 2 - Limpieza y modelo base en Colab ✅

- [x] Limpieza como funciones (precio, nulos, outliers, categóricas)
- [x] Elegir variables finales
- [x] One-hot encoding de `room_type`, `property_type`, `neighbourhood_cleansed`
- [x] XGBoost de referencia en Colab (métrica base, v1)

## Fase 3 - Entrenamiento en Colab ✅

- [x] Filtro de precios sospechosos y variables premium (v2)
- [x] Ajuste de hiperparámetros con validación cruzada (v3)
- [x] Learning rate más bajo con early stopping (v4 a v6)
- [x] Elegir el modelo final (v5) y registrar todas las versiones en [experimentos](docs/experimentos.md)
- [x] Commit del notebook en `notebooks/`

## Fase 4 - Ejecución en AWS

Se verá en otra plataforma, todavía por definir. Ver la sección [Próxima etapa: Despliegue en SageMaker](README.md#próxima-etapa-despliegue-en-sagemaker) del README.
