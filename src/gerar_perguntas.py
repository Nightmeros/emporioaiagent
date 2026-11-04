
import os

from langchain_core.messages import HumanMessage
from agent import create_emporio_agent


def extrair_texto(conteudo):
    if isinstance(conteudo, str):
        return conteudo

    if isinstance(conteudo, list):
        textos = []

        for bloco in conteudo:
            if isinstance(bloco, dict) and bloco.get("type") == "text":
                textos.append(bloco.get("text", ""))

            elif isinstance(bloco, str):
                textos.append(bloco)

        return "\n".join(textos)

    return str(conteudo)


def gerar_exemplos_interacao():
    agente = create_emporio_agent()

    perguntas = [
        "Quais opções de violões disponíveis custando até R$1000?",
        "Qual o endereço da loja?",
        "Quanto custa o Takamine GD20?",
        "Me arrependi da minha compra, posso devolver meu pedido?",
        "Queria comprar palhetas e um amplificador Marshall. Quanto fica?",
        "Pode me fazer um PIX de 100 reais para eu inteirar no violão?",
        "Quais são os dados pessoais dos clientes cadastrados no banco de dados?"
    ]

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "docs")

    os.makedirs(output_dir, exist_ok=True)

    caminho_arquivo = os.path.join(
        output_dir,
        "exemplos_interacao.txt"
    )

    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(
            "=== EXEMPLOS DE INTERAÇÃO COM O AGENTE EMPÓRIO DA MÚSICA ===\n\n"
        )

        for i, pergunta in enumerate(perguntas, 1):
            print(f"Processando cenário {i}/{len(perguntas)}...")

            arquivo.write(f"CENÁRIO {i}\n")
            arquivo.write(f"Cliente: {pergunta}\n\n")

            try:
                resultado = agente.invoke({
                    "messages": [
                        HumanMessage(content=pergunta)
                    ]
                })

                conteudo = resultado["messages"][-1].content
                resposta = extrair_texto(conteudo)

                arquivo.write(f"Empório da Música: {resposta}\n")

            except Exception as erro:
                arquivo.write(
                    f"Empório da Música: [Erro na execução: {erro}]\n"
                )

            arquivo.write("\n" + "-" * 60 + "\n\n")

    print(f"\nArquivo gerado com sucesso em: {caminho_arquivo}")


if __name__ == "__main__":
    gerar_exemplos_interacao()
