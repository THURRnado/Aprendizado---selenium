import pandas as pd
import pdfplumber
import os
import zipfile

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


def process_nf(file_path, output_dir):
    # Verifica se o caminho fornecido é um arquivo ZIP
    if not zipfile.is_zipfile(file_path):
        raise ValueError(f"O arquivo {file_path} não é um arquivo ZIP válido.")
    
    # Cria o diretório de saída, se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Abre o arquivo ZIP
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # Lista os arquivos no ZIP
        txt_files = [file for file in zip_ref.namelist() if file.endswith('.txt')]
        
        if not txt_files:
            raise ValueError("Nenhum arquivo .txt encontrado no arquivo ZIP.")
        
        for txt_file in txt_files:
            # Lê o conteúdo do arquivo .txt
            with zip_ref.open(txt_file) as f:
                # Lê o conteúdo do arquivo diretamente em um DataFrame
                df = pd.read_csv(f, sep='|', encoding='latin1')
            
            # Obtém os nomes das colunas
            colunas = df.columns.tolist()

            # Caminho para o arquivo de saída (salva as colunas em um arquivo .txt)
            output_txt_path = os.path.join(output_dir, "colunas_output.txt")
            
            # Grava os nomes das colunas em um arquivo .txt
            with open(output_txt_path, 'w', encoding='utf-8') as output_file:
                for coluna in colunas:
                    output_file.write(f"{coluna}\n")

            # Exibe uma mensagem de confirmação
            print(f"Colunas foram salvas em: {output_txt_path}")
            print(f"Colunas do arquivo {txt_file}: {colunas}")


# Caminho para a pasta
directory = os.path.join(os.getcwd(), "uploads", "pdf")

# Listar todos os arquivos na pasta
files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Verificar se há arquivos na pasta
file_path = max(files, key=os.path.getmtime)

# Diretório para salvar os arquivos
output_dir = os.path.join(os.getcwd(), "uploads", "pdf") 
process_nf(file_path, output_dir)