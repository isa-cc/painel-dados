import json
import requests
import pandas as pd

URL="https://servicodados.ibge.gov.br/api/v1/localidades/estados"

def buscar_estados():
    resposta=requests.get(URL, timeout=30)
    resposta.raise_for_status()
    return resposta.json()

def limpar(dados):
    linhas=[]
    for e in dados:
        linhas.append({
            "id": e ["id"],
            "sigla": e ["sigla"],
            "nome": e ["nome"],
            "regiao": e ["regiao"]["nome"],
        })
    df=pd.DataFrame(linhas).sort_values("nome")
    return df

if __name__ == "__main__":
    dados=buscar_estados()
    df=limpar(dados)
    print(df.head())
    df.to_json("estados.json",orient="records", force_ascii=False,indent=2)
    print(f"{len(df)} estados salvos em estados.json")