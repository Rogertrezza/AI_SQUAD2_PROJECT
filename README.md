<<<<<<< HEAD
🧠 Agente Inteligente para Análise de Notas Fiscais TCU
📋 Descrição do Projeto
Este projeto implementa um agente inteligente capaz de responder perguntas em linguagem natural sobre dados de notas fiscais do Tribunal de Contas da União (TCU). O sistema utiliza o framework LangChain para criar um agente que combina processamento de linguagem natural com análise de dados usando Pandas.

🛠️ Framework Escolhido
LangChain foi escolhido como framework principal pelos seguintes motivos:

Integração Nativa: Excelente integração com modelos de linguagem da OpenAI
Agentes Especializados: Possui agentes pré-construídos para análise de DataFrames do Pandas
Flexibilidade: Permite customização e extensão facilmente
Comunidade Ativa: Grande comunidade e documentação abundante
Callbacks: Sistema de callbacks para monitoramento do processo de análise
🏗️ Estrutura da Solução
Arquitetura do Sistema
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   LangChain      │    │   OpenAI GPT    │
│   Interface     │───▶│   Agent          │───▶│   Language      │
│                 │    │                  │    │   Model         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         │                        ▼                       │
         │              ┌──────────────────┐             │
         │              │   Pandas         │             │
         └──────────────│   DataFrames     │◀────────────┘
                        │                  │
                        └──────────────────┘
Componentes Principais
NFAnalyzerAgent: Classe principal que encapsula toda a lógica do agente
StreamlitCallbackHandler: Handler personalizado para mostrar progresso
Interface Streamlit: Interface web interativa para o usuário
Processamento de Dados: Extração de ZIP e carregamento de CSVs
Fluxo de Funcionamento
Carregamento de Dados:
Extração do arquivo ZIP fornecido
Identificação automática dos arquivos de cabeçalho e itens
Conversão de tipos de dados (datas, números)
Criação de DataFrame combinado para análises complexas
Criação do Agente:
Inicialização do modelo OpenAI
Criação do agente pandas com acesso aos DataFrames
Configuração de callbacks para monitoramento
Processamento de Consultas:
Recebimento da pergunta em linguagem natural
Adição de contexto sobre os dados disponíveis
Geração de código Python/Pandas pelo agente
Execução do código e formatação da resposta
🚀 Como Executar
Pré-requisitos
Python 3.8 ou superior
Chave da API OpenAI
Arquivo ZIP com os dados das notas fiscais
Instalação
Clone o repositório:
bash
git clone https://github.com/seu-usuario/nf-analyzer-agent.git
cd nf-analyzer-agent
Instale as dependências:
bash
pip install -r requirements.txt
Execute a aplicação:
bash
streamlit run app.py
Acesse no navegador: http://localhost:8501
Configuração
Insira sua chave da API OpenAI na barra lateral
Faça upload do arquivo 202401_NFs.zip ou use os dados de exemplo
Aguarde o carregamento dos dados
Comece a fazer perguntas!
❓ Exemplos de Perguntas e Respostas
1. Qual é o fornecedor que teve maior montante recebido?
Resposta do Agente: "Com base na análise dos dados, o Fornecedor B teve o maior montante recebido, totalizando R$ 234.567,89 distribuídos em 23 notas fiscais durante o período analisado."

2. Qual item teve maior volume entregue em quantidade?
Resposta do Agente: "O item com maior volume entregue foi Produto A, com um total de 1.847 unidades distribuídas em 45 notas fiscais diferentes, representando aproximadamente 32% do volume total de produtos."

3. Quantas notas fiscais foram emitidas por cada fornecedor?
Resposta do Agente: "A distribuição de notas fiscais por fornecedor é:

Fornecedor A: 18 notas fiscais (18%)
Fornecedor B: 23 notas fiscais (23%)
Fornecedor C: 21 notas fiscais (21%)
Fornecedor D: 19 notas fiscais (19%)
Fornecedor E: 19 notas fiscais (19%)"
4. Qual é o valor médio das notas fiscais e qual fornecedor tem a maior média?
Resposta do Agente: "O valor médio geral das notas fiscais é R$ 15.234,56. O fornecedor com maior valor médio por nota fiscal é o Fornecedor C, com média de R$ 18.789,23 por nota, seguido pelo Fornecedor B com R$ 17.456,78."

🔧 Funcionalidades Técnicas
Características do Agente
Processamento Inteligente: Converte perguntas em linguagem natural para código Pandas
Análise Multitabela: Trabalha simultaneamente com dados de cabeçalho e itens
Validação de Dados: Verifica integridade e converte tipos automaticamente
Feedback em Tempo Real: Mostra o progresso da análise via callbacks
Tratamento de Erros: Captura e trata erros de forma elegante
Segurança
API keys não são armazenadas permanentemente
Execução de código em ambiente controlado
Validação de entrada para prevenir injeção de código
Dados processados apenas na sessão local
Performance
Carregamento otimizado de arquivos CSV
Cache de DataFrames na sessão
Processamento eficiente com Pandas
Interface responsiva com Streamlit
📊 Métricas e Visualizações
O sistema fornece automaticamente:

Resumo Estatístico: Total de NFs, itens, fornecedores e valores
Período de Análise: Datas de início e fim dos dados
Distribuições: Análises de distribuição por diferentes dimensões
Rankings: Top fornecedores, produtos, valores, etc.
🔄 Extensões Futuras
Integração com outros modelos de IA (Claude, Llama, etc.)
Visualizações gráficas automáticas das respostas
Exportação de relatórios em PDF/Excel
API REST para integração com outros sistemas
Suporte a múltiplos formatos de arquivo
Cache persistente para melhor performance
📝 Considerações Importantes
Dados Sensíveis: O sistema pode processar dados reais do governo, portanto deve ser usado com responsabilidade
Custo da API: Uso da OpenAI API gera custos - monitore o uso
Precisão: Sempre valide respostas críticas manualmente
Limitações: O agente pode não conseguir responder todas as perguntas complexas
🤝 Contribuição
Para contribuir com o projeto:

Fork o repositório
Crie uma branch para sua feature
Implemente as mudanças
Adicione testes se necessário
Abra um Pull Request
📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

👥 Equipe
Desenvolvedor Principal: [Seu Nome]
Framework: LangChain + Streamlit + Pandas
Modelo de IA: OpenAI GPT-3.5/4
Período: Janeiro 2024
=======
# AI_SQUAD2_PROJECT
Grupo para projeto I2A2
>>>>>>> a91062af0378de1c4406ddf193b83e0b41b1f676
