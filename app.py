import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from streamlit_option_menu import option_menu

st.set_page_config(
    layout="wide",
    page_title="FIRESTATS.br - Banco de Estatísticas",
    initial_sidebar_state="collapsed",
)

CORES = ["#1E293B", "#F97316", "#14B8A6", "#94A3B8", "#E2E8F0"]
MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]
MESES_ABREVIADOS = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez",
]
ESTADOS = [
    "Acre (AC)", "Alagoas (AL)", "Amapá (AP)", "Amazonas (AM)", "Bahia (BA)",
    "Ceará (CE)", "Distrito Federal (DF)", "Espírito Santo (ES)", "Goiás (GO)",
    "Maranhão (MA)", "Mato Grosso (MT)", "Mato Grosso do Sul (MS)", "Minas Gerais (MG)",
    "Pará (PA)", "Paraíba (PB)", "Paraná (PR)", "Pernambuco (PE)", "Piauí (PI)",
    "Rio de Janeiro (RJ)", "Rio Grande do Norte (RN)", "Rio Grande do Sul (RS)",
    "Rondônia (RO)", "Roraima (RR)", "Santa Catarina (SC)", "São Paulo (SP)",
    "Sergipe (SE)", "Tocantins (TO)",
]

# Estilização responsiva global
st.markdown(
    """
    <style>
    .titulo-principal {
        color: #1E293B;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    .sub-titulo {
        text-align: center;
        color: #475569;
        font-size: 16px;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data(ttl=600)
def obter_clima(estado_completo):
    nome_estado = estado_completo.split(" (")[0]
    api_key = "915268d2f3185d3e55562d15ff511f88"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={nome_estado},BR&appid={api_key}&units=metric&lang=pt_br"
    try:
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados["main"]["temp"], dados["weather"][0]["description"]
    except:
        pass
    return None, None

def render_pie_card(title, subtitle, data, label_column, value_column, colors):
    with st.container(border=True):
        st.markdown(f"#### {title}\n**{subtitle}**")
        figure = px.pie(
            data,
            values=value_column,
            names=label_column,
            hole=0.5,
            color_discrete_sequence=colors,
        )
        figure.update_traces(textposition="inside", textinfo="percent")
        figure.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),
            margin=dict(t=20, b=20, l=10, r=10),
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(figure, use_container_width=True)

def monthly_data(month_index):
    residential = pd.DataFrame({"Causa": ["Curto-Circuito", "Fogão", "Velas", "Ferro", "Outros"], "Ocorrências": [40, 25, 15, 10, 10]})
    commercial = pd.DataFrame({"Causa": ["Sobrecarga", "Superaquecimento", "Curto-circuito", "Quadros", "Outros"], "Ocorrências": [35, 25, 20, 10, 10]})
    industrial = pd.DataFrame({"Setor": ["Falha elétrica", "Inflamáveis", "Manutenção", "Trabalhos a quente", "Outros"], "Ocorrências": [45, 35, 35, 30, 15]})
    return residential, commercial, industrial

def render_national_charts(month_index, month_name):
    residential, commercial, industrial = monthly_data(month_index)
    st.markdown(f"### Dados Nacionais — {month_name} de 2026")
    col1, col2, col3 = st.columns(3)
    with col1: render_pie_card("🏠 RESIDENCIAL", "MORADIAS", residential, "Causa", "Ocorrências", CORES)
    with col2: render_pie_card("🏪 COMERCIAL", "ESTABELECIMENTOS", commercial, "Causa", "Ocorrências", CORES)
    with col3: render_pie_card("🏭 INDUSTRIAL", "FÁBRICAS", industrial, "Setor", "Ocorrências", CORES)

def render_state_charts(state, month_index, month_name):
    residential, commercial, industrial = monthly_data(month_index)
    st.markdown(f"### Gráficos Estaduais — {state}")
    col1, col2, col3 = st.columns(3)
    with col1: render_pie_card("🏠 RESIDENCIAL", "MORADIAS", residential, "Causa", "Ocorrências", CORES)
    with col2: render_pie_card("🏪 COMERCIAL", "ESTABELECIMENTOS", commercial, "Causa", "Ocorrências", CORES)
    with col3: render_pie_card("🏭 INDUSTRIAL", "FÁBRICAS", industrial, "Setor", "Ocorrências", CORES)

def render_timeline():
    st.markdown("### Linha do Tempo Nacional")
    st.info("💡 **Dica interativa:** Dê dois cliques num setor na legenda para isolar o gráfico.")
    
    res_totals, com_totals, ind_totals = [], [], []
    for m in range(12):
        r, c, i = monthly_data(m)
        res_totals.append(r["Ocorrências"].sum())
        com_totals.append(c["Ocorrências"].sum())
        ind_totals.append(i["Ocorrências"].sum())
        
    timeline = pd.DataFrame({"Mês": MESES_ABREVIADOS, "Residencial": res_totals, "Comercial": com_totals, "Industrial": ind_totals})
    
    fig = px.line(timeline, x="Mês", y=["Residencial", "Comercial", "Industrial"], color_discrete_sequence=CORES[:3], markers=True)
    
    fig.update_layout(
        legend_title_text="",
        yaxis_title="Total de Ocorrências", 
        xaxis_title="", 
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=10, b=10, l=0, r=0), 
        height=340, 
        hovermode="x unified"
    )
    fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig, use_container_width=True)

# Menu responsivo otimizado
menu = option_menu(
    menu_title=None,
    options=["Principal", "Gráficos", "Nacionais", "Tempo", "Contato"],
    icons=["house", "bar-chart", "globe", "clock", "envelope"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#1e293b", "border-radius": "8px"},
        "icon": {"color": "white", "font-size": "15px"},
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "padding": "10px 6px", "color": "white"},
        "nav-link-selected": {"background-color": "#f97316", "color": "white"},
    },
)

# Imagem centralizada de forma responsiva
col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
with col_img2:
    try:
        st.image("1790536883532.jpg", use_column_width=True)
    except:
        pass

st.markdown('<div class="titulo-principal">PLATAFORMA NACIONAL DE ANÁLISE E PREVENÇÃO DE PRINCÍPIOS DE INCÊNDIO</div>', unsafe_allow_html=True)

if menu == "Principal":
    st.markdown('<div class="sub-titulo">Informação estratégica para fortalecer a prevenção e a resposta coordenada.</div>', unsafe_allow_html=True)
    
    estado_alerta = st.selectbox("Selecione o estado para ver o Boletim Climático:", ESTADOS, index=ESTADOS.index("São Paulo (SP)"))
    temp, condicao = obter_clima(estado_alerta)
    
    if temp is not None:
        if temp >= 30:
            st.warning(f"☀️ **Boletim de Risco ({estado_alerta.split(' (')[0]}):** {temp:.1f}°C ({condicao}). Calor elevado. Risco de curto-circuito por sobrecarga de ar-condicionado.")
        elif temp <= 20:
            st.info(f"❄️ **Boletim de Risco ({estado_alerta.split(' (')[0]}):** {temp:.1f}°C ({condicao}). Frio. Atenção ao uso de aquecedores e redes elétricas antigas.")
        else:
            st.success(f"🌤️ **Boletim de Risco ({estado_alerta.split(' (')[0]}):** {temp:.1f}°C ({condicao}). Condições amenas. Atenção ao superaquecimento industrial.")

    st.markdown("O FIRESTATS.br é uma plataforma nacional de análise e prevenção de princípios de incêndio alimentada por registros integrados.")

elif menu == "Gráficos":
    estado_grafico = st.selectbox("Estado", ESTADOS, index=0)
    mes_grafico = st.selectbox("Mês", MESES, index=0)
    render_state_charts(estado_grafico, MESES.index(mes_grafico), mes_grafico)

elif menu == "Nacionais":
    mes_nac = st.selectbox("Mês", MESES, index=0)
    render_national_charts(MESES.index(mes_nac), mes_nac)

elif menu == "Tempo":
    render_timeline()

elif menu == "Contato":
    st.markdown("### Contato")
    st.write("Para suporte ou dúvidas sobre a integração de dados:")
    st.markdown("[contato@firestats-brasil.example](mailto:contato@firestats-brasil.example)")

st.divider()
st.markdown('<div style="text-align: center; color: #94A3B8; font-size: 13px;">© 2026 FIRESTATS BRASIL | CONECTADO AO SISTEMA</div>', unsafe_allow_html=True)
