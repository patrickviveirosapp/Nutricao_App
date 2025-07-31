"""
Sistema Nutri Análises - Aplicação Principal V2
Versão atualizada com tabelas por categoria e importação JSON
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

# Configuração da página
st.set_page_config(
    page_title="Nutri Análises",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Importar módulos
from modules.data_manager import DataManager
from modules.exam_analyzer_v2 import ExamAnalyzerV2
from modules.utils import apply_custom_css, show_header

# Aplicar CSS customizado
apply_custom_css()

# Inicializar gerenciadores
@st.cache_resource
def init_managers():
    data_manager = DataManager()
    exam_analyzer = ExamAnalyzerV2(data_manager)
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
        show_insercao_exames_v2()
    
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

def show_insercao_exames_v2():
    """Aba de inserção de exames - Versão 2 com tabelas por categoria"""
    paciente = st.session_state.paciente_ativo
    
    st.subheader("Inserção de Exames")
    
    # Escolher método de entrada
    metodo = st.radio(
        "Método de entrada:",
        ["Inserção Manual por Categoria", "Importação JSON"],
        horizontal=True
    )
    
    if metodo == "Inserção Manual por Categoria":
        show_insercao_manual_categorias()
    else:
        show_importacao_json()

def show_insercao_manual_categorias():
    """Interface de inserção manual organizada por categorias"""
    paciente = st.session_state.paciente_ativo
    
    # Data de coleta
    data_coleta = st.date_input("Data de coleta*", value=datetime.now().date())
    
    # Obter categorias
    categorias = exam_analyzer.categorias
    
    if not categorias:
        st.error("Erro ao carregar categorias de exames.")
        return
    
    # Inicializar estado dos exames se não existir
    if 'exames_por_categoria' not in st.session_state:
        st.session_state.exames_por_categoria = {}
    
    # Criar abas para cada categoria
    tabs = st.tabs(categorias)
    
    for i, categoria in enumerate(categorias):
        with tabs[i]:
            show_categoria_table(categoria, paciente['sexo'], data_coleta)
    
    # Botões de ação global
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 6])
    
    with col1:
        if st.button("💾 Salvar todos os exames"):
            salvar_todos_exames(paciente['id'], data_coleta)
    
    with col2:
        if st.button("🗑️ Limpar todos"):
            st.session_state.exames_por_categoria = {}
            st.rerun()

def show_categoria_table(categoria, sexo_paciente, data_coleta):
    """Mostra tabela interativa para uma categoria específica"""
    
    # Obter parâmetros da categoria
    parametros = exam_analyzer.get_parameters_by_category(categoria)
    
    if not parametros:
        st.info(f"Nenhum parâmetro encontrado para a categoria {categoria}")
        return
    
    st.markdown(f"""
    <div class="category-header">
        📋 {categoria} ({len(parametros)} parâmetros)
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar valores da categoria se não existir
    if categoria not in st.session_state.exames_por_categoria:
        st.session_state.exames_por_categoria[categoria] = {}
    
    # Criar tabela interativa
    with st.container():
        # Cabeçalhos
        cols = st.columns([3, 1, 1, 2, 2, 1, 1])
        cols[0].write("**Parâmetro**")
        cols[1].write("**Valor**")
        cols[2].write("**Unidade**")
        cols[3].write("**Faixa Ideal**")
        cols[4].write("**Faixa Referência**")
        cols[5].write("**Status**")
        cols[6].write("**Ação**")
        
        st.divider()
        
        # Linhas de parâmetros
        for param in parametros:
            cols = st.columns([3, 1, 1, 2, 2, 1, 1])
            
            # Nome do parâmetro
            cols[0].write(param['parametro'])
            
            # Campo de valor
            valor_key = f"{categoria}_{param['parametro']}_valor"
            valor_atual = st.session_state.exames_por_categoria[categoria].get(param['parametro'], {}).get('valor', 0.0)
            
            valor = cols[1].number_input(
                "Valor",
                value=valor_atual,
                step=0.01,
                key=valor_key,
                label_visibility="collapsed"
            )
            
            # Unidade
            cols[2].write(param['unidade'] or "")
            
            # Faixas de referência baseadas no sexo
            if sexo_paciente.upper() == 'M':
                ideal_min = param.get('valor_ideal_homem_min')
                ideal_max = param.get('valor_ideal_homem_max')
                ref_min = param.get('valor_ref_homem_min')
                ref_max = param.get('valor_ref_homem_max')
            else:
                ideal_min = param.get('valor_ideal_mulher_min')
                ideal_max = param.get('valor_ideal_mulher_max')
                ref_min = param.get('valor_ref_mulher_min')
                ref_max = param.get('valor_ref_mulher_max')
            
            # Mostrar faixas
            ideal_range = f"{ideal_min or '-'} - {ideal_max or '-'}"
            ref_range = f"{ref_min or '-'} - {ref_max or '-'}"
            
            cols[3].write(ideal_range)
            cols[4].write(ref_range)
            
            # Calcular e mostrar status
            if valor > 0:
                classification = exam_analyzer.classify_exam(param['parametro'], valor, sexo_paciente)
                status_color = classification['color']
                status_icon = classification['icon']
                status_text = classification['status']
                
                cols[5].markdown(f"""
                <div style="background-color: {status_color}; padding: 0.25rem; border-radius: 0.25rem; text-align: center;">
                    {status_icon} {status_text}
                </div>
                """, unsafe_allow_html=True)
                
                # Salvar no estado da sessão
                st.session_state.exames_por_categoria[categoria][param['parametro']] = {
                    'valor': valor,
                    'unidade': param['unidade'],
                    'status': status_text
                }
            else:
                cols[5].write("—")
            
            # Botão para limpar valor
            if cols[6].button("🗑️", key=f"clear_{categoria}_{param['parametro']}"):
                if param['parametro'] in st.session_state.exames_por_categoria[categoria]:
                    del st.session_state.exames_por_categoria[categoria][param['parametro']]
                st.rerun()

def show_importacao_json():
    """Interface de importação de arquivo JSON"""
    st.subheader("Importação de Arquivo JSON")
    
    # Data de coleta
    data_coleta = st.date_input("Data de coleta*", value=datetime.now().date())
    
    # Instruções
    with st.expander("📋 Formato do arquivo JSON"):
        st.write("""
        **Estrutura esperada:**
        ```json
        [
          {
            "parameter_name": "eritrocitos",
            "nome_original": "Hemácias",
            "unit": "milhões/mm³",
            "valor": 4.6
          },
          {
            "parameter_name": "glicose jejum",
            "nome_original": "Glicose em Jejum",
            "unit": "mg/dL",
            "valor": 89
          }
        ]
        ```
        
        **Campos obrigatórios:**
        - `parameter_name`: Nome do parâmetro para busca
        - `nome_original`: Nome original do exame
        - `unit`: Unidade de medida
        - `valor`: Valor numérico do resultado
        """)
    
    # Upload do arquivo
    uploaded_file = st.file_uploader(
        "Escolha o arquivo JSON",
        type=['json'],
        help="Arquivo deve estar em formato JSON válido"
    )
    
    if uploaded_file is not None:
        try:
            # Ler arquivo JSON
            json_content = uploaded_file.read().decode('utf-8')
            json_data = json.loads(json_content)
            
            st.success(f"✅ Arquivo carregado: {len(json_data)} registros encontrados")
            
            # Validar dados
            validation = exam_analyzer.validate_json_data(json_data)
            
            if not validation['valid']:
                st.error(f"❌ Erro na validação: {validation['error']}")
                return
            
            # Processar importação
            paciente = st.session_state.paciente_ativo
            result = exam_analyzer.process_json_import(
                json_data, 
                paciente['id'], 
                paciente['sexo'], 
                data_coleta.strftime('%Y-%m-%d')
            )
            
            # Mostrar resultados
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✅ Exames Reconhecidos")
                if result['conhecidos']:
                    df_conhecidos = pd.DataFrame(result['conhecidos'])
                    
                    # Adicionar ícones de status
                    status_icons = {
                        'Ideal': '✅',
                        'Referência': '☑️',
                        'Fora': '❌'
                    }
                    df_conhecidos['Status Visual'] = df_conhecidos['status'].map(
                        lambda x: f"{status_icons.get(x, '❓')} {x}"
                    )
                    
                    # Reordenar colunas
                    cols_display = ['parametro', 'valor', 'unidade', 'Status Visual']
                    df_display = df_conhecidos[cols_display].copy()
                    df_display.columns = ['Parâmetro', 'Valor', 'Unidade', 'Status']
                    
                    st.dataframe(df_display, use_container_width=True)
                    
                    
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
            
        except json.JSONDecodeError as e:
            st.error(f"❌ Erro ao decodificar JSON: {str(e)}")
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")

def salvar_todos_exames(id_paciente, data_coleta):
    """Salva todos os exames preenchidos nas categorias"""
    exames_para_salvar = []
    
    for categoria, parametros in st.session_state.exames_por_categoria.items():
        for parametro, dados in parametros.items():
            if dados['valor'] > 0:  # Só salvar se valor foi preenchido
                exame_data = {
                    'parametro': parametro,
                    'valor': dados['valor'],
                    'unidade': dados['unidade'],
                    'data_coleta': data_coleta.strftime('%Y-%m-%d'),
                    'status': dados['status']
                }
                exames_para_salvar.append(exame_data)
    
    if exames_para_salvar:
        if data_manager.save_exames(exames_para_salvar, id_paciente):
            st.success(f"✅ {len(exames_para_salvar)} exames salvos com sucesso!")
            st.session_state.exames_por_categoria = {}
            st.rerun()
        else:
            st.error("❌ Erro ao salvar exames.")
    else:
        st.warning("⚠️ Nenhum exame preenchido para salvar.")

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

