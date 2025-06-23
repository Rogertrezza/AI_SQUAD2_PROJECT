import streamlit as st
import pandas as pd
import os
import io
from typing import Dict, List, Any, Optional
import requests
import json
from datetime import datetime
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

class OpenRouterAgent:
    """Agente para análise de dados usando OpenRouter"""
    
    def __init__(self, api_key: str, model: str = "anthropic/claude-3.5-sonnet"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",  # Para Streamlit
            "X-Title": "Analisador de Notas Fiscais"
        }
        self.cabecalho_df = None
        self.itens_df = None
        self.combined_df = None
        
    def load_csv_files(self, uploaded_files: List) -> bool:
        """Carrega arquivos CSV enviados pelo usuário"""
        try:
            dataframes = {}
            
            for uploaded_file in uploaded_files:
                if uploaded_file.name.endswith('.csv'):
                    # Lê o arquivo CSV
                    df = pd.read_csv(uploaded_file, encoding='utf-8', sep=',')
                    
                    # Converte colunas de data se existirem
                    date_columns = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
                    for col in date_columns:
                        try:
                            df[col] = pd.to_datetime(df[col], errors='coerce')
                        except:
                            pass
                    
                    dataframes[uploaded_file.name] = df
                    
                    # Identifica o tipo de arquivo baseado no nome
                    file_name_lower = uploaded_file.name.lower()
                    if 'cabecalho' in file_name_lower or 'header' in file_name_lower or 'nf' in file_name_lower:
                        self.cabecalho_df = df
                        st.success(f"✅ Arquivo de cabeçalho carregado: {uploaded_file.name}")
                    elif 'itens' in file_name_lower or 'items' in file_name_lower or 'produtos' in file_name_lower:
                        self.itens_df = df
                        st.success(f"✅ Arquivo de itens carregado: {uploaded_file.name}")
                    else:
                        # Se não conseguir identificar, assume como primeiro arquivo = cabeçalho
                        if self.cabecalho_df is None:
                            self.cabecalho_df = df
                            st.info(f"📋 Assumindo como arquivo de cabeçalho: {uploaded_file.name}")
                        elif self.itens_df is None:
                            self.itens_df = df
                            st.info(f"📦 Assumindo como arquivo de itens: {uploaded_file.name}")
            
            # Se temos apenas um arquivo, vamos assumir que contém tudo
            if len(dataframes) == 1 and self.cabecalho_df is not None and self.itens_df is None:
                self.itens_df = self.cabecalho_df.copy()
                st.info("ℹ️ Usando o mesmo arquivo para cabeçalho e itens")
            
            # Cria DataFrame combinado se temos ambos
            if self.cabecalho_df is not None and self.itens_df is not None:
                # Tenta encontrar coluna de junção
                common_columns = set(self.cabecalho_df.columns) & set(self.itens_df.columns)
                if common_columns:
                    join_column = list(common_columns)[0]
                    st.info(f"🔗 Juntando tabelas pela coluna: {join_column}")
                    try:
                        self.combined_df = pd.merge(
                            self.cabecalho_df, 
                            self.itens_df, 
                            on=join_column, 
                            how='left'
                        )
                    except:
                        self.combined_df = self.cabecalho_df.copy()
                else:
                    self.combined_df = self.cabecalho_df.copy()
                
                return True
            else:
                st.error("❌ Não foi possível carregar os dados. Verifique os arquivos CSV.")
                return False
                
        except Exception as e:
            st.error(f"❌ Erro ao carregar arquivos CSV: {str(e)}")
            return False
    
    def create_sample_data(self) -> bool:
        """Cria dados de exemplo para demonstração"""
        try:
            # Dados de exemplo para cabeçalho das NFs
            np.random.seed(42)  # Para reprodutibilidade
            
            cabecalho_data = {
                'numero_nf': [f'NF{str(i).zfill(6)}' for i in range(1, 101)],
                'fornecedor': np.random.choice(['Empresa Alpha Ltda', 'Beta Soluções SA', 'Gamma Tech Corp', 'Delta Serviços', 'Epsilon Materiais'], 100),
                'data_emissao': pd.date_range('2024-01-01', periods=100, freq='D')[:100],
                'valor_total': np.random.uniform(1000, 50000, 100).round(2),
                'status': np.random.choice(['Pago', 'Pendente', 'Cancelado'], 100, p=[0.7, 0.2, 0.1]),
                'categoria': np.random.choice(['Material de Escritório', 'Equipamentos de TI', 'Serviços de Consultoria', 'Material de Limpeza', 'Manutenção'], 100)
            }
            
            # Dados de exemplo para itens das NFs
            itens_data = []
            for nf_num in range(1, 101):
                num_itens = np.random.randint(1, 6)  # 1 a 5 itens por NF
                for item_num in range(1, num_itens + 1):
                    produto = np.random.choice(['Notebook Dell', 'Impressora HP', 'Mouse Óptico', 'Teclado Mecânico', 'Monitor 24"', 'Papel A4', 'Caneta Esferográfica'])
                    quantidade = np.random.randint(1, 50)
                    valor_unitario = np.random.uniform(10, 2000).round(2)
                    
                    itens_data.append({
                        'numero_nf': f'NF{str(nf_num).zfill(6)}',
                        'item_numero': item_num,
                        'descricao': produto,
                        'quantidade': quantidade,
                        'valor_unitario': valor_unitario,
                        'valor_total_item': (quantidade * valor_unitario).round(2),
                        'unidade': np.random.choice(['UN', 'PC', 'KG', 'CX', 'LT'])
                    })
            
            self.cabecalho_df = pd.DataFrame(cabecalho_data)
            self.itens_df = pd.DataFrame(itens_data)
            
            # Cria DataFrame combinado
            self.combined_df = pd.merge(
                self.cabecalho_df, 
                self.itens_df, 
                on='numero_nf', 
                how='left'
            )
            
            st.success("✅ Dados de exemplo criados com sucesso!")
            return True
            
        except Exception as e:
            st.error(f"❌ Erro ao criar dados de exemplo: {str(e)}")
            return False
    
    def get_data_info(self) -> str:
        """Retorna informações sobre os dados carregados"""
        info = []
        
        if self.cabecalho_df is not None:
            info.append(f"DADOS DE CABEÇALHO ({self.cabecalho_df.shape[0]} registros):")
            info.append(f"Colunas: {', '.join(self.cabecalho_df.columns.tolist())}")
            info.append(f"Tipos de dados: {dict(self.cabecalho_df.dtypes)}")
            info.append("")
            
        if self.itens_df is not None:
            info.append(f"DADOS DE ITENS ({self.itens_df.shape[0]} registros):")
            info.append(f"Colunas: {', '.join(self.itens_df.columns.tolist())}")
            info.append(f"Tipos de dados: {dict(self.itens_df.dtypes)}")
            info.append("")
            
        if self.combined_df is not None:
            info.append(f"DADOS COMBINADOS ({self.combined_df.shape[0]} registros):")
            info.append(f"Colunas: {', '.join(self.combined_df.columns.tolist())}")
            
        return "\n".join(info)
    
    def get_data_sample(self) -> str:
        """Retorna uma amostra dos dados"""
        samples = []
        
        if self.cabecalho_df is not None:
            samples.append("AMOSTRA DO CABEÇALHO (primeiras 3 linhas):")
            samples.append(self.cabecalho_df.head(3).to_string())
            samples.append("")
            
        if self.itens_df is not None:
            samples.append("AMOSTRA DOS ITENS (primeiras 3 linhas):")
            samples.append(self.itens_df.head(3).to_string())
            samples.append("")
            
        return "\n".join(samples)
    
    def query_data(self, question: str) -> str:
        """Consulta os dados usando OpenRouter"""
        if self.cabecalho_df is None:
            return "❌ Nenhum dado carregado. Carregue os arquivos CSV primeiro."
        
        try:
            # Prepara o contexto com informações dos dados
            data_info = self.get_data_info()
            data_sample = self.get_data_sample()
            
            # Calcula estatísticas básicas
            stats = self.get_basic_stats()
            
            # Prompt para o modelo
            prompt = f"""
            Você é um analista de dados especializado em notas fiscais. Você tem acesso aos seguintes dados:

            {data_info}

            ESTATÍSTICAS BÁSICAS:
            {stats}

            AMOSTRA DOS DADOS:
            {data_sample}

            PERGUNTA DO USUÁRIO: {question}

            Por favor, analise os dados e responda à pergunta de forma clara e detalhada. 
            Se necessário, forneça cálculos, percentuais e insights relevantes.
            Se a pergunta envolver análises específicas que requerem cálculos, explique o raciocínio.
            
            Formato da resposta:
            - Responda de forma direta e clara
            - Use dados específicos quando possível
            - Forneça insights adicionais se relevante
            - Use formatação em markdown para melhor legibilidade
            """
            
            # Faz a requisição para o OpenRouter
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"❌ Erro na API do OpenRouter: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ Erro ao processar consulta: {str(e)}"
    
    def get_basic_stats(self) -> str:
        """Calcula estatísticas básicas dos dados"""
        stats = []
        
        try:
            if self.cabecalho_df is not None:
                stats.append("ESTATÍSTICAS DO CABEÇALHO:")
                stats.append(f"- Total de registros: {len(self.cabecalho_df)}")
                
                # Colunas numéricas
                numeric_cols = self.cabecalho_df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    stats.append(f"- {col}: média={self.cabecalho_df[col].mean():.2f}, min={self.cabecalho_df[col].min():.2f}, max={self.cabecalho_df[col].max():.2f}")
                
                # Colunas categóricas
                categorical_cols = self.cabecalho_df.select_dtypes(include=['object']).columns
                for col in categorical_cols[:3]:  # Limita a 3 colunas
                    unique_count = self.cabecalho_df[col].nunique()
                    stats.append(f"- {col}: {unique_count} valores únicos")
                
                stats.append("")
            
            if self.itens_df is not None:
                stats.append("ESTATÍSTICAS DOS ITENS:")
                stats.append(f"- Total de registros: {len(self.itens_df)}")
                
                # Colunas numéricas
                numeric_cols = self.itens_df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    stats.append(f"- {col}: média={self.itens_df[col].mean():.2f}, min={self.itens_df[col].min():.2f}, max={self.itens_df[col].max():.2f}")
                
                stats.append("")
                
        except Exception as e:
            stats.append(f"Erro ao calcular estatísticas: {str(e)}")
        
        return "\n".join(stats)
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Retorna um resumo dos dados carregados"""
        if self.cabecalho_df is None:
            return {}
        
        summary = {
            'total_registros_cabecalho': len(self.cabecalho_df),
            'total_registros_itens': len(self.itens_df) if self.itens_df is not None else 0,
            'colunas_cabecalho': list(self.cabecalho_df.columns),
            'colunas_itens': list(self.itens_df.columns) if self.itens_df is not None else []
        }
        
        # Adiciona estatísticas específicas se as colunas existirem
        try:
            if 'valor_total' in self.cabecalho_df.columns:
                summary['valor_total_geral'] = self.cabecalho_df['valor_total'].sum()
                summary['valor_medio'] = self.cabecalho_df['valor_total'].mean()
                
            if 'fornecedor' in self.cabecalho_df.columns:
                summary['fornecedores_unicos'] = self.cabecalho_df['fornecedor'].nunique()
                
            if 'data_emissao' in self.cabecalho_df.columns:
                summary['periodo'] = {
                    'inicio': self.cabecalho_df['data_emissao'].min(),
                    'fim': self.cabecalho_df['data_emissao'].max()
                }
        except:
            pass
            
        return summary

def main():
    st.set_page_config(
        page_title="Analisador de Notas Fiscais - OpenRouter",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🧠 Analisador Inteligente de Notas Fiscais")
    st.markdown("**Análise automatizada usando OpenRouter e IA**")
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Campo para API Key do OpenRouter
        openrouter_api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            help="Digite sua chave da API do OpenRouter"
        )
        
        # Seleção do modelo
        model_options = [
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-haiku",
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "google/gemini-pro",
            "meta-llama/llama-3.1-8b-instruct"
        ]
        
        selected_model = st.selectbox(
            "Modelo de IA",
            model_options,
            index=0,
            help="Selecione o modelo de IA para análise"
        )
        
        st.markdown("---")
        
        # Upload de arquivos CSV
        uploaded_files = st.file_uploader(
            "📁 Upload dos arquivos CSV",
            type=['csv'],
            accept_multiple_files=True,
            help="Faça upload de um ou mais arquivos CSV com dados de notas fiscais"
        )
        
        # Opção para usar dados de exemplo
        use_sample_data = st.checkbox(
            "🎲 Usar dados de exemplo",
            value=False,
            help="Marque para usar dados sintéticos para demonstração"
        )
        
        st.markdown("---")
        st.info("💡 Você pode obter sua API key do OpenRouter em: https://openrouter.ai/")
    
    # Verifica se a API key foi fornecida
    if not openrouter_api_key:
        st.warning("⚠️ Por favor, forneça sua OpenRouter API Key na barra lateral para continuar.")
        return
    
    # Inicializa o agente
    if 'agent' not in st.session_state or st.session_state.get('current_api_key') != openrouter_api_key:
        st.session_state.agent = OpenRouterAgent(openrouter_api_key, selected_model)
        st.session_state.current_api_key = openrouter_api_key
        st.session_state.data_loaded = False
    
    # Carregamento de dados
    if not st.session_state.data_loaded:
        if use_sample_data:
            with st.spinner("🔄 Criando dados de exemplo..."):
                success = st.session_state.agent.create_sample_data()
                if success:
                    st.session_state.data_loaded = True
        elif uploaded_files:
            with st.spinner("🔄 Carregando arquivos CSV..."):
                success = st.session_state.agent.load_csv_files(uploaded_files)
                if success:
                    st.session_state.data_loaded = True
        else:
            st.info("📁 Faça upload dos arquivos CSV ou marque a opção para usar dados de exemplo.")
            return
    
    # Mostra resumo dos dados
    if st.session_state.data_loaded:
        summary = st.session_state.agent.get_data_summary()
        
        st.subheader("📈 Resumo dos Dados")
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📄 Registros Cabeçalho", summary.get('total_registros_cabecalho', 0))
        with col2:
            st.metric("📦 Registros Itens", summary.get('total_registros_itens', 0))
        with col3:
            st.metric("🏢 Fornecedores", summary.get('fornecedores_unicos', 'N/A'))
        with col4:
            valor_total = summary.get('valor_total_geral', 0)
            if valor_total > 0:
                st.metric("💰 Valor Total", f"R$ {valor_total:,.2f}")
            else:
                st.metric("💰 Valor Total", "N/A")
        
        # Informações das colunas
        with st.expander("📋 Informações das Colunas"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Colunas do Cabeçalho:**")
                for col in summary.get('colunas_cabecalho', []):
                    st.write(f"• {col}")
            with col2:
                if summary.get('colunas_itens'):
                    st.write("**Colunas dos Itens:**")
                    for col in summary.get('colunas_itens', []):
                        st.write(f"• {col}")
    
    # Interface principal de consulta
    st.header("💬 Faça sua Análise")
    
    # Exemplos de perguntas
    st.subheader("🎯 Exemplos de perguntas:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Análises Financeiras:**
        - Qual fornecedor teve maior faturamento?
        - Qual é o valor médio das notas fiscais?
        - Quais são os 5 itens mais caros?
        - Como está distribuído o faturamento por mês?
        """)
    
    with col2:
        st.markdown("""
        **Análises Operacionais:**
        - Quantas notas fiscais por fornecedor?
        - Qual produto teve maior volume?
        - Quantas notas estão pendentes?
        - Qual categoria representa maior gasto?
        """)
    
    # Campo de entrada para pergunta
    question = st.text_area(
        "✍️ Digite sua pergunta:",
        height=100,
        placeholder="Ex: Qual é o fornecedor com maior faturamento e qual o valor total?"
    )
    
    # Botão para executar consulta
    if st.button("🚀 Analisar", type="primary"):
        if not question.strip():
            st.warning("⚠️ Por favor, digite uma pergunta.")
        elif not st.session_state.data_loaded:
            st.error("❌ Carregue os dados primeiro.")
        else:
            with st.spinner("🤖 Analisando dados..."):
                response = st.session_state.agent.query_data(question)
            
            st.subheader("📋 Resposta da Análise:")
            st.markdown(response)
    
    # Histórico (opcional)
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    # Seção de informações técnicas
    with st.expander("🔧 Informações Técnicas"):
        st.markdown(f"""
        ### Configuração Atual
        - **Modelo**: {selected_model}
        - **API**: OpenRouter
        - **Dados Carregados**: {'✅ Sim' if st.session_state.data_loaded else '❌ Não'}
        
        ### Como Funciona
        1. **Upload**: Arquivos CSV são carregados e processados
        2. **Análise**: O modelo de IA analisa a estrutura dos dados
        3. **Consulta**: Perguntas em linguagem natural são processadas
        4. **Resposta**: O modelo retorna análises detalhadas e insights
        
        ### Formatos de Arquivo Suportados
        - Arquivos CSV com encoding UTF-8
        - Separador de campos: vírgula (,)
        - Suporte a múltiplos arquivos
        - Detecção automática de colunas de data
        """)

if __name__ == "__main__":
    main()