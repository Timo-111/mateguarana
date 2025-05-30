import pandas as pd
import os

pasta_base = "C:/Users/202402369989/Desktop/mateguarana/"

# dicionário com os nomes dos arquivos
arquivos = {
    "venda_por_dia_jan": "VENDA_POR_DIA_JANEIRO_2025.csv",
    "venda_por_produto_jan": "VENDA_POR_PRODUTO_JANEIRO_2025.csv",
    "venda_por_dia_fev": "vendas_de_fevereiro.csv",
    "venda_por_produto_fev": "vendas_de_fevereiro_por_produto.csv",
    "venda_por_pagamento_fev": "vendas_de_fevereiro_por_pagamento.csv",
    "faturamento_jan": "faturamento_JANEIRO_2025.csv",
    "movimentacao_produtos_fev": "movimentacao_de_produtos_fevereiro.csv",
    "planilha_custos": "PLANILHA_DE_CUSTO_2025_MATE_GUARANA.csv"
}

# carregar csv
def carregar_csv(caminho):
    try:
        return pd.read_csv(caminho, sep=";", encoding="latin1")
    except Exception as e:
        print(f"Erro ao carregar {caminho}: {e}")
        return pd.DataFrame()

# carregar dicionario
dfs = {}
for nome, arquivo in arquivos.items():
    caminho_completo = os.path.join(pasta_base, arquivo)
    if caminho_completo.lower().endswith(".csv"):
        df = carregar_csv(caminho_completo)
    else:
        try:
            df = pd.read_excel(caminho_completo)
        except Exception as e:
            print(f"Erro ao carregar {caminho_completo}: {e}")
            df = pd.DataFrame()

    if not df.empty:
        dfs[nome] = df
        print(f"✅ {nome.upper()} carregado com sucesso.")
    else:
        print(f"⚠️ {nome} está vazio ou falhou ao carregar.")

# verificar se foi carregado
df_jan_dia = dfs.get("venda_por_dia_jan")
df_fev_dia = dfs.get("venda_por_dia_fev")

# exportar limpos
if df_jan_dia is not None:
    caminho_jan_corrigido = os.path.join(pasta_base, "dados_janeiro.csv")
    df_jan_dia.to_csv(caminho_jan_corrigido, index=False, encoding="utf-8")
    print(f"📁 Arquivo de janeiro exportado: {caminho_jan_corrigido}")

if df_fev_dia is not None:
    caminho_fev_corrigido = os.path.join(pasta_base, "dados_fevereiro.csv")
    df_fev_dia.to_csv(caminho_fev_corrigido, index=False, encoding="utf-8")
    print(f"📁 Arquivo de fevereiro exportado: {caminho_fev_corrigido}")
