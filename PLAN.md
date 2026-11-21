# Plan de trabajo

El plan está ordenado por fases, según lo que hay que hacer, y no tiene fechas. Cada fase depende de la anterior. Se avanza en el orden de la lista, al ritmo que permita la agenda.

> **Principio rector:** bajo costo. Todo se prueba primero en Colab; a AWS solo pasa lo testeado.
>
> **Regla de cada sesión:** antes de cerrar → apagar recursos en AWS + registrar decisiones en `docs/decisiones.md` + commit en GitHub.

**Hitos:** el **MVP** se cumple al terminar la Fase 5. El **proyecto completo** se cumple al terminar la Fase 8.

## Fase 1 — Exploración en Colab ✅

- [x] Descargar `listings.csv.gz` de Santiago (Inside Airbnb) en `data/raw/`
- [x] Anotar fecha del snapshot en `data/README.md` (septiembre 2026)
- [x] EDA: forma, nulos, distribución de `price`, outliers → [hallazgos](docs/hallazgos_eda.md)
- [x] Crear repo en GitHub con `.gitignore` y README → [xavendano/airbnb-santiago-sagemaker-pipeline](https://github.com/xavendano/airbnb-santiago-sagemaker-pipeline) (privado)

## Fase 2 — Limpieza y modelo base en Colab

- [x] Limpieza como funciones (precio, nulos, outliers, categóricas)
- [x] Elegir variables finales
- [ ] One-hot encoding de `room_type`, `property_type`, `neighbourhood_cleansed`
- [ ] XGBoost de referencia en Colab (métrica base)
- [ ] Commit del notebook en `notebooks/`

## Fase 3 — Montar AWS ⚠️ puede alargarse

- [ ] Alerta en AWS Budgets
- [ ] Usuario IAM con MFA
- [ ] Bucket S3 con `raw/`, `processed/`, `output/`
- [ ] Dominio de SageMaker Studio
- [ ] Subir CSV crudo a `raw/`

## Fase 4 — Limpieza en SageMaker

- [ ] Pasar funciones a `src/preprocess.py`
- [ ] Ejecutar desde Studio y guardar en `processed/`
- [ ] Recordar: XGBoost integrado pide CSV **sin encabezado y con el target en la primera columna**

## Fase 5 — Entrenamiento (MVP ✅)

- [ ] Training job con XGBoost
- [ ] Comparar contra métrica de Colab
- [ ] Batch transform de prueba
- [ ] Capturas + README v1
- [ ] **Apagar todo**

## Fase 6 — Pipeline ⚠️ puede alargarse

- [ ] SageMaker Pipelines: processing step + training step
- [ ] Ejecución de punta a punta
- [ ] Evaluation step + registro del modelo
- [ ] Captura del grafo del pipeline
- [ ] Captura de Cost Explorer

## Fase 7 — Demo

- [ ] Descargar modelo desde S3
- [ ] App Gradio en Hugging Face Spaces

## Fase 8 — Cierre

- [ ] README final: diagrama, decisiones, costo real, aprendizajes
- [ ] Grabar video (3–5 min)
- [ ] Borrador de post en LinkedIn

## Pendientes sueltos

- [x] Copiar desde Google Drive a `images/eda/` los gráficos 02, 03, 04 y 07 y enlazarlos en el README y en `docs/hallazgos_eda.md`
- [ ] Revisar `images/eda/01_distribucion_precios_crudos.png`: muestra los precios crudos pero los títulos dicen "Precio limpio". Regenerarlo con el título correcto o eliminarlo (el README usa `01_distribucion_precios.png`)
