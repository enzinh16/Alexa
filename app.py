from flask import Flask, request, jsonify
from flask_ask import Ask, question, statement
import json
import requests
from functions import carregar_dispositivos, atualizar_prioridade, weather_codes
from goodwe_client import fetch_data_from_sems, client_from_env, get_plant_detail, crosslogin, get_monitor_detail
import os

app = Flask(__name__)
ask = Ask(app, "/")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta do app.py

# === Hack para desligar verificação de certificado (local com ngrok) ===
_original_alexa_request = ask._alexa_request

def _alexa_request_no_verify(*args, **kwargs):
    kwargs['verify'] = False
    return _original_alexa_request(*args, **kwargs)

ask._alexa_request = _alexa_request_no_verify
# =======================================================================

try:
    CONFIG = client_from_env()
except RuntimeError as e:
    CONFIG = {}
    print("Aviso: {}. Usando credenciais demo.".format(e))
    CONFIG["account"] = "ecopower.management@gmail.com"
    CONFIG["password"] = "Goodwe2018"
    CONFIG["region"] = "us"

# =================== Rota Flask ===================
@app.route("/detalhes-monitor")
def get_detalhes_monitor():
    plant_id = request.args.get("plantId")
    if not plant_id:
        return jsonify({"error": "Parâmetro 'plantId' é obrigatório"}), 400

    try:
        token = crosslogin(CONFIG["account"], CONFIG["password"], CONFIG["region"])
        data = get_monitor_detail(token, plant_id, region="us")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Falha ao buscar detalhes do monitor", "details": str(e)}), 500

def carregar_dados_monitor():
    arquivo_json = os.path.join(BASE_DIR, "detalhes_monitor.json")
    if os.path.exists(arquivo_json):
        with open(arquivo_json, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

@ask.intent("DadosDaPlantaIntent")
def nome_planta():
    dados = carregar_dados_monitor()
    # Extrai os dados da planta
    if dados and "data" in dados and "info" in dados["data"]:
        nome = dados["data"]["info"].get("stationname", "Desconhecido")

        return statement("O nome da planta é {}, ela está localizada em Av. Lins de Vasconcelos, 1222 - Cambuci, há duas baterias e a carga delas estão em 100% e 10%".format(nome))
    else:
        return statement("Não consegui acessar os dados da planta no momento.")

@ask.intent('CurrentWeatherIntent')
def weather_intent():
    dados = carregar_dados_monitor()
    endereco = dados["data"]["info"]["address"]
    parte_bairro = endereco.split(" - ")[1]
    bairro = parte_bairro.split(",")[0].strip()
    latitude = dados["data"]["info"]["latitude"]
    longitude = dados["data"]["info"]["longitude"]

    # Endpoint da API
    url = ("https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&current=wind_speed_10m,precipitation,apparent_temperature,temperature_2m,relative_humidity_2m,weather_code").format(latitude, longitude)
    resposta = requests.get(url).json()

    # Dados atuais
    current = resposta.get("current", {})
    vento = current.get("wind_speed_10m")
    precipitacao = current.get("precipitation")
    sensacao = current.get("apparent_temperature")
    temperatura = current.get("temperature_2m")
    umidade = current.get("relative_humidity_2m")
    codigo_atual = current.get("weather_code")
    descricao_atual = weather_codes.get(codigo_atual, "Código desconhecido")

    fala = ("Em {}, o clima está {}. "
        "A temperatura atual é de {:.1f}°C, "
        "com sensação térmica de {:.1f}°C. "
        "A umidade do ar está em {}% "
        "A precipitação de chuva é de {:.0f}% "
        "e a velocidade do vento é de {} m/s.").format(
            bairro, descricao_atual, temperatura, sensacao, umidade, precipitacao, vento)
    
    return question(fala)

@ask.intent("DailyWeatherIntent")
def daily_weather():
    dados = carregar_dados_monitor()
    # Extrair bairro do endereço
    endereco = dados["data"]["info"]["address"]
    try:
        parte_bairro = endereco.split(" - ")[1]
        bairro = parte_bairro.split(",")[0].strip()
    except:
        bairro = "local selecionado"

    latitude = dados["data"]["info"]["latitude"]
    longitude = dados["data"]["info"]["longitude"]

    # === Chamada API ===
    url = ("https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=America/Sao_Paulo").format(latitude, longitude)

    resposta = requests.get(url).json()
    diario = resposta.get('daily', {})

    # === Montar resposta ===
    texto = "Previsão do tempo para {0}: ".format(bairro)
    for i, data_dia in enumerate(diario.get('time', [])):
        max_temp = diario['temperature_2m_max'][i]
        min_temp = diario['temperature_2m_min'][i]
        chuva = diario['precipitation_probability_max'][i]
        texto += ("No dia {0}, máxima de {1} graus, mínima de {2} graus, com {3}% de chance de chuva. ").format(data_dia, max_temp, min_temp, chuva)

    return statement(texto)

@ask.intent("ListarDispositivosIntent")
def listar_dispositivos():
    dispositivos = carregar_dispositivos()
    falas = []
    for d in dispositivos:
        fala = "{} consome {} watts e tem prioridade {}. ".format(d['nome'], d['consumo'], d['prioridade'])
        falas.append(fala)
    resposta = "Aqui estão os dispositivos cadastrados: " + " ".join(falas)
    return question(resposta)

@ask.intent("AlterarPrioridadeIntent", mapping={'dispositivo': 'dispositivo', 'prioridade': 'prioridade'})
def alterar_prioridade(dispositivo, prioridade):
    if not dispositivo or not prioridade:
        return statement("Não entendi o nome do dispositivo ou a prioridade.")
    sucesso = atualizar_prioridade(dispositivo.lower(), int(prioridade))
    if sucesso:
        return question("A prioridade do dispositivo {} foi alterada para {}.".format(dispositivo, prioridade))
    else:
        return statement("Não encontrei o dispositivo {}.".format(dispositivo))

@ask.intent("AMAZON.FallbackIntent")
def fallback():
    return statement("Desculpe, não entendi o que você quis dizer. Tente perguntar novamente de outra forma.")

@ask.session_ended
def session_ended():
    return '{}', 200

if __name__ == "__main__":
    # Baixa o JSON direto usando o goodwe_client
    try:
        plant_id_demo = "7f9af1fc-3a9a-4779-a4c0-ca6ec87bd93a"
        token = crosslogin(CONFIG["account"], CONFIG["password"], CONFIG["region"])
        dados_monitor = get_monitor_detail(token, plant_id_demo, region="us")

        arquivo_saida = os.path.join(BASE_DIR, "detalhes_monitor.json")
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            json.dump(dados_monitor, f, indent=4, ensure_ascii=False)
        print("JSON de detalhes do monitor salvo em {}".format(arquivo_saida))
    except Exception as e:
        print("Falha ao baixar detalhes do monitor: {}".format(e))

    # Depois inicia o servidor Flask normalmente
    print("Servidor web iniciado. Acesse http://127.0.0.1:5000/ no navegador.")
    app.run(port=5000, debug=True)