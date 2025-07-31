"""
Funções utilitárias para o Sistema Nutri Análises
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def apply_custom_css():
    """Aplica CSS customizado ao Streamlit com tema claro e alta legibilidade"""
    st.markdown("""
    <style>
    /* Configurações globais - Tema Claro com Alta Legibilidade */
    .main {
        font-family: Arial, sans-serif;
        font-size: 13pt;
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    .stApp {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* Texto principal */
    .stMarkdown, .stText, p, div, span, label {
        color: #212529 !important;
    }
                
    
    /* Cabeçalhos */
    h1, h2, h3, h4, h5, h6 {
        color: #212529 !important;
        font-weight: 600 !important;
    }
    
    /* Cabeçalho do sistema */
    .header-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #007bff;
        border: 1px solid #e9ecef;
        color: #212529 !important;
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #007bff !important;
        margin: 0;
    }
    
    .patient-info {
        font-size: 1rem;
        color: #495057 !important;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    /* Tabelas com status colorido */
    .status-ideal {
        background-color: #d4edda !important;
        color: #155724 !important;
        border: 1px solid #c3e6cb !important;
        font-weight: 600 !important;
    }
    
    .status-referencia {
        background-color: #fff3cd !important;
        color: #856404 !important;
        border: 1px solid #ffeaa7 !important;
        font-weight: 600 !important;
    }
    
    .status-fora {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border: 1px solid #f5c6cb !important;
        font-weight: 600 !important;
    }
    
    /* Tabelas interativas */
    .exam-table {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        margin: 1rem 0;
        color: #212529 !important;
    }
    
    .exam-table th {
        background-color: #f8f9fa;
        color: #212529 !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #dee2e6;
        padding: 0.75rem;
    }
    
    .exam-table td {
        padding: 0.5rem;
        border-bottom: 1px solid #dee2e6;
        background-color: #ffffff;
        color: #212529 !important;
    }
    
    .exam-table input {
        border: 1px solid #ced4da;
        border-radius: 0.25rem;
        padding: 0.375rem 0.75rem;
        background-color: #ffffff;
        color: #212529 !important;
        font-weight: 500;
    }
    
    .exam-table input:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        color: #212529 !important;
    }
    
    /* Botões customizados */
    .stButton > button {
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
        padding: 0.5rem 1rem;
        font-weight: 600;
        background-color: #d1ecf1;
        color: #0c5460 !important;
    }

    .stButton > button:hover {
        background-color: #bee5eb;
        border-color: #a8d4de;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        color: #0c5460 !important;
    }
    
    /* Cards informativos */
    .info-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
        color: #212529 !important;
    }
    
    .metric-card {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white !important;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #007bff;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
        color: white !important;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
        color: white !important;
    }
    
    /* Alertas */
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724 !important;
        padding: 0.75rem 1.25rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404 !important;
        padding: 0.75rem 1.25rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24 !important;
        padding: 0.75rem 1.25rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    .alert-info {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460 !important;
        padding: 0.75rem 1.25rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    /* Sidebar customizada */
    .css-1d391kg {
        background-color: #f8f9fa;
        color: #212529 !important;
    }
    
    /* Abas customizadas */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 0.25rem;
        color: #495057 !important;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #d1ecf1;
        color: #0c5460 !important;
        font-weight: 700;
        border-bottom: 2px solid #bee5eb;
    }

    
    /* Inputs customizados */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 0.25rem;
        color: #212529 !important;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        color: #212529 !important;
    }
    
    .stSelectbox > div > div > div {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 0.25rem;
        color: #212529 !important;
    }
    
    .stSelectbox label {
        color: #212529 !important;
        font-weight: 600;
    }
    
    /* Labels e textos de formulário */
    .stTextInput label, .stSelectbox label, .stNumberInput label, .stDateInput label {
        color: #212529 !important;
        font-weight: 600;
        font-size: 14px;
    }
    
    /* DataFrames customizados */
    .dataframe {
        background-color: #ffffff !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 0.5rem !important;
        color: #212529 !important;
    }
    
    .dataframe th {
        background-color: #f8f9fa !important;
        color: #212529 !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #dee2e6 !important;
    }
    
    .dataframe td {
        background-color: #ffffff !important;
        color: #212529 !important;
        font-weight: 500;
        border-bottom: 1px solid #dee2e6 !important;
    }
    
    /* Categoria headers */
    .category-header {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 1rem 0 0.5rem 0;
        color: #212529 !important;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    /* Radio buttons */
    .stRadio > div {
        color: #212529 !important;
    }
    
    .stRadio label {
        color: #212529 !important;
        font-weight: 600;
    }
    
    /* Checkboxes */
    .stCheckbox > div {
        color: #212529 !important;
    }
    
    .stCheckbox label {
        color: #212529 !important;
        font-weight: 600;
    }
    
    /* Métricas */
    .metric-container {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        color: #212529 !important;
    }
    
    /* Texto de ajuda e informações */
    .stInfo, .stSuccess, .stWarning, .stError {
        color: #212529 !important;
        font-weight: 500;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        color: #212529 !important;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        color: #212529 !important;
    }
    
    /* File uploader */
    .stFileUploader label {
        color: #212529 !important;
        font-weight: 600;
    }
    
    .stFileUploader > div {
        color: #212529 !important;
    }
    
    /* Texto geral do Streamlit */
    .element-container {
        color: #212529 !important;
    }
    
    /* Ocultar menu do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def show_header(patient_name=None, patient_info=None):
    """Exibe cabeçalho do sistema"""
    st.markdown(f"""
    <div class="header-container">
        <h1 class="header-title">🩺 Nutri Análises</h1>
        {f'<p class="patient-info">Paciente: {patient_name} {patient_info or ""}</p>' if patient_name else ''}
    </div>
    """, unsafe_allow_html=True)

def format_dataframe_with_status(df, status_column='status'):
    """Formata DataFrame com cores baseadas no status"""
    if status_column not in df.columns:
        return df
    
    def highlight_status(row):
        if row[status_column] == 'Ideal':
            return ['background-color: #d4edda; color: #155724'] * len(row)
        elif row[status_column] == 'Referência':
            return ['background-color: #fff3cd; color: #856404'] * len(row)
        elif row[status_column] == 'Fora':
            return ['background-color: #f8d7da; color: #721c24'] * len(row)
        else:
            return [''] * len(row)
    
    return df.style.apply(highlight_status, axis=1)

def create_evolution_chart(df, parameter, date_column='data_coleta', value_column='valor'):
    """Cria gráfico de evolução de um parâmetro"""
    if df.empty:
        return None
    
    # Filtrar dados do parâmetro
    df_param = df[df['parametro'] == parameter].copy()
    
    if df_param.empty:
        return None
    
    # Converter data
    df_param[date_column] = pd.to_datetime(df_param[date_column])
    df_param = df_param.sort_values(date_column)
    
    # Definir cores baseadas no status
    color_map = {
        'Ideal': '#28a745',
        'Referência': '#ffc107',
        'Fora': '#dc3545'
    }
    
    colors = [color_map.get(status, '#6c757d') for status in df_param['status']]
    
    # Criar gráfico
    fig = go.Figure()
    
    # Linha de evolução
    fig.add_trace(go.Scatter(
        x=df_param[date_column],
        y=df_param[value_column],
        mode='lines+markers',
        line=dict(color='#007bff', width=2),
        marker=dict(
            color=colors,
            size=8,
            line=dict(color='white', width=2)
        ),
        name=parameter,
        hovertemplate='<b>%{text}</b><br>Data: %{x}<br>Valor: %{y}<extra></extra>',
        text=df_param['status']
    ))
    
    # Configurar layout
    fig.update_layout(
        title=f'Evolução - {parameter}',
        xaxis_title='Data',
        yaxis_title='Valor',
        hovermode='closest',
        showlegend=False,
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def create_weight_chart(df_weight):
    """Cria gráfico de evolução do peso"""
    if df_weight.empty:
        return None
    
    fig = px.line(
        df_weight, 
        x='data', 
        y='peso_kg',
        title='Evolução do Peso',
        markers=True
    )
    
    fig.update_layout(
        xaxis_title='Data',
        yaxis_title='Peso (kg)',
        height=300,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def validate_numeric_input(value, field_name):
    """Valida entrada numérica"""
    try:
        return float(value)
    except (ValueError, TypeError):
        st.error(f"Valor inválido para {field_name}. Digite um número válido.")
        return None

def validate_date_input(date_value):
    """Valida entrada de data"""
    if date_value is None:
        st.error("Data é obrigatória.")
        return None
    return date_value

def show_success_message(message):
    """Exibe mensagem de sucesso"""
    st.markdown(f'<div class="alert-success">{message}</div>', unsafe_allow_html=True)

def show_warning_message(message):
    """Exibe mensagem de aviso"""
    st.markdown(f'<div class="alert-warning">{message}</div>', unsafe_allow_html=True)

def show_error_message(message):
    """Exibe mensagem de erro"""
    st.markdown(f'<div class="alert-danger">{message}</div>', unsafe_allow_html=True)

def create_metric_card(title, value, subtitle=None):
    """Cria card de métrica"""
    subtitle_html = f'<p class="metric-label">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{value}</p>
        <p class="metric-label">{title}</p>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def export_to_csv(df, filename):
    """Exporta DataFrame para CSV"""
    csv = df.to_csv(index=False)
    return csv

def format_date_br(date_value):
    """Formata data para padrão brasileiro"""
    if pd.isna(date_value):
        return ""
    
    if isinstance(date_value, str):
        try:
            date_value = pd.to_datetime(date_value)
        except:
            return date_value
    
    return date_value.strftime('%d/%m/%Y')

def parse_date_input(date_str):
    """Converte string de data para datetime"""
    if not date_str:
        return None
    
    # Tentar diferentes formatos
    formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

