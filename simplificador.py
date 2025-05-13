import pandas as pd
import openpyxl
from openpyxl.utils import get_column_letter

def processar_excel(caminho_entrada, caminho_saida):
    # Lê a planilha principal, pulando as 5 primeiras linhas
    df = pd.read_excel(caminho_entrada, sheet_name=0, skiprows=4)

    # A primeira linha lida (linha 6 da planilha original) vira o cabeçalho
    df.columns = df.iloc[0]
    df = df[1:]  # Remove a linha do cabeçalho agora redundante

    # Corrige colunas duplicadas e remove colunas sem nome
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.loc[:, df.columns.notna()]

    print("🔍 Colunas detectadas:", list(df.columns))

    colunas_desejadas = [
        "Unidades", "# de anúncio",
        "Título do anúncio", "Variação", "Comprador"
    ]

    colunas_existentes = [col for col in colunas_desejadas if col in df.columns]
    if not colunas_existentes:
        raise ValueError("❌ Nenhuma das colunas esperadas foi encontrada.")

    # Lê a planilha base para obter os nomes dos anúncios
    base_df = pd.read_excel("base.xlsx")

    # Garantir que a planilha base tenha as colunas esperadas
    if '# de anúncio' not in base_df.columns or 'Nome do anúncio' not in base_df.columns:
        raise ValueError("❌ A planilha base deve conter as colunas '# de anúncio' e 'Nome do anúncio'.")

    # Mapeia os valores de '# de anúncio' para os nomes na base
    base_dict = dict(zip(base_df['# de anúncio'], base_df['Nome do anúncio']))

    # Substitui o título do anúncio pelo nome correspondente da planilha base
    df['Título do anúncio'] = df['# de anúncio'].map(base_dict)

    # Cria o DataFrame simplificado com as colunas desejadas
    df_simplificado = df[colunas_existentes]

    # Salva o DataFrame simplificado em um arquivo Excel
    df_simplificado.to_excel(caminho_saida, index=False)

    # Agora ajusta a formatação do arquivo gerado
    wb = openpyxl.load_workbook(caminho_saida)
    ws = wb.active

    # Ajusta a altura das linhas
    for row in ws.iter_rows():
        ws.row_dimensions[row[0].row].height = 22.5

    # Ajusta a largura das colunas automaticamente
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Obtém a letra da coluna
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)  # Ajusta com um pouco de margem
        ws.column_dimensions[column].width = adjusted_width

    # Salva as modificações em um novo arquivo
    wb.save(caminho_saida)