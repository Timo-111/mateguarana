import pandas as pd
import os
pasta_base = "C:/Users/202402369989/Desktop/mateguarana/"

arquivos = {
    "venda_por_dia_jan": "VENDA_POR_DIA_JANEIRO_2025.csv",
    "venda_por_produto_jan": "VENDA_POR_PRODUTO_JANEIRO_2025.csv",
    "venda_por_dia_fev": "vendas_de_fevereiro.csv",
    "venda_por_produto_fev": "vendas_de_fevereiro_por_produto.csv",
    "venda_por_pagamento_fev": "vendas_de_fevereiro_por_pagamento.csv",
    "faturamento_jan": "faturamento_JANEIRO_2025.csv",
    "movimentacao_produtos_fev": "movimentacao_de_produtos_fevereiro.csv",
    "planilha_custos": "PLANILHA_DE_CUSTO_2025_MATE_GUARANA.xlsx"
}

def carregar_csv(caminho):
    try:
        return pd.read_csv(caminho, sep=";", encoding="latin1")
    except Exception as e:
        print(f"Erro ao carregar {caminho}: {e}")
        return pd.DataFrame()

dfs = {}
for nome, arquivo in arquivos.items():
    caminho_completo = os.path.join(pasta_base, arquivo)
    if not os.path.exists(caminho_completo):
        print(f"❌ Arquivo não encontrado: {caminho_completo}")
        continue

    if caminho_completo.endswith(".csv"):
        df = carregar_csv(caminho_completo)
    else:
        try:
            df = pd.read_excel(caminho_completo)
        except Exception as e:
            print(f"Erro ao carregar {caminho_completo}: {e}")
            df = pd.DataFrame()

    if not df.empty:
        dfs[nome] = df
        print(f"\n✅ {nome.upper()} carregado com sucesso:")
        print(df.head())
    else:
        print(f"⚠️ {nome} está vazio ou falhou ao carregar.")

tabelas_combinadas = []
for chave in ["venda_por_dia_jan", "venda_por_dia_fev", "venda_por_produto_jan", "venda_por_produto_fev"]:
    if chave in dfs:
        tabelas_combinadas.append(dfs[chave])

if tabelas_combinadas:
    df_final = pd.concat(tabelas_combinadas, ignore_index=True)
    output_path = os.path.join(pasta_base, "dados_tratados.csv")
    df_final.to_csv(output_path, index=False)
    print(f"\n✅ Arquivo final salvo em: {output_path}")
else:
    print("⚠️ Nenhuma tabela foi combinada.")
