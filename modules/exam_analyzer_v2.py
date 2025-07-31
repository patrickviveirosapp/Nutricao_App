"""
Módulo de análise de exames para o Sistema Nutri Análises - Versão 2
Suporte para JSON e tabelas por categoria
"""

import pandas as pd
import streamlit as st
import json

class ExamAnalyzerV2:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.referencias = data_manager.get_referencias()
        self.categorias = self._get_categorias()
    
    def _get_categorias(self):
        """Extrai as categorias únicas dos valores de referência"""
        try:
            df_ref = pd.read_excel("data/valores_referencia.xlsx")
            categorias = df_ref['categoria'].dropna().unique().tolist()
            return sorted(categorias)
        except Exception as e:
            st.error(f"Erro ao carregar categorias: {e}")
            return []
    
    def get_parameters_by_category(self, categoria):
        """Retorna parâmetros de uma categoria específica"""
        try:
            df_ref = pd.read_excel("data/valores_referencia.xlsx")
            df_categoria = df_ref[df_ref['categoria'] == categoria]
            
            parametros = []
            for _, row in df_categoria.iterrows():
                parametros.append({
                    'parametro': row['parametro'],
                    'unidade': row['unidade_medida'],
                    'valor_ideal_homem_min': row.get('valor_ideal_homem_min'),
                    'valor_ideal_homem_max': row.get('valor_ideal_homem_max'),
                    'valor_ideal_mulher_min': row.get('valor_ideal_mulher_min'),
                    'valor_ideal_mulher_max': row.get('valor_ideal_mulher_max'),
                    'valor_ref_homem_min': row.get('valor_ref_homem_min'),
                    'valor_ref_homem_max': row.get('valor_ref_homem_max'),
                    'valor_ref_mulher_min': row.get('valor_ref_mulher_min'),
                    'valor_ref_mulher_max': row.get('valor_ref_mulher_max'),
                    'observacao': row.get('observacao', '')
                })
            
            return parametros
        except Exception as e:
            st.error(f"Erro ao carregar parâmetros da categoria {categoria}: {e}")
            return []
    
    def classify_exam(self, parametro, valor, sexo):
        """
        Classifica um exame baseado nos valores de referência
        
        Args:
            parametro (str): Nome do parâmetro do exame
            valor (float): Valor do exame
            sexo (str): Sexo do paciente ('M' ou 'F')
        
        Returns:
            dict: {'status': str, 'color': str, 'icon': str}
        """
        param_key = parametro.lower().strip()
        
        if param_key not in self.referencias:
            return {
                'status': 'Não encontrado',
                'color': '#6C757D',
                'icon': '❓'
            }
        
        ref_data = self.referencias[param_key]
        
        # Selecionar limites baseado no sexo
        if sexo.upper() == 'M':
            ideal_min = ref_data.get('valor_ideal_homem_min')
            ideal_max = ref_data.get('valor_ideal_homem_max')
            ref_min = ref_data.get('valor_ref_homem_min')
            ref_max = ref_data.get('valor_ref_homem_max')
        else:
            ideal_min = ref_data.get('valor_ideal_mulher_min')
            ideal_max = ref_data.get('valor_ideal_mulher_max')
            ref_min = ref_data.get('valor_ref_mulher_min')
            ref_max = ref_data.get('valor_ref_mulher_max')
        
        # Verificar se há valores válidos
        if pd.isna(ideal_min) and pd.isna(ideal_max) and pd.isna(ref_min) and pd.isna(ref_max):
            return {
                'status': 'Sem referência',
                'color': '#6C757D',
                'icon': '—'
            }
        
        # Classificar valor
        try:
            valor = float(valor)
            
            # Verificar se está na faixa ideal
            if not pd.isna(ideal_min) and not pd.isna(ideal_max):
                if ideal_min <= valor <= ideal_max:
                    return {
                        'status': 'Ideal',
                        'color': '#D4EDDA',
                        'icon': '✅'
                    }
            
            # Verificar se está na faixa de referência
            if not pd.isna(ref_min) and not pd.isna(ref_max):
                if ref_min <= valor <= ref_max:
                    return {
                        'status': 'Referência',
                        'color': '#FFF3CD',
                        'icon': '☑️'
                    }
            
            # Fora da referência
            if not pd.isna(ref_min) and valor < ref_min:
                return {
                    'status': 'Abaixo da Referência',
                    'color': '#F8D7DA',
                    'icon': '⬇️'
                }

            # Acima da referência
            if not pd.isna(ref_max) and valor > ref_max:
                return {
                    'status': 'Acima da Referência',
                    'color': '#F8D7DA',
                    'icon': '⬆️'
                }
            
        except (ValueError, TypeError):
            return {
                'status': 'Valor inválido',
                'color': '#6C757D',
                'icon': '⚠️'
            }
    
    def get_reference_ranges(self, parametro, sexo):
        """
        Retorna as faixas de referência para um parâmetro
        
        Args:
            parametro (str): Nome do parâmetro
            sexo (str): Sexo do paciente ('M' ou 'F')
        
        Returns:
            dict: Faixas ideal e referência
        """
        param_key = parametro.lower().strip()
        
        if param_key not in self.referencias:
            return None
        
        ref_data = self.referencias[param_key]
        
        if sexo.upper() == 'M':
            return {
                'ideal_min': ref_data.get('valor_ideal_homem_min'),
                'ideal_max': ref_data.get('valor_ideal_homem_max'),
                'ref_min': ref_data.get('valor_ref_homem_min'),
                'ref_max': ref_data.get('valor_ref_homem_max'),
                'unidade': ref_data.get('unidade_medida'),
                'observacao': ref_data.get('observacao')
            }
        else:
            return {
                'ideal_min': ref_data.get('valor_ideal_mulher_min'),
                'ideal_max': ref_data.get('valor_ideal_mulher_max'),
                'ref_min': ref_data.get('valor_ref_mulher_min'),
                'ref_max': ref_data.get('valor_ref_mulher_max'),
                'unidade': ref_data.get('unidade_medida'),
                'observacao': ref_data.get('observacao')
            }
    
    def get_available_parameters(self):
        """Retorna lista de parâmetros disponíveis"""
        return list(self.referencias.keys())
    
    def validate_json_data(self, json_data):
        """
        Valida dados de JSON importado
        
        Args:
            json_data (list): Lista de dicionários com dados dos exames
        
        Returns:
            dict: Resultado da validação
        """
        required_fields = ['parameter_name', 'nome_original', 'unit', 'valor']
        
        if not isinstance(json_data, list):
            return {
                'valid': False,
                'error': "JSON deve ser uma lista de objetos"
            }
        
        errors = []
        
        for idx, item in enumerate(json_data):
            if not isinstance(item, dict):
                errors.append(f"Item {idx + 1}: Deve ser um objeto")
                continue
            
            # Verificar campos obrigatórios
            missing_fields = [field for field in required_fields if field not in item]
            if missing_fields:
                errors.append(f"Item {idx + 1}: Campos ausentes: {', '.join(missing_fields)}")
                continue
            
            # Validar valor numérico
            try:
                float(item['valor'])
            except (ValueError, TypeError):
                errors.append(f"Item {idx + 1}: Valor '{item['valor']}' não é numérico")
        
        if errors:
            return {
                'valid': False,
                'error': '; '.join(errors[:5])  # Mostrar apenas os primeiros 5 erros
            }
        
        return {'valid': True}
    
    def process_json_import(self, json_data, id_paciente, sexo_paciente, data_coleta):
        """
        Processa importação de JSON
        
        Args:
            json_data (list): Lista de dicionários com dados dos exames
            id_paciente (int): ID do paciente
            sexo_paciente (str): Sexo do paciente
            data_coleta (str): Data de coleta no formato YYYY-MM-DD
        
        Returns:
            dict: Resultado do processamento
        """
        # Separar parâmetros conhecidos e desconhecidos
        conhecidos = []
        desconhecidos = []
        
        for item in json_data:
            # Tentar encontrar o parâmetro usando parameter_name ou nome_original
            param_key = item['parameter_name'].lower().strip()
            nome_original_key = item['nome_original'].lower().strip()
            
            found = False
            parametro_encontrado = None
            
            # Buscar por parameter_name
            if param_key in self.referencias:
                parametro_encontrado = item['parameter_name']
                found = True
            # Buscar por nome_original
            elif nome_original_key in self.referencias:
                parametro_encontrado = item['nome_original']
                found = True
            else:
                # Buscar por correspondência parcial
                for ref_param in self.referencias.keys():
                    if param_key in ref_param or ref_param in param_key:
                        parametro_encontrado = list(self.referencias.keys())[list(self.referencias.keys()).index(ref_param)]
                        found = True
                        break
                    if nome_original_key in ref_param or ref_param in nome_original_key:
                        parametro_encontrado = list(self.referencias.keys())[list(self.referencias.keys()).index(ref_param)]
                        found = True
                        break
            
            if found:
                # Classificar exame
                classification = self.classify_exam(
                    parametro_encontrado, 
                    item['valor'], 
                    sexo_paciente
                )
                
                exame_data = {
                    'parametro': parametro_encontrado,
                    'valor': float(item['valor']),
                    'unidade': item['unit'],
                    'data_coleta': data_coleta,
                    'status': classification['status']
                }
                conhecidos.append(exame_data)
            else:
                desconhecidos.append({
                    'parameter_name': item['parameter_name'],
                    'nome_original': item['nome_original'],
                    'valor': item['valor'],
                    'unit': item['unit']
                })
        
        return {
            'conhecidos': conhecidos,
            'desconhecidos': desconhecidos
        }
    
    def calculate_imc(self, peso_kg, altura_m):
        """Calcula IMC e retorna classificação"""
        try:
            imc = peso_kg / (altura_m ** 2)
            
            if imc < 18.5:
                classificacao = "Baixo peso"
            elif imc < 25:
                classificacao = "Eutrofia"
            elif imc < 30:
                classificacao = "Sobrepeso"
            elif imc < 35:
                classificacao = "Obesidade grau I"
            elif imc < 40:
                classificacao = "Obesidade grau II"
            else:
                classificacao = "Obesidade grau III"
            
            return {
                'valor': round(imc, 1),
                'classificacao': classificacao
            }
        except (ValueError, TypeError, ZeroDivisionError):
            return {
                'valor': 0,
                'classificacao': "Dados inválidos"
            }
    
    def find_parameter_by_name(self, search_name):
        """
        Busca parâmetro por nome (flexível)
        
        Args:
            search_name (str): Nome a ser buscado
        
        Returns:
            str or None: Nome do parâmetro encontrado ou None
        """
        search_key = search_name.lower().strip()
        
        # Busca exata
        if search_key in self.referencias:
            return search_name
        
        # Busca por correspondência parcial
        for param_key, param_data in self.referencias.items():
            if search_key in param_key or param_key in search_key:
                return param_data['parametro']
        
        return None

