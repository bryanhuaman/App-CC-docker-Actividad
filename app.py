import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timezone

st.set_page_config(page_title="FIFA World Cup 2026", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.hero {
    background: linear-gradient(135deg, #041a0c 0%, #0a2d14 50%, #041a0c 100%);
    border-radius: 16px; padding: 2.5rem 2rem; margin-bottom: 1.5rem; text-align: center;
}
.hero h1 { font-family: 'Bebas Neue', sans-serif; font-size: 3.5rem; color: #fff; letter-spacing: 3px; margin-bottom: 0.3rem; }
.hero h1 span { color: #D4A017; }
.hero p { color: rgba(255,255,255,0.6); font-size: 0.95rem; }
.metric-card { background: #161616; border: 1px solid #2a2a2a; border-radius: 12px; padding: 1.2rem; text-align: center; }
.metric-num { font-family: 'Bebas Neue', sans-serif; font-size: 2.8rem; color: #00e676; line-height: 1; }
.metric-lbl { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
.group-card { background: #161616; border: 1px solid #2a2a2a; border-radius: 12px; overflow: hidden; margin-bottom: 0.8rem; }
.group-header { padding: 0.5rem 1rem; font-family: 'Bebas Neue', sans-serif; font-size: 1rem; letter-spacing: 1.5px; }
.result-card { background: #0a2d14; border: 1px solid #1a7a3c; border-radius: 12px; padding: 1.2rem; text-align: center; margin-top: 1rem; }
.winner-badge { background: #D4A017; color: #000; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; display: inline-block; margin-top: 0.5rem; }
.sede-card { background: #161616; border: 1px solid #2a2a2a; border-radius: 10px; padding: 0.9rem; height: 100%; }
</style>
""", unsafe_allow_html=True)

GRUPOS = {
    "A": {"equipos": ["Mexico", "Sudafrica", "Corea del Sur", "Rep. Checa"],       "color": "#1a7a3c"},
    "B": {"equipos": ["Canada", "Suiza", "Qatar", "Bosnia y Herz."],               "color": "#c0392b"},
    "C": {"equipos": ["Brasil", "Marruecos", "Escocia", "Haiti"],                  "color": "#D4A017"},
    "D": {"equipos": ["Estados Unidos", "Paraguay", "Australia", "Turquia"],       "color": "#185FA5"},
    "E": {"equipos": ["Alemania", "Ecuador", "Costa de Marfil", "Curazao"],        "color": "#0f6e56"},
    "F": {"equipos": ["Paises Bajos", "Japon", "Tunez", "Suecia"],                 "color": "#534AB7"},
    "G": {"equipos": ["Belgica", "Egipto", "Iran", "Nueva Zelanda"],               "color": "#1a7a3c"},
    "H": {"equipos": ["Espana", "Uruguay", "Arabia Saudita", "Cabo Verde"],        "color": "#c0392b"},
    "I": {"equipos": ["Francia", "Senegal", "Noruega", "Irak"],                    "color": "#D4A017"},
    "J": {"equipos": ["Argentina", "Argelia", "Austria", "Jordania"],              "color": "#185FA5"},
    "K": {"equipos": ["Portugal", "Colombia", "Uzbekistan", "RD del Congo"],       "color": "#0f6e56"},
    "L": {"equipos": ["Inglaterra", "Croacia", "Ghana", "Panama"],                 "color": "#534AB7"},
}

FLAGS = {
    "Mexico": "MX", "Sudafrica": "ZA", "Corea del Sur": "KR", "Rep. Checa": "CZ",
    "Canada": "CA", "Suiza": "CH", "Qatar": "QA", "Bosnia y Herz.": "BA",
    "Brasil": "BR", "Marruecos": "MA", "Escocia": "GB-SCT", "Haiti": "HT",
    "Estados Unidos": "US", "Paraguay": "PY", "Australia": "AU", "Turquia": "TR",
    "Alemania": "DE", "Ecuador": "EC", "Costa de Marfil": "CI", "Curazao": "CW",
    "Paises Bajos": "NL", "Japon": "JP", "Tunez": "TN", "Suecia": "SE",
    "Belgica": "BE", "Egipto": "EG", "Iran": "IR", "Nueva Zelanda": "NZ",
    "Espana": "ES", "Uruguay": "UY", "Arabia Saudita": "SA", "Cabo Verde": "CV",
    "Francia": "FR", "Senegal": "SN", "Noruega": "NO", "Irak": "IQ",
    "Argentina": "AR", "Argelia": "DZ", "Austria": "AT", "Jordania": "JO",
    "Portugal": "PT", "Colombia": "CO", "Uzbekistan": "UZ", "RD del Congo": "CD",
    "Inglaterra": "GB-ENG", "Croacia": "HR", "Ghana": "GH", "Panama": "PA",
}

SEDES = [
    {"ciudad": "Ciudad de Mexico", "estadio": "Estadio Azteca",    "pais": "Mexico",  "cap": 83000, "nota": "INAUGURACION"},
    {"ciudad": "Guadalajara",      "estadio": "Estadio Akron",     "pais": "Mexico",  "cap": 48000, "nota": ""},
    {"ciudad": "Monterrey",        "estadio": "Estadio BBVA",      "pais": "Mexico",  "cap": 53500, "nota": ""},
    {"ciudad": "Toronto",          "estadio": "BMO Field",         "pais": "Canada",  "cap": 45000, "nota": ""},
    {"ciudad": "Vancouver",        "estadio": "BC Place",          "pais": "Canada",  "cap": 54000, "nota": ""},
    {"ciudad": "Nueva York/NJ",    "estadio": "MetLife Stadium",   "pais": "EE.UU.",  "cap": 82500, "nota": "FINAL"},
    {"ciudad": "Dallas/Arlington", "estadio": "AT&T Stadium",      "pais": "EE.UU.",  "cap": 94000, "nota": ""},
    {"ciudad": "Los Angeles",      "estadio": "SoFi Stadium",      "pais": "EE.UU.",  "cap": 70000, "nota": ""},
    {"ciudad": "San Francisco",    "estadio": "Levi's Stadium",    "pais": "EE.UU.",  "cap": 68500, "nota": ""},
    {"ciudad": "Miami",            "estadio": "Hard Rock Stadium", "pais": "EE.UU.",  "cap": 65000, "nota": ""},
    {"ciudad": "Atlanta",          "estadio": "Mercedes-Benz",     "pais": "EE.UU.",  "cap": 71000, "nota": ""},
    {"ciudad": "Boston",           "estadio": "Gillette Stadium",  "pais": "EE.UU.",  "cap": 65000, "nota": ""},
    {"ciudad": "Seattle",          "estadio": "Lumen Field",       "pais": "EE.UU.",  "cap": 69000, "nota": ""},
    {"ciudad": "Houston",          "estadio": "NRG Stadium",       "pais": "EE.UU.",  "cap": 72220, "nota": ""},
    {"ciudad": "Kansas City",      "estadio": "Arrowhead Stadium", "pais": "EE.UU.",  "cap": 73000, "nota": ""},
    {"ciudad": "Filadelfia",       "estadio": "Lincoln Financial", "pais": "EE.UU.",  "cap": 69000, "nota": ""},
]

PARTIDOS_J1 = [
    {"grupo": "A", "eq1": "Mexico",         "eq2": "Sudafrica",  "fecha": "11 Jun", "sede": "Ciudad de Mexico"},
    {"grupo": "A", "eq1": "Corea del Sur",  "eq2": "Rep. Checa", "fecha": "11 Jun", "sede": "Guadalajara"},
    {"grupo": "B", "eq1": "Canada",         "eq2": "Suiza",      "fecha": "12 Jun", "sede": "Toronto"},
    {"grupo": "C", "eq1": "Brasil",         "eq2": "Marruecos",  "fecha": "13 Jun", "sede": "Nueva York/NJ"},
    {"grupo": "D", "eq1": "Estados Unidos", "eq2": "Turquia",    "fecha": "13 Jun", "sede": "Los Angeles"},
    {"grupo": "E", "eq1": "Alemania",       "eq2": "Curazao",    "fecha": "14 Jun", "sede": "Houston"},
]

# COUNTDOWN - sin f-strings anidados
inicio  = datetime(2026, 6, 11, 13, 0, 0, tzinfo=timezone.utc)
ahora   = datetime.now(timezone.utc)
diff    = inicio - ahora
dias    = max(diff.days, 0)
horas   = max(diff.seconds // 3600, 0)
minutos = max((diff.seconds % 3600) // 60, 0)

BOX_STYLE = "display:inline-block;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);border-radius:10px;padding:12px 18px;text-align:center;min-width:72px;margin:4px;"
NUM_STYLE = "font-family:sans-serif;font-size:2rem;color:#fff;line-height:1;display:block;"
LBL_STYLE = "font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:1px;text-transform:uppercase;"

def make_cd_box(valor, etiqueta):
    return (
        '<div style="' + BOX_STYLE + '">'
        + '<span style="' + NUM_STYLE + '">' + str(valor) + '</span>'
        + '<span style="' + LBL_STYLE + '">' + etiqueta + '</span>'
        + '</div>'
    )

cd_html = make_cd_box(dias, "Dias") + make_cd_box(horas, "Horas") + make_cd_box(minutos, "Min")

hero_html = (
    '<div class="hero">'
    + '<div style="display:inline-block;background:#D4A017;color:#000;font-size:11px;font-weight:700;letter-spacing:2px;padding:4px 14px;border-radius:20px;margin-bottom:12px;">FIFA WORLD CUP 2026</div>'
    + '<h1>EL MUNDIAL MAS GRANDE <span>DE LA HISTORIA</span></h1>'
    + '<p>Estados Unidos &nbsp; Mexico &nbsp; Canada &nbsp;|&nbsp; 11 JUN - 19 JUL 2026</p>'
    + '<div style="display:flex;justify-content:center;flex-wrap:wrap;margin-top:1.5rem;">'
    + cd_html
    + '</div>'
    + '</div>'
)

st.markdown(hero_html, unsafe_allow_html=True)

# METRICAS
c1, c2, c3, c4, c5, c6 = st.columns(6)
for col, num, lbl in zip(
    [c1, c2, c3, c4, c5, c6],
    ["48", "104", "16", "3", "39", "4"],
    ["Selecciones", "Partidos", "Sedes", "Paises", "Dias", "Debutantes"]
):
    col.markdown(
        '<div class="metric-card">'
        + '<div class="metric-num">' + num + '</div>'
        + '<div class="metric-lbl">' + lbl + '</div>'
        + '</div>',
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Grupos", "Sedes", "Estadisticas", "Simulador de Resultados", "Formato"])

# TAB 1 GRUPOS
with tab1:
    st.subheader("Los 12 Grupos del Mundial 2026")
    st.caption("12 grupos de 4 equipos · Los 2 primeros + 8 mejores terceros avanzan")

    keys = list(GRUPOS.keys())
    for i in range(0, len(keys), 4):
        cols = st.columns(4)
        for j, key in enumerate(keys[i:i+4]):
            g = GRUPOS[key]
            eq_rows = ""
            for eq in g["equipos"]:
                eq_rows += '<div style="padding:7px 12px;font-size:13px;border-top:1px solid #2a2a2a;">' + eq + '</div>'
            txt_color = "#000" if key in ["C", "I"] else "#fff"
            card = (
                '<div class="group-card">'
                + '<div class="group-header" style="background:' + g["color"] + ';color:' + txt_color + ';">GRUPO ' + key + '</div>'
                + eq_rows
                + '</div>'
            )
            with cols[j]:
                st.markdown(card, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Buscar equipo en los grupos")
    busqueda = st.text_input("Escribe el nombre de un pais:", placeholder="Ej: Argentina, Francia, Brasil...")
    if busqueda:
        encontrado = False
        for key, g in GRUPOS.items():
            for eq in g["equipos"]:
                if busqueda.lower() in eq.lower():
                    st.success(eq + " esta en el Grupo " + key)
                    rivales = [e for e in g["equipos"] if e != eq]
                    st.write("Sus rivales:")
                    for r in rivales:
                        st.write("  · " + r)
                    encontrado = True
        if not encontrado:
            st.warning("No se encontro '" + busqueda + "'. Escribe el nombre sin tildes.")

# TAB 2 SEDES
with tab2:
    st.subheader("Las 16 Sedes del Mundial")
    filtro = st.selectbox("Filtrar por pais:", ["Todos", "Mexico", "Canada", "EE.UU."])
    sedes_f = SEDES if filtro == "Todos" else [s for s in SEDES if filtro in s["pais"]]

    cols4 = st.columns(4)
    for idx, s in enumerate(sedes_f):
        color_p = "#1a7a3c" if s["pais"] == "Mexico" else "#c0392b"
        if s["nota"] == "INAUGURACION":
            nota_h = '<div style="background:#D4A017;color:#000;font-size:9px;font-weight:700;padding:2px 8px;border-radius:3px;display:inline-block;margin-top:6px;">INAUGURACION</div>'
        elif s["nota"] == "FINAL":
            nota_h = '<div style="background:#c0392b;color:#fff;font-size:9px;font-weight:700;padding:2px 8px;border-radius:3px;display:inline-block;margin-top:6px;">FINAL</div>'
        else:
            nota_h = ""
        card = (
            '<div class="sede-card">'
            + '<div style="font-size:10px;font-weight:600;letter-spacing:1px;color:' + color_p + ';margin-bottom:4px;">' + s["pais"] + '</div>'
            + '<div style="font-weight:600;font-size:15px;">' + s["ciudad"] + '</div>'
            + '<div style="font-size:12px;color:#888;margin-top:2px;">' + s["estadio"] + '</div>'
            + '<div style="font-size:12px;color:#00e676;font-weight:500;margin-top:4px;">' + str(s["cap"]) + ' espectadores</div>'
            + nota_h
            + '</div>'
        )
        with cols4[idx % 4]:
            st.markdown(card, unsafe_allow_html=True)
            st.write("")

    st.markdown("---")
    st.subheader("Capacidad por Estadio")
    df_s = pd.DataFrame(SEDES).sort_values("cap", ascending=True)
    colores_bar = ["#1a7a3c" if p == "Mexico" else ("#c0392b" if p == "Canada" else "#185FA5") for p in df_s["pais"]]
    fig_s = go.Figure(go.Bar(
        x=df_s["cap"], y=df_s["ciudad"], orientation="h",
        marker_color=colores_bar,
        text=[str(c) for c in df_s["cap"]], textposition="outside"
    ))
    fig_s.update_layout(
        paper_bgcolor="#0d0d0d", plot_bgcolor="#161616", font_color="#f0f0f0",
        height=520, margin=dict(l=10, r=80, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor="#2a2a2a"),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_s, use_container_width=True)

# TAB 3 ESTADISTICAS
with tab3:
    st.subheader("Estadisticas del Mundial 2026")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Clasificados por Confederacion")
        df_conf = pd.DataFrame({
            "Confederacion": ["UEFA", "CAF", "AFC", "CONMEBOL", "CONCACAF", "OFC"],
            "Equipos": [16, 10, 9, 6, 6, 1]
        })
        fig_conf = px.bar(
            df_conf, x="Confederacion", y="Equipos", color="Confederacion",
            color_discrete_map={"UEFA": "#185FA5", "CAF": "#c0392b", "AFC": "#D4A017",
                                "CONMEBOL": "#1a7a3c", "CONCACAF": "#534AB7", "OFC": "#888"},
            text="Equipos"
        )
        fig_conf.update_traces(textposition="outside")
        fig_conf.update_layout(
            paper_bgcolor="#0d0d0d", plot_bgcolor="#161616", font_color="#f0f0f0",
            showlegend=False, height=320, margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_conf, use_container_width=True)

    with col_b:
        st.markdown("#### Sedes por Pais Anfitrion")
        fig_pie = px.pie(
            values=[11, 3, 2], names=["EE.UU.", "Mexico", "Canada"],
            color_discrete_sequence=["#c0392b", "#1a7a3c", "#185FA5"], hole=0.45
        )
        fig_pie.update_layout(paper_bgcolor="#0d0d0d", font_color="#f0f0f0",
                               height=320, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Evolucion historica de participantes")
    df_hist = pd.DataFrame({
        "Anio":    [1930,1934,1938,1950,1954,1958,1962,1966,1970,1974,1978,1982,1986,1990,1994,1998,2002,2006,2010,2014,2018,2022,2026],
        "Equipos": [13,  16,  15,  13,  16,  16,  16,  16,  16,  16,  16,  24,  24,  24,  24,  32,  32,  32,  32,  32,  32,  32,  48]
    })
    fig_hist = px.area(df_hist, x="Anio", y="Equipos", color_discrete_sequence=["#00e676"], markers=True)
    fig_hist.update_traces(fill="tozeroy", fillcolor="rgba(0,230,118,0.1)", line_width=2)
    fig_hist.update_layout(
        paper_bgcolor="#0d0d0d", plot_bgcolor="#161616", font_color="#f0f0f0",
        height=300, margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=True, gridcolor="#2a2a2a"),
        yaxis=dict(showgrid=True, gridcolor="#2a2a2a")
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Campeones del Mundo - historico")
    df_camp = pd.DataFrame({
        "Pais":    ["Brasil", "Alemania", "Italia", "Argentina", "Francia", "Uruguay", "Espana", "Inglaterra"],
        "Titulos": [5, 4, 4, 3, 2, 2, 1, 1]
    })
    fig_camp = px.bar(
        df_camp.sort_values("Titulos", ascending=True),
        x="Titulos", y="Pais", orientation="h",
        color="Titulos", color_continuous_scale=["#1a7a3c", "#D4A017"], text="Titulos"
    )
    fig_camp.update_traces(textposition="outside")
    fig_camp.update_layout(
        paper_bgcolor="#0d0d0d", plot_bgcolor="#161616", font_color="#f0f0f0",
        height=320, showlegend=False, coloraxis_showscale=False,
        margin=dict(l=0, r=40, t=10, b=0)
    )
    st.plotly_chart(fig_camp, use_container_width=True)

# TAB 4 SIMULADOR
with tab4:
    st.subheader("Simulador de Resultados")
    st.caption("Ingresa los marcadores y ve quien avanza")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Registrar Resultado")
        grupo_sel = st.selectbox("Grupo:", list(GRUPOS.keys()), format_func=lambda x: "Grupo " + x)
        equipos_g = GRUPOS[grupo_sel]["equipos"]
        eq1       = st.selectbox("Equipo 1:", equipos_g, index=0)
        eq2_opts  = [e for e in equipos_g if e != eq1]
        eq2       = st.selectbox("Equipo 2:", eq2_opts, index=0)

        cg1, cvs, cg2 = st.columns([2, 1, 2])
        with cg1:
            goles1 = st.number_input("Goles " + eq1[:8], min_value=0, max_value=20, value=0, step=1)
        with cvs:
            st.markdown("<br><h3 style='text-align:center;color:#888'>VS</h3>", unsafe_allow_html=True)
        with cg2:
            goles2 = st.number_input("Goles " + eq2[:8], min_value=0, max_value=20, value=0, step=1)

        fecha_p = st.text_input("Fecha:", placeholder="Ej: 11 Jun 2026")
        sede_p  = st.text_input("Sede:",  placeholder="Ej: Ciudad de Mexico")

        if st.button("Registrar Resultado", use_container_width=True):
            marcador = str(goles1) + " - " + str(goles2)
            if goles1 > goles2:
                ganador  = eq1
                tipo_res = "Victoria"
            elif goles2 > goles1:
                ganador  = eq2
                tipo_res = "Victoria"
            else:
                ganador  = "Empate"
                tipo_res = "Empate"

            if ganador != "Empate":
                badge = '<div class="winner-badge">GANADOR: ' + ganador + '</div>'
            else:
                badge = '<div class="winner-badge" style="background:#888;">EMPATE</div>'

            result_html = (
                '<div class="result-card">'
                + '<div style="font-size:0.9rem;color:#888;margin-bottom:8px;">Grupo ' + grupo_sel + ' | ' + fecha_p + ' | ' + sede_p + '</div>'
                + '<div style="font-size:1.6rem;font-weight:700;">'
                + eq1 + ' &nbsp; <span style="color:#D4A017;">' + marcador + '</span> &nbsp; ' + eq2
                + '</div>'
                + '<div style="margin-top:8px;color:#aaa;">' + tipo_res + '</div>'
                + badge
                + '</div>'
            )
            st.markdown(result_html, unsafe_allow_html=True)
            if goles1 != goles2:
                st.balloons()

    with col_right:
        st.markdown("### Tabla de Posiciones - Grupo " + grupo_sel)
        puntos_d = {}
        gf_d     = {}
        gc_d     = {}
        for eq in equipos_g:
            ca, cb, cc, cd = st.columns(4)
            with ca:
                st.markdown("<small>" + eq + "</small>", unsafe_allow_html=True)
            with cb:
                puntos_d[eq] = st.number_input("Pts", min_value=0, max_value=9,  value=0, step=1, key="pts_" + eq)
            with cc:
                gf_d[eq]     = st.number_input("GF",  min_value=0, max_value=30, value=0, step=1, key="gf_"  + eq)
            with cd:
                gc_d[eq]     = st.number_input("GC",  min_value=0, max_value=30, value=0, step=1, key="gc_"  + eq)

        if st.button("Ver Tabla", use_container_width=True):
            df_tabla = pd.DataFrame({
                "Equipo": equipos_g,
                "Pts": [puntos_d[e] for e in equipos_g],
                "GF":  [gf_d[e]    for e in equipos_g],
                "GC":  [gc_d[e]    for e in equipos_g],
            })
            df_tabla["DG"] = df_tabla["GF"] - df_tabla["GC"]
            df_tabla = df_tabla.sort_values(["Pts", "DG", "GF"], ascending=False).reset_index(drop=True)
            df_tabla.index += 1

            def highlight_top2(row):
                if row.name <= 2:
                    return ["background-color:#0a2d14;color:#00e676"] * len(row)
                return [""] * len(row)

            st.dataframe(df_tabla.style.apply(highlight_top2, axis=1), use_container_width=True)
            st.caption("Verde = clasifican directamente a 1/16 de final")

    st.markdown("---")
    st.subheader("Prediccion del Campeon")
    cp1, cp2 = st.columns(2)

    with cp1:
        todos        = [eq for g in GRUPOS.values() for eq in g["equipos"]]
        campeon_pred = st.selectbox("Quien crees que sera el campeon?", todos)
        razon        = st.text_area("Por que?", placeholder="Ej: Argentina llega como campeon vigente...")
        nombre_fan   = st.text_input("Tu nombre:", placeholder="Ej: Carlos")

        if st.button("Registrar Prediccion", use_container_width=True):
            if nombre_fan and razon:
                st.success("Prediccion registrada, " + nombre_fan + "!")
                pred_html = (
                    '<div style="background:#0a2d14;border:1px solid #1a7a3c;border-radius:12px;padding:1.2rem;margin-top:0.5rem;">'
                    + '<div style="color:#D4A017;font-weight:700;font-size:1.1rem;">' + nombre_fan + ' predice: ' + campeon_pred + '</div>'
                    + '<div style="color:#aaa;font-size:0.9rem;margin-top:8px;font-style:italic;">' + razon + '</div>'
                    + '</div>'
                )
                st.markdown(pred_html, unsafe_allow_html=True)
            else:
                st.warning("Escribe tu nombre y argumento.")

    with cp2:
        st.markdown("#### Partidos Jornada 1")
        for p in PARTIDOS_J1:
            row_html = (
                '<div style="background:#161616;border:1px solid #2a2a2a;border-radius:8px;padding:8px 12px;margin-bottom:6px;">'
                + '<span style="font-size:11px;color:#888;">Grupo ' + p["grupo"] + ' · ' + p["fecha"] + ' · ' + p["sede"] + '</span><br>'
                + '<span style="font-size:14px;">' + p["eq1"] + ' <b style="color:#D4A017;">vs</b> ' + p["eq2"] + '</span>'
                + '</div>'
            )
            st.markdown(row_html, unsafe_allow_html=True)

# TAB 5 FORMATO
with tab5:
    st.subheader("Formato y Calendario del Mundial 2026")
    cf1, cf2 = st.columns(2)

    with cf1:
        st.markdown("#### Nuevo Formato")
        items_fmt = [
            ("12 Grupos de 4",      "Primera vez con 48 equipos en la historia"),
            ("104 partidos totales", "+40 partidos vs Qatar 2022 (64 partidos)"),
            ("1/16 de final",       "Nueva ronda — 32 equipos compiten"),
            ("8 mejores terceros",  "Tambien clasifican a la siguiente ronda"),
            ("3 paises sede",       "Primera vez que 3 paises organizan juntos"),
        ]
        for titulo, desc in items_fmt:
            st.markdown(
                '<div style="background:#161616;border-left:3px solid #00e676;border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:8px;">'
                + '<div style="font-weight:600;font-size:14px;">' + titulo + '</div>'
                + '<div style="color:#888;font-size:12px;margin-top:2px;">' + desc + '</div>'
                + '</div>',
                unsafe_allow_html=True
            )

    with cf2:
        st.markdown("#### Linea de Tiempo")
        timeline = [
            ("5 Dic 2025",   "Sorteo de grupos",    "Kennedy Center, Washington D.C."),
            ("31 Mar 2026",  "Ultimos clasificados", "Suecia, Turquia, R. Checa, Bosnia, Congo, Irak"),
            ("11 Jun 2026",  "PARTIDO INAUGURAL",   "Mexico vs Sudafrica - Estadio Azteca"),
            ("27 Jun 2026",  "Fin fase de grupos",  "Jornada final de todos los grupos"),
            ("28 Jun-3 Jul", "1/16 de final",       "Primera ronda eliminatoria"),
            ("4-7 Jul",      "Octavos de final",    "16 equipos en juego"),
            ("9-11 Jul",     "Cuartos de final",    "Boston, Miami, Kansas City, LA"),
            ("14-15 Jul",    "Semifinales",         "Dallas y Atlanta"),
            ("18 Jul 2026",  "Tercer lugar",        "Ciudad por confirmar"),
            ("19 Jul 2026",  "GRAN FINAL",          "MetLife Stadium - Nueva York / Nueva Jersey"),
        ]
        for fecha_t, evento_t, detalle_t in timeline:
            es_clave = evento_t in ["PARTIDO INAUGURAL", "GRAN FINAL"]
            bc = "#D4A017" if es_clave else "#2a2a2a"
            bg = "#1a1000" if es_clave else "#161616"
            st.markdown(
                '<div style="background:' + bg + ';border:1px solid ' + bc + ';border-radius:8px;padding:8px 12px;margin-bottom:6px;display:flex;gap:12px;">'
                + '<div style="min-width:100px;font-size:11px;font-weight:600;color:#D4A017;">' + fecha_t + '</div>'
                + '<div>'
                + '<div style="font-size:13px;font-weight:500;">' + evento_t + '</div>'
                + '<div style="font-size:11px;color:#888;margin-top:2px;">' + detalle_t + '</div>'
                + '</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown("#### Comparativa de Mundiales")
    df_comp = pd.DataFrame({
        "Edicion":  ["Qatar 2022", "Rusia 2018", "Brasil 2014", "Sudafrica 2010", "USA/MEX/CAN 2026"],
        "Equipos":  [32, 32, 32, 32, 48],
        "Partidos": [64, 64, 64, 64, 104],
        "Sedes":    [8,  12, 12, 10, 16],
        "Dias":     [29, 32, 32, 30, 39],
    })
    st.dataframe(
        df_comp.style.highlight_max(subset=["Equipos", "Partidos", "Sedes", "Dias"], color="#0a2d14"),
        use_container_width=True, hide_index=True
    )

st.markdown("---")
st.markdown(
    '<div style="text-align:center;padding:1rem;color:#555;font-size:0.8rem;">'
    + 'FIFA World Cup 2026 — Dashboard Streamlit · Datos FIFA · 11 Jun - 19 Jul 2026'
    + '</div>',
    unsafe_allow_html=True
)
