"""
Assistente de Investimentos com RPA e IA Generativa (DIO Lab)
Script de automação RPA para extração de clientes e integração com N8N.
"""

import requests
from bs4 import BeautifulSoup
import json

URL_PAGINA = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"
N8N_WEBHOOK = "https://testtest222.app.n8n.cloud/webhook/clientes"


def extrair_clientes():
    print(f"1) Acessando página de clientes: {URL_PAGINA}")
    response = requests.get(URL_PAGINA)
    response.raise_for_status()

    print("2) Extraindo dados da tabela com BeautifulSoup...")
    soup = BeautifulSoup(response.text, "html.parser")
    linhas = soup.select("#clientes tbody tr")

    clientes = []
    for linha in linhas:
        colunas = linha.find_all("td")
        if len(colunas) >= 4:
            clientes.append({
                "nome": colunas[0].get_text(strip=True),
                "email": colunas[1].get_text(strip=True),
                "saldo": colunas[2].get_text(strip=True),
                "perfil": colunas[3].get_text(strip=True),
            })

    print(f"-> {len(clientes)} clientes extraídos com sucesso:")
    for c in clientes:
        print(f"   • {c['nome']:<18} | {c['perfil']:<12} | {c['saldo']:<14} | {c['email']}")

    return clientes


def enviar_para_n8n(clientes):
    print(f"\n3) Enviando lista de clientes para o Webhook N8N: {N8N_WEBHOOK}")
    headers = {"Content-Type": "application/json"}
    payload = {"clientes": clientes}

    try:
        response = requests.post(N8N_WEBHOOK, json=payload, headers=headers)
        response.raise_for_status()

        print(f"-> Sucesso! Status HTTP {response.status_code}")
        resultado = response.json()

        print("\n" + "=" * 60)
        print("RELATÓRIO DE RECOMENDAÇÕES GERADAS PELO N8N + GEMINI")
        print("=" * 60)

        dados_clientes = resultado.get("clientes", [])
        for item in dados_clientes:
            print(f"\n👤 Cliente: {item.get('cliente')} ({item.get('email')})")
            print(f"💼 Perfil: {item.get('perfil')} | Saldo: {item.get('saldo')}")
            print(f"\n🤖 Recomendação Personalizada (IA Gemini):")
            print("-" * 50)
            print(item.get("recomendacao_ia", "").strip())
            print("-" * 50)

        return resultado

    except requests.exceptions.RequestException as e:
        print(f"-> Erro na comunicação com o N8N: {e}")
        return None


if __name__ == "__main__":
    lista_clientes = extrair_clientes()
    enviar_para_n8n(lista_clientes)
