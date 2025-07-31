"""
Módulo de análise de exames para o Sistema Nutri Análises
"""

import pandas as pd
import streamlit as st

class ExamAnalyzer:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.referencias = data_manager.get_referencias()
    
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
                        'icon': '⚠️'
                    }
            
            # Fora da referência
            return {
                'status': 'Fora',
                'color': '#F8D7DA',
                'icon': '❌'
            }
            
        except (ValueError, TypeError):
            return {
                'status': 'Valor inválido',
                'color': '#6C757D',
                'icon': '❓'
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
    
    def validate_csv_data(self, df):
        """
        Valida dados de CSV importado
        
        Args:
            df (DataFrame): Dados do CSV
        
        Returns:
            dict: Resultado da validação
        """
        required_columns = ['nome_exame', 'valor', 'unidade', 'data_exame']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return {
                'valid': False,
                'error': f"Colunas obrigatórias ausentes: {', '.join(missing_columns)}"
            }
        
        # Validar tipos de dados
        errors = []
        
        for idx, row in df.iterrows():
            # Validar valor numérico
            try:
                float(row['valor'])
            except (ValueError, TypeError):
                errors.append(f"Linha {idx + 1}: Valor '{row['valor']}' não é numérico")
            
            # Validar data
            try:
                pd.to_datetime(row['data_exame'])
            except:
                errors.append(f"Linha {idx + 1}: Data '{row['data_exame']}' inválida")
        
        if errors:
            return {
                'valid': False,
                'error': '; '.join(errors[:5])  # Mostrar apenas os primeiros 5 erros
            }
        
        return {'valid': True}
    
    def process_csv_import(self, df, id_paciente, sexo_paciente):
        """
        Processa importação de CSV
        
        Args:
            df (DataFrame): Dados do CSV
            id_paciente (int): ID do paciente
            sexo_paciente (str): Sexo do paciente
        
        Returns:
            dict: Resultado do processamento
        """
        # Separar parâmetros conhecidos e desconhecidos
        conhecidos = []
        desconhecidos = []
        
        for _, row in df.iterrows():
            param_key = row['nome_exame'].lower().strip()
            
            if param_key in self.referencias:
                # Classificar exame
                classification = self.classify_exam(
                    row['nome_exame'], 
                    row['valor'], 
                    sexo_paciente
                )
                
                exame_data = {
                    'parametro': row['nome_exame'],
                    'valor': float(row['valor']),
                    'unidade': row['unidade'],
                    'data_coleta': pd.to_datetime(row['data_exame']).strftime('%Y-%m-%d'),
                    'status': classification['status']
                }
                conhecidos.append(exame_data)
            else:
                desconhecidos.append({
                    'nome_exame': row['nome_exame'],
                    'valor': row['valor'],
                    'unidade': row['unidade'],
                    'data_exame': row['data_exame']
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

