import os
import json

def carregar_dispositivos():
    dispositivos = []
    pasta = "dispositivos"

    if not os.path.exists(pasta):
        return []

    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".json"):
            caminho = os.path.join(pasta, arquivo)
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    if isinstance(dados, list):
                        dispositivos.extend(dados)
                    else:
                        dispositivos.append(dados)
            except Exception as e:
                print("Erro ao ler {}: {}").format(arquivo, e)
    return dispositivos

def atualizar_prioridade(nome_dispositivo, nova_prioridade):
    caminho = os.path.join("dispositivos", "dispositivos.json")

    try:
        with open(caminho, "r") as f:
            dispositivos = json.load(f)

        encontrado = False
        for d in dispositivos:
            if d['nome'].lower() == nome_dispositivo:
                d['prioridade'] = nova_prioridade
                encontrado = True
                break

        if encontrado:
            with open(caminho, "w") as f:
                json.dump(dispositivos, f, indent=4)
            return True
        else:
            return False

    except Exception as e:
        print("Erro ao atualizar prioridade:", e)
        return False

weather_codes = {
    0: "céu limpo",
    1: "parcialmente nublado",
    2: "parcialmente nublado",
    3: "nublado",
    45: "neblina",
    48: "neblina com gelo",
    51: "chuvisco leve",
    53: "chuvisco moderado",
    55: "chuvisco intenso",
    56: "chuvisco leve com gelo",
    57: "chuvisco intenso com gelo",
    61: "chuva fraca",
    63: "chuva moderada",
    65: "chuva forte",
    66: "chuva fraca com gelo",
    67: "chuva forte com gelo",
    71: "neve fraca",
    73: "neve moderada",
    75: "neve forte",
    77: "granizo",
    80: "chuva de verão fraca",
    81: "chuva de verão moderada",
    82: "chuva de verão intensa",
    85: "neve fraca com chuva",
    86: "neve intensa com chuva",
    95: "tempestade com trovões",
    96: "tempestade com trovões e granizo leve",
    99: "tempestade com trovões e granizo intenso"
}