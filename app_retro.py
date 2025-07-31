"""
Sistema Nutri Análises - Aplicação Principal
Desenvolvido para análise de exames laboratoriais de pacientes
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="Nutri Análises",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Importar módulos
from modules.data_manager import DataManager
from modules.exam_analyzer import ExamAnalyzer
from modules.utils import apply_custom_css, show_header

# Aplicar CSS customizado
apply_custom_css()

# Inicializar gerenciadores
@st.cache_resource
def init_managers():
    data_manager = DataManager()
    exam_analyzer = ExamAnalyzer(data_manager)
    return data_manager, exam_analyzer

data_manager, exam_analyzer = init_managers()

# Estado da sessão
if 'paciente_ativo' not in st.session_state:
    st.session_state.paciente_ativo = None

def main():
    """Função principal da aplicação"""
    
    # Se não há paciente ativo, mostrar tela de seleção
    if st.session_state.paciente_ativo is None:
        show_patient_selection()
    else:
        show_patient_dashboard()

def show_patient_selection():
    """Tela de seleção/cadastro de paciente"""
    show_header()
    
    st.title("Seleção de Paciente")
    
    # Carregar pacientes existentes
    df_pacientes = data_manager.load_pacientes()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Pacientes Cadastrados")
        
        if not df_pacientes.empty:
            # Mostrar lista de pacientes
            for _, paciente in df_pacientes.iterrows():
                with st.container():
                    col_info, col_btn = st.columns([3, 1])
                    
                    with col_info:
                        st.write(f"**{paciente['nome']}** - {paciente['sexo']}, {paciente['idade']} anos")
                        if not pd.isna(paciente['peso_kg']) and not pd.isna(paciente['altura_m']):
                            imc_data = exam_analyzer.calculate_imc(paciente['peso_kg'], paciente['altura_m'])
                            st.write(f"Peso: {paciente['peso_kg']}kg | Altura: {paciente['altura_m']}m | IMC: {imc_data['valor']} ({imc_data['classificacao']})")
                    
                    with col_btn:
                        if st.button(f"Selecionar", key=f"select_{paciente['id']}"):
                            st.session_state.paciente_ativo = paciente.to_dict()
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("Nenhum paciente cadastrado ainda.")
    
    with col2:
        st.subheader("Novo Paciente")
        
        with st.form("novo_paciente"):
            nome = st.text_input("Nome completo*")
            
            col_sexo, col_idade = st.columns(2)
            with col_sexo:
                sexo = st.selectbox("Sexo*", ["M", "F"], format_func=lambda x: "Masculino" if x == "M" else "Feminino")
            with col_idade:
                idade = st.number_input("Idade*", min_value=0, max_value=120, value=30)
            
            col_peso, col_altura = st.columns(2)
            with col_peso:
                peso = st.number_input("Peso (kg)", min_value=0.0, max_value=300.0, value=70.0, step=0.1)
            with col_altura:
                altura = st.number_input("Altura (m)", min_value=0.0, max_value=3.0, value=1.70, step=0.01)
            
            notas = st.text_area("Observações")
            
            submitted = st.form_submit_button("Cadastrar Paciente")
            
            if submitted:
                if nome.strip():
                    paciente_data = {
                        'nome': nome.strip(),
                        'sexo': sexo,
                        'idade': idade,
                        'peso_kg': peso,
                        'altura_m': altura,
                        'notas': notas
                    }
                    
                    if data_manager.save_paciente(paciente_data):
                        st.success("Paciente cadastrado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao cadastrar paciente.")
                else:
                    st.error("Nome é obrigatório.")

def show_patient_dashboard():
    """Dashboard principal do paciente"""
    paciente = st.session_state.paciente_ativo
    
    # Cabeçalho com informações do paciente
    imc_data = exam_analyzer.calculate_imc(paciente['peso_kg'], paciente['altura_m'])
    patient_info = f"({paciente['sexo']}, {paciente['idade']} anos) - IMC: {imc_data['valor']} ({imc_data['classificacao']})"
    
    show_header(paciente['nome'], patient_info)
    
    # Botão para sair do paciente
    col1, col2, col3 = st.columns([1, 1, 8])
    with col1:
        if st.button("← Sair do paciente"):
            st.session_state.paciente_ativo = None
            st.rerun()
    
    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Dados Gerais", 
        "🧪 Inserção de Exames", 
        "📊 Acompanhamento", 
        "⚙️ Base de Referência"
    ])
    
    with tab1:
        show_dados_gerais()
    
    with tab2:
        show_insercao_exames()
    
    with tab3:
        show_acompanhamento()
    
    with tab4:
        show_base_referencia()

def show_dados_gerais():
    """Aba de dados gerais do paciente"""
    paciente = st.session_state.paciente_ativo
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Ficha do Paciente")
        
        with st.form("atualizar_dados"):
            peso_atual = st.number_input(
                "Peso atual (kg)", 
                value=float(paciente['peso_kg']), 
                min_value=0.0, 
                max_value=300.0, 
                step=0.1
            )
            
            altura_atual = st.number_input(
                "Altura (m)", 
                value=float(paciente['altura_m']), 
                min_value=0.0, 
                max_value=3.0, 
                step=0.01
            )
            
            # Calcular IMC em tempo real
            imc_data = exam_analyzer.calculate_imc(peso_atual, altura_atual)
            st.metric("IMC", f"{imc_data['valor']}", imc_data['classificacao'])
            
            notas_atuais = st.text_area(
                "Notas clínicas", 
                value=paciente.get('notas', ''),
                height=150
            )
            
            if st.form_submit_button("Salvar alterações"):
                # Atualizar dados do paciente
                paciente['peso_kg'] = peso_atual
                paciente['altura_m'] = altura_atual
                paciente['notas'] = notas_atuais
                
                if data_manager.save_paciente(paciente):
                    st.session_state.paciente_ativo = paciente
                    st.success("Dados atualizados com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao salvar dados.")
    
    with col2:
        st.subheader("Histórico de Peso")
        
        # Aqui seria implementado o gráfico de evolução do peso
        # Por enquanto, mostrar informação atual
        st.info("Funcionalidade de histórico de peso será implementada na próxima versão.")
        
        # Adicionar novo peso
        with st.expander("Adicionar registro de peso"):
            with st.form("novo_peso"):
                data_peso = st.date_input("Data", value=datetime.now().date())
                valor_peso = st.number_input("Peso (kg)", min_value=0.0, max_value=300.0, step=0.1)
                
                if st.form_submit_button("Adicionar"):
                    st.info("Funcionalidade será implementada.")

def show_insercao_exames():
    """Aba de inserção de exames"""
    paciente = st.session_state.paciente_ativo
    
    st.subheader("Inserção de Exames")
    
    # Escolher método de entrada
    metodo = st.radio(
        "Método de entrada:",
        ["Entrada Manual", "Importação CSV"],
        horizontal=True
    )
    
    if metodo == "Entrada Manual":
        show_entrada_manual()
    else:
        show_importacao_csv()

def show_entrada_manual():
    """Interface de entrada manual de exames"""
    paciente = st.session_state.paciente_ativo
    
    # Data de coleta
    data_coleta = st.date_input("Data de coleta*", value=datetime.now().date())
    
    st.subheader("Grade de Exames")
    
    # Inicializar estado da grade se não existir
    if 'grade_exames' not in st.session_state:
        st.session_state.grade_exames = []
    
    # Formulário para adicionar exame
    with st.form("adicionar_exame"):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Lista de parâmetros disponíveis
            referencias = data_manager.get_referencias()
            parametros_disponiveis = [param.title() for param in referencias.keys()]
            parametro = st.selectbox("Parâmetro", parametros_disponiveis)
        
        with col2:
            valor = st.number_input("Valor", step=0.01)
        
        with col3:
            # Buscar unidade do parâmetro selecionado
            if parametro:
                param_key = parametro.lower()
                unidade_padrao = referencias.get(param_key, {}).get('unidade_medida', '')
                unidade = st.text_input("Unidade", value=unidade_padrao)
            else:
                unidade = st.text_input("Unidade")
        
        if st.form_submit_button("Adicionar à grade"):
            if parametro and valor is not None:
                # Classificar exame
                classification = exam_analyzer.classify_exam(parametro, valor, paciente['sexo'])
                
                exame = {
                    'parametro': parametro,
                    'valor': valor,
                    'unidade': unidade,
                    'status': classification['status'],
                    'icon': classification['icon']
                }
                
                st.session_state.grade_exames.append(exame)
                st.rerun()
    
    # Mostrar grade atual
    if st.session_state.grade_exames:
        st.subheader("Exames na Grade")
        
        # Criar DataFrame para exibição
        df_grade = pd.DataFrame(st.session_state.grade_exames)
        
        # Adicionar faixas de referência
        for idx, row in df_grade.iterrows():
            ranges = exam_analyzer.get_reference_ranges(row['parametro'], paciente['sexo'])
            if ranges:
                ideal_range = f"{ranges['ideal_min'] or '-'} - {ranges['ideal_max'] or '-'}"
                ref_range = f"{ranges['ref_min'] or '-'} - {ranges['ref_max'] or '-'}"
                df_grade.at[idx, 'Faixa Ideal'] = ideal_range
                df_grade.at[idx, 'Faixa Referência'] = ref_range
        
        # Reordenar colunas
        cols_order = ['icon', 'parametro', 'valor', 'unidade', 'Faixa Ideal', 'Faixa Referência', 'status']
        df_display = df_grade[cols_order].copy()
        df_display.columns = ['', 'Parâmetro', 'Valor', 'Unidade', 'Ideal', 'Referência', 'Status']
        
        st.dataframe(df_display, use_container_width=True)
        
        # Botões de ação
        col1, col2, col3 = st.columns([1, 1, 6])
        
        with col1:
            if st.button("💾 Salvar exames"):
                # Preparar dados para salvar
                exames_para_salvar = []
                for exame in st.session_state.grade_exames:
                    exame_data = {
                        'parametro': exame['parametro'],
                        'valor': exame['valor'],
                        'unidade': exame['unidade'],
                        'data_coleta': data_coleta.strftime('%Y-%m-%d'),
                        'status': exame['status']
                    }
                    exames_para_salvar.append(exame_data)
                
                if data_manager.save_exames(exames_para_salvar, paciente['id']):
                    st.success(f"✅ {len(exames_para_salvar)} exames salvos com sucesso!")
                    st.session_state.grade_exames = []
                    st.rerun()
                else:
                    st.error("❌ Erro ao salvar exames.")
        
        with col2:
            if st.button("🗑️ Limpar grade"):
                st.session_state.grade_exames = []
                st.rerun()
    else:
        st.info("Nenhum exame na grade. Use o formulário acima para adicionar exames.")

def show_importacao_csv():
    """Interface de importação de CSV"""
    st.subheader("Importação de Arquivo CSV")
    
    # Instruções
    with st.expander("📋 Formato do arquivo CSV"):
        st.write("""
        **Cabeçalhos obrigatórios:**
        - `nome_exame`: Nome do exame/parâmetro
        - `valor`: Valor numérico do resultado
        - `unidade`: Unidade de medida
        - `data_exame`: Data da coleta (YYYY-MM-DD ou DD/MM/YYYY)
        
        **Exemplo:**
        ```
        nome_exame,valor,unidade,data_exame
        Glicose jejum,89,mg/dL,2025-01-15
        Colesterol total,180,mg/dL,2025-01-15
        ```
        """)
    
    # Upload do arquivo
    uploaded_file = st.file_uploader(
        "Escolha o arquivo CSV",
        type=['csv'],
        help="Arquivo deve estar em formato CSV com codificação UTF-8"
    )
    
    if uploaded_file is not None:
        try:
            # Ler arquivo CSV
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ Arquivo carregado: {len(df)} registros encontrados")
            
            # Validar dados
            validation = exam_analyzer.validate_csv_data(df)
            
            if not validation['valid']:
                st.error(f"❌ Erro na validação: {validation['error']}")
                return
            
            # Processar importação
            paciente = st.session_state.paciente_ativo
            result = exam_analyzer.process_csv_import(df, paciente['id'], paciente['sexo'])
            
            # Mostrar resultados
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✅ Exames Reconhecidos")
                if result['conhecidos']:
                    df_conhecidos = pd.DataFrame(result['conhecidos'])
                    st.dataframe(df_conhecidos, use_container_width=True)
                    
                    if st.button("💾 Salvar exames reconhecidos"):
                        if data_manager.save_exames(result['conhecidos'], paciente['id']):
                            st.success(f"✅ {len(result['conhecidos'])} exames salvos!")
                        else:
                            st.error("❌ Erro ao salvar exames.")
                else:
                    st.info("Nenhum exame reconhecido automaticamente.")
            
            with col2:
                st.subheader("❓ Exames Não Reconhecidos")
                if result['desconhecidos']:
                    df_desconhecidos = pd.DataFrame(result['desconhecidos'])
                    st.dataframe(df_desconhecidos, use_container_width=True)
                    st.info("Estes exames precisam ser vinculados manualmente na aba 'Base de Referência'.")
                else:
                    st.success("Todos os exames foram reconhecidos!")
            
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")

def show_acompanhamento():
    """Aba de acompanhamento de exames"""
    paciente = st.session_state.paciente_ativo
    
    st.subheader("Acompanhamento de Exames")
    
    # Carregar exames do paciente
    df_exames = data_manager.load_exames(paciente['id'])
    
    if df_exames.empty:
        st.info("Nenhum exame registrado para este paciente ainda.")
        return
    
    # Filtros
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # Filtro de parâmetro
        parametros_disponiveis = ['Todos'] + sorted(df_exames['parametro'].unique().tolist())
        parametro_selecionado = st.selectbox("Parâmetro", parametros_disponiveis)
    
    with col2:
        # Filtro de data
        data_inicio = st.date_input("Data início", value=pd.to_datetime(df_exames['data_coleta']).min().date())
        data_fim = st.date_input("Data fim", value=pd.to_datetime(df_exames['data_coleta']).max().date())
    
    with col3:
        # Filtro de status
        apenas_alterados = st.checkbox("Apenas alterados")
    
    # Aplicar filtros
    df_filtrado = df_exames.copy()
    
    if parametro_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['parametro'] == parametro_selecionado]
    
    df_filtrado['data_coleta'] = pd.to_datetime(df_filtrado['data_coleta'])
    df_filtrado = df_filtrado[
        (df_filtrado['data_coleta'].dt.date >= data_inicio) &
        (df_filtrado['data_coleta'].dt.date <= data_fim)
    ]
    
    if apenas_alterados:
        df_filtrado = df_filtrado[df_filtrado['status'] != 'Ideal']
    
    # Mostrar tabela de resultados
    if not df_filtrado.empty:
        st.subheader("Histórico de Exames")
        
        # Formatar dados para exibição
        df_display = df_filtrado.copy()
        df_display['data_coleta'] = df_display['data_coleta'].dt.strftime('%d/%m/%Y')
        df_display = df_display.sort_values('data_coleta', ascending=False)
        
        # Adicionar ícones de status
        status_icons = {
            'Ideal': '✅',
            'Referência': '⚠️',
            'Fora': '❌'
        }
        df_display['Status'] = df_display['status'].map(lambda x: f"{status_icons.get(x, '❓')} {x}")
        
        # Selecionar colunas para exibição
        cols_display = ['data_coleta', 'parametro', 'valor', 'unidade', 'Status']
        df_display = df_display[cols_display]
        df_display.columns = ['Data', 'Parâmetro', 'Valor', 'Unidade', 'Status']
        
        st.dataframe(df_display, use_container_width=True)
        
        # Gráfico de evolução (se um parâmetro específico estiver selecionado)
        if parametro_selecionado != 'Todos' and len(df_filtrado) > 1:
            st.subheader(f"Evolução - {parametro_selecionado}")
            
            from modules.utils import create_evolution_chart
            fig = create_evolution_chart(df_filtrado, parametro_selecionado)
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # Botão de exportação
        if st.button("📥 Exportar dados"):
            csv = df_display.to_csv(index=False)
            st.download_button(
                label="Baixar CSV",
                data=csv,
                file_name=f"exames_{paciente['nome'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.info("Nenhum exame encontrado com os filtros aplicados.")

def show_base_referencia():
    """Aba de base de referência"""
    st.subheader("Base de Referência de Valores")
    
    # Carregar dados de referência
    try:
        df_ref = pd.read_excel("data/valores_referencia.xlsx")
        
        st.info("💡 Esta aba permite visualizar e editar os valores de referência. Funcionalidade de edição será implementada na próxima versão.")
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            categorias = ['Todas'] + sorted(df_ref['categoria'].dropna().unique().tolist())
            categoria_selecionada = st.selectbox("Categoria", categorias)
        
        with col2:
            busca = st.text_input("Buscar parâmetro")
        
        # Aplicar filtros
        df_filtrado = df_ref.copy()
        
        if categoria_selecionada != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_selecionada]
        
        if busca:
            df_filtrado = df_filtrado[
                df_filtrado['parametro'].str.contains(busca, case=False, na=False)
            ]
        
        # Mostrar tabela
        if not df_filtrado.empty:
            # Selecionar colunas principais para exibição
            cols_display = [
                'parametro', 'categoria', 'unidade_medida',
                'valor_ideal_homem_min', 'valor_ideal_homem_max',
                'valor_ideal_mulher_min', 'valor_ideal_mulher_max',
                'observacao'
            ]
            
            df_display = df_filtrado[cols_display].copy()
            df_display.columns = [
                'Parâmetro', 'Categoria', 'Unidade',
                'Ideal H (min)', 'Ideal H (max)',
                'Ideal M (min)', 'Ideal M (max)',
                'Observações'
            ]
            
            st.dataframe(df_display, use_container_width=True)
            
            st.info(f"📊 Mostrando {len(df_display)} parâmetros de {len(df_ref)} total")
        else:
            st.warning("Nenhum parâmetro encontrado com os filtros aplicados.")
            
    except Exception as e:
        st.error(f"Erro ao carregar base de referência: {e}")

if __name__ == "__main__":
    main()

