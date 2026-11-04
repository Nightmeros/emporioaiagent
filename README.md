1. Instruções para rodar o projeto

Pré-requisitos:
    Python 3.10 ou superior.
    Chave de API válida do Google AI Studio (Escolha tanto por ser uma api com diversos modelos para uso quanto por ser gratuita e de facil implementação)


Clonar o repositório
Criar um arquivo .env com as seguintes variáveis:

GOOGLE_API_KEY=CHAVE_AQUI
GEMINI_MODEL=gemini-3.1-flash-lite 

(Pode ser necessário utilizar outros modelos caso esteja fora do ar, sugestões: gemini-3.8-flash, gemini-3.6-flash, gemini-3.7-flash. Basta trocar na variável)

Execução:
O projeto possui um script de inicialização automatizado que configura o ambiente virtual, inicializa as bases de dados e inicia a interface web. No terminal, execute:

chmod +x start.sh
./start.sh

2. Justificativa das decisões técnicas

    LLM (Provedor do Modelo): Foram escolhidas as Apis do google devido à alta velocidade de inferência e excelente capacidade nativa de Tool Calling. Para os embeddings, optou-se pelo gemini-embedding-001 pela integração nativa com o ecossistema do google.

    Framework (Orquestração): Utilizou-se o ecossistema LangChain em conjunto com as chamadas modernas do LangGraph (create_agent). Esta escolha garante um código modular e capaz para diversos fluxos de raciocínio complexos.

    Arquitetura de Retrieval (RAG): A base vetorial foi implementada com ChromaDB pela sua facilidade de execução local sem necessidade de infraestrutura externa. O texto do PDF foi processado com o RecursiveCharacterTextSplitter (chunk de 1000, overlap de 200) para garantir que o contexto não perca o sentido entre os blocos.

    Estratégia de Prompt: O System Prompt foi desenhado com foco em Guardrails. Foram implementadas regras explícitas de escopo para garantir que o agente não inventa preços (obrigando o uso das ferramentas SQL) e recusa a venda de produtos não suportados, como acessórios.

3. Limitações conhecidas e melhorias

Limitações Atuais:

    Persistência de Memória: O historico da conversa é gerido pelo estado de sessão do Streamlit. Se a página for atualizada, o contexto da conversa some.
    Bases de Dados Local: O uso de SQLite e ChromaDB em ficheiros locais é excelente para projetos rápidos, mas apresenta gargalos em cenários de múltiplos utilizadores ao mesmo tempo.

O que poderia ser melhorado:

    Dockerização: Criar um Dockerfile e um docker-composepara isolar a aplicação e as dependencias, garantindo que corre da mesma forma em qualquer máquina sem scripts manuais.
    Infraestrutura Escalável: Migrar o SQLite para PostgreSQL e o armazenamento vetorial local para uma solução cloud-native.
    Testes Automatizados: Implementar pytest para testar unitariamente o retorno das tools (SQL e RAG) antes de passarem pelo LLM.
    Memória Persistente: Integrar o Redis ou o próprio SQLite para guardar o histórico de sessões.

4. Uso de assistentes de código

Ferramenta utilizada: Gemini
Workflow e Aplicação:
O assistente foi utilizado num formato de Pair Programming (programação em par) focado na resolução de problemas e otimização. As principais aplicações foram:

    Debugging de Dependências: Resolução rápida de conflitos de versões e métodos depreciados na transição das ferramentas clássicas do LangChain para a arquitetura moderna baseada em LangGraph e langchain_core.tools.

    Brainstorming: Validação de ideias para as regras de negócio aplicadas no System Prompt para garantir cenários de falha controlada (ex: cliente tentar comprar palhetas).
    As decisões arquiteturais finais e o fluxo lógico permaneceram sob meu controle, usando a IA como um acelerador de produtividade, não um gerador de codigo copia e cola