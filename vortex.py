import os
import requests
from bs4 import BeautifulSoup
import openai



# Função para coletar o conteúdo de um site
def coletar_conteudo_site(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        conteudo = soup.get_text()
        return conteudo
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o site: {e}")
        return None

# Função para classificar o conteúdo usando a OpenAI
def classificar_conteudo(conteudo):
    if conteudo:
        prompt = f"Analise o conteúdo a seguir e identifique o tipo de site e seu tema:\n\n{conteudo[:1000]}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Utilize o modelo disponível para sua chave
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            classificacao = response['choices'][0]['message']['content'].strip()
            return classificacao
        except Exception as e:
            print(f"Erro ao usar a API da OpenAI: {e}")
            return "Classificação não disponível"
    else:
        return "Conteúdo vazio"

# Função principal para processar a URL
def processar_site(url):
    print(f"\nProcessando o site: {url}")
    conteudo = coletar_conteudo_site(url)
    if conteudo:
        classificacao = classificar_conteudo(conteudo)
        print("\nResumo e Classificação do Site:")
        print(f"URL: {url}")
        print(f"Classificação: {classificacao}")
        print(f"Tamanho do Conteúdo (caracteres): {len(conteudo)}\n")
    else:
        print("Não foi possível obter o conteúdo do site.")

# Exemplo de uso
processar_site("https://www.uol.com.br/")
