import pandas as pd
import os

# caminho base
pasta_base = "C:/Users/202402369989/Desktop/mateguarana"

# arquivos
arquivos = {
    "vendas_jan": os.path.join(pasta_base, "VENDA_POR_DIA_JANEIRO_2025.csv"),
    "vendas_fev": os.path.join(pasta_base, "vendas_de_fevereiro.csv"),
    "vendas_prod_jan": os.path.join(pasta_base, "VENDA_POR_PRODUTO_JANEIRO_2025.csv"),
    "vendas_prod_fev": os.path.join(pasta_base, "vendas_de_fevereiro_por_produto.csv"),
    "pagamento_fev": os.path.join(pasta_base, "vendas_de_fevereiro_por_pagamento.csv"),
    "pagamento_jan": os.path.join(pasta_base, "pagamentos_janeiro.csv"),
}

def carregar_csv(caminho, sep=";", encoding="latin1"):
    return pd.read_csv(caminho, sep=sep, encoding=encoding)

def limpar_espacos(series):
    return series.astype(str).str.strip()

def formatar_valores(series):
    def formatar(v):
        try:
            valor = float(
                str(v).replace("R$", "").replace(".", "").replace(",", ".").strip()
            )
            return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        except:
            return v
    return series.apply(formatar)

# carregar arquivos
vendas_jan = carregar_csv(arquivos["vendas_jan"])
vendas_fev = carregar_csv(arquivos["vendas_fev"])
vendas_prod_jan = carregar_csv(arquivos["vendas_prod_jan"])
vendas_prod_fev = carregar_csv(arquivos["vendas_prod_fev"])
pagamento_fev = carregar_csv(arquivos["pagamento_fev"])
pagamento_jan = carregar_csv(arquivos["pagamento_jan"])

# processamento e renomeação de colunas
def processar_vendas(dia_df, prod_df, mes):
    dia_df["Mês"] = mes
    dia_df["Dia"] = dia_df["Dia"].str.strip()
    prod_df = prod_df.rename(columns={"Descrição": "Produto", "Quant.Vendas": "Quantidade", "Valor Pago": "ValorPago"})
    prod_df["Mês"] = mes
    return prod_df

vendas_prod_jan_df = processar_vendas(vendas_jan, vendas_prod_jan, "Janeiro")
vendas_prod_fev_df = processar_vendas(vendas_fev, vendas_prod_fev, "Fevereiro")

vendas_produtos_total = pd.concat([vendas_prod_jan_df, vendas_prod_fev_df], ignore_index=True)

for col in ["Quantidade", "ValorPago", "Custo Total"]:
    if col in vendas_produtos_total.columns:
        vendas_produtos_total[col] = formatar_valores(vendas_produtos_total[col])

pagamento_fev["Meio de pagamento"] = limpar_espacos(pagamento_fev["Meio de pagamento"])
pagamento_fev["Total"] = formatar_valores(pagamento_fev["Total"])
pagamento_fev["Mês"] = "Fevereiro"

pagamento_jan["Meio de pagamento"] = limpar_espacos(pagamento_jan["Meio de pagamento"])
pagamento_jan["Total"] = formatar_valores(pagamento_jan["Total"])
pagamento_jan["Mês"] = "Janeiro"

pagamentos = pd.concat(
    [pagamento_jan[["Meio de pagamento", "Total", "Mês"]],
     pagamento_fev[["Meio de pagamento", "Total", "Mês"]]],
    ignore_index=True
)

# exportação
vendas_produtos_total.to_csv("vendas_produtos_integradas.csv", index=False, encoding="utf-8-sig")
pagamentos.to_csv("pagamentos_integrados.csv", index=False, encoding="utf-8-sig")

print("✅ Integração concluída. Arquivos exportados:")
print("- vendas_produtos_integradas.csv")
print("- pagamentos_integrados.csv")
