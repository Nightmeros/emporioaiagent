import pandas as pd
import sqlite3
import os
import re

def setup_database():
    db_path = 'data/database/emporio.db'
    rawdata_dir = 'data/arquivos/'
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    csv_files = [f for f in os.listdir(rawdata_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("Nenhum arquivo para processar")
        return

    for file in csv_files:
        file_path = os.path.join(rawdata_dir, file)
       
        table_name = re.sub(r'^.*-\s*', '', file).replace('.csv', '').strip()
        
        try:
            df = pd.read_csv(file_path)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"✅ Tabela '{table_name}' populada com {len(df)} registros.")
        except Exception as e:
            print(f"❌ Erro ao processar {file}: {e}")
            
    conn.close()

if __name__ == "__main__":
    setup_database()