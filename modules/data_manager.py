"""
Módulo de gerenciamento de dados para o Sistema Nutri Análises
"""

import pandas as pd
import os
from datetime import datetime
import streamlit as st

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.pacientes_file = os.path.join(self.data_dir, "pacientes.xlsx")
        self.exames_file = os.path.join(self.data_dir, "exames.xlsx")
        self.referencias_file = os.path.join(self.data_dir, "valores_referencia.xlsx")
        
        # Criar arquivos se não existirem
        self._initialize_files()
        
        # Carregar dados em cache
        self._load_referencias()
    
    def _initialize_files(self):
        """Inicializa arquivos de dados se não existirem"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Inicializar pacientes.xlsx
        if not os.path.exists(self.pacientes_file):
            df_pacientes = pd.DataFrame(columns=[
                'id', 'nome', 'sexo', 'idade', 'peso_kg', 'altura_m', 
                'data_cadastro', 'notas'
            ])
            df_pacientes.to_excel(self.pacientes_file, index=False)
        
        # Inicializar exames.xlsx
        if not os.path.exists(self.exames_file):
            df_exames = pd.DataFrame(columns=[
                'id_exame', 'id_paciente', 'parametro', 'valor', 
                'unidade', 'data_coleta', 'status'
            ])
            df_exames.to_excel(self.exames_file, index=False)
    
    @st.cache_data
    def _load_referencias(_self):
        """Carrega valores de referência em cache"""
        try:
            df = pd.read_excel(_self.referencias_file)
            # Criar índice por parâmetro (case-insensitive)
            referencias_dict = {}
            for _, row in df.iterrows():
                param = str(row['parametro']).lower().strip()
                referencias_dict[param] = row.to_dict()
            return referencias_dict
        except Exception as e:
            st.error(f"Erro ao carregar valores de referência: {e}")
            return {}
    
    def get_referencias(self):
        """Retorna valores de referência"""
        return self._load_referencias()
    
    def load_pacientes(self):
        """Carrega lista de pacientes"""
        try:
            return pd.read_excel(self.pacientes_file)
        except Exception as e:
            st.error(f"Erro ao carregar pacientes: {e}")
            return pd.DataFrame()
    
    def save_paciente(self, paciente_data):
        """Salva dados de um paciente"""
        try:
            df = self.load_pacientes()
            
            if 'id' in paciente_data and paciente_data['id'] in df['id'].values:
                # Atualizar paciente existente
                df.loc[df['id'] == paciente_data['id']] = paciente_data
            else:
                # Novo paciente
                if df.empty:
                    paciente_data['id'] = 1
                else:
                    paciente_data['id'] = df['id'].max() + 1
                paciente_data['data_cadastro'] = datetime.now().strftime('%Y-%m-%d')
                df = pd.concat([df, pd.DataFrame([paciente_data])], ignore_index=True)
            
            df.to_excel(self.pacientes_file, index=False)
            return True
        except Exception as e:
            st.error(f"Erro ao salvar paciente: {e}")
            return False
    
    def load_exames(self, id_paciente=None):
        """Carrega exames de um paciente específico ou todos"""
        try:
            df = pd.read_excel(self.exames_file)
            if id_paciente is not None:
                df = df[df['id_paciente'] == id_paciente]
            return df
        except Exception as e:
            st.error(f"Erro ao carregar exames: {e}")
            return pd.DataFrame()
    
    def save_exames(self, exames_data, id_paciente):
        """Salva lista de exames para um paciente"""
        try:
            df_existente = pd.read_excel(self.exames_file)
            
            # Preparar novos exames
            novos_exames = []
            for exame in exames_data:
                exame['id_paciente'] = id_paciente
                if df_existente.empty:
                    exame['id_exame'] = 1
                else:
                    exame['id_exame'] = df_existente['id_exame'].max() + 1 if not df_existente.empty else 1
                novos_exames.append(exame)
            
            # Adicionar novos exames
            df_novos = pd.DataFrame(novos_exames)
            df_final = pd.concat([df_existente, df_novos], ignore_index=True)
            
            df_final.to_excel(self.exames_file, index=False)
            return True
        except Exception as e:
            st.error(f"Erro ao salvar exames: {e}")
            return False
    
    def backup_referencias(self):
        """Cria backup dos valores de referência"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
            backup_file = os.path.join(self.data_dir, f"valores_referencia_{timestamp}.xlsx")
            
            # Copiar arquivo atual
            df = pd.read_excel(self.referencias_file)
            df.to_excel(backup_file, index=False)
            
            return backup_file
        except Exception as e:
            st.error(f"Erro ao criar backup: {e}")
            return None
    
    def save_referencias(self, df_referencias):
        """Salva valores de referência atualizados"""
        try:
            # Criar backup antes de salvar
            self.backup_referencias()
            
            # Salvar novos valores
            df_referencias.to_excel(self.referencias_file, index=False)
            
            # Limpar cache
            st.cache_data.clear()
            
            return True
        except Exception as e:
            st.error(f"Erro ao salvar referências: {e}")
            return False

