import pandas as pd
import requests
# Agregado 6579 = população residente estimada; variável 9324
# N3[all] = todos os estados; -1 = período mais recente

URL = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/6579"
    "/periodos/-1/variaveis/9324?localidades=N3[all]"
)

def buscar_populacao():
    resposta=requests.get(URL, timeout=30)
    resposta.raise_for_status()
    return resposta.json()

def extrair(dados):
    # dados[0] -> variável; ["resultados"][0]["series"] -> lista de estados
    series=dados[0]["resultados"][0]["series"]
    linhas=[]
    for item in series:
        # "serie" tem um único par {ano:valor}; pegamos esse par
        ano,valor=next(iter(item["serie"].items()))
        linhas.append({
            "id": int(item["localidade"]["id"]),
            "ano": int(ano),
            "populacao": pd.to_numeric(valor, errors="coerce"),
        })
    return pd.DataFrame(linhas).dropna()

if __name__ == "__main__":
    populacao=extrair(buscar_populacao())
    estados=pd.read_json("estados.json")

    # junta as duas tabelas pela coluna "id"
    df=estados.merge(populacao, on="id")
    df["populacao"]=df["populacao"].astype(int)
    df=df.sort_values("populacao", ascending=False)

    print(df.head(10))
    df.to_json("populacao_estados.json", orient="records",
               force_ascii=False, indent=2)
    print(f"{len(df)} estados salvos em populacao_estados.json")