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