import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timezone

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FIFA World Cup 2026",
    page_icon="⚽",
    layout="wide"
)

# ─────────────────────────────────────────────
# CSS PERSONALIZADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #041a0c 0%, #0a2d14 50%, #041a0c 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    color: #fff;
    letter-spacing: 3px;
    margin-bottom: 0.3rem;
}
.hero h1 span { color: #D4A017; }
.hero p { color: rgba(255,255,255,0.6); font-size: 0.95rem; }

.metric-card {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.metric-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    color: #00e676;
    line-height: 1;
}
.metric-lbl { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

.group-card {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 0.8rem;
}
.group-header {
    padding: 0.5rem 1rem;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    letter-spacing: 1.5px;
}
.result-card {
    background: #0a2d14;
    border: 1px solid #1a7a3c;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    margin-top: 1rem;
}
.winner-badge {
    background: #D4A017;
    color: #000;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
    margin-top: 0.5rem;
}
.sede-card {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 0.9rem;
    height: 100%;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATOS
# ─────────────────────────────────────────────
GRUPOS = {
    "A": {"equipos": ["🇲🇽 México", "🇿🇦 Sudáfrica", "🇰🇷 Corea del Sur", "🇨🇿 Rep. Checa"], "color": "#1a7a3c"},
    "B": {"equipos": ["🇨🇦 Canadá", "🇨🇭 Suiza", "🇶🇦 Qatar", "🇧🇦 Bosnia y Herz."], "color": "#c0392b"},
    "C": {"equipos": ["🇧🇷 Brasil", "🇲🇦 Marruecos", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia", "🇭🇹 Haití"], "color": "#D4A017"},
    "D": {"equipos": ["🇺🇸 Estados Unidos", "🇵🇾 Paraguay", "🇦🇺 Australia", "🇹🇷 Turquía"], "color": "#185FA5"},
    "E": {"equipos": ["🇩🇪 Alemania", "🇪🇨 Ecuador", "🇨🇮 Costa de Marfil", "🇨🇼 Curazao"], "color": "#0f6e56"},
    "F": {"equipos": ["🇳🇱 Países Bajos", "🇯🇵 Japón", "🇹🇳 Túnez", "🇸🇪 Suecia"], "color": "#534AB7"},
    "G": {"equipos": ["🇧🇪 Bélgica", "🇪🇬 Egipto", "🇮🇷 Irán", "🇳🇿 Nueva Zelanda"], "color": "#1a7a3c"},
    "H": {"equipos": ["🇪🇸 España ⭐", "🇺🇾 Uruguay ⭐", "🇸🇦 Arabia Saudita", "🇨🇻 Cabo Verde"], "color": "#c0392b"},
    "I": {"equipos": ["🇫🇷 Francia ⭐", "🇸🇳 Senegal", "🇳🇴 Noruega", "🇮🇶 Irak"], "color": "#D4A017"},
    "J": {"equipos": ["🇦🇷 Argentina ⭐⭐", "🇩🇿 Argelia", "🇦🇹 Austria", "🇯🇴 Jordania"], "color": "#185FA5"},
    "K": {"equipos": ["🇵🇹 Portugal", "🇨🇴 Colombia", "🇺🇿 Uzbekistán", "🇨🇩 RD del Congo"], "color": "#0f6e56"},
    "L": {"equipos": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "🇭🇷 Croacia", "🇬🇭 Ghana", "🇵🇦 Panamá"], "color": "#534AB7"},
}

SEDES = [
    {"ciudad": "Ciudad de México", "estadio": "Estadio Azteca", "pais": "🇲🇽 México", "cap": 83000, "nota": "🏟 INAUGURACIÓN"},
    {"ciudad": "Guadalajara", "estadio": "Estadio Akron", "pais": "🇲🇽 México", "cap": 48000, "nota": ""},
    {"ciudad": "Monterrey", "estadio": "Estadio BBVA", "pais": "🇲🇽 México", "cap": 53500, "nota": ""},
    {"ciudad": "Toronto", "estadio": "BMO Field", "pais": "🇨🇦 Canadá", "cap": 45000, "nota": ""},
    {"ciudad": "Vancouver", "estadio": "BC Place", "pais": "🇨🇦 Canadá", "cap": 54000, "nota": ""},
    {"ciudad": "Nueva York/NJ", "estadio": "MetLife Stadium", "pais": "🇺🇸 EE.UU.", "cap": 82500, "nota": "🏆 FINAL"},
    {"ciudad": "Dallas/Arlington", "estadio": "AT&T Stadium", "pais": "🇺🇸 EE.UU.", "cap": 94000, "nota": ""},
    {"ciudad": "Los Ángeles", "estadio": "SoFi Stadium", "pais": "🇺🇸 EE.UU.", "cap": 70000, "nota": ""},
    {"ciudad": "San Francisco", "estadio": "Levi's Stadium", "pais": "🇺🇸 EE.UU.", "cap": 68500, "nota": ""},
    {"ciudad": "Miami", "estadio": "Hard Rock Stadium", "pais": "🇺🇸 EE.UU.", "cap": 65000, "nota": ""},
    {"ciudad": "Atlanta", "estadio": "Mercedes-Benz", "pais": "🇺🇸 EE.UU.", "cap": 71000, "nota": ""},
    {"ciudad": "Boston", "estadio": "Gillette Stadium", "pais": "🇺🇸 EE.UU.", "cap": 65000, "nota": ""},
    {"ciudad": "Seattle", "estadio": "Lumen Field", "pais": "🇺🇸 EE.UU.", "cap": 69000, "nota": ""},
    {"ciudad": "Houston", "estadio": "NRG Stadium", "pais": "🇺🇸 EE.UU.", "cap": 72220, "nota": ""},
    {"ciudad": "Kansas City", "estadio": "Arrowhead Stadium", "pais": "🇺🇸 EE.UU.", "cap": 73000, "nota": ""},
    {"ciudad": "Filadelfia", "estadio": "Lincoln Financial", "pais": "🇺🇸 EE.UU.", "cap": 69000, "nota": ""},
]

PARTIDOS_EJEMPLO = [
    {"grupo": "A", "equipo1": "🇲🇽 México", "equipo2": "🇿🇦 Sudáfrica", "fecha": "11 Jun", "sede": "Ciudad de México"},
    {"grupo": "A", "equipo1": "🇰🇷 Corea del Sur", "equipo2": "🇨🇿 Rep. Checa", "fecha": "11 Jun", "sede": "Guadalajara"},
    {"grupo": "B", "equipo1": "🇨🇦 Canadá", "equipo2": "🇨🇭 Suiza", "fecha": "12 Jun", "sede": "Toronto"},
    {"grupo": "C", "equipo1": "🇧🇷 Brasil", "equipo2": "🇲🇦 Marruecos", "fecha": "13 Jun", "sede": "Nueva York/NJ"},
    {"grupo": "D", "equipo1": "🇺🇸 Estados Unidos", "equipo2": "🇹🇷 Turquía", "fecha": "13 Jun", "sede": "Los Ángeles"},
    {"grupo": "E", "equipo1": "🇩🇪 Alemania", "equipo2": "🇨🇼 Curazao", "fecha": "14 Jun", "sede": "Houston"},
    {"grupo": "F", "equipo1": "🇳🇱 Países Bajos", "equipo2": "🇯🇵 Japón", "fecha": "14 Jun", "sede": "Dallas"},
    {"grupo": "H", "equipo1": "🇪🇸 España ⭐", "equipo2": "🇺🇾 Uruguay ⭐", "fecha": "15 Jun", "sede": "Miami"},
    {"grupo": "I", "equipo1": "🇫🇷 Francia ⭐", "equipo2": "🇸🇳 Senegal", "fecha": "16 Jun", "sede": "Boston"},
    {"grupo": "J", "equipo1": "🇦🇷 Argentina ⭐⭐", "equipo2": "🇩🇿 Argelia", "fecha": "16 Jun", "sede": "Dallas"},
    {"grupo": "K", "equipo1": "🇵🇹 Portugal", "equipo2": "🇨🇴 Colombia", "fecha": "17 Jun", "sede": "Miami"},
    {"grupo": "L", "equipo1": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "equipo2": "🇭🇷 Croacia", "fecha": "17 Jun", "sede": "Dallas"},
]

# ─────────────────────────────────────────────
# HERO + COUNTDOWN
# ─────────────────────────────────────────────
inicio_mundial = datetime(2026, 6, 11, 13, 0, 0, tzinfo=timezone.utc)
ahora = datetime.now(timezone.utc)
delta = inicio_mundial - ahora
dias = max(delta.days, 0)
horas = max((delta.seconds // 3600), 0)
minutos = max(((delta.seconds % 3600) // 60), 0)

cd_html = "".join(
    f'<div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);'
    f'border-radius:10px;padding:12px 18px;text-align:center;min-width:72px">'
    f'<div style="font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#fff;line-height:1">{v}</div>'
    f'<div style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:1px;text-transform:uppercase">{l}</div>'
    f'</div>'
    for v, l in [(dias, "Días"), (horas, "Horas"), (minutos, "Min")]
)

st.markdown(f"""
<div class="hero">
  <div style="display:inline-block;background:#D4A017;color:#000;font-size:11px;font-weight:700;
       letter-spacing:2px;padding:4px 14px;border-radius:20px;margin-bottom:12px;">
    FIFA WORLD CUP 2026
  </div>
  <h1>EL MUNDIAL MÁS GRANDE <span>DE LA HISTORIA</span></h1>
  <p>🇺🇸 Estados Unidos &nbsp;·&nbsp; 🇲🇽 México &nbsp;·&nbsp; 🇨🇦 Canadá &nbsp;|&nbsp; 11 JUN – 19 JUL 2026</p>
  <div style="display:flex;justify-content:center;gap:12px;margin-top:1.5rem;flex-wrap:wrap">
    {cd_html}
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MÉTRICAS PRINCIPALES
# ─────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
metrics = [
    ("48", "Selecciones"), ("104", "Partidos"), ("16", "Sedes"),
    ("3", "Países"), ("39", "Días"), ("4", "Debutantes"),
]
for col, (num, lbl) in zip([c1,c2,c3,c4,c5,c6], metrics):
    col.markdown(f"""
    <div class="metric-card">
      <div class="metric-num">{num}</div>
      <div class="metric-lbl">{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS PRINCIPALES
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚽ Grupos", "🏟 Sedes", "📊 Estadísticas", "🎯 Simulador de Resultados", "📅 Formato"
])

# ══════════════════════════════════════════════
# TAB 1 — GRUPOS
# ══════════════════════════════════════════════
with tab1:
    st.subheader("🗂 Los 12 Grupos del Mundial 2026")
    st.caption("12 grupos de 4 equipos · Los 2 primeros + 8 mejores terceros avanzan a 1/16 de final")

    cols_per_row = 4
    grupo_keys = list(GRUPOS.keys())
    for i in range(0, len(grupo_keys), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, key in enumerate(grupo_keys[i:i+cols_per_row]):
            g = GRUPOS[key]
            with cols[j]:
                st.markdown(f"""
                <div class="group-card">
                  <div class="group-header" style="background:{g['color']};color:{'#000' if key in ['C','I'] else '#fff'}">
                    ⚽ GRUPO {key}
                  </div>
                  {''.join(f'<div style="padding:7px 12px;font-size:13px;border-top:1px solid #2a2a2a">{eq}</div>' for eq in g['equipos'])}
                </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔍 Buscar equipo en los grupos")
    busqueda = st.text_input("Escribe el nombre de un país para encontrar su grupo:", placeholder="Ej: Argentina, Francia, Brasil...")
    if busqueda:
        encontrado = False
        for key, g in GRUPOS.items():
            for eq in g["equipos"]:
                if busqueda.lower() in eq.lower():
                    st.success(f"**{eq.strip()}** está en el **Grupo {key}**")
                    st.write("Sus rivales en el grupo:")
                    rivales = [e for e in g["equipos"] if e != eq]
                    for r in rivales:
                        st.write(f"  · {r}")
                    encontrado = True
                    break
        if not encontrado:
            st.warning(f"No se encontró '{busqueda}' entre los 48 clasificados. Verifica el nombre.")

# ══════════════════════════════════════════════
# TAB 2 — SEDES
# ══════════════════════════════════════════════
with tab2:
    st.subheader("🌎 Las 16 Sedes del Mundial")

    pais_filter = st.selectbox("Filtrar por país:", ["Todos", "🇲🇽 México", "🇨🇦 Canadá", "🇺🇸 EE.UU."])

    sedes_filtradas = SEDES if pais_filter == "Todos" else [s for s in SEDES if pais_filter in s["pais"]]

    cols = st.columns(4)
    for idx, s in enumerate(sedes_filtradas):
        with cols[idx % 4]:
            color_pais = "#1a7a3c" if "México" in s["pais"] else "#c0392b"
            nota_html = f'<div style="background:#D4A017;color:#000;font-size:9px;font-weight:700;padding:2px 8px;border-radius:3px;display:inline-block;margin-top:6px">{s["nota"]}</div>' if s["nota"] else ""
            st.markdown(f"""
            <div class="sede-card">
              <div style="font-size:10px;font-weight:600;letter-spacing:1px;color:{color_pais};margin-bottom:4px">{s['pais']}</div>
              <div style="font-weight:600;font-size:15px">{s['ciudad']}</div>
              <div style="font-size:12px;color:#888;margin-top:2px">{s['estadio']}</div>
              <div style="font-size:12px;color:#00e676;font-weight:500;margin-top:4px">⚡ {s['cap']:,} espectadores</div>
              {nota_html}
            </div>""", unsafe_allow_html=True)
            st.write("")

    st.markdown("---")
    st.subheader("📊 Capacidad por Estadio")
    df_sedes = pd.DataFrame(SEDES)
    df_sedes_sorted = df_sedes.sort_values("cap", ascending=True)
    colores = ["#1a7a3c" if "México" in p else ("#c0392b" if "Canadá" in p else "#185FA5") for p in df_sedes_sorted["pais"]]

    fig_sedes = go.Figure(go.Bar(
        x=df_sedes_sorted["cap"],
        y=df_sedes_sorted["ciudad"],
        orientation="h",
        marker_color=colores,
        text=[f"{c:,}" for c in df_sedes_sorted["cap"]],
        textposition="outside",
    ))
    fig_sedes.update_layout(
        paper_bgcolor="#0d0d0d", plot_bgcolor="#161616",
        font_color="#f0f0f0", height=520,
        xaxis=dict(showgrid=True, gridcolor="#2a2a2a"),
        yaxis=dict(showgrid=False),
        margin=dict(l=10, r=80, t=10, b=10),
    )
    st.plotly_chart(fig_sedes, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — ESTADÍSTICAS
# ══════════════════════════════════════════════
with tab3:
    st.subheader("📊 Estadísticas del Mundial 2026")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Clasificados por Confederación")
        conf_data = pd.DataFrame({
            "Confederación": ["UEFA", "CAF", "AFC", "CONMEBOL", "CONCACAF", "OFC"],
            "Equipos": [16, 10, 9, 6, 6, 1],
        })
        fig_conf = px.bar(
            conf_data, x="Confederación", y="Equipos", color="Confederación",
            color_discrete_map={"UEFA":"#185FA5","CAF":"#c0392b","AFC":"#D4A017",
                                "CONMEBOL":"#1a7a3c","CONCACAF":"#534AB7","OFC":"#888"},
            text="Equipos",
        )
        fig_conf.update_traces(textposition="outside")
        fig_conf.update_layout(
            paper_bgcolor="#0d0d0d", plot_bgcolor="#161616",
            font_color="#f0f0f0", showlegend=False, height=320,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_conf, use_container_width=True)

    with col_b:
        st.markdown("#### Sedes por País Anfitrión")
        fig_pie = px.pie(
            values=[11, 3, 2], names=["🇺🇸 EE.UU.", "🇲🇽 México", "🇨🇦 Canadá"],
            color_discrete_sequence=["#c0392b", "#1a7a3c", "#185FA5"],
            hole=0.45,
        )
        fig_pie.update_layout(
            paper_bgcolor="#0d0d0d", font_color="#f0f0f0", height=320,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📅 Evolución histórica de participantes en el Mundial")
    hist_data = pd.DataFrame({
        "Año": [1930,1934,1938,1950,1954,1958,1962,1966,1970,1974,1978,1982,1986,1990,1994,1998,2002,2006,2010,2014,2018,2022,2026],
        "Equipos": [13,16,15,13,16,16,16,16,16,16,16,24,24,24,24,32,32,32,32,32,32,32,48],
    })
    fig_hist = px.area(
        hist_data, x="Año", y="Equipos",
        color_discrete_sequence=["#00e676"],
        markers=True,
        labels={"Equipos": "Número de equipos"},
    )
    fig_hist.update_traces(fill="tozeroy", fillcolor="rgba(0,230,118,0.1)", line_width=2)
    fig_hist.update_layout(
        paper_bgcolor="#0d0d0d", plot_bgcolor="#161616",
        font_color="#f0f0f0", height=300,
        xaxis=dict(showgrid=True, gridcolor="#2a2a2a"),
        yaxis=dict(showgrid=True, gridcolor="#2a2a2a"),
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🏆 Campeones del Mundo — histórico")
    campeon_data = pd.DataFrame({
        "País": ["🇧🇷 Brasil","🇩🇪 Alemania","🇮🇹 Italia","🇦🇷 Argentina","🇫🇷 Francia","🇺🇾 Uruguay","🇪🇸 España","🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra"],
        "Títulos": [5, 4, 4, 3, 2, 2, 1, 1],
    })
    fig_camp = px.bar(
        campeon_data.sort_values("Títulos", ascending=True),
        x="Títulos", y="País", orientation="h",
        color="Títulos", color_continuous_scale=["#1a7a3c","#D4A017"],
        text="Títulos",
    )
    fig_camp.update_traces(textposition="outside")
    fig_camp.update_layout(
        paper_bgcolor="#0d0d0d", plot_bgcolor="#161616",
        font_color="#f0f0f0", height=320, showlegend=False,
        margin=dict(l=0, r=40, t=10, b=0),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_camp, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 — SIMULADOR DE RESULTADOS
# ══════════════════════════════════════════════
with tab4:
    st.subheader("🎯 Simulador de Resultados")
    st.caption("Ingresa los marcadores de los partidos y veremos quién avanza")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### ✏️ Registrar Resultado de Partido")

        grupo_sel = st.selectbox("Selecciona el grupo:", list(GRUPOS.keys()), format_func=lambda x: f"Grupo {x}")
        equipos_grupo = GRUPOS[grupo_sel]["equipos"]

        eq1 = st.selectbox("Equipo 1:", equipos_grupo, index=0)
        eq2_opts = [e for e in equipos_grupo if e != eq1]
        eq2 = st.selectbox("Equipo 2:", eq2_opts, index=0)

        col_g1, col_vs, col_g2 = st.columns([2, 1, 2])
        with col_g1:
            goles1 = st.number_input(f"Goles {eq1[:6]}", min_value=0, max_value=20, value=0, step=1)
        with col_vs:
            st.markdown("<br><h3 style='text-align:center;color:#888'>VS</h3>", unsafe_allow_html=True)
        with col_g2:
            goles2 = st.number_input(f"Goles {eq2[:6]}", min_value=0, max_value=20, value=0, step=1)

        fecha = st.text_input("Fecha del partido:", placeholder="Ej: 11 Jun 2026")
        sede_partido = st.text_input("Sede:", placeholder="Ej: Ciudad de México")

        if st.button("⚽ Registrar Resultado", use_container_width=True):
            if goles1 > goles2:
                ganador = eq1
                resultado_txt = "Victoria"
                emoji_res = "🏆"
            elif goles2 > goles1:
                ganador = eq2
                resultado_txt = "Victoria"
                emoji_res = "🏆"
            else:
                ganador = "Empate"
                resultado_txt = "Empate"
                emoji_res = "🤝"

            st.markdown(f"""
            <div class="result-card">
              <div style="font-size:0.9rem;color:#888;margin-bottom:8px">Grupo {grupo_sel} · {fecha} · {sede_partido}</div>
              <div style="font-size:1.8rem;font-weight:700;letter-spacing:1px">
                {eq1}&nbsp;&nbsp;
                <span style="color:#D4A017;font-family:'Bebas Neue',sans-serif;font-size:2.2rem">{goles1} – {goles2}</span>
                &nbsp;&nbsp;{eq2}
              </div>
              <div style="margin-top:10px;font-size:0.85rem;color:#aaa">{emoji_res} {resultado_txt}</div>
              {'<div class="winner-badge">GANADOR: ' + ganador + '</div>' if ganador != "Empate" else '<div class="winner-badge" style="background:#888">EMPATE</div>'}
            </div>
            """, unsafe_allow_html=True)

            if goles1 > goles2:
                st.balloons()
            elif goles2 > goles1:
                st.snow()

    with col_right:
        st.markdown("### 📋 Tabla de posiciones — Grupo")
        st.caption("Ingresa los resultados acumulados de tu grupo")

        st.markdown(f"**Equipos en Grupo {grupo_sel}:**")

        puntos = {}
        gf_dict = {}
        gc_dict = {}

        for eq in equipos_grupo:
            nombre_corto = eq[:20]
            c1b, c2b, c3b, c4b = st.columns(4)
            with c1b:
                st.markdown(f"<small>{nombre_corto}</small>", unsafe_allow_html=True)
            with c2b:
                pts = st.number_input("Pts", min_value=0, max_value=9, value=0, step=1, key=f"pts_{eq}")
            with c3b:
                gf = st.number_input("GF", min_value=0, max_value=30, value=0, step=1, key=f"gf_{eq}")
            with c4b:
                gc = st.number_input("GC", min_value=0, max_value=30, value=0, step=1, key=f"gc_{eq}")
            puntos[eq] = pts
            gf_dict[eq] = gf
            gc_dict[eq] = gc

        if st.button("📊 Ver Tabla", use_container_width=True):
            tabla = pd.DataFrame({
                "Equipo": equipos_grupo,
                "Pts": [puntos[e] for e in equipos_grupo],
                "GF": [gf_dict[e] for e in equipos_grupo],
                "GC": [gc_dict[e] for e in equipos_grupo],
            })
            tabla["DG"] = tabla["GF"] - tabla["GC"]
            tabla = tabla.sort_values(["Pts","DG","GF"], ascending=False).reset_index(drop=True)
            tabla.index += 1

            def highlight_clasificados(row):
                if row.name <= 2:
                    return ["background-color: #0a2d14; color: #00e676"] * len(row)
                return [""] * len(row)

            st.dataframe(
                tabla.style.apply(highlight_clasificados, axis=1),
                use_container_width=True,
                hide_index=False,
            )
            st.caption("🟢 Verde = clasifican directamente a 1/16 de final")

    st.markdown("---")
    st.subheader("📝 Predicción del Campeón")
    col_pred1, col_pred2 = st.columns(2)

    with col_pred1:
        todos_equipos = [eq for g in GRUPOS.values() for eq in g["equipos"]]
        campeon_pred = st.selectbox("¿Quién crees que será el campeón?", todos_equipos)
        razon = st.text_area("¿Por qué? Escribe tu argumento:", placeholder="Ej: Argentina llega como bicampeón de América y campeón del mundo vigente con Messi en plena forma...")
        nombre_fan = st.text_input("Tu nombre:", placeholder="Ej: Carlos")

        if st.button("🏆 Registrar Predicción", use_container_width=True):
            if nombre_fan and razon:
                st.success(f"¡Predicción registrada, {nombre_fan}! 🎉")
                st.markdown(f"""
                <div style="background:#0a2d14;border:1px solid #1a7a3c;border-radius:12px;padding:1.2rem;margin-top:0.5rem">
                  <div style="color:#D4A017;font-weight:700;font-size:1.1rem">{nombre_fan} predice: {campeon_pred}</div>
                  <div style="color:#aaa;font-size:0.9rem;margin-top:8px;font-style:italic">"{razon}"</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Escribe tu nombre y tu argumento para registrar la predicción.")

    with col_pred2:
        st.markdown("#### 🔥 Partidos de la Jornada 1")
        for p in PARTIDOS_EJEMPLO[:6]:
            st.markdown(f"""
            <div style="background:#161616;border:1px solid #2a2a2a;border-radius:8px;
                 padding:8px 12px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center">
              <span style="font-size:12px;color:#888">Grupo {p['grupo']} · {p['fecha']}</span>
              <span style="font-size:13px">{p['equipo1']} <b style="color:#D4A017">vs</b> {p['equipo2']}</span>
              <span style="font-size:11px;color:#888">{p['sede']}</span>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 5 — FORMATO
# ══════════════════════════════════════════════
with tab5:
    st.subheader("📅 Formato y Calendario del Mundial 2026")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("#### 🆕 Nuevo Formato (primera vez)")
        formato_info = [
            ("12 Grupos de 4", "Por primera vez desde 1994 con más de 32 equipos"),
            ("104 partidos totales", "+40 partidos vs Qatar 2022 (64 partidos)"),
            ("1/16 de final", "Nueva ronda eliminatoria — 32 equipos compiten"),
            ("8 mejores terceros", "También clasifican a la siguiente ronda"),
            ("3 países sede", "Primera vez que 3 países organizan juntos"),
        ]
        for titulo, desc in formato_info:
            st.markdown(f"""
            <div style="background:#161616;border-left:3px solid #00e676;border-radius:0 8px 8px 0;
                 padding:10px 14px;margin-bottom:8px">
              <div style="font-weight:600;font-size:14px">{titulo}</div>
              <div style="color:#888;font-size:12px;margin-top:2px">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("#### 🗓 Línea de Tiempo")
        timeline = [
            ("5 Dic 2025", "Sorteo de grupos", "Kennedy Center, Washington D.C."),
            ("31 Mar 2026", "Últimos clasificados", "Suecia, Turquía, R. Checa, Bosnia, Congo, Irak"),
            ("11 Jun 2026", "🎉 Partido inaugural", "México vs Sudáfrica · Estadio Azteca"),
            ("27 Jun 2026", "Fin fase de grupos", "Jornada final de todos los grupos"),
            ("28 Jun – 3 Jul", "1/16 de final", "Primera ronda eliminatoria del torneo"),
            ("4–7 Jul", "Octavos de final", "16 equipos en juego"),
            ("9–11 Jul", "Cuartos de final", "Boston, Miami, Kansas City, L.A."),
            ("14–15 Jul", "Semifinales", "Dallas y Atlanta"),
            ("18 Jul 2026", "Tercer y cuarto lugar", "Ciudad por confirmar"),
            ("19 Jul 2026", "🏆 Gran Final", "MetLife Stadium · Nueva York / Nueva Jersey"),
        ]
        for fecha, evento, detalle in timeline:
            is_key = "🎉" in evento or "🏆" in evento
            border_color = "#D4A017" if is_key else "#2a2a2a"
            bg_color = "#1a1000" if is_key else "#161616"
            st.markdown(f"""
            <div style="background:{bg_color};border:1px solid {border_color};border-radius:8px;
                 padding:8px 12px;margin-bottom:6px;display:flex;gap:12px;align-items:flex-start">
              <div style="min-width:100px;font-size:11px;font-weight:600;color:#D4A017;padding-top:1px">{fecha}</div>
              <div>
                <div style="font-size:13px;font-weight:500">{evento}</div>
                <div style="font-size:11px;color:#888;margin-top:2px">{detalle}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📊 Comparativa de Mundiales")
    comp_data = pd.DataFrame({
        "Edición": ["Qatar 2022", "Rusia 2018", "Brasil 2014", "Sudáfrica 2010", "USA/MÉX/CAN 2026"],
        "Equipos": [32, 32, 32, 32, 48],
        "Partidos": [64, 64, 64, 64, 104],
        "Sedes": [8, 12, 12, 10, 16],
        "Días": [29, 32, 32, 30, 39],
    })
    st.dataframe(
        comp_data.style.highlight_max(subset=["Equipos","Partidos","Sedes","Días"], color="#0a2d14"),
        use_container_width=True, hide_index=True
    )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:1rem;color:#555;font-size:0.8rem">
  ⚽ <strong style="color:#D4A017">FIFA World Cup 2026</strong> — Dashboard creado con Streamlit &nbsp;·&nbsp;
  Datos oficiales FIFA &nbsp;·&nbsp; 11 Jun – 19 Jul 2026
</div>
""", unsafe_allow_html=True)
