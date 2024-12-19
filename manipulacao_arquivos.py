import pandas as pd
import pdfplumber
import os

def extract_and_save_tables(file_path, output_dir):
    # Abrir o PDF com pdfplumber
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extrair tabelas da página
            tables = page.extract_tables()
            for table in tables:
                # Obter informações para o nome do arquivo
                nome_arquivo = table[0][0].strip()
                inf_empresa = table[1][2].strip()
                competencia = table[2][2].replace('/', '-').strip()

                # Criar o DataFrame
                df = pd.DataFrame(table[4:-1], columns=table[3])

                # Criar o nome do arquivo dinamicamente
                new_filename = f"{nome_arquivo} - {inf_empresa} - {competencia}.pdf"
                new_filepath = os.path.join(output_dir, new_filename)

                # Fecha o arquivo PDF antes de renomear
                pdf.close()

                # Renomear o arquivo de entrada
                os.rename(file_path, new_filepath)
                print(df)
                print("\n")
                print(f"Arquivo salvo: {new_filepath}")

# Exemplo de uso
file_path = os.path.join(os.getcwd(), "uploads", "pdf", "Saida.pdf")
output_dir = os.path.join(os.getcwd(), "uploads", "pdf")  # Diretório para salvar os arquivos
extract_and_save_tables(file_path, output_dir)