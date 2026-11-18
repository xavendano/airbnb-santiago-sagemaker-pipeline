# Plan de trabajo

4–6 horas diarias, días hábiles. Inicio: **mié 18 nov**. MVP: **mar 24 nov**. Proyecto completo: **lun 30 nov**.

> **Principio rector:** bajo costo. Todo se prueba primero en Colab; a AWS solo pasa lo testeado.
>
> **Regla diaria:** antes de cerrar → apagar recursos en AWS + registrar decisiones en `docs/decisiones.md` + commit en GitHub.

## Semana 1 — Datos y MVP

### Mié 18 nov — Exploración en Colab

- [x] Descargar `listings.csv.gz` de Santiago (Inside Airbnb) en `data/raw/`
- [x] Anotar fecha del snapshot en `data/README.md` (septiembre 2026)
- [x] EDA: forma, nulos, distribución de `price`, outliers → [hallazgos](docs/hallazgos_eda.md)
- [x] Crear repo en GitHub con `.gitignore` y README → [xavendano/airbnb-santiago-sagemaker-pipeline](https://github.com/xavendano/airbnb-santiago-sagemaker-pipeline) (privado)

### Jue 19 nov — Limpieza en Colab

- [x] Limpieza como funciones (precio, nulos, outliers, categóricas) — _adelantado el mié 18_
- [ ] One-hot encoding de `room_type`, `property_type`, `neighbourhood_cleansed`
- [x] Elegir variables finales — _adelantado el mié 18_
- [ ] XGBoost de referencia en Colab (métrica base)
- [ ] Commit del notebook

### Vie 20 nov — Montar AWS ⚠️ puede alargarse

- [ ] Alerta en AWS Budgets
- [ ] Usuario IAM con MFA
- [ ] Bucket S3 con `raw/`, `processed/`, `output/`
- [ ] Dominio de SageMaker Studio
- [ ] Subir CSV crudo a `raw/`

### Lun 23 nov — Limpieza en SageMaker

- [ ] Pasar funciones a `src/preprocess.py`
- [ ] Ejecutar desde Studio y guardar en `processed/`
- [ ] Recordar: XGBoost integrado pide CSV **sin encabezado y con el target en la primera columna**

### Mar 24 nov — Entrenamiento (MVP ✅)

- [ ] Training job con XGBoost
- [ ] Comparar contra métrica de Colab
- [ ] Batch transform de prueba
- [ ] Capturas + README v1
- [ ] **Apagar todo**

## Semana 2 — Automatización y vitrina

### Mié 25 nov — Pipeline, parte 1 ⚠️ puede alargarse

- [ ] SageMaker Pipelines: processing step + training step
- [ ] Ejecución de punta a punta

### Jue 26 nov — Pipeline, parte 2 (día con margen)

- [ ] Evaluation step + registro del modelo
- [ ] Captura del grafo del pipeline
- [ ] Captura de Cost Explorer

### Vie 27 nov — Demo

- [ ] Descargar modelo desde S3
- [ ] App Gradio en Hugging Face Spaces

### Lun 30 nov — Cierre

- [ ] README final: diagrama, decisiones, costo real, aprendizajes
- [ ] Grabar video (3–5 min)
- [ ] Borrador de post en LinkedIn

## Pendientes

- [x] Copiar desde Google Drive a `images/eda/` los gráficos 02, 03, 04 y 07 y enlazarlos en el README y en `docs/hallazgos_eda.md`
- [ ] Revisar `images/eda/01_distribucion_precios_crudos.png`: muestra los precios crudos pero los títulos dicen "Precio limpio". Regenerarlo con el título correcto o eliminarlo (el README usa `01_distribucion_precios.png`)
