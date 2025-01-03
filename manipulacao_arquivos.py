import pandas as pd
import pdfplumber
import os

def extract_and_save_tables(file_path, output_dir):
    all_tables = []  # Lista para armazenar todas as tabelas concatenadas
    new_filename = None  # Nome do arquivo baseado na primeira página

    # Abrir o PDF com pdfplumber
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extrair tabelas da página
            tables = page.extract_tables()

            for table in tables:
                # Obter informações para o nome do arquivo com base na primeira página
                if page_num == 1 and not new_filename:
                    nome_arquivo = table[0][0].strip()
                    inf_empresa = table[1][2].strip()
                    competencia = table[2][2].replace('/', '-').strip()
                    new_filename = f"{nome_arquivo} - {inf_empresa} - {competencia}.pdf"

                # Criar o DataFrame para a tabela e adicioná-lo à lista
                df = pd.DataFrame(table[4:-1], columns=table[3])
                all_tables.append(df)

    # Concatenar todas as tabelas em um único DataFrame
    final_df = pd.concat(all_tables, ignore_index=True)

    # Salvar o DataFrame concatenado em um arquivo CSV (opcional)
    csv_filename = os.path.splitext(file_path)[0] + "_concatenated.csv"
    final_df.to_csv(csv_filename, index=False)
    print(f"Tabelas concatenadas salvas em: {csv_filename}")

    # Renomear o arquivo de entrada com base na primeira página
    if new_filename:
        new_filepath = os.path.join(output_dir, new_filename)
        os.rename(file_path, new_filepath)
        print(f"Arquivo PDF renomeado para: {new_filepath}")

'''# Exemplo de uso

# Caminho para a pasta
directory = os.path.join(os.getcwd(), "uploads", "pdf")

# Listar todos os arquivos na pasta
files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Verificar se há arquivos na pasta

file_path = max(files, key=os.path.getmtime)

# Diretório para salvar os arquivos
output_dir = os.path.join(os.getcwd(), "uploads", "pdf") 
extract_and_save_tables(file_path, output_dir)'''