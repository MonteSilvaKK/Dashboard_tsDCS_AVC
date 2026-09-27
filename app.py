import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Dashboard tsDCS e mobilidade após AVC",
    page_icon="📊",
    layout="wide",
)


COLORS = {
    "tsDCS real": "#3B6FB6",
    "Sham": "#D55E73",
}
SYMBOLS = {
    "tsDCS real": "circle",
    "Sham": "diamond",
}
ASSESSMENTS = [
    "Baseline",
    "Após 5 sessões",
    "Após 10 sessões",
    "Follow-up de 1 mês",
]


@st.cache_data
def load_data():
    ages = pd.DataFrame(
        {
            "Idade": [
                37, 63, 50, 38, 64, 52, 47, 44, 42, 61, 60, 52, 59, 63,
                38, 74, 46, 57, 49, 58, 59, 65, 38, 62, 63, 51, 75,
            ]
        }
    )

    baseline = pd.DataFrame(
        {
            "Grupo": ["tsDCS real"] * 11 + ["Sham"] * 11,
            "TUG": [
                14.41333333, 12.50666667, 16.17666667, 44.15666667,
                109.9, 10.52, 58.47666667, 19.59333333, 9.296666667,
                136.9966667, 16.02333333, 29.14, 10.46333333, 18.73,
                7.636666667, 63.66666667, 18.90333333, 13.19, 14.31,
                37.26333333, 11.64333333, 24.09,
            ],
        }
    )

    motor = pd.DataFrame(
        {
            "Tempo desde o diagnóstico (meses)": [
                37, 56, 70, 36, 30, 36, 90, 34, 42, 59, 41, 15, 48,
                13, 77, 9, 62, 24, 90, 19, 31,
            ],
            "Fugl-Meyer de membro inferior": [
                19, 21, 27, 10, 21, 24, 23, 23, 21, 17, 28, 22, 25,
                10, 23, 24, 20, 23, 29, 28, 27,
            ],
            "Grupo": [
                "tsDCS real", "Sham", "Sham", "Sham", "tsDCS real",
                "Sham", "tsDCS real", "tsDCS real", "Sham", "tsDCS real",
                "tsDCS real", "Sham", "Sham", "tsDCS real", "tsDCS real",
                "tsDCS real", "Sham", "Sham", "Sham", "tsDCS real",
                "tsDCS real",
            ],
        }
    )

    trajectory = pd.DataFrame(
        {
            "Avaliação": ASSESSMENTS * 2,
            "Grupo": ["tsDCS real"] * 4 + ["Sham"] * 4,
            "Mediana do TUG": [16.18, 15.90, 13.22, 13.73, 18.73, 16.60, 12.82, 12.82],
        }
    )
    trajectory["Avaliação"] = pd.Categorical(
        trajectory["Avaliação"], categories=ASSESSMENTS, ordered=True
    )
    return ages, baseline, motor, trajectory


def format_figure(fig, height=390):
    fig.update_layout(
        height=height,
        margin=dict(l=24, r=24, t=58, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=14, color="#243447"),
        title=dict(font=dict(size=18, color="#17324D"), x=0.02, xanchor="left"),
        legend=dict(
            title_text="Grupo",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hoverlabel=dict(font_size=13),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#B7C5D3",
        tickcolor="#B7C5D3",
        title_font=dict(size=14),
    )
    fig.update_yaxes(
        gridcolor="#E6ECF2",
        zeroline=False,
        linecolor="#B7C5D3",
        tickcolor="#B7C5D3",
        title_font=dict(size=14),
    )
    return fig


ages, baseline, motor, trajectory = load_data()

st.markdown(
    """
    <style>
    .stApp { background: #F4F7FA; }
    .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1500px; }
    h1 { color: #17324D; letter-spacing: -0.02em; }
    h2, h3 { color: #17324D; }
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #DCE4EB;
        border-radius: 10px;
        padding: 14px 16px;
    }
    [data-testid="stMetricLabel"] { color: #526779; }
    [data-testid="stMetricValue"] { color: #17324D; }
    [data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border: 1px solid #DCE4EB;
        border-radius: 10px;
        padding: 4px 8px 2px 8px;
    }
    div[data-testid="stAlert"] { border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

title_col, info_col = st.columns([4, 1])
with title_col:
    st.title("Mobilidade e função motora após AVC")
    st.caption(
        "Análise exploratória de participantes acompanhados em um estudo com "
        "estimulação transcraniana por corrente contínua"
    )
with info_col:
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.info("Análise descritiva\n\nValores menores no TUG indicam melhor mobilidade.")

st.divider()

filter_col, note_col = st.columns([1.2, 3.8], vertical_alignment="bottom")
with filter_col:
    selected_groups = st.multiselect(
        "Grupos exibidos",
        options=list(COLORS),
        default=list(COLORS),
        help="O filtro atualiza os gráficos que possuem informação por grupo.",
    )
with note_col:
    st.caption(
        "Os gráficos utilizam os dados disponíveis em cada avaliação; por isso, "
        "o número de participantes varia entre as análises. Passe o cursor sobre "
        "os elementos para consultar valores exatos."
    )

if not selected_groups:
    st.warning("Selecione pelo menos um grupo para visualizar as comparações.")
    st.stop()

baseline_filtered = baseline[baseline["Grupo"].isin(selected_groups)]
motor_filtered = motor[motor["Grupo"].isin(selected_groups)]
trajectory_filtered = trajectory[trajectory["Grupo"].isin(selected_groups)]

metric_cols = st.columns(4)
metric_cols[0].metric("Idades registradas", f"{len(ages)}")
metric_cols[1].metric("TUG no baseline", f"{len(baseline_filtered)} participantes")
metric_cols[2].metric(
    "Mediana tsDCS real",
    "16,2 s" if "tsDCS real" in selected_groups else "—",
    help="Mediana do TUG no baseline.",
)
metric_cols[3].metric(
    "Mediana Sham",
    "18,7 s" if "Sham" in selected_groups else "—",
    help="Mediana do TUG no baseline.",
)

left, right = st.columns(2, gap="large")

with left:
    age_fig = px.histogram(
        ages,
        x="Idade",
        nbins=5,
        range_x=[35, 85],
        title="Distribuição da idade dos participantes",
        labels={"count": "Número de participantes"},
        color_discrete_sequence=[COLORS["tsDCS real"]],
    )
    age_fig.update_traces(
        marker_line_width=1,
        marker_line_color="#FFFFFF",
        hovertemplate="Faixa etária: %{x}<br>Participantes: %{y}<extra></extra>",
    )
    age_fig.update_layout(bargap=0.04, showlegend=False)
    age_fig.update_xaxes(dtick=10, title="Idade (anos)")
    age_fig.update_yaxes(title="Número de participantes", dtick=2)
    st.plotly_chart(
        format_figure(age_fig),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )
    st.caption("Predomínio de participantes entre 45 e 64 anos.")

with right:
    box_fig = px.box(
        baseline_filtered,
        x="Grupo",
        y="TUG",
        color="Grupo",
        points="all",
        color_discrete_map=COLORS,
        category_orders={"Grupo": list(COLORS)},
        title="TUG no baseline por grupo",
        labels={"TUG": "Tempo no TUG (segundos)"},
    )
    box_fig.update_traces(
        jitter=0.35,
        pointpos=0,
        marker=dict(size=8, opacity=0.78, line=dict(width=1, color="#FFFFFF")),
        hovertemplate="Grupo: %{x}<br>TUG: %{y:.1f} s<extra></extra>",
    )
    box_fig.update_layout(showlegend=False)
    box_fig.update_xaxes(title="Grupo")
    box_fig.update_yaxes(title="Tempo no TUG (segundos)", rangemode="tozero")
    st.plotly_chart(
        format_figure(box_fig),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )
    st.caption("Medianas próximas, com maior dispersão no grupo tsDCS real.")

left, right = st.columns(2, gap="large")

with left:
    scatter_fig = px.scatter(
        motor_filtered,
        x="Tempo desde o diagnóstico (meses)",
        y="Fugl-Meyer de membro inferior",
        color="Grupo",
        symbol="Grupo",
        color_discrete_map=COLORS,
        symbol_map=SYMBOLS,
        category_orders={"Grupo": list(COLORS)},
        title="Tempo desde o diagnóstico e função motora",
    )
    scatter_fig.update_traces(
        marker=dict(size=11, opacity=0.88, line=dict(width=1.2, color="#FFFFFF")),
        hovertemplate=(
            "Tempo desde o diagnóstico: %{x} meses<br>"
            "Fugl-Meyer de membro inferior: %{y} pontos<extra></extra>"
        ),
    )
    scatter_fig.update_xaxes(title="Tempo desde o diagnóstico do AVC (meses)")
    scatter_fig.update_yaxes(title="Fugl-Meyer de membro inferior (pontos)")
    st.plotly_chart(
        format_figure(scatter_fig),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )
    st.caption("Não se observa relação visual forte entre cronicidade e função motora.")

with right:
    line_fig = px.line(
        trajectory_filtered.sort_values("Avaliação"),
        x="Avaliação",
        y="Mediana do TUG",
        color="Grupo",
        symbol="Grupo",
        color_discrete_map=COLORS,
        symbol_map=SYMBOLS,
        category_orders={"Avaliação": ASSESSMENTS, "Grupo": list(COLORS)},
        markers=True,
        title="Evolução da mediana do TUG",
    )
    line_fig.update_traces(
        line=dict(width=3),
        marker=dict(size=10, line=dict(width=1.2, color="#FFFFFF")),
        hovertemplate=(
            "Avaliação: %{x}<br>Mediana do TUG: %{y:.1f} s<extra></extra>"
        ),
    )
    line_fig.update_xaxes(title="Momento da avaliação", tickangle=0)
    line_fig.update_yaxes(title="Mediana do TUG (segundos)", rangemode="tozero")
    st.plotly_chart(
        format_figure(line_fig),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )
    st.caption("A mediana do TUG diminui até a terceira avaliação em ambos os grupos.")

with st.expander("Como interpretar e quais são os limites desta visualização"):
    st.markdown(
        """
        - O TUG é expresso em segundos; menores valores indicam melhor desempenho de mobilidade.
        - Os resultados são descritivos e não demonstram efeito causal da intervenção.
        - O número de observações varia entre os gráficos por causa de dados ausentes.
        - Um registro incompatível com a escala esperada foi desconsiderado nas medianas das
          avaliações após 10 sessões e no follow-up, conforme a preparação da Atividade 1.
        """
    )

st.caption(
    "Fonte: base de estudo clínico em reabilitação neurológica utilizada na disciplina "
    "Visualização de Dados. Dashboard elaborado para fins acadêmicos."
)
