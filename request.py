import requests
import json

url = 'http://localhost:8000/convert'

dados = {
    "titulo": "Meu Documento",
    "seções": [
        "Introdução",
        "Desenvolvimento",
        "Conclusão"
    ]
}

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

response = requests.post(
    url,
    headers=headers,
    json=dados
)

if response.status_code == 200:

    resultado = response.json()
    print("Markdown gerado:")
    print(resultado['markdown'])
else:
    print(f"Erro {response.status_code}:")
    print(response.json())