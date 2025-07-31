# Sistema Nutri Análises - Versão 2.0

Sistema web desenvolvido em Python/Streamlit para análise de exames laboratoriais de pacientes por nutricionistas.

## 🆕 **Novidades da Versão 2.0**

### ✨ **Nova Inserção Manual por Categoria**
- **Tabelas organizadas por categoria**: Perfil Metabólico, Hemograma, Perfil Tireoidiano, etc.
- **Visualização em tempo real**: Valores de referência e ideais exibidos lado a lado
- **Status automático**: Classificação instantânea com cores (Verde=Ideal, Laranja=Referência, Vermelho=Fora)
- **Interface intuitiva**: Preenchimento direto na tabela com feedback visual imediato

### 📁 **Nova Importação JSON**
- **Formato simplificado**: Apenas dados dos exames (parameter_name, nome_original, unit, valor)
- **Data flexível**: Preenchida pelo nutricionista na interface do sistema
- **Validação automática**: Verificação de formato e consistência dos dados
- **Separação inteligente**: Exames reconhecidos vs. não reconhecidos

### 🎨 **Tema Claro**
- **Fundo branco**: Interface limpa e profissional
- **Cores intuitivas**: Sistema de cores consistente para status
- **Tipografia otimizada**: Arial 13pt para melhor legibilidade
- **Design responsivo**: Adaptado para diferentes tamanhos de tela

## 🎯 Funcionalidades Principais

### ✅ Gestão de Pacientes
- Cadastro completo de pacientes (nome, sexo, idade, peso, altura)
- Cálculo automático de IMC com classificação
- Histórico de peso (funcionalidade base implementada)
- Notas clínicas editáveis

### ✅ Inserção de Exames - NOVA VERSÃO
- **Inserção Manual por Categoria**: Interface com tabelas organizadas por categoria
  - 9 categorias disponíveis: Adequação cálcio, Adrenal, Hemograma Leucograma, Metais Tóxicos, Minerais e vitaminas, Perfil Metabólico Cardiovascular, Perfil Tireoidiano, Saúde intestinal, Urina
  - 37 parâmetros no Perfil Metabólico Cardiovascular
  - Visualização simultânea de faixas ideais e de referência
  - Status em tempo real ao digitar valores
- **Importação JSON**: Suporte ao novo formato JSON simplificado
- **Classificação Automática**: Status visual (Ideal ✅ / Referência ⚠️ / Fora ❌)
- **Validação**: Verificação de tipos de dados e consistência

### ✅ Acompanhamento
- Histórico completo de exames por paciente
- Filtros por parâmetro, data e status
- Tabela interativa com cores por status
- Exportação de dados em CSV
- Gráficos de evolução (base implementada)

### ✅ Base de Referência
- Visualização completa dos valores de referência
- Filtros por categoria e busca por parâmetro
- 132 parâmetros pré-carregados
- Valores ideais e de referência por sexo
- Interface preparada para edição futura

## 🏗️ Arquitetura Técnica

### Tecnologias Utilizadas
- **Python 3.11** - Linguagem principal
- **Streamlit** - Framework web
- **Pandas** - Manipulação de dados
- **Plotly** - Gráficos interativos
- **OpenPyXL** - Leitura/escrita Excel

### Estrutura do Projeto
```
nutri_analises/
├── app_v2.py              # Aplicação principal V2 (NOVA)
├── app.py                 # Aplicação original (mantida)
├── data/
│   ├── pacientes.xlsx     # Dados dos pacientes
│   ├── exames.xlsx        # Histórico de exames
│   └── valores_referencia.xlsx  # Base de referência
├── modules/
│   ├── data_manager.py    # Gerenciamento de dados
│   ├── exam_analyzer_v2.py # Análise de exames V2 (NOVA)
│   ├── exam_analyzer.py   # Análise original (mantida)
│   └── utils.py          # Funções utilitárias (atualizada)
└── README.md             # Esta documentação
```

### Persistência de Dados
- **Arquivos Excel**: Formato acessível e editável
- **Backup Automático**: Versioning da base de referência
- **Cache Inteligente**: Otimização de performance

## 🚀 Como Usar

### 1. Instalação
```bash
# Instalar dependências
pip install streamlit pandas plotly openpyxl

# Executar aplicação V2 (recomendada)
streamlit run app_v2.py

# Ou executar aplicação original
streamlit run app.py
```

### 2. Fluxo de Trabalho
1. **Cadastrar Paciente**: Preencher dados básicos
2. **Selecionar Paciente**: Escolher da lista ou cadastrar novo
3. **Inserir Exames**: 
   - **Manual por Categoria**: Navegar pelas abas de categoria e preencher valores
   - **Importação JSON**: Fazer upload do arquivo JSON
4. **Acompanhar Evolução**: Visualizar histórico e gráficos
5. **Consultar Referências**: Verificar valores ideais

### 3. Formato JSON para Importação (NOVO)
```json
[
  {
    "parameter_name": "glicose jejum",
    "nome_original": "Glicose em Jejum",
    "unit": "mg/dL",
    "valor": 92
  },
  {
    "parameter_name": "colesterol total",
    "nome_original": "Colesterol Total",
    "unit": "mg/dL",
    "valor": 195
  }
]
```

**Campos obrigatórios:**
- `parameter_name`: Nome do parâmetro para busca na base
- `nome_original`: Nome original do exame
- `unit`: Unidade de medida
- `valor`: Valor numérico do resultado

**Nota:** A data de coleta é preenchida pelo nutricionista na interface.

## 📊 Sistema de Classificação

### Status dos Exames
- **✅ Ideal**: Valor dentro da faixa ideal (verde)
- **⚠️ Referência**: Valor na faixa de referência mas fora do ideal (laranja)
- **❌ Fora**: Valor fora da faixa de referência (vermelho)

### Critérios de Classificação
1. Localizar parâmetro na base de referência
2. Selecionar limites por sexo do paciente
3. Comparar valor com faixas ideal e referência
4. Aplicar cor e ícone correspondente

## 🎨 Interface do Usuário - ATUALIZADA

### Design Responsivo
- **Tema claro** com fundo branco
- **Layout wide** otimizado para desktop
- **Cores intuitivas** por status
- **Tipografia Arial 13pt**
- **Componentes interativos** com feedback visual

### Navegação por Abas
- **📋 Dados Gerais**: Ficha do paciente
- **🧪 Inserção de Exames**: 
  - Inserção Manual por Categoria (NOVA)
  - Importação JSON (ATUALIZADA)
- **📊 Acompanhamento**: Histórico e evolução
- **⚙️ Base de Referência**: Valores de referência

### Inserção Manual por Categoria (NOVA)
- **Abas por categoria**: Organização intuitiva dos exames
- **Tabela interativa**: Preenchimento direto com validação
- **Faixas visíveis**: Valores ideais e de referência sempre visíveis
- **Status em tempo real**: Atualização instantânea ao digitar
- **Botões de ação**: Salvar todos, limpar todos, limpar individual

## 📈 Base de Dados

### Parâmetros Incluídos
- **Perfil Metabólico Cardiovascular**: 37 parâmetros (Glicose, HbA1C, Insulina, Colesterol, etc.)
- **Hemograma Leucograma**: Eritrócitos, Hemoglobina, Leucócitos, etc.
- **Perfil Tireoidiano**: TSH, T3, T4, Anticorpos, etc.
- **Metais Tóxicos**: Chumbo, Mercúrio, Cádmio, etc.
- **Minerais e Vitaminas**: Zinco, Selênio, Vitaminas, etc.
- **Adequação Cálcio**: Parâmetros relacionados ao metabolismo do cálcio
- **Adrenal**: Hormônios adrenais e cortisol
- **Saúde Intestinal**: Marcadores de permeabilidade e inflamação
- **Urina**: Análise urinária completa

### Valores por Sexo
- Limites ideais específicos para homens e mulheres
- Limites de referência laboratorial
- Observações clínicas detalhadas
- Unidades de medida padronizadas

## 🔧 Funcionalidades Avançadas

### Validações Implementadas
- Tipos de dados numéricos
- Formatos de data válidos
- Consistência de limites
- Duplicatas de exames
- Validação de JSON (NOVA)

### Performance
- Cache de dados de referência
- Carregamento otimizado por categoria
- Interface responsiva
- Feedback visual imediato
- Atualização em tempo real

## 🚀 Próximas Versões

### Funcionalidades Planejadas
- Edição completa da base de referência
- Gráficos de evolução avançados
- Relatórios em PDF
- Histórico detalhado de peso
- Backup em nuvem
- Múltiplos usuários

### Melhorias Técnicas
- Migração para SQLite
- API REST
- Autenticação
- Logs de auditoria
- Testes automatizados

## 📝 Notas de Desenvolvimento

### Conformidade com Especificações V2
✅ Todas as novas especificações foram implementadas:
- Inserção manual organizada por categorias
- Tabelas interativas com valores de referência visíveis
- Status em tempo real
- Importação JSON simplificada
- Data preenchida pelo nutricionista
- Tema claro com fundo branco

### Qualidade do Código
- Modularização clara com versioning
- Documentação inline atualizada
- Tratamento de erros robusto
- Padrões de codificação mantidos
- Estrutura escalável preservada

### Compatibilidade
- **app_v2.py**: Nova versão com todas as melhorias
- **app.py**: Versão original mantida para compatibilidade
- **Dados compartilhados**: Mesma base de dados para ambas versões

---

**Versão 2.0 - Desenvolvida seguindo as novas especificações do usuário**
**Sistema aprimorado e pronto para uso em ambiente de produção**

