from flask import Flask
from flask_ask import Ask, statement
import requests
from functions import carregar_dispositivos, atualizar_prioridade

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('CurrentWeatherIntent')
def weather_intent():
    API_KEY = "e30f65d5c490822248b696c846d33704"
    cidade = "São Paulo"
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=pt_br&units=metric".format(cidade, API_KEY)

    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        try:
            temperatura = dados['main']['temp']
            sensacao = dados['main']['feels_like']
            clima = dados['weather'][0]['description']
            umidade = dados['main']['humidity']
            vento = dados['wind']['speed']

            fala = ("Em {}, o clima está com {}. "
            "A temperatura atual é de {:.1f}°C, "
            "com sensação térmica de {:.1f}°C. "
            "A umidade do ar está em {}% "
            "e a velocidade do vento é de {} m/s.").format(
                cidade, clima, temperatura, sensacao, umidade, vento)

        except (KeyError, IndexError):
            fala = "Desculpe, não consegui obter todos os dados do clima no momento."
    else:
        fala = "Não consegui obter as informações do tempo para essa cidade agora. Tente novamente mais tarde."

    return statement(fala)

@ask.intent("ListarDispositivosIntent")
def listar_dispositivos():
    dispositivos = carregar_dispositivos()
    falas = []
    for d in dispositivos:
        fala = "{} consome {} watts e tem prioridade {}. ".format(
            d['nome'], d['consumo'], d['prioridade']
        )
        falas.append(fala)
    resposta = "Aqui estão os dispositivos cadastrados: " + " ".join(falas)
    return statement(resposta)

@ask.intent("AlterarPrioridadeIntent", mapping={'dispositivo': 'dispositivo', 'prioridade': 'prioridade'})
def alterar_prioridade(dispositivo, prioridade):
    if not dispositivo or not prioridade:
        return statement("Não entendi o nome do dispositivo ou a prioridade.")

    sucesso = atualizar_prioridade(dispositivo.lower(), int(prioridade))
    if sucesso:
        return statement("A prioridade do dispositivo {} foi alterada para {}.".format(dispositivo, prioridade))
    else:
        return statement("Não encontrei o dispositivo {}.".format(dispositivo))

@ask.intent("AMAZON.FallbackIntent")
def fallback():
    return statement("Desculpe, não entendi o que você quis dizer. Tente perguntar novamente de outra forma.")

@ask.session_ended
def session_ended():
    return '{}', 200


if __name__ == '__main__':
    app.run()
