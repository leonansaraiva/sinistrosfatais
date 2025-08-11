import folium
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import json


RESULTADO_ICONES = {
    "Óbito": "❌",
    "Ferimentos": "⚠️",
    "Sem Ferimentos": "✅"
}

def mapa_sinistros(df):
    with open('curitiba_limite.geojson', 'r', encoding='utf-8') as f:
        curitiba_geo = json.load(f)

    center_lat, center_lon = -25.4284, -49.2733

    coords = []
    for feature in curitiba_geo['features']:
        geom = feature['geometry']
        if geom['type'] == "Polygon":
            coords.extend(geom['coordinates'][0])
        elif geom['type'] == "MultiPolygon":
            for poly in geom['coordinates']:
                coords.extend(poly[0])

    lats = [c[1] for c in coords]
    lons = [c[0] for c in coords]
    bounds = [[min(lats), min(lons)], [max(lats), max(lons)]]

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        min_zoom=11,
        max_zoom=15,
        max_bounds=True
    )

    m.fit_bounds(bounds)
    m.options['maxBounds'] = bounds

    folium.GeoJson(curitiba_geo, name="Limite Curitiba", style_function=lambda x: {
        'fillColor': '#4e79a750',
        'color': '#4e79a7',
        'weight': 3,
        'fillOpacity': 0.1
    }).add_to(m)

    ignorados = 0

    for idx, row in df.iterrows():
        lat = row.get("Latitude")
        lon = row.get("Longitude")
        
        if pd.isna(lat) or pd.isna(lon):
            ignorados += 1
            continue
        if not pd.isna(lat) and not pd.isna(lon):
            st.write(f"Registro {idx}: Latitude={lat}, Longitude={lon}")
            # Aqui continua o código de adicionar o marcador...
        else:
            st.write(f"Registro {idx} ignorado por falta de coordenadas")

        popup_html = "<div style='width:320px; font-family:Arial, sans-serif; font-size:14px;'>"
        popup_html += f"<b>Ano:</b> {row.get('Ano', '')}<br>"
        popup_html += f"<b>Mês:</b> {row.get('Mês', '')}<br>"
        popup_html += f"<b>Protocolo BATEU:</b> {row.get('Protocolo BATEU', '')}<br>"
        popup_html += f"<b>Hora:</b> {row.get('Hora', '')}"
        popup_html += "</div>"

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=350),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    if ignorados > 0:
        st.warning(f"{ignorados} registros não foram exibidos no mapa por não conterem coordenadas válidas.")

    return m

def show_map(df):
    st.title("SINISTROS DE TRÂNSITO COM ÓBITOS - CURITIBA")
    mapa = mapa_sinistros(df)
    st_folium(mapa, width=900, height=600)
