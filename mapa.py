import streamlit as st
import folium
from streamlit_folium import st_folium
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

    for idx, row in df.iterrows():
        popup_html = "<div style='width:320px; font-family:Arial, sans-serif; font-size:14px;'>"
        popup_html += f"<b>Tipo:</b> {row['tipo']}<br><b>Data:</b> {row['data']}<br><b>Bairro:</b> {row['bairro']}<hr>"

        for i, envolvido in enumerate(row['envolvidos'], 1):
            icone = RESULTADO_ICONES.get(envolvido.get("resultado", ""), "")
            cor_resultado = {
                "Óbito": "#e15759",
                "Ferimentos": "#f28e2b",
                "Sem Ferimentos": "#59a14f"
            }.get(envolvido.get("resultado", ""), "black")

            popup_html += f"<div style='margin-bottom:10px; padding:5px; border:1px solid #ccc; border-radius:5px; background-color:#fff;'>"
            popup_html += f"<b>Envolvido {i}:</b><br>"
            popup_html += f"Tipo: {envolvido.get('tipo', '')}<br>"
            nome = envolvido.get("nome", "N/A")
            popup_html += f"Nome: {nome}<br>"
            if "veiculo" in envolvido:
                popup_html += f"Veículo: {envolvido.get('veiculo')}<br>"
            if "placa" in envolvido:
                popup_html += f"Placa: {envolvido.get('placa')}<br>"
            popup_html += f"<b style='color:{cor_resultado}'>Resultado: {icone} {envolvido.get('resultado')}</b>"
            popup_html += "</div>"

        popup_html += "</div>"

        icon_color = 'green'
        resultados = [e.get("resultado", "") for e in row['envolvidos']]
        if "Óbito" in resultados:
            icon_color = 'red'
        elif "Ferimentos" in resultados:
            icon_color = 'orange'

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=350),
            icon=folium.Icon(color=icon_color, icon='info-sign')
        ).add_to(m)

    return m

def show_map(df):
    st.title("SINISTROS DE TRÂNSITO COM ÓBITOS - CURITIBA")
    mapa = mapa_sinistros(df)
    st_folium(mapa, width=900, height=600)
