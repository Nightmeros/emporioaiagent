import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_sql_tools():
    banco = "sqlite:///data/database/emporio.db"
    db = SQLDatabase.from_uri(banco)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return toolkit.get_tools()

if __name__ == "__main__":
    ferramentas = get_sql_tools()
    print(f"🛠️ Ferramentas disponíveis para o Agente:")
    for tool in ferramentas:
        print(f" - {tool.name}: {tool.description[:60]}...")