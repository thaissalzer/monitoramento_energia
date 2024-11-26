import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pandas as pd

# Palavras-chave a serem buscadas na ementa
keywords = ["energia", "eletr", "CDE", "geração", "renováve", "transmissão", "resíduo", "transição energética"]

# Calcular a data inicial
data_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')

# Criar a URL
url = f"https://legis.senado.leg.br/dadosabertos/materia/tramitando?data={data_inicio}"

# Fazer a requisição
response = requests.get(url)

# Verificar o status da requisição
if response.status_code == 200:
    # Parsear o XML da resposta
    root = ET.fromstring(response.content)

    # Inicializar lista para matérias filtradas
    materias_filtradas = []

    # Iterar sobre todas as matérias
    for materia in root.findall(".//Materia"):
        ementa = materia.find("Ementa").text  # Obter o texto da Ementa
        if ementa and any(keyword in ementa.lower() for keyword in keywords):
            # Obter informações da matéria
            identificacao = materia.find(".//DescricaoIdentificacaoMateria").text
            codigo_materia = materia.find(".//CodigoMateria").text
            ultima_atualizacao = materia.find(".//DataUltimaAtualizacao").text
            link = f"https://www25.senado.leg.br/web/atividade/materias/-/materia/{codigo_materia}"

            # Adicionar matéria à lista filtrada
            materias_filtradas.append({
                "identificacao": identificacao,
                "ementa": ementa,
                "ultima_atualizacao": ultima_atualizacao,
                "link": link
            })

    # Criar o dataframe
    df = pd.DataFrame(materias_filtradas)

else:
    print(f"Erro ao acessar a API: {response.status_code}")
    print(response.text)
st.dataframe(df)
