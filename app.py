import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(
    layout="wide",
    page_title="FIRESTATS.br - Banco de Estatísticas",
    initial_sidebar_state="collapsed",
)

CORES = ["#1E293B", "#F97316", "#14B8A6", "#94A3B8", "#E2E8F0"]
MESES = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]
MESES_ABREVIADOS = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
]
ESTADOS = [
    "Acre (AC)",
    "Alagoas (AL)",
    "Amapá (AP)",
    "Amazonas (AM)",
    "Bahia (BA)",
    "Ceará (CE)",
    "Distrito Federal (DF)",
    "Espírito Santo (ES)",
    "Goiás (GO)",
    "Maranhão (MA)",
    "Mato Grosso (MT)",
    "Mato Grosso do Sul (MS)",
    "Minas Gerais (MG)",
    "Pará (PA)",
    "Paraíba (PB)",
    "Paraná (PR)",
    "Pernambuco (PE)",
    "Piauí (PI)",
    "Rio de Janeiro (RJ)",
    "Rio Grande do Norte (RN)",
    "Rio Grande do Sul (RS)",
    "Rondônia (RO)",
    "Roraima (RR)",
    "Santa Catarina (SC)",
    "São Paulo (SP)",
    "Sergipe (SE)",
    "Tocantins (TO)",
]

st.markdown(
    """
    <style>
    .titulo-principal {
        text-align: center;
        color: #1E293B;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 5px;
        margin-top: 18px;
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


def render_pie_legend(data, label_column, value_column, colors):
    total = data[value_column].sum()
    legend_items = []

    for index, (_, row) in enumerate(data.iterrows()):
        percentage = row[value_column] / total * 100
        legend_items.append(
            f'<div><span style="color:{colors[index]}; font-size:18px;">●</span> '
            f'{row[label_column]} '
            f'<span style="color:#64748B;">({percentage:.1f}%)</span></div>'
        )

    st.markdown("\n".join(legend_items), unsafe_allow_html=True)


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
            showlegend=False,
            margin=dict(t=20, b=10, l=10, r=10),
            height=280,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(figure, width="stretch")
        st.divider()
        render_pie_legend(data, label_column, value_column, colors)


def monthly_data(month_index):
    residential = pd.DataFrame(
        {
            "Causa": [
                "Curto-Circuito",
                "Fogão/Cozinha",
                "Velas",
                "Ferro de passar",
                "Outros",
            ],
            "Ocorrências": [
                38 + (month_index % 3) * 2,
                25 + (month_index % 2),
                15 + ((month_index + 1) % 3),
                12 + (month_index % 2),
                10 + ((month_index + 2) % 3),
            ],
        }
    )
    commercial = pd.DataFrame(
        {
            "Causa": [
                "Sobrecarga elétrica",
                "Superaquecimento",
                "Curto-circuito",
                "Quadros elétricos",
                "Outros",
            ],
            "Ocorrências": [
                32 + month_index % 4,
                24 + (month_index + 1) % 4,
                20 + (month_index % 3),
                10 + ((month_index + 1) % 3),
                14 + ((month_index + 2) % 3),
            ],
        }
    )
    industrial = pd.DataFrame(
        {
            "Setor": [
                "Falha elétrica",
                "Acúmulo de inflamáveis no armazenamento",
                "Falta de manutenção em equipamentos",
                "Trabalhos a quente",
                "Outros",
            ],
            "Ocorrências": [
                44 + (month_index % 4),
                38 + ((month_index + 1) % 5),
                35 + ((month_index + 2) % 4),
                31 + ((month_index + 3) % 5),
                18 + (month_index % 3),
            ],
        }
    )
    return residential, commercial, industrial


def render_national_charts(month_index, month_name):
    residential, commercial, industrial = monthly_data(month_index)
    st.markdown(
        f"### Dados Nacionais — {month_name} de 2026"
    )
    st.caption(
        "Distribuição das ocorrências registradas no mês selecionado por setor e causa."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        render_pie_card(
            "🏠 RESIDENCIAL",
            "OCORRÊNCIAS EM MORADIAS",
            residential,
            "Causa",
            "Ocorrências",
            CORES,
        )
    with col2:
        render_pie_card(
            "🏪 COMERCIAL",
            "INCIDENTES EM ESTABELECIMENTOS",
            commercial,
            "Causa",
            "Ocorrências",
            CORES,
        )
    with col3:
        render_pie_card(
            "🏭 INDUSTRIAL",
            "PRINCÍPIOS DE INCÊNDIO EM FÁBRICAS",
            industrial,
            "Setor",
            "Ocorrências",
            CORES,
        )


def state_data(state, month_index):
    state_index = ESTADOS.index(state)
    factor = 0.72 + (state_index % 8) * 0.07
    residential, commercial, industrial = monthly_data(month_index)

    residential = residential.copy()
    residential["Ocorrências"] = [
        round(value * factor + (state_index + item_index) % 4)
        for item_index, value in enumerate(residential["Ocorrências"])
    ]

    commercial = commercial.copy()
    commercial["Ocorrências"] = [
        round(value * (factor + 0.03) + (state_index + item_index * 2) % 5)
        for item_index, value in enumerate(commercial["Ocorrências"])
    ]

    industrial = industrial.copy()
    industrial["Ocorrências"] = [
        round(value * (factor + 0.06) + (state_index + item_index) % 6)
        for item_index, value in enumerate(industrial["Ocorrências"])
    ]
    return residential, commercial, industrial


def render_state_charts(state, month_index, month_name):
    residential, commercial, industrial = state_data(state, month_index)
    st.markdown(f"### Gráficos Estaduais — {state}")
    st.caption(
        f"Período selecionado: {month_name} de 2026. "
        "Os valores desta visualização são fictícios para demonstração."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        render_pie_card(
            "🏠 RESIDENCIAL",
            "OCORRÊNCIAS EM MORADIAS",
            residential,
            "Causa",
            "Ocorrências",
            CORES,
        )
    with col2:
        render_pie_card(
            "🏪 COMERCIAL",
            "INCIDENTES EM ESTABELECIMENTOS",
            commercial,
            "Causa",
            "Ocorrências",
            CORES,
        )
    with col3:
        render_pie_card(
            "🏭 INDUSTRIAL",
            "PRINCÍPIOS DE INCÊNDIO EM FÁBRICAS",
            industrial,
            "Setor",
            "Ocorrências",
            CORES,
        )


def timeline_data():
    return pd.DataFrame(
        {
            "Mês": MESES_ABREVIADOS,
            # Criei a variação alta pra forçar as outras a ficarem "esmagadinhas" juntas embaixo
            "Residencial": [18, 24, 12, 28, 42, 57, 45, 32, 22, 15, 9, 18], 
            "Comercial": [10, 14, 8, 15, 22, 28, 25, 18, 14, 10, 6, 12],
            "Industrial": [5, 8, 4, 7, 10, 14, 12, 9, 6, 4, 2, 6], 
        }
    )

def render_timeline():
    st.markdown("### Linha do Tempo Nacional")
    st.caption(
        "Média mensal nacional estimada de ocorrências por setor em 2026. "
        "Os valores são fictícios para demonstração."
    )
    
    st.info(
        "💡 **Dica interativa:** Dê dois cliques em um setor na legenda para dar zoom e visualizar os detalhes isolados."
    )
    
    timeline = timeline_data()
    fig = px.line(
        timeline,
        x="Mês",
        y=["Residencial", "Comercial", "Industrial"],
        color_discrete_sequence=CORES[:3],
        line_shape="linear", 
    )
    
    for trace in fig.data:
        trace_name = trace.name
        trace_color = trace.line.color
        trace.mode = "lines+markers"
        trace.marker = dict(symbol="circle", size=8, color=trace_color)
        trace.showlegend = False
        trace.legendgroup = trace_name
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(symbol="circle", size=10, color=trace_color),
                name=trace_name,
                legendgroup=trace_name,
                showlegend=True,
                hoverinfo="skip",
            )
        )
        
    fig.update_xaxes(
        tickangle=0,
        showline=True,        # Isso cria o "chão" visual no eixo X
        linewidth=1,          # Grossura da linha do chão
        linecolor="#94A3B8"   # Cor do chão para o zero não parecer que tá flutuando
    )
    
    fig.update_layout(
        legend_title_text="",
        yaxis_title="", 
        xaxis_title="", 
        legend=dict(
            orientation="v",
            yanchor="top",
            y=-0.2,
            xanchor="left",
            x=0,
            groupclick="togglegroup",
        ),
        margin=dict(t=10, b=10, l=0, r=0), 
        height=280, 
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified"
    )
    
    fig.update_yaxes(
        autorange=True,      
        rangemode="tozero",  
        showgrid=True,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor="#94A3B8"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Este gráfico reúne a média das categorias de cada setor mês a mês. "
        "Ele poderá ser substituído por dados oficiais quando estiverem disponíveis."
    )


menu = option_menu(
    menu_title="🔥 FIRESTATS.br",
    options=["Início", "Gráficos", "Dados Nacionais", "Linha do Tempo", "Contato"],
    icons=["house", "bar-chart-line", "globe2", "clock-history", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important",
            "background-color": "#1e293b",
            "border-radius": "8px",
        },
        "menu-title": {
            "color": "white",
            "font-size": "20px",
            "font-weight": "bold",
            "margin-right": "18px",
        },
        "icon": {"color": "white", "font-size": "16px"},
        "nav-link": {
            "font-size": "15px",
            "text-align": "center",
            "margin": "0px",
            "padding": "12px 8px",
            "color": "white",
            "--hover-color": "#334155",
        },
        "nav-link-selected": {
            "background-color": "#f97316",
            "color": "white",
        },
    },
)

if menu == "Dados Nacionais":
    st.markdown(
        '<h1 style="text-align:center; color:#1e293b; font-size:42px; '
        'margin:28px 0 18px;">BANCO DE ESTATÍSTICAS DE PRINCÍPIO DE INCÊNDIO</h1>',
        unsafe_allow_html=True,
    )
    selected_month = st.selectbox(
        "Mês das estatísticas",
        MESES,
        index=0,
        help="Selecione o mês usado nos gráficos nacionais.",
    )
elif menu == "Gráficos":
    selected_month = st.selectbox(
        "Período (mês)",
        MESES,
        index=0,
        help="Selecione o período usado na visualização atual.",
    )
else:
    selected_month = MESES[0]
month_index = MESES.index(selected_month)

if menu == "Início":
    st.markdown(
        '<div class="titulo-principal">PLATAFORMA NACIONAL DE ANÁLISE E PREVENÇÃO '
        "DE PRINCÍPIOS DE INCÊNDIO</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sub-titulo">Informação estratégica para fortalecer a prevenção, '
        'a análise de riscos e a resposta coordenada em todo o Brasil.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "O FIRESTATS.br é uma plataforma nacional de análise e prevenção de "
        "princípios de incêndio. Sua finalidade é apoiar órgãos públicos, equipes "
        "de emergência e comunidades na tomada de decisões de segurança com base "
        "em informações organizadas por setor, estado e período."
    )
    
    st.markdown("### Informações em destaque")
    temp = 32
    if temp > 30:
        st.warning(
            "☀️ **Boletim de Risco Sazonal**\n\n"
            f"Temperatura simulada: {temp} °C. O calor elevado aumenta o risco "
            "de curto-circuito por sobrecarga de ar-condicionado nos setores "
            "Residencial e Comercial. Reforce a inspeção preventiva."
        )
    else:
        st.warning(
            "☀️ **Boletim de Risco Sazonal**\n\n"
            f"Temperatura simulada: {temp} °C. O tempo seco aumenta o perigo "
            "de incêndios e superaquecimento de equipamentos na Indústria. "
            "Reforce a inspeção preventiva."
        )
    st.caption(
        "Leitura simulada preparada para futura integração com a API do OpenWeather."
    )

    highlights = st.columns(3)
    with highlights[0]:
        st.info(
            "📊 **Destaque do Mês — Residencial**\n\n"
            "36,9% dos princípios de incêndio residenciais recentes são causados "
            "por curtos-circuitos."
        )
    with highlights[1]:
        st.info(
            "📊 **Destaque do Mês — Comercial**\n\n"
            "A sobrecarga elétrica e o superaquecimento concentram os principais "
            "riscos nos estabelecimentos."
        )
    with highlights[2]:
        st.info(
            "📊 **Destaque do Mês — Industrial**\n\n"
            "Falhas elétricas e trabalhos a quente exigem atenção redobrada "
            "nas áreas industriais."
        )

elif menu == "Gráficos":
    selected_state = st.selectbox(
        "Estado",
        ESTADOS,
        index=ESTADOS.index("São Paulo (SP)"),
        help="Escolha o estado que deseja analisar.",
    )
    st.markdown("### Gráficos do painel")
    st.caption(
        "Selecione um estado e um período para visualizar os gráficos estaduais "
        "de Residencial, Comercial e Industrial."
    )
    render_state_charts(selected_state, month_index, selected_month)

elif menu == "Dados Nacionais":
    render_national_charts(month_index, selected_month)

elif menu == "Linha do Tempo":
    render_timeline()

elif menu == "Contato":
    st.markdown("### Contato")
    st.write(
        "Para dúvidas sobre os dados e o painel, entre em contato com a equipe "
        "FIRESTATS BRASIL."
    )
    st.markdown(
        "[contato@firestats-brasil.example](mailto:contato@firestats-brasil.example)"
    )

st.divider()
st.markdown(
    '<div style="text-align: center; color: #94A3B8; font-size: 13px;">© 2026 '
    "FIRESTATS BRASIL | DADOS OFICIAIS | POLÍTICA DE PRIVACIDADE</div>",
    unsafe_allow_html=True,
)
