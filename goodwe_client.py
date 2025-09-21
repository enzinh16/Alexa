# goodwe_client.py
"""
Starter mínimo para acessar a API do SEMS Portal (GoodWe).
⚠️ Educacional. Endpoints e contratos podem mudar. Use credenciais próprias.
"""

import os
import json
import base64
import requests
from typing import Dict, Any

# No Python 3.5 não existe Literal, então usamos apenas str
Region = str

BASE = {
    "us": "https://us.semsportal.com",
    "eu": "https://eu.semsportal.com",
}

def _initial_token():
    """
    Gera o Token inicial (pré-login).
    """
    original = {"uid": "", "timestamp": 0, "client": "web", "version": "", "language": "us"}
    b = json.dumps(original).encode("utf-8")
    return base64.b64encode(b).decode("utf-8")

def crosslogin(account, pwd, region="us"):
    """
    Faz o crosslogin e devolve o Token válido (Base64 do campo 'data' da resposta).
    """
    url = "{}/api/v2/common/crosslogin".format(BASE[region])
    headers = {"Token": _initial_token(), "Content-Type": "application/json", "Accept": "*/*"}
    payload = {
        "account": account,
        "pwd": pwd,
        "agreement_agreement": 0,
        "is_local": False
    }
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    js = r.json()
    if "data" not in js or js.get("code") not in (0, 1, 200):
        raise RuntimeError("Login falhou: {}".format(js))
    data_to_string = json.dumps(js["data"])
    token = base64.b64encode(data_to_string.encode("utf-8")).decode("utf-8")
    return token

def get_inverter_data_by_column(token, inv_id, column, date, region="us"):
    """
    Chama o endpoint GetInverterDataByColumn.
    Ex.: column='Cbattery1', date='YYYY-MM-DD HH:MM:SS', inv_id='5010KETU229W6177'
    """
    url = "{}/api/PowerStationMonitor/GetInverterDataByColumn".format(BASE[region])
    headers = {"Token": token, "Content-Type": "application/json", "Accept": "*/*"}
    payload = {"date": date, "column": column, "id": inv_id}
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

plant_id = "7f9af1fc-3a9a-4779-a4c0-ca6ec87bd93a"

def get_plant_detail(token, plant_id, region="us"):
    """
    Chama o endpoint GetPlantDetailByPowerstationId.
    """
    url = "{}/api/v3/PowerStation/GetPlantDetailByPowerstationId".format(BASE[region])
    headers = {"Token": token, "Content-Type": "application/json", "Accept": "*/*"}
    payload = {"powerStationId": plant_id}
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

def get_monitor_detail(token, plant_id, region="us"):
    """
    Chama o endpoint GetMonitorDetailByPowerstationId.
    """
    url = "{}/api/v3/PowerStation/GetMonitorDetailByPowerstationId".format(BASE[region])
    headers = {"Token": token, "Content-Type": "application/json", "Accept": "*/*"}
    payload = {"powerStationId": plant_id}
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

def client_from_env():
    """
    Lê variáveis de ambiente SEMS_ACCOUNT, SEMS_PASSWORD, SEMS_REGION (us|eu).
    """
    acc = os.getenv("SEMS_ACCOUNT", "")
    pwd = os.getenv("SEMS_PASSWORD", "")
    region = os.getenv("SEMS_REGION", "us")
    if not acc or not pwd:
        raise RuntimeError("Defina SEMS_ACCOUNT e SEMS_PASSWORD no ambiente.")
    return {"account": acc, "password": pwd, "region": region}

def fetch_data_from_sems(account, password, inverter_sn, req_date, column, login_region, data_region):
    """
    Busca dados de uma única coluna do SEMS.
    """
    try:
        token = crosslogin(account, password, login_region)
        data = get_inverter_data_by_column(token, inverter_sn, column, req_date, data_region)
        return data
    except Exception as e:
        print("Erro ao buscar dados: {}".format(e))
        return {"code": -1, "msg": str(e), "data": None}


if __name__ == "__main__":
    try:
        cfg = client_from_env()
        token = crosslogin(cfg["account"], cfg["password"], cfg["region"])
        print("Login OK. Token pronto.")
        # Exemplo:
        # resp = get_inverter_data_by_column(token, "5010KETU229W6177", "Cbattery1", "2025-08-12 00:21:01", "eu")
        # print(resp)
    except Exception as e:
        print("Aviso: {}".format(e))
