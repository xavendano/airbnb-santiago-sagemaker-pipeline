import json
import numpy as np

# --- 1. Eliminar precios sospechosos (solo para entrenar) ---
TOPE_HABITACION = 150_000      # CLP/noche, habitaciones privadas o compartidas
TOPE_POR_HUESPED = 150_000     # CLP/noche por huésped, unidades completas

es_habitacion = df_modelo["room_type"].isin(["Private room", "Shared room"])
es_completa = df_modelo["room_type"] == "Entire home/apt"
precio_por_huesped = df_modelo["price"] / df_modelo["accommodates"].clip(lower=1)

sospechoso = (es_habitacion & (df_modelo["price"] > TOPE_HABITACION)) | \
             (es_completa & (precio_por_huesped > TOPE_POR_HUESPED))

print(f"Precios sospechosos eliminados: {sospechoso.sum()} "
      f"(habitaciones: {(es_habitacion & sospechoso).sum()}, completas: {(es_completa & sospechoso).sum()})")
df_modelo = df_modelo[~sospechoso].copy()

# --- 2. Variables premium ---
# Se traen desde df (el CSV tras quitar columnas vacías), alineando por índice
extra = df.loc[df_modelo.index, ["amenities", "name", "calculated_host_listings_count_entire_homes"]]

amenities = extra["amenities"].fillna("[]").apply(lambda s: [a.lower() for a in json.loads(s)])
df_modelo["n_amenities"] = amenities.apply(len)

amenities_clave = {
    "tiene_estacionamiento": "free parking",
    "tiene_aire":            "air conditioning",
    "tiene_piscina":         "pool",
    "tiene_jacuzzi":         "hot tub",
    "tiene_gimnasio":        "gym",
    "tiene_lavavajillas":    "dishwasher",
    "tiene_calefaccion":     "heating",
}
for col, texto in amenities_clave.items():
    df_modelo[col] = amenities.apply(lambda lista: int(any(texto in a for a in lista)))

# Distancia en km al barrio El Golf (Las Condes)
EL_GOLF = (-33.4150, -70.5983)
def distancia_km(lat, lon, punto):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat, lon, punto[0], punto[1]])
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * np.arcsin(np.sqrt(a))
df_modelo["dist_el_golf_km"] = distancia_km(df_modelo["latitude"], df_modelo["longitude"], EL_GOLF)

df_modelo["titulo_premium"] = (extra["name"].fillna("").str.lower()
                               .str.contains("lujo|luxury|premium|exclusiv").astype(int))
df_modelo["calculated_host_listings_count_entire_homes"] = extra["calculated_host_listings_count_entire_homes"]

print(df_modelo.shape)
print("Nulos restantes:", df_modelo.isnull().sum().sum())
